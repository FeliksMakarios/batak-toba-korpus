"""Jalur reproduksi tanpa GPU: semua angka evaluasi naskah dari berkas yang dirilis.

Yang dihitung ulang dari awal:
  1. set uji (korpus kita + NusaX + NusaTranslation yang diunduh dari rilis resmi IndoNLP), dalam dua versi
     rujukan: "lama" (rujukan asli) dan "terkoreksi" (rujukan Toba set uji kita setelah koreksi penutur, C6);
  2. chrF++ dan BLEU semua sistem, selang kepercayaan bootstrap, rata-rata antarbenih, tabel utama,
     tabel bahasa asli (Tabel 3) dan genre;
  3. uji beda berpasangan dengan koreksi Holm, dan selang kepercayaan Tabel 3;
  4. audit varietas (penanda Angkola-Mandailing) pada korpus dan keluaran sistem;
  5. analisis ESA: skor manusia, kesepakatan penilai dengan selang kepercayaan, Kendall tau metrik-manusia;
  6. statistik korpus per genre, kovariat pembaur, jumlah langkah pelatihan;
  7. (opsional) ringkasan lembar penutur asli C1 sampai C5, bila folder lembarnya diberikan;
  8. verifikasi: angka versi "lama" dicocokkan dengan tabel yang sudah dirilis di hasil/tabel/.

Pelatihan dan dekode model TIDAK diulang (butuh GPU); prediksinya dibaca dari prediksi/.

Pemakaian (dari akar repo):
  python riset-lanjutan/skrip/jalankan_semua.py [--cache FOLDER] [--keluaran FOLDER] [--lembar FOLDER] [--B_holm 10000]
Kebutuhan: pandas, numpy, scipy, openpyxl, sacrebleu==2.6.0.
Teks NusaX dan NusaTranslation hanya disimpan di folder cache, tidak di repo.
"""
import argparse, json, re, time, urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from sacrebleu.metrics import BLEU, CHRF
from scipy import stats

AKAR = Path(__file__).resolve().parents[2]
RL = AKAR / "riset-lanjutan"
ap = argparse.ArgumentParser()
ap.add_argument("--cache", default=str(Path.home() / ".cache" / "btb-reproduksi"))
ap.add_argument("--keluaran", default=str(RL / "hasil" / "v3"))
ap.add_argument("--lembar", default="", help="folder berisi C1.xlsx sampai C5.xlsx (opsional)")
ap.add_argument("--B_ik", type=int, default=1000, help="sampel bootstrap untuk selang kepercayaan (sama dengan S10)")
ap.add_argument("--B_holm", type=int, default=10000, help="sampel bootstrap untuk uji beda berpasangan")
arg = ap.parse_args()
CACHE, OUT = Path(arg.cache), Path(arg.keluaran)
CACHE.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
CHRF_M, BLEU_M = CHRF(word_order=2), BLEU()
BLEU_KAL = BLEU(effective_order=True)   # BLEU tingkat kalimat, sama dengan sacrebleu.sentence_bleu
ARAH = ["id2bbc", "bbc2id"]
VERSI = ["lama", "terkoreksi"]
RINGKAS, VERIF = {}, []
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.0f} d]", *a, flush=True)


def simpan(df, nama):
    df.to_csv(OUT / nama, index=False)


# ======================================================================
# 0. Data
# ======================================================================
URL_NX = "https://raw.githubusercontent.com/IndoNLP/nusax/main/datasets/mt/{s}.csv"
URL_NT = "https://raw.githubusercontent.com/IndoNLP/nusa-writes/main/data/nusa_kalimat-mt-btk-{s}.csv"


def unduh(url, tujuan):
    if not tujuan.exists():
        log("mengunduh", url)
        for i in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "python-urllib"})
                tujuan.write_bytes(urllib.request.urlopen(req, timeout=60).read())
                break
            except Exception:
                if i == 3:
                    raise
                time.sleep(2 ** (i + 1))
    return tujuan


nama_split = {"train": "latih", "valid": "validasi", "test": "uji"}
nx, nt = [], []
for s in ["train", "valid", "test"]:
    d = pd.read_csv(unduh(URL_NX.format(s=s), CACHE / f"nusax_mt_{s}.csv"), dtype=str, keep_default_na=False)
    d = d[d["toba_batak"].str.strip() != ""].reset_index(drop=True)
    nx.append(pd.DataFrame({"uji_id": [f"nx-{s}-{i:04d}" for i in range(len(d))], "split": nama_split[s],
                            "teks_id": d["indonesian"], "teks_bbc": d["toba_batak"]}))
    d = pd.read_csv(unduh(URL_NT.format(s=s), CACHE / f"nusatranslation_btk_{s}.csv"), dtype=str, keep_default_na=False)
    nt.append(pd.DataFrame({"uji_id": [f"nt-{s}-{i:04d}" for i in range(len(d))], "split": nama_split[s],
                            "teks_id": d["ind_text"], "teks_bbc": d["tgt_text"]}))
