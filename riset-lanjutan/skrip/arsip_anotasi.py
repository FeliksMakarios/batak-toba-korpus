"""Arsip hasil anotasi penutur asli (C1 sampai C6) dalam bentuk stand-off yang bisa dirilis.

Semua berkas memakai ID butir. Teks NusaX dan NusaTranslation tidak disalin; label untuk kedua korpus itu
dikaitkan lewat `id_asli` (ID resmi di rilis IndoNLP) dan `uji_id` (ID posisi yang dipakai di riset ini).

Pemakaian (dari akar repo):
  python riset-lanjutan/skrip/arsip_anotasi.py <folder_lembar_C1-C6> <s02_nusatranslation.csv>
Keluaran: riset-lanjutan/data/anotasi_penutur/*.csv
"""
import re, sys
from pathlib import Path
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
RL = AKAR / "riset-lanjutan"
L, P_NT = Path(sys.argv[1]), sys.argv[2]
OUT = RL / "data" / "anotasi_penutur"
OUT.mkdir(parents=True, exist_ok=True)

korpus = pd.read_csv(AKAR / "data/btb_parallel_sentence.csv")
split = pd.read_csv(RL / "data/split_korpus_kami.csv")[["pair_id", "uji_id", "split"]]
asal = korpus.set_index("pair_id")

# ---------- 1. penilaian dan koreksi korpus kita (C1 dan C6) ----------
c1 = pd.read_excel(L / "C1.xlsx", sheet_name="Periksa")
c1 = c1.merge(split, on="pair_id", how="left")
p1 = pd.DataFrame({"pair_id": c1.pair_id, "split": c1.split, "lembar": "C1", "keputusan": c1.keputusan,
                   "teks_bbc_baru": c1.perbaikan_toba.fillna("").astype(str).str.strip(),
                   "teks_id_baru": c1.perbaikan_indonesia.fillna("").astype(str).str.strip(),
                   "catatan": c1.catatan.fillna("")})
c6 = pd.read_csv(RL / "data/set_uji_kami_terkoreksi.csv", keep_default_na=False)
c6["pair_id"] = c6.uji_id.str[5:]
p6 = pd.DataFrame({"pair_id": c6.pair_id, "split": "uji", "lembar": "C6", "keputusan": c6.keputusan,
                   "teks_bbc_baru": [b if b != a else "" for a, b in zip(c6.teks_bbc_lama, c6.teks_bbc_baru)],
                   "teks_id_baru": [b if b != a else "" for a, b in zip(c6.teks_id_lama, c6.teks_id_baru)],
                   "catatan": c6.catatan_anotator})
nilai = pd.concat([p1, p6], ignore_index=True)
nilai.to_csv(OUT / "penilaian_korpus_kami.csv", index=False)

# koreksi akhir per pasangan: C6 (pemeriksaan penuh set uji) mengalahkan C1 untuk butir yang sama
rows = []
for pid, g in nilai.groupby("pair_id", sort=False):
    g = g.sort_values("lembar", key=lambda s: s.map({"C6": 0, "C1": 1}))
    bt = next((x for x in g.teks_bbc_baru if x), "")
    idn = next((x for x in g.teks_id_baru if x), "")
    if g.iloc[0].lembar == "C6":          # untuk butir uji, hanya keputusan C6 yang berlaku
        bt, idn = g.iloc[0].teks_bbc_baru, g.iloc[0].teks_id_baru
    if bt or idn:
        rows.append({"pair_id": pid, "split": g.iloc[0].split, "sumber": "+".join(sorted(set(g.lembar))),
                     "keputusan": g.iloc[0].keputusan,
                     "teks_bbc_lama": asal.loc[pid, "toba_final"], "teks_bbc_baru": bt or asal.loc[pid, "toba_final"],
                     "teks_id_lama": asal.loc[pid, "indo_final"], "teks_id_baru": idn or asal.loc[pid, "indo_final"]})
kor = pd.DataFrame(rows)
kor.to_csv(OUT / "koreksi_korpus_kami.csv", index=False)
print("penilaian:", nilai.lembar.value_counts().to_dict(), "| pasangan dikoreksi:", len(kor), kor.split.value_counts().to_dict())

