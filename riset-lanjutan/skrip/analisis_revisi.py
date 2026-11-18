"""Angka-angka baru untuk revisi naskah LRE (kelompok A).

Pemakaian: python analisis_revisi.py <repo> <folder_paket_keluaran> <folder_keluaran>
"""
import json, re, sys
from pathlib import Path
import numpy as np, pandas as pd

REPO, PAKET, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
RL = REPO / "riset-lanjutan"
OUT.mkdir(parents=True, exist_ok=True)
tok = lambda s: re.findall(r"\w+", str(s).lower())
hasil = {}

# ---------- A1 statistik per genre ----------
p = pd.read_csv(REPO / "data/btb_parallel_sentence.csv")
lab = pd.read_csv(RL / "metadata/arah_penerjemahan.csv")
p["n_bt"] = p.toba_final.map(lambda s: len(tok(s)))
p["n_id"] = p.indo_final.map(lambda s: len(tok(s)))
dom = lab.set_index("doc_id").domain_sumber
g = p.groupby("genre").agg(dok=("doc_id", "nunique"), pasangan=("pair_id", "size"), kata_bt=("n_bt", "sum"),
                           kata_id=("n_id", "sum"), rata_bt=("n_bt", "mean"), rata_id=("n_id", "mean"))
g["domain"] = p.groupby("genre").doc_id.apply(lambda d: ", ".join(dom.reindex(d.unique()).value_counts().index[:4]))
g.loc["Total"] = [p.doc_id.nunique(), len(p), p.n_bt.sum(), p.n_id.sum(), p.n_bt.mean(), p.n_id.mean(), ""]
g.to_csv(OUT / "a1_genre.csv")
print(g.round(1).to_string())
m = pd.read_csv(REPO / "data/btb_multigenre.csv")
ag = m[m.title.str.contains("Agenda HKBP", na=False)]
hasil["agenda"] = {"dokumen": len(ag), "kata_bt": int(ag.text_bt.map(lambda s: len(tok(s))).sum()),
                   "semua_kata_bt": int(m.text_bt.map(lambda s: len(tok(s))).sum())}
print(hasil["agenda"])
print(p.review_status.value_counts().to_dict())

# ---------- A3 kovariat pembaur ----------
uji = pd.read_csv(PAKET / "s05_uji.csv", keep_default_na=False)
k = uji[uji.set_uji == "kami"]
latih = pd.read_csv(PAKET / "s05_latih_kami.csv", keep_default_na=False)
print("kolom latih:", latih.columns.tolist())
kol_bt, kol_id = "teks_bbc", "teks_id"
vok_bt = set(w for s in latih[kol_bt] for w in tok(s)); vok_id = set(w for s in latih[kol_id] for w in tok(s))
lain = [pd.read_csv(PAKET / f"s05_latih_{n}.csv", keep_default_na=False) for n in ["nusax", "nusatranslation"]]
vok_bt_all = vok_bt | set(w for d in lain for s in d[kol_bt] for w in tok(s))
def oov(teks, vok):
    t = [w for s in teks for w in tok(s)]
    return 100 * np.mean([w not in vok for w in t])
from sacrebleu.metrics import CHRF
chrf = CHRF(word_order=2)
baris = []
for a, d in k.groupby("arah_asli"):
    baris.append({"arah_asli": a, "n": len(d), "panjang_bt": np.mean([len(tok(s)) for s in d.teks_bbc]),
                  "panjang_id": np.mean([len(tok(s)) for s in d.teks_id]),
                  "rasio_panjang_bt_id": np.mean([len(tok(b)) / max(1, len(tok(i))) for b, i in zip(d.teks_bbc, d.teks_id)]),
                  "oov_bt_latih_kami": oov(d.teks_bbc, vok_bt), "oov_bt_semua_latih": oov(d.teks_bbc, vok_bt_all),
                  "oov_id_latih_kami": oov(d.teks_id, vok_id),
                  "tumpang_tindih_kata": 100 * np.mean([len(set(tok(b)) & set(tok(i))) / max(1, len(set(tok(b)))) for b, i in zip(d.teks_bbc, d.teks_id)]),
                  "chrf_salin_id2bbc": chrf.corpus_score(list(d.teks_id), [list(d.teks_bbc)]).score})
kov = pd.DataFrame(baris); kov.to_csv(OUT / "a3_kovariat.csv", index=False); print(kov.round(2).to_string())