nx, nt = pd.concat(nx, ignore_index=True), pd.concat(nt, ignore_index=True)

korpus = pd.read_csv(AKAR / "data/btb_parallel_sentence.csv")
split = pd.read_csv(RL / "data/split_korpus_kami.csv")
meta = pd.read_csv(RL / "data/set_uji.csv", keep_default_na=False)
kor = pd.read_csv(RL / "data/draf_berbantuan_ai/set_uji_kami_koreksi_draf.csv", keep_default_na=False)

# set uji kita: teks dari korpus, dicocokkan dengan teks "lama" di berkas koreksi
k = split[split.split == "uji"].merge(korpus[["pair_id", "toba_final", "indo_final"]], on="pair_id")
k = k.set_index("uji_id").loc[kor.uji_id]
assert (k.toba_final.values == kor.teks_bbc_lama.values).all() and (k.indo_final.values == kor.teks_id_lama.values).all(), \
    "teks set uji kita tidak sama dengan korpus"
teks = {}
for v in VERSI:
    akhir = "lama" if v == "lama" else "baru"
    t = pd.concat([kor[["uji_id", f"teks_id_{akhir}", f"teks_bbc_{akhir}"]].set_axis(["uji_id", "teks_id", "teks_bbc"], axis=1),
                   nx[["uji_id", "teks_id", "teks_bbc"]], nt[["uji_id", "teks_id", "teks_bbc"]]]).drop_duplicates("uji_id")
    teks[v] = t.set_index("uji_id")
UJI = {v: meta.join(teks[v], on="uji_id") for v in VERSI}
for v in VERSI:
    assert UJI[v].teks_bbc.notna().all(), "ada butir uji tanpa teks"
RINGKAS["set_uji"] = meta.set_uji.value_counts().to_dict()
RINGKAS["rujukan_dikoreksi"] = {"toba": int((kor.teks_bbc_lama != kor.teks_bbc_baru).sum()),
                                "indonesia": int((kor.teks_id_lama != kor.teks_id_baru).sum()),
                                "per_keputusan": kor.keputusan.value_counts().to_dict()}
log("set uji siap:", RINGKAS["set_uji"], "| rujukan dikoreksi:", RINGKAS["rujukan_dikoreksi"])

# prediksi
PRED = {}
for p in sorted((RL / "prediksi").glob("*/*.jsonl")):
    sistem, arah = p.parent.name, p.stem.split(".")[-1]
    d = PRED.setdefault(sistem, {})
    for b in p.read_text(encoding="utf-8").splitlines()[1:]:
        r = json.loads(b)
        d[(arah, r["uji_id"])] = r["hipotesis"]
SISTEM = sorted(PRED)
log(len(SISTEM), "sistem")


# ======================================================================
# 1. Skor otomatis (logika S10)
# ======================================================================
def subset(uji):
    out = []
    for s in ["kami", "nusax", "nusatranslation", "nusatranslation_toba"]:
        d = uji[uji.set_uji == s].reset_index(drop=True)
        out.append((s, "semua", "semua", d))
        for dim in {"kami": ["arah_asli", "genre", "validasi_manusia"], "nusatranslation": ["varietas_rujukan"]}.get(s, []):
            for nilai, g in d.groupby(dim):
                if str(nilai).strip():
                    out.append((s, dim, str(nilai), g.reset_index(drop=True)))
    return out


def stat(m, hip, ruj):
    return np.array(m._extract_corpus_statistics(hip, [ruj]), dtype=float)


def skor_stat(m, S):
    return m._compute_score_from_stats(S.tolist()).score


_W = {}


def bobot(n, B, benih=12345):
    # matriks hitungan kalimat per sampel ulang; indeks sama untuk semua sistem dengan n kalimat sama
    if (n, B, benih) not in _W:
        idx = np.random.RandomState(benih).randint(0, n, size=(B, n))
        W = np.zeros((B, n))
        np.add.at(W, (np.repeat(np.arange(B), n), idx.ravel()), 1)
        _W[(n, B, benih)] = W
    return _W[(n, B, benih)]


def sampel(S, B, benih=12345):
    return np.array([skor_stat(CHRF_M, t) for t in bobot(len(S), B, benih) @ S])


def hipotesis(sistem, d, arah):
    h = [PRED[sistem].get((arah, i)) for i in d.uji_id]
    return None if any(x is None for x in h) else h