# ---------- 2. empat kalimat korpus kita yang bertanda AM (putusan penutur asli) ----------
am = pd.DataFrame({"pair_id": ["doc_0072_s005_a", "doc_0075_s018", "doc_0075_s022", "doc_0076_s064"],
                   "penanda": ["giot", "giot, tai", "juo", "giot, juo"],
                   "putusan_penutur": ["Toba_wajar", "ada_unsur_AM", "ada_unsur_AM", "ada_unsur_AM"]})
am.to_csv(OUT / "putusan_am_korpus_kami.csv", index=False)

# ---------- 3. label varietas NusaTranslation dari penutur asli (C3) ----------
nt = pd.read_csv(P_NT, keep_default_na=False).set_index("uji_id")
c3 = pd.read_excel(L / "C3.xlsx", sheet_name="Label")
pd.DataFrame({"uji_id": c3.id, "id_asli": c3.id.map(nt.id_asli), "penanda_terdeteksi": c3.penanda_terdeteksi,
              "label_penutur": c3.label, "catatan": c3.catatan.fillna("")}).to_csv(OUT / "label_varietas_nusatranslation_c3.csv", index=False)

# ---------- 4. label varietas otomatis untuk seluruh NusaX dan NusaTranslation ----------
tok = lambda s: re.findall(r"\w+", str(s).lower())
leks = pd.read_csv(RL / "data/leksikon_am_terverifikasi.csv")
KUAT, LEMAH = set(leks[leks.kekuatan_penanda == "kuat"].bentuk), set(leks[leks.kekuatan_penanda == "lemah"].bentuk)
AM32 = set("inda madung kehe akkon angkon anso harana bope giot doma milas mur pade halai adaboru oppot "
           "ngen juo tai sannari soni sattak napedo abope unjung deges sarupo copat satiop manyogot natuari tarimokasih".split())
TOBA = set("dang ndang nunga nungga sian naeng jabu alai unang ahu ibana nasida".split())


def ngram(t):
    return set(t) | {" ".join(t[i:i + 2]) for i in range(len(t) - 1)} | {" ".join(t[i:i + 3]) for i in range(len(t) - 2)}


def label(teks):
    t = tok(teks); g = ngram(t); w = set(t)
    k, l = sorted(g & KUAT), sorted(g & LEMAH)
    am32 = "AM" if w & AM32 else ("Toba_saja" if w & TOBA else "tak_bertanda")
    lk = "AM" if (k or len(l) >= 2) else ("AM_lemah" if l else ("Toba_saja" if w & TOBA else "tak_bertanda"))
    return am32, lk, ", ".join(k), ", ".join(l)


rows = []
for uid, r in nt.iterrows():
    rows.append(("nusatranslation", uid, r.id_asli, r.split, *label(r.teks_bbc)))
P_NX = Path(P_NT).with_name("s02_nusax.csv")
if P_NX.exists():
    for r in pd.read_csv(P_NX, keep_default_na=False).itertuples():
        rows.append(("nusax", r.uji_id, "", r.split, *label(r.teks_bbc)))
lab = pd.DataFrame(rows, columns=["korpus", "uji_id", "id_asli", "split", "label_am32", "label_leksikon",
                                  "bentuk_kuat", "bentuk_lemah"])
lab.to_csv(OUT / "label_varietas_otomatis.csv", index=False)
print(pd.crosstab([lab.korpus], lab.label_leksikon).to_string())
print(pd.crosstab(lab.label_am32, lab.label_leksikon).to_string())

# ---------- 5. kategori tag [VARIETY] pada keluaran sistem (C2) dan glos contoh (C4) ----------
c2 = pd.read_excel(L / "C2.xlsx", sheet_name="Kategori")
c2[["item_id", "penanda_AM_otomatis", "kategori", "kata_bermasalah", "catatan"]].to_csv(OUT / "kategori_variety_esa_c2.csv", index=False)
c4 = pd.read_excel(L / "C4.xlsx", sheet_name="Contoh")
c4.to_csv(OUT / "glos_contoh_kualitatif_c4.csv", index=False)
print("selesai:", sorted(p.name for p in OUT.iterdir()))
