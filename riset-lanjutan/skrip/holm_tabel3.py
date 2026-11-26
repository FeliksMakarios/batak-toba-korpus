"""Uji beda berpasangan ulang (B besar) + koreksi Holm, dan selang kepercayaan Tabel 3.

Pemakaian: python -I holm_tabel3.py <s05_uji.csv> <folder_prediksi> <folder_keluaran> <B>
Logika sama dengan S10 di notebook: statistik chrF++ per kalimat, indeks sampel ulang
dari RandomState(12345) yang sama untuk semua sistem dengan n kalimat sama.
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
from sacrebleu.metrics import CHRF

P_UJI, DIR_PRED, DIR_OUT, B = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
DIR_OUT.mkdir(parents=True, exist_ok=True)
CHRF_M = CHRF(word_order=2)
ARAH = ["id2bbc", "bbc2id"]

uji = pd.read_csv(P_UJI, keep_default_na=False)


def muat(sistem, s, arah):
    p = DIR_PRED / sistem / f"{s}.{arah}.jsonl"
    if not p.exists() and s == "nusatranslation_toba":
        # seperti S10: butir NT-Toba adalah bagian dari set NusaTranslation penuh
        p = DIR_PRED / sistem / f"nusatranslation.{arah}.jsonl"
    if not p.exists():
        return None
    return {json.loads(b)["uji_id"]: json.loads(b)["hipotesis"] for b in p.read_text(encoding="utf-8").splitlines()[1:]}


def subset_list():
    out = []
    for s in ["kami", "nusax", "nusatranslation", "nusatranslation_toba"]:
        d = uji[uji.set_uji == s].reset_index(drop=True)
        out.append((s, "semua", "semua", d))
        if s == "kami":
            for v, g in d.groupby("arah_asli"):
                out.append((s, "arah_asli", v, g.reset_index(drop=True)))
    return out


def stat(hip, ruj):
    return np.array(CHRF_M._extract_corpus_statistics(hip, [ruj]), dtype=float)


def skor(S):
    return CHRF_M._compute_score_from_stats(S.tolist()).score


_W = {}


def bobot(n, benih=12345):
    # matriks hitungan: berapa kali kalimat j terambil pada sampel ulang ke-b
    if (n, benih) not in _W:
        idx = np.random.RandomState(benih).randint(0, n, size=(B, n))
        W = np.zeros((B, n), dtype=np.float32)
        np.add.at(W, (np.repeat(np.arange(B), n), idx.ravel()), 1)
        _W[(n, benih)] = W
    return _W[(n, benih)]


def sampel_bootstrap(S, benih=12345):
    T = bobot(len(S), benih) @ S.astype(np.float32)
    return np.array([skor(t) for t in T.astype(float)])


CACHE = {}


def hitung(sistem, s, dim, nilai, d, arah, benih=12345):
    kunci = (sistem, s, dim, nilai, arah, benih)
    if kunci not in CACHE:
        pred = muat(sistem, s, arah)
        if pred is None:
            CACHE[kunci] = None
        else:
            hip = [pred[i] for i in d.uji_id]
            ruj = list(d.teks_bbc if arah == "id2bbc" else d.teks_id)
            S = stat(hip, ruj)
            CACHE[kunci] = (skor(S.sum(0)), sampel_bootstrap(S, benih))
    return CACHE[kunci]


# ---------- 1) uji beda berpasangan ----------
PASANGAN = [("ft_kami+nusatranslation_s42", "ft_nusatranslation_s42"), ("ft_kami+nusax_s42", "ft_nusax_s42"),
            ("ft_kami_s42", "ft_nusax_s42"), ("ft_kami_s42", "ft_nusatranslation_s42")]
for m in ["llm_gemma3-27b-cpt-gotoai-v3-instruct_", "llm_qwen2.5-7b-instruct_"]:
    PASANGAN += [(m + "few_shot_retrieval", m + "few_shot_acak"), (m + "few_shot_acak", m + "zero_shot")]

baris = []
for a, b in PASANGAN:
    for s, dim, nilai, d in subset_list():
        for arah in ARAH:
            ra, rb = hitung(a, s, dim, nilai, d, arah), hitung(b, s, dim, nilai, d, arah)
            if ra is None or rb is None:
                continue
            dd = ra[1] - rb[1]
            p_lama = 2 * min((dd <= 0).mean(), (dd >= 0).mean())
            # versi (k+1)/(B+1): tidak pernah 0, sehingga sah untuk koreksi Holm
            p = min(1.0, 2 * min(((dd <= 0).sum() + 1) / (B + 1), ((dd >= 0).sum() + 1) / (B + 1)))
            baris.append({"sistem_a": a, "sistem_b": b, "set_uji": s, "dimensi": dim, "nilai": nilai, "arah": arah,
                          "selisih_chrf": round(ra[0] - rb[0], 2), "ik_bawah": round(np.percentile(dd, 2.5), 2),
                          "ik_atas": round(np.percentile(dd, 97.5), 2), "p_dua_sisi_tanpa_koreksi_lama": round(p_lama, 4),
                          "p_dua_sisi": p})
beda = pd.DataFrame(baris)

# Holm (step-down) atas seluruh perbandingan
m = len(beda)
urut = np.argsort(beda.p_dua_sisi.values, kind="stable")
p_holm = np.empty(m)
maks = 0.0
for rank, i in enumerate(urut):
    maks = max(maks, min(1.0, (m - rank) * beda.p_dua_sisi.values[i]))
    p_holm[i] = maks
beda["p_holm"] = p_holm
beda["signifikan_holm_0_05"] = np.where(beda.p_holm < 0.05, "ya", "tidak")
beda["p_dua_sisi"] = beda.p_dua_sisi.round(5)
beda["p_holm"] = beda.p_holm.round(4)
beda.drop(columns=["p_dua_sisi_tanpa_koreksi_lama"]).to_csv(DIR_OUT / "tambahan_perbandingan_holm.csv", index=False)
print(f"{m} perbandingan, B = {B}; lolos Holm: {(beda.p_holm < 0.05).sum()}")

# ---------- 2) Tabel 3: chrF++ menurut bahasa asli, dengan selang 95% ----------
SISTEM_T3 = ["copy_source", "madlad3b_zeroshot", "ft_nusatranslation_s42", "ft_kami_s42",
             "ft_kami+nusatranslation_s42", "llm_gemma3-27b-cpt-gotoai-v3-instruct_few_shot_retrieval"]
sub = {v: d for s, dim, v, d in subset_list() if dim == "arah_asli"}
t3 = []
for sistem in SISTEM_T3:
    for arah in ARAH:
        ri = hitung(sistem, "kami", "arah_asli", "asli_indonesia", sub["asli_indonesia"], arah)
        # benih lain untuk subset Toba agar sampel kedua subset saling bebas
        rt = hitung(sistem, "kami", "arah_asli", "asli_toba", sub["asli_toba"], arah, benih=54321)
        dd = rt[1] - ri[1]
        p = min(1.0, 2 * min(((dd <= 0).sum() + 1) / (B + 1), ((dd >= 0).sum() + 1) / (B + 1)))
        t3.append({"sistem": sistem, "arah": arah,
                   "asli_indonesia": round(ri[0], 2), "asli_indonesia_ik": f"[{np.percentile(ri[1], 2.5):.1f}, {np.percentile(ri[1], 97.5):.1f}]",
                   "asli_toba": round(rt[0], 2), "asli_toba_ik": f"[{np.percentile(rt[1], 2.5):.1f}, {np.percentile(rt[1], 97.5):.1f}]",
                   "selisih_toba_minus_indonesia": round(rt[0] - ri[0], 2),
                   "selisih_ik": f"[{np.percentile(dd, 2.5):.1f}, {np.percentile(dd, 97.5):.1f}]", "p_dua_sisi": round(p, 5)})
pd.DataFrame(t3).to_csv(DIR_OUT / "tambahan_tabel3_ik.csv", index=False)
print(pd.DataFrame(t3).to_string())