baris = []
STAT = {}   # (versi, sistem, set, dim, nilai, arah) -> statistik chrF++ per kalimat
for v in VERSI:
    for s, dim, nilai, d in subset(UJI[v]):
        if v == "terkoreksi" and s != "kami":
            continue          # set lain tidak berubah
        for sistem in SISTEM:
            for arah in ARAH:
                hip = hipotesis(sistem, d, arah)
                if hip is None:
                    continue
                ruj = list(d.teks_bbc if arah == "id2bbc" else d.teks_id)
                Sc, Sb = stat(CHRF_M, hip, ruj), stat(BLEU_M, hip, ruj)
                r = {"rujukan": v, "sistem": sistem, "set_uji": s, "dimensi": dim, "nilai": nilai, "arah": arah,
                     "n": len(hip), "chrf": skor_stat(CHRF_M, Sc.sum(0)), "bleu": skor_stat(BLEU_M, Sb.sum(0))}
                if dim in ("semua", "arah_asli"):
                    r["chrf_ik_bawah"], r["chrf_ik_atas"] = np.percentile(sampel(Sc, arg.B_ik), [2.5, 97.5])
                    STAT[(v, sistem, s, dim, nilai, arah)] = Sc
                baris.append(r)
SK = pd.DataFrame(baris)
# set selain "kami" sama untuk kedua versi rujukan
SK = pd.concat([SK, SK[(SK.rujukan == "lama") & (SK.set_uji != "kami")].assign(rujukan="terkoreksi")], ignore_index=True)
SK["grup"] = SK.sistem.str.replace(r"_s\d+$", "", regex=True)
simpan(SK.round(2), "skor.csv")
log("skor:", len(SK), "baris")

# rata-rata antarbenih
benih = (SK[SK.dimensi.isin(["semua", "arah_asli", "genre"])].groupby(["rujukan", "grup", "set_uji", "dimensi", "nilai", "arah"])
         .agg(n_benih=("sistem", "nunique"), chrf_rata=("chrf", "mean"), chrf_sb=("chrf", "std"),
              bleu_rata=("bleu", "mean"), bleu_sb=("bleu", "std")).reset_index())
simpan(benih.round(2), "skor_rata_benih.csv")

# tabel utama (benih 42 dengan IK) dan tabel BLEU (rata-rata benih)
for v in VERSI:
    u = SK[(SK.rujukan == v) & (SK.dimensi == "semua")].copy()
    u["teks"] = [f"{a:.1f} [{b:.1f}, {c:.1f}]" for a, b, c in zip(u.chrf, u.chrf_ik_bawah, u.chrf_ik_atas)]
    t = u.pivot_table(index="sistem", columns=["set_uji", "arah"], values="teks", aggfunc="first")
    t.columns = [f"{a}|{b}" for a, b in t.columns]
    simpan(t.reset_index(), f"tabel_utama_{v}.csv")
    a = SK[(SK.rujukan == v) & (SK.set_uji == "kami") & (SK.dimensi == "arah_asli")].pivot_table(
        index="sistem", columns=["arah", "nilai"], values="chrf")
    for r in ARAH:
        a[(r, "selisih_toba_minus_indonesia")] = a[(r, "asli_toba")] - a[(r, "asli_indonesia")]
    a = a.sort_index(axis=1); a.columns = [f"{x}|{y}" for x, y in a.columns]
    simpan(a.round(2).reset_index(), f"arah_asli_{v}.csv")
    g = SK[(SK.rujukan == v) & (SK.set_uji == "kami") & (SK.dimensi == "genre")].pivot_table(
        index="sistem", columns=["arah", "nilai"], values="chrf")
    g.columns = [f"{x}|{y}" for x, y in g.columns]
    simpan(g.round(2).reset_index(), f"genre_{v}.csv")
bl = benih[benih.dimensi == "semua"].pivot_table(index=["rujukan", "grup"], columns=["set_uji", "arah"], values="bleu_rata")
bl.columns = [f"{a}|{b}" for a, b in bl.columns]
simpan(bl.round(1).reset_index(), "bleu.csv")
RINGKAS["signature"] = {"chrf": str(CHRF_M.get_signature()), "bleu": str(BLEU_M.get_signature())}

# perubahan akibat koreksi rujukan, set uji kita
x = SK[(SK.set_uji == "kami") & (SK.dimensi.isin(["semua", "arah_asli"]))].pivot_table(
    index=["grup", "sistem", "dimensi", "nilai", "arah"], columns="rujukan", values="chrf").reset_index()
x["selisih"] = x.terkoreksi - x.lama
simpan(x.round(2), "perubahan_koreksi_rujukan.csv")
y = x[(x.dimensi == "semua") & (x.arah == "id2bbc")].groupby("grup")[["lama", "terkoreksi"]].mean()
RINGKAS["koreksi_id2bbc"] = {"naik_min": round((y.terkoreksi - y.lama).min(), 2), "naik_maks": round((y.terkoreksi - y.lama).max(), 2),
                             "spearman_peringkat": round(y.lama.rank().corr(y.terkoreksi.rank(), method="spearman"), 3)}
log("koreksi rujukan:", RINGKAS["koreksi_id2bbc"])

