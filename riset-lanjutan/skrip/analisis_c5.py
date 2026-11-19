"""Analisis hasil C5 (verifikasi kosakata Angkola-Mandailing) dan uji kepekaan angka penanda AM di naskah.

Pemakaian: python analisis_c5.py <repo> <C5.xlsx> <folder_paket_keluaran> <folder_keluaran>
Keluaran:
  leksikon_am_terverifikasi.csv  bentuk, jenis, kategori, arti, padanan Toba (tanpa contoh kalimat pihak ketiga)
  c5_presisi.csv                 sebaran kategori per status (penanda lama, kandidat statistik, dari penutur)
  c5_kepekaan_korpus.csv         persentase kalimat bertanda AM per korpus untuk tiap daftar penanda
  c5_kepekaan_keluaran.csv       persentase keluaran id->bbc bertanda AM per sistem dan set uji
"""
import json, re, sys
from pathlib import Path
import pandas as pd

REPO, P_C5, PAKET, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
RL = REPO / "riset-lanjutan"
tok = lambda s: re.findall(r"\w+", str(s).lower())     # sama dengan token_kata di notebook

LAMA = set("inda madung kehe akkon angkon anso harana bope giot doma milas mur pade halai adaboru oppot "
           "ngen juo tai sannari soni sattak napedo abope unjung deges sarupo copat satiop manyogot "
           "natuari tarimokasih".split())

v = pd.read_excel(P_C5, sheet_name="Verifikasi")
v["bentuk"] = v.bentuk.str.strip().str.lower()
kat = v.set_index("bentuk").kategori

# ---------- 1. presisi per status ----------
pres = pd.crosstab(v.status, v.kategori, margins=True)
pres["presisi_AM_saja"] = (pres.get("AM_saja", 0) / pres["All"]).round(3)
pres["presisi_AM_termasuk_perbatasan"] = ((pres.get("AM_saja", 0) + pres.get("AM_dan_Toba_perbatasan", 0)) / pres["All"]).round(3)
pres.to_csv(OUT / "c5_presisi.csv")
print(pres.to_string())

# ---------- 2. leksikon terverifikasi (dirilis) ----------
leks = v[["bentuk", "jenis", "status", "kalimat_AM", "kalimat_Toba", "kategori", "arti_Indonesia", "padanan_Toba", "catatan"]]
leks = leks.sort_values(["kategori", "jenis", "kalimat_AM"], ascending=[True, False, False])
leks.to_csv(OUT / "leksikon_am_terverifikasi.csv", index=False)


# ---------- 3. daftar penanda untuk uji kepekaan ----------
def bentuk(kategori, jenis=None, hanya_lama=False):
    d = v[v.kategori.isin(kategori)]
    if jenis:
        d = d[d.jenis == jenis]
    if hanya_lama:
        d = d[d.bentuk.isin(LAMA)]
    return set(d.bentuk)


DAFTAR = {
    "lama_32": (LAMA, set()),
    "lama_tanpa_toba_umum_29": (LAMA - bentuk(["juga_Toba_umum", "bukan_Batak"]), set()),
    "lama_AM_saja_26": (bentuk(["AM_saja"], hanya_lama=True), set()),
    "leksikon_AM_saja": (bentuk(["AM_saja"]), set()),
}
PERBATASAN = bentuk(["AM_dan_Toba_perbatasan"])
print({k: len(a) for k, (a, _) in DAFTAR.items()}, "perbatasan", len(PERBATASAN))


def ngram(t):
    return set(t) | {" ".join(t[i:i + 2]) for i in range(len(t) - 1)} | {" ".join(t[i:i + 3]) for i in range(len(t) - 2)}


def tanda(teks, nama):
    g = ngram(tok(teks))
    if nama == "aturan_saring":
        # >=1 bentuk AM_saja, atau >=2 bentuk perbatasan yang berbeda
        return bool(g & DAFTAR["leksikon_AM_saja"][0]) or len(g & PERBATASAN) >= 2
    return bool(g & DAFTAR[nama][0])


NAMA = list(DAFTAR) + ["aturan_saring"]

# ---------- 4. kepekaan: korpus ----------
korpus = pd.read_csv(PAKET / "s01_korpus.csv", keep_default_na=False)
nx = pd.read_csv(PAKET / "s02_nusax.csv", keep_default_na=False)
nt = pd.read_csv(PAKET / "s02_nusatranslation.csv", keep_default_na=False)
uji = pd.read_csv(PAKET / "s05_uji.csv", keep_default_na=False)
himp = {"korpus_kami": korpus.teks_bbc, "nusax_semua": nx.teks_bbc, "nusatranslation_semua": nt.teks_bbc,
        "nusatranslation_uji": nt[nt.split == "uji"].teks_bbc,
        "rujukan_uji_nusatranslation_toba": uji[uji.set_uji == "nusatranslation_toba"].teks_bbc,
        "rujukan_uji_kami": uji[uji.set_uji == "kami"].teks_bbc}
rows = []
for h, teks in himp.items():
    r = {"himpunan": h, "n": len(teks)}
    for n in NAMA:
        f = teks.map(lambda t: tanda(t, n))
        r[f"persen_{n}"] = round(f.mean() * 100, 2); r[f"jumlah_{n}"] = int(f.sum())
    rows.append(r)
kp = pd.DataFrame(rows); kp.to_csv(OUT / "c5_kepekaan_korpus.csv", index=False)
print(kp[["himpunan", "n"] + [f"persen_{n}" for n in NAMA]].to_string(index=False))
print(kp[["himpunan"] + [f"jumlah_{n}" for n in NAMA]].to_string(index=False))

# kalimat korpus kami yang bertanda
for n in NAMA:
    f = korpus[korpus.teks_bbc.map(lambda t: tanda(t, n))]
    print(n, list(f.pair_id))

# ---------- 5. kepekaan: keluaran id->bbc ----------
rows = []
for d in sorted((RL / "prediksi").iterdir()):
    for s in ["kami", "nusax", "nusatranslation", "nusatranslation_toba"]:
        p = d / f"{s}.id2bbc.jsonl"
        if not p.exists():
            continue
        L = p.read_text(encoding="utf-8").splitlines()[1:]
        hip = pd.Series([json.loads(l)["hipotesis"] for l in L])
        r = {"sistem": d.name, "set_uji": s, "n": len(hip)}
        for n in NAMA:
            r[f"persen_{n}"] = round(hip.map(lambda t: tanda(t, n)).mean() * 100, 2)
        rows.append(r)
kk = pd.DataFrame(rows); kk.to_csv(OUT / "c5_kepekaan_keluaran.csv", index=False)
kk["grup"] = kk.sistem.str.replace(r"_s\d+$", "", regex=True)
g = kk.groupby(["grup", "set_uji"])[[f"persen_{n}" for n in NAMA]].mean().round(1).reset_index()
pd.set_option("display.width", 250)
print(g[g.grup.str.contains("nusatranslation|gotoai.*retrieval|madlad|ft_kami_?$|ft_kami$")].to_string(index=False))
g.to_csv(OUT / "c5_kepekaan_keluaran_rata_benih.csv", index=False)
