"""Set uji terkoreksi (C6) dan penilaian ulang semua sistem tanpa GPU.

Pemakaian: python nilai_ulang_c6.py <repo> <s05_uji.csv> <C6.xlsx> <folder_keluaran>
Keluaran: s05_uji_c6.csv (set uji terkoreksi), skor lama vs baru, Kendall tau ESA lama vs baru.
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
from sacrebleu.metrics import BLEU, CHRF
from scipy.stats import kendalltau

REPO, P_UJI, P_C6, OUT = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
RL = REPO / "riset-lanjutan"
chrf, bleu = CHRF(word_order=2), BLEU()

u = pd.read_csv(P_UJI, keep_default_na=False)
t = pd.read_excel(P_C6, sheet_name="Rujukan_Toba").set_index("uji_id")
i = pd.read_excel(P_C6, sheet_name="Rujukan_Indonesia_opsional").set_index("uji_id")
baru = u.copy()
ub = t[t.keputusan != "benar"].rujukan_toba_baru
ui = i[i.keputusan != "benar"].rujukan_indonesia_baru
m = baru.uji_id.isin(ub.index); baru.loc[m, "teks_bbc"] = baru.loc[m, "uji_id"].map(ub).str.strip()
m2 = baru.uji_id.isin(ui.index); baru.loc[m2, "teks_id"] = baru.loc[m2, "uji_id"].map(ui).str.strip()
baru.to_csv(OUT / "s05_uji_c6.csv", index=False)
print("rujukan Toba diubah", int(m.sum()), "| rujukan Indonesia diubah", int(m2.sum()))

# besarnya perubahan: chrF++ rujukan baru terhadap rujukan lama
lama_k = u[u.set_uji == "kami"].set_index("uji_id"); baru_k = baru[baru.set_uji == "kami"].set_index("uji_id")
ub_ids = list(ub.index)
s_ubah = [chrf.sentence_score(baru_k.teks_bbc[x], [lama_k.teks_bbc[x]]).score for x in ub_ids]
kep = t.keputusan
ringkas = {"diubah": int(m.sum()), "dari": len(t), "per_keputusan": kep.value_counts().to_dict(),
           "chrf_baru_vs_lama_median": float(np.median(s_ubah)),
           "chrf_baru_vs_lama_korpus": chrf.corpus_score([baru_k.teks_bbc[x] for x in ub_ids], [[lama_k.teks_bbc[x] for x in ub_ids]]).score,
           "per_genre": pd.crosstab(t.genre, t.keputusan).to_dict()}
for kp in ["perbaiki_kata", "perbaiki_makna"]:
    ids = [x for x in ub_ids if kep[x] == kp]
    ringkas[f"chrf_{kp}"] = chrf.corpus_score([baru_k.teks_bbc[x] for x in ids], [[lama_k.teks_bbc[x] for x in ids]]).score

# skor semua sistem, set uji kami, rujukan lama vs baru
def pred(sis, arah):
    L = (RL / f"prediksi/{sis}/kami.{arah}.jsonl").read_text(encoding="utf-8").splitlines()[1:]
    return {json.loads(l)["uji_id"]: json.loads(l)["hipotesis"] for l in L}
sistem = sorted(p.name for p in (RL / "prediksi").iterdir() if (p / "kami.id2bbc.jsonl").exists())
rows = []
for s in sistem:
    for arah in ["id2bbc", "bbc2id"]:
        P = pred(s, arah)
        for sub in ["semua", "asli_indonesia", "asli_toba"]:
            d_l = lama_k if sub == "semua" else lama_k[lama_k.arah_asli == sub]
            d_b = baru_k.loc[d_l.index]
            kol = "teks_bbc" if arah == "id2bbc" else "teks_id"
            hip = [P[x] for x in d_l.index]
            rows.append({"sistem": s, "arah": arah, "subset": sub, "n": len(hip),
                         "chrf_lama": chrf.corpus_score(hip, [list(d_l[kol])]).score,
                         "chrf_baru": chrf.corpus_score(hip, [list(d_b[kol])]).score,
                         "bleu_lama": bleu.corpus_score(hip, [list(d_l[kol])]).score,
                         "bleu_baru": bleu.corpus_score(hip, [list(d_b[kol])]).score})
sk = pd.DataFrame(rows); sk["selisih_chrf"] = sk.chrf_baru - sk.chrf_lama
sk["grup"] = sk.sistem.str.replace(r"_s\d+$", "", regex=True)
sk.round(2).to_csv(OUT / "skor_lama_baru.csv", index=False)
g = sk.groupby(["grup", "arah", "subset"])[["chrf_lama", "chrf_baru", "bleu_lama", "bleu_baru", "selisih_chrf"]].mean().reset_index()
g.round(2).to_csv(OUT / "skor_lama_baru_rata_benih.csv", index=False)
for sub in ["semua", "asli_indonesia"]:
    x = g[(g.arah == "id2bbc") & (g.subset == sub)].copy()
    x["rank_lama"] = x.chrf_lama.rank(ascending=False).astype(int); x["rank_baru"] = x.chrf_baru.rank(ascending=False).astype(int)
    print(f"\n== id2bbc, {sub}"); print(x.sort_values("chrf_baru", ascending=False)[["grup", "chrf_lama", "chrf_baru", "selisih_chrf", "rank_lama", "rank_baru"]].round(2).to_string(index=False))
    ringkas[f"spearman_rank_{sub}"] = float(x.rank_lama.corr(x.rank_baru, method="spearman"))
x = g[(g.arah == "bbc2id") & (g.subset == "asli_toba")]; print("\nbbc2id asli_toba selisih maks", x.selisih_chrf.abs().max().round(2))

# Kendall tau metrik vs skor manusia ESA, id2bbc, rujukan lama vs baru
e = pd.read_csv(RL / "data/esa_anonim.csv"); e = e[e.arah == "id2bbc"].copy()
e["manusia"] = (e.skor_A + e.skor_B) / 2
for versi, d in [("lama", lama_k), ("baru", baru_k)]:
    e[f"chrf_{versi}"] = [chrf.sentence_score(h, [d.teks_bbc[x]]).score for h, x in zip(e.terjemahan, e.uji_id)]
    e[f"bleu_{versi}"] = [bleu.sentence_score(h, [d.teks_bbc[x]]).score for h, x in zip(e.terjemahan, e.uji_id)]
ft = e.sistem.str.startswith("ft_")
rng = np.random.RandomState(12345); kt = []
for nama, d in [("semua", e), ("fine_tuned", e[ft])]:
    n = len(d); idx = rng.randint(0, n, size=(1000, n))
    for met in ["chrf", "bleu"]:
        for versi in ["lama", "baru"]:
            a, b = d[f"{met}_{versi}"].values, d.manusia.values
            tau = kendalltau(a, b).statistic
            bs = [kendalltau(a[j], b[j]).statistic for j in idx]
            kt.append({"kelompok": nama, "metrik": met, "rujukan": versi, "n": n, "tau": tau,
                       "bawah": np.nanpercentile(bs, 2.5), "atas": np.nanpercentile(bs, 97.5)})
kt = pd.DataFrame(kt); kt.round(3).to_csv(OUT / "kendall_lama_baru.csv", index=False); print(kt.round(3).to_string(index=False))
# skor chrF++ sistem ESA pada 60 kalimat: lama vs baru
print(e.groupby("sistem")[["manusia", "chrf_lama", "chrf_baru"]].mean().round(1).to_string())
ringkas["esa_item_ref_diubah"] = int(e.uji_id.isin(ub_ids).sum()); ringkas["esa_item_total"] = len(e)
json.dump(ringkas, open(OUT / "ringkasan_c6.json", "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in ringkas.items() if k != "per_genre"}, indent=1, default=str))