# ======================================================================
# 2. Uji beda berpasangan + Holm, dan Tabel 3 dengan IK
# ======================================================================
PASANGAN = [("ft_kami+nusatranslation_s42", "ft_nusatranslation_s42"), ("ft_kami+nusax_s42", "ft_nusax_s42"),
            ("ft_kami_s42", "ft_nusax_s42"), ("ft_kami_s42", "ft_nusatranslation_s42")]
for m in ["llm_gemma3-27b-cpt-gotoai-v3-instruct_", "llm_qwen2.5-7b-instruct_"]:
    PASANGAN += [(m + "few_shot_retrieval", m + "few_shot_acak"), (m + "few_shot_acak", m + "zero_shot")]
B = arg.B_holm
_SAMPEL = {}


def sampel_holm(v, sistem, s, dim, nilai, arah, benih=12345):
    kunci = (v if s == "kami" else "lama", sistem, s, dim, nilai, arah, benih)
    if kunci not in _SAMPEL:
        S = STAT.get(kunci[:6])
        _SAMPEL[kunci] = None if S is None else (skor_stat(CHRF_M, S.sum(0)), sampel(S, B, benih))
    return _SAMPEL[kunci]


def p_dua(dd):
    return min(1.0, 2 * min(((dd <= 0).sum() + 1) / (B + 1), ((dd >= 0).sum() + 1) / (B + 1)))


def holm(p):
    p = np.asarray(p); m = len(p); o = np.argsort(p, kind="stable"); out = np.empty(m); maks = 0.0
    for r, i in enumerate(o):
        maks = max(maks, min(1.0, (m - r) * p[i])); out[i] = maks
    return out


HOLM = {}
for v in VERSI:
    rows = []
    for a, b in PASANGAN:
        for s, dim, nilai, d in subset(UJI[v]):
            if dim not in ("semua", "arah_asli"):
                continue
            for arah in ARAH:
                ra, rb = sampel_holm(v, a, s, dim, nilai, arah), sampel_holm(v, b, s, dim, nilai, arah)
                if ra is None or rb is None:
                    continue
                dd = ra[1] - rb[1]
                rows.append({"sistem_a": a, "sistem_b": b, "set_uji": s, "dimensi": dim, "nilai": nilai, "arah": arah,
                             "selisih_chrf": ra[0] - rb[0], "ik_bawah": np.percentile(dd, 2.5),
                             "ik_atas": np.percentile(dd, 97.5), "p_dua_sisi": p_dua(dd)})
    h = pd.DataFrame(rows); h["p_holm"] = holm(h.p_dua_sisi)
    h["signifikan_holm_0_05"] = np.where(h.p_holm < 0.05, "ya", "tidak")
    simpan(h.round(5), f"perbandingan_holm_{v}.csv"); HOLM[v] = h
    RINGKAS[f"holm_{v}"] = {"perbandingan": len(h), "signifikan": int((h.p_holm < 0.05).sum()),
                            "p_holm_min": round(h.p_holm.min(), 4)}
    # Tabel 3: kedua subset bahasa asli memakai benih berbeda agar sampelnya saling bebas
    t3 = []
    for sistem in ["copy_source", "madlad3b_zeroshot", "ft_nusatranslation_s42", "ft_kami_s42",
                   "ft_kami+nusatranslation_s42", "llm_gemma3-27b-cpt-gotoai-v3-instruct_few_shot_retrieval"]:
        for arah in ARAH:
            ri = sampel_holm(v, sistem, "kami", "arah_asli", "asli_indonesia", arah)
            rt = sampel_holm(v, sistem, "kami", "arah_asli", "asli_toba", arah, benih=54321)
            dd = rt[1] - ri[1]
            t3.append({"sistem": sistem, "arah": arah, "asli_indonesia": ri[0],
                       "asli_indonesia_ik_bawah": np.percentile(ri[1], 2.5), "asli_indonesia_ik_atas": np.percentile(ri[1], 97.5),
                       "asli_toba": rt[0], "asli_toba_ik_bawah": np.percentile(rt[1], 2.5), "asli_toba_ik_atas": np.percentile(rt[1], 97.5),
                       "selisih_toba_minus_indonesia": rt[0] - ri[0], "selisih_ik_bawah": np.percentile(dd, 2.5),
                       "selisih_ik_atas": np.percentile(dd, 97.5), "p_dua_sisi": p_dua(dd)})
    simpan(pd.DataFrame(t3).round(4), f"tabel3_{v}.csv")
    log("Holm", v, RINGKAS[f"holm_{v}"])
m = HOLM["lama"].merge(HOLM["terkoreksi"], on=["sistem_a", "sistem_b", "set_uji", "dimensi", "nilai", "arah"])
RINGKAS["holm_keputusan_berubah"] = int((m.signifikan_holm_0_05_x != m.signifikan_holm_0_05_y).sum())