# ---------- A4 paradoks kesalahan mayor ----------
e = pd.read_csv(RL / "data/esa_anonim.csv")
rows = []
for (arah, s), d in e.groupby(["arah", "sistem"]):
    r = {"arah": arah, "sistem": s}
    for x in "AB":
        r[f"mayor_{x}"] = 100 * d[f"kesalahan_mayor_{x}"].notna().mean()
        r[f"minor_{x}"] = 100 * d[f"kesalahan_minor_{x}"].notna().mean()
        r[f"n_minor_{x}"] = d[f"kesalahan_minor_{x}"].fillna("").map(lambda v: len([q for q in str(v).split("|") if q.strip()])).mean()
        r[f"skor_{x}"] = d[f"skor_{x}"].mean()
        if arah == "id2bbc":
            r[f"variety_{x}"] = 100 * d[f"variety_{x}"].mean()
    rows.append(r)
par = pd.DataFrame(rows); par.to_csv(OUT / "a4_paradoks.csv", index=False)
print(par[par.arah == "id2bbc"].round(1).to_string())
# skor rata-rata untuk butir tanpa kesalahan mayor menurut masing-masing penilai
for s in ["ft_kami+nusatranslation_s42", "ft_nusatranslation_s42"]:
    d = e[(e.arah == "id2bbc") & (e.sistem == s)]
    for x in "AB":
        tanpa = d[d[f"kesalahan_mayor_{x}"].isna()][f"skor_{x}"].mean(); dengan = d[d[f"kesalahan_mayor_{x}"].notna()][f"skor_{x}"].mean()
        print(s[:20], x, "skor tanpa mayor", round(tanpa, 1), "dengan mayor", round(dengan, 1))

# ---------- A5 selang kepercayaan alfa dan kappa ----------
def alfa_interval(a, b):
    v = np.concatenate([a, b]); n = len(v)
    do = np.mean((a - b) ** 2)
    de = np.sum((v[:, None] - v[None, :]) ** 2) / (n * (n - 1))
    return 1 - do / de
def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b)
    po = np.mean(a == b); kat = np.union1d(a, b)
    pe = sum(np.mean(a == c) * np.mean(b == c) for c in kat)
    return (po - pe) / (1 - pe) if pe < 1 else np.nan
rng = np.random.RandomState(12345); B = 10000; ci = []
for arah, d in e.groupby("arah"):
    sa, sb = d.skor_A.values.astype(float), d.skor_B.values.astype(float)
    ma, mb = d.kesalahan_mayor_A.notna().values, d.kesalahan_mayor_B.notna().values
    ukur = {"alfa": lambda i: alfa_interval(sa[i], sb[i]), "kappa_mayor": lambda i: kappa(ma[i], mb[i])}
    if arah == "id2bbc":
        va, vb = d.variety_A.values, d.variety_B.values
        ukur["kappa_variety"] = lambda i: kappa(va[i], vb[i])
    n = len(d); idx = rng.randint(0, n, size=(B, n)); semua = np.arange(n)
    for nama, f in ukur.items():
        sampel = np.array([f(i) for i in idx])
        ci.append({"arah": arah, "ukuran": nama, "nilai": f(semua), "bawah": np.nanpercentile(sampel, 2.5),
                   "atas": np.nanpercentile(sampel, 97.5)})
ci = pd.DataFrame(ci); ci.to_csv(OUT / "a5_ci.csv", index=False); print(ci.round(3).to_string())

# ---------- A6 BLEU ----------
s10 = pd.read_csv(RL / "hasil/tabel/s10_skor.csv")
s10 = s10[s10.dimensi == "semua"]
s10["grup"] = s10.sistem.str.replace(r"_s\d+$", "", regex=True)
bl = s10.groupby(["grup", "set_uji", "arah"])[["bleu", "chrf"]].mean().reset_index()
bl.to_csv(OUT / "a6_bleu.csv", index=False)
from sacrebleu.metrics import BLEU
m1, m2 = CHRF(word_order=2), BLEU(); m1.corpus_score(["a b"], [["a b"]]); m2.corpus_score(["a b"], [["a b"]])
hasil["signature"] = {"chrf": str(m1.get_signature()), "bleu": str(m2.get_signature())}
print(hasil["signature"])

# ---------- A7 langkah dan loss validasi ----------
lg = pd.read_csv(RL / "hasil/tabel/s08_log_pelatihan.csv")
lg2 = lg.dropna(subset=["loss_validasi"])
ringk = lg2.groupby("run").apply(lambda d: pd.Series({"langkah": d.langkah.max(),
        "val_epoch": "; ".join(f"{e}:{v:.3f}" for e, v in zip(d.epoch, d.loss_validasi))}))
ringk.to_csv(OUT / "a7_langkah.csv"); print(ringk.to_string())
json.dump(hasil, open(OUT / "ringkasan.json", "w"), indent=1)