# ======================================================================
# 3. Audit varietas
# ======================================================================
tok = lambda s: re.findall(r"\w+", str(s).lower())     # sama dengan token_kata di notebook
AM32 = set("inda madung kehe akkon angkon anso harana bope giot doma milas mur pade halai adaboru oppot "
           "ngen juo tai sannari soni sattak napedo abope unjung deges sarupo copat satiop manyogot "
           "natuari tarimokasih".split())
TOBA = set("dang ndang nunga nungga sian naeng jabu alai unang ahu ibana nasida".split())
# hasil C5: tiga penanda juga lazim di Toba umum, tiga juga dipakai di Toba perbatasan (Silindung, Pahae)
TOBA_UMUM = {"sarupo", "manyogot", "natuari"}
PERBATASAN = {"giot", "akkon", "milas"}
DAFTAR = {"am32": AM32, "am26_ketat": AM32 - TOBA_UMUM - PERBATASAN}


def label(t, am):
    w = set(tok(t))
    return "AM" if w & am else ("Toba_saja" if w & TOBA else "tak_bertanda")


rows = []
himp = [("korpus_kami", korpus.toba_final), ("nusax", nx.teks_bbc), ("nusatranslation", nt.teks_bbc),
        ("nusatranslation_uji", nt[nt.split == "uji"].teks_bbc)]
for nama, t in himp:
    for dn, am in DAFTAR.items():
        lab = t.map(lambda x: label(x, am))
        rows.append({"himpunan": nama, "daftar": dn, "n": len(t), **{f"persen_{c}": 100 * (lab == c).mean() for c in
                                                                    ["AM", "Toba_saja", "tak_bertanda"]},
                     "jumlah_AM": int((lab == "AM").sum())})
AUD = pd.DataFrame(rows); simpan(AUD.round(2), "audit_varietas.csv")
rows = []
for s in ["kami", "nusax", "nusatranslation", "nusatranslation_toba"]:
    d = UJI["lama"][UJI["lama"].set_uji == s]
    for sistem in ["rujukan"] + SISTEM:
        hip = list(d.teks_bbc) if sistem == "rujukan" else hipotesis(sistem, d, "id2bbc")
        if hip is None:
            continue
        for dn, am in DAFTAR.items():
            rows.append({"sistem": sistem, "set_uji": s, "daftar": dn, "n": len(hip),
                         "persen_AM": 100 * np.mean([label(h, am) == "AM" for h in hip])})
VAR = pd.DataFrame(rows); simpan(VAR.round(2), "varietas_keluaran.csv")
log("audit varietas selesai")

# ======================================================================
# 4. ESA
# ======================================================================
E = pd.read_csv(RL / "data/esa_anonim.csv")
E["skor"] = (E.skor_A + E.skor_B) / 2
for x in "AB":
    E[f"mayor_{x}"] = E[f"kesalahan_mayor_{x}"].notna().astype(int)
    E[f"variety_{x}"] = E[f"variety_{x}"].fillna(0).astype(int)
rng = np.random.RandomState(12345)
rows = []
for (arah, sistem), g in E.groupby(["arah", "sistem"]):
    ik = np.percentile(g.skor.values[np.random.RandomState(12345).randint(0, len(g), size=(1000, len(g)))].mean(1), [2.5, 97.5])
    rows.append({"arah": arah, "sistem": sistem, "n": len(g), "skor_rata": g.skor.mean(), "skor_A": g.skor_A.mean(),
                 "skor_B": g.skor_B.mean(), "ik_bawah": ik[0], "ik_atas": ik[1],
                 "persen_mayor": 100 * g[["mayor_A", "mayor_B"]].mean(axis=1).mean(),
                 "persen_mayor_A": 100 * g.mayor_A.mean(), "persen_mayor_B": 100 * g.mayor_B.mean(),
                 "variety_A": 100 * g.variety_A.mean() if arah == "id2bbc" else np.nan,
                 "variety_B": 100 * g.variety_B.mean() if arah == "id2bbc" else np.nan})
simpan(pd.DataFrame(rows).round(2), "esa_skor_manusia.csv")


def alfa(x1, x2):
    v = np.concatenate([x1, x2]).astype(float); n = len(v); ss = ((v - v.mean()) ** 2).sum()
    return 1 - (n - 1) * ((np.asarray(x1, float) - np.asarray(x2, float)) ** 2).sum() / (n * ss)


def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b); po = np.mean(a == b)
    pe = sum(np.mean(a == c) * np.mean(b == c) for c in np.union1d(a, b))
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


rows = []
for arah, d in E.groupby("arah"):
    ukur = {"krippendorff_alpha_interval": lambda i: alfa(d.skor_A.values[i], d.skor_B.values[i]),
            "kappa_mayor": lambda i: kappa(d.mayor_A.values[i], d.mayor_B.values[i])}
    if arah == "id2bbc":
        ukur["kappa_variety"] = lambda i: kappa(d.variety_A.values[i], d.variety_B.values[i])
    n = len(d); idx = rng.randint(0, n, size=(10000, n))
    for nama, f in ukur.items():
        smp = np.array([f(i) for i in idx])
        rows.append({"arah": arah, "ukuran": nama, "nilai": f(np.arange(n)), "ik_bawah": np.nanpercentile(smp, 2.5),
                     "ik_atas": np.nanpercentile(smp, 97.5)})
    rows.append({"arah": arah, "ukuran": "pearson", "nilai": stats.pearsonr(d.skor_A, d.skor_B)[0]})
    rows.append({"arah": arah, "ukuran": "spearman", "nilai": stats.spearmanr(d.skor_A, d.skor_B)[0]})
simpan(pd.DataFrame(rows).round(3), "esa_kesepakatan.csv")

# Kendall tau-b metrik vs manusia, bootstrap per kalimat (logika S13), dua versi rujukan
rows = []
for v in VERSI:
    ruj = UJI[v].set_index("uji_id")
    D = E.copy()
    for met, M in [("chrf", CHRF_M), ("bleu", BLEU_KAL)]:
        D[met] = [M.sentence_score(PRED[s][(a, i)], [ruj.loc[i, "teks_bbc" if a == "id2bbc" else "teks_id"]]).score
                  for s, a, i in zip(D.sistem, D.arah, D.uji_id)]
    r2 = np.random.RandomState(12345)
    for arah, g0 in D.groupby("arah"):
        for cak, g in [("semua_sistem", g0), ("hanya_ft", g0[g0.sistem.str.startswith("ft_")])]:
            g = g.reset_index(drop=True); per = list(g.groupby("uji_id").indices.values())
            for met in ["chrf", "bleu"]:
                x, y = g[met].values, g.skor.values
                smp = []
                for _ in range(1000):
                    ix = np.concatenate([per[j] for j in r2.randint(0, len(per), size=len(per))])
                    smp.append(stats.kendalltau(x[ix], y[ix]).statistic)
                rows.append({"rujukan": v, "arah": arah, "cakupan": cak, "metrik": met, "n_butir": len(g),
                             "kendall_tau_b": stats.kendalltau(x, y).statistic, "ik_bawah": np.nanpercentile(smp, 2.5),
                             "ik_atas": np.nanpercentile(smp, 97.5)})
    if v == "terkoreksi":
        simpan(D.groupby(["arah", "sistem"])[["skor", "chrf"]].mean().round(2).reset_index(), "esa_chrf_kalimat_terkoreksi.csv")
KEN = pd.DataFrame(rows); simpan(KEN.round(3), "esa_kendall.csv")
log("ESA selesai")

# ======================================================================
# 5. Statistik korpus, kovariat, langkah pelatihan
# ======================================================================
lab = pd.read_csv(RL / "metadata/arah_penerjemahan.csv")
korpus["n_bt"] = korpus.toba_final.map(lambda s: len(tok(s))); korpus["n_id"] = korpus.indo_final.map(lambda s: len(tok(s)))
g = korpus.groupby("genre").agg(dokumen=("doc_id", "nunique"), pasangan=("pair_id", "size"), kata_bt=("n_bt", "sum"),
                                kata_id=("n_id", "sum"), rata_bt=("n_bt", "mean"), rata_id=("n_id", "mean"))
g.loc["Total"] = [korpus.doc_id.nunique(), len(korpus), korpus.n_bt.sum(), korpus.n_id.sum(), korpus.n_bt.mean(), korpus.n_id.mean()]
simpan(g.round(2).reset_index(), "korpus_genre.csv")
mg = pd.read_csv(AKAR / "data/btb_multigenre.csv")
ag = mg[mg.title.str.contains("Agenda HKBP", na=False)]
RINGKAS["korpus"] = {"pasangan": len(korpus), "dokumen": int(korpus.doc_id.nunique()), "kata_bt": int(korpus.n_bt.sum()),
                     "kata_id": int(korpus.n_id.sum()), "kata_bt_terkumpul": int(mg.text_bt.map(lambda s: len(tok(s))).sum()),
                     "agenda_hkbp_dokumen": len(ag), "agenda_hkbp_kata_bt": int(ag.text_bt.map(lambda s: len(tok(s))).sum()),
                     "status_tinjauan": korpus.review_status.value_counts().to_dict()}

latih = split[split.split == "latih"].merge(korpus, on="pair_id")
vok_bt = {w for s in latih.toba_final for w in tok(s)}; vok_id = {w for s in latih.indo_final for w in tok(s)}
vok_bt_semua = vok_bt | {w for s in nx[nx.split == "latih"].teks_bbc for w in tok(s)} | {w for s in nt[nt.split == "latih"].teks_bbc for w in tok(s)}


def oov(tt, vok):
    w = [x for s in tt for x in tok(s)]
    return 100 * np.mean([x not in vok for x in w])


rows = []
for v in VERSI:
    u = UJI[v][UJI[v].set_uji == "kami"]
    for a, d in u.groupby("arah_asli"):
        rows.append({"rujukan": v, "arah_asli": a, "n": len(d), "panjang_bt": np.mean([len(tok(s)) for s in d.teks_bbc]),
                     "panjang_id": np.mean([len(tok(s)) for s in d.teks_id]),
                     "oov_bt_latih_kami": oov(d.teks_bbc, vok_bt), "oov_bt_semua_latih": oov(d.teks_bbc, vok_bt_semua),
                     "oov_id_latih_kami": oov(d.teks_id, vok_id),
                     "kata_bersama_persen": 100 * np.mean([len(set(tok(b)) & set(tok(i))) / max(1, len(set(tok(b))))
                                                           for b, i in zip(d.teks_bbc, d.teks_id)]),
                     "chrf_salin_id2bbc": CHRF_M.corpus_score(list(d.teks_id), [list(d.teks_bbc)]).score})
simpan(pd.DataFrame(rows).round(2), "kovariat.csv")

lg = pd.read_csv(RL / "hasil/tabel/s08_log_pelatihan.csv").dropna(subset=["loss_validasi"])
lk = lg.groupby("run")[["langkah", "epoch", "loss_validasi"]].apply(lambda d: pd.Series({"langkah": int(d.langkah.max()),
                                                    "epoch_loss_min": int(d.epoch.iloc[d.loss_validasi.values.argmin()]),
                                                    "loss_min": d.loss_validasi.min(), "loss_akhir": d.loss_validasi.iloc[-1]}))
lk["naik_dari_min"] = lk.loss_akhir - lk.loss_min
simpan(lk.round(3).reset_index(), "langkah_pelatihan.csv")
log("statistik korpus selesai")

# ======================================================================
# 6. Lembar penutur asli (opsional)
# ======================================================================
if arg.lembar:
    L = Path(arg.lembar); lb = {}

    def wilson(k, n, z=1.96):
        p = k / n; c = (p + z * z / (2 * n)) / (1 + z * z / n); h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        return [round(100 * (c - h), 1), round(100 * (c + h), 1)]

    if (L / "C1.xlsx").exists():
        c1 = pd.read_excel(L / "C1.xlsx", sheet_name="Periksa").merge(korpus[["pair_id", "doc_id"]], on="pair_id", how="left")
        c1["arah_asli"] = c1.doc_id.map(lab.set_index("doc_id").arah_final)
        n_rev = int((c1.keputusan == "revise_translation").sum())
        lb["C1"] = {"keputusan": c1.keputusan.value_counts().to_dict(), "revisi_wilson95": wilson(n_rev, len(c1)),
                    "per_genre": pd.crosstab(c1.genre, c1.keputusan).to_dict(),
                    "per_arah_asli": pd.crosstab(c1.arah_asli, c1.keputusan).to_dict(orient="index")}
    if (L / "C2.xlsx").exists():
        c2 = pd.read_excel(L / "C2.xlsx", sheet_name="Kategori").merge(E[["item_id", "sistem"]], on="item_id")
        # penyebut: semua butir id->bbc sistem itu (60), bukan hanya butir yang diberi tag [VARIETY]
        n_sis = E[E.arah == "id2bbc"].sistem.value_counts()
        lb["C2"] = {s: {"persen_AM_atau_Batak_lain": round(100 * g.kategori.isin(["AM_atau_Batak_lain", "keduanya"]).sum() / n_sis[s], 1),
                        "persen_serapan_Indonesia": round(100 * g.kategori.isin(["serapan_Indonesia", "keduanya"]).sum() / n_sis[s], 1),
                        "butir_bertag": len(g), "butir_total": int(n_sis[s])}
                    for s, g in c2.groupby("sistem")}
    if (L / "C3.xlsx").exists():
        c3 = pd.read_excel(L / "C3.xlsx", sheet_name="Label")
        lb["C3"] = c3.label.value_counts().to_dict()
    if (L / "C5.xlsx").exists():
        c5 = pd.read_excel(L / "C5.xlsx", sheet_name="Verifikasi")
        lb["C5"] = {"per_status": pd.crosstab(c5.status, c5.kategori).to_dict(orient="index"),
                    "penanda_lama_bukan_AM_saja": c5[(c5.status == "penanda lama") & (c5.kategori != "AM_saja")]
                    .set_index("bentuk").kategori.to_dict()}
    RINGKAS["lembar_penutur"] = lb
    log("lembar penutur:", list(lb))

# ======================================================================
# 7. Verifikasi terhadap tabel yang sudah dirilis (versi rujukan lama)
# ======================================================================
T = RL / "hasil/tabel"


def cocok(nama, a, b, kunci, kolom, tol=0.011):
    m = a.merge(b, on=kunci, suffixes=("_baru", "_rilis"))
    for c in kolom:
        selisih = (m[f"{c}_baru"] - m[f"{c}_rilis"]).abs().max()
        VERIF.append({"pemeriksaan": nama, "kolom": c, "baris_dicocokkan": len(m), "baris_rilis": len(b),
                      "selisih_maks": round(float(selisih), 4), "lolos": bool(len(m) == len(b) and selisih <= tol)})


cocok("s10_skor", SK[SK.rujukan == "lama"], pd.read_csv(T / "s10_skor.csv"),
      ["sistem", "set_uji", "dimensi", "nilai", "arah"], ["chrf", "bleu", "chrf_ik_bawah", "chrf_ik_atas"])
cocok("holm_lama", HOLM["lama"], pd.read_csv(T / "tambahan_perbandingan_holm.csv"),
      ["sistem_a", "sistem_b", "set_uji", "dimensi", "nilai", "arah"], ["selisih_chrf", "ik_bawah", "ik_atas", "p_holm"], tol=0.011)
cocok("holm_terkoreksi", HOLM["terkoreksi"], pd.read_csv(T / "c6_perbandingan_holm.csv"),
      ["sistem_a", "sistem_b", "set_uji", "dimensi", "nilai", "arah"], ["selisih_chrf", "p_holm"], tol=0.011)
r = pd.read_csv(OUT / "tabel3_lama.csv"); rr = pd.read_csv(T / "tambahan_tabel3_ik.csv")
cocok("tabel3_lama", r, rr, ["sistem", "arah"], ["asli_indonesia", "asli_toba", "selisih_toba_minus_indonesia"])
va = VAR[VAR.daftar == "am32"]
cocok("varietas_keluaran", va, pd.read_csv(T / "s10_varietas_keluaran.csv"), ["sistem", "set_uji"], ["persen_AM"], tol=0.006)
au = AUD[(AUD.daftar == "am32") & (AUD.himpunan == "korpus_kami")].assign(korpus="Korpus kami", split="semua")
cocok("audit_korpus_kami", au, pd.read_csv(T / "s03_audit_varietas.csv").query("korpus == 'Korpus kami'"),
      ["korpus", "split"], ["persen_AM", "persen_Toba_saja"], tol=0.006)
kes = pd.read_csv(T / "s13_kesepakatan.csv").melt(id_vars=["arah", "n"], var_name="ukuran", value_name="nilai").dropna()
cocok("esa_kesepakatan", pd.read_csv(OUT / "esa_kesepakatan.csv"), kes[["arah", "ukuran", "nilai"]], ["arah", "ukuran"], ["nilai"], tol=0.0015)
cocok("esa_kendall_lama", KEN[KEN.rujukan == "lama"], pd.read_csv(T / "s13_korelasi_metrik.csv"),
      ["arah", "cakupan", "metrik"], ["kendall_tau_b", "ik_bawah", "ik_atas"], tol=0.0015)
cocok("esa_skor_manusia", pd.read_csv(OUT / "esa_skor_manusia.csv"), pd.read_csv(T / "s13_skor_manusia.csv"),
      ["arah", "sistem"], ["skor_rata"], tol=0.011)
cocok("esa_persen_mayor (rilis dibulatkan 1 desimal)", pd.read_csv(OUT / "esa_skor_manusia.csv"), pd.read_csv(T / "s13_skor_manusia.csv"),
      ["arah", "sistem"], ["persen_mayor"], tol=0.051)
# Selang skor manusia hanya informatif: urutan butir di esa_anonim.csv diacak saat anonimisasi, sehingga sampel
# bootstrap-nya berbeda dari S13 walau titik tengahnya sama. Toleransi 1,5 poin.
cocok("esa_skor_manusia_ik (informatif)", pd.read_csv(OUT / "esa_skor_manusia.csv"), pd.read_csv(T / "s13_skor_manusia.csv"),
      ["arah", "sistem"], ["ik_bawah", "ik_atas"], tol=1.5)
c6 = pd.read_csv(T / "c6_skor_lama_baru.csv")
sk = SK[(SK.set_uji == "kami") & (SK.dimensi.isin(["semua", "arah_asli"]))].pivot_table(
    index=["sistem", "arah", "nilai"], columns="rujukan", values="chrf").reset_index()
sk["subset"] = sk.nilai.replace({"semua": "semua"})
cocok("c6_skor", sk.rename(columns={"lama": "chrf_lama", "terkoreksi": "chrf_baru"}), c6, ["sistem", "arah", "subset"],
      ["chrf_lama", "chrf_baru"], tol=0.006)
VF = pd.DataFrame(VERIF); simpan(VF, "verifikasi.csv")
print(VF.to_string(index=False))
RINGKAS["verifikasi_lolos"] = f"{int(VF.lolos.sum())} dari {len(VF)}"
json.dump(RINGKAS, open(OUT / "ringkasan.json", "w"), indent=1, ensure_ascii=False, default=str)
log("selesai. verifikasi lolos:", RINGKAS["verifikasi_lolos"])
