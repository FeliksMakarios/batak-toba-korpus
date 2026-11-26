"""Kandidat kosakata dan frasa penanda Angkola-Mandailing (AM) untuk penyaringan data Batak Toba.

Metode: log-odds berbobot dengan prior Dirichlet informatif (Monroe, Colaresi dan Quinn 2008)
antara kalimat NusaTranslation yang memuat penanda AM dan kalimat Toba (NusaX, NusaTranslation
yang hanya memuat penanda Toba, dan korpus kita). Bukti penutur asli dari lembar C2 sampai C4 digabungkan.

Pemakaian: python leksikon_am.py <repo> <folder_paket_keluaran> <folder_hasil_lembar> <folder_keluaran>
"""
import re, sys
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd

REPO, PAKET, HL, OUT = map(Path, sys.argv[1:5])
OUT.mkdir(parents=True, exist_ok=True)
AM = set("inda madung kehe akkon angkon anso harana bope giot doma milas mur pade halai adaboru oppot ngen juo tai "
         "sannari soni sattak napedo abope unjung deges sarupo copat satiop manyogot natuari tarimokasih".split())
TB = set("dang ndang nunga nungga sian naeng jabu alai unang ahu ibana nasida".split())
tok = lambda s: [w for w in re.findall(r"[^\W\d_]+", str(s).lower()) if len(w) >= 2]

nt = pd.read_csv(PAKET / "s02_nusatranslation.csv", keep_default_na=False)
nx = pd.read_csv(PAKET / "s02_nusax.csv", keep_default_na=False)
kami = pd.read_csv(REPO / "data/btb_parallel_sentence.csv")
nt["tk"] = nt.teks_bbc.map(tok)
nt["am"] = nt.tk.map(lambda t: bool(set(t) & AM)); nt["tb"] = nt.tk.map(lambda t: bool(set(t) & TB))
A = nt[nt.am]
B_teks = list(nx.teks_bbc) + list(nt[~nt.am & nt.tb].teks_bbc) + list(kami.toba_final)
B = [tok(s) for s in B_teks]
print("kalimat AM", len(A), "| kalimat Toba", len(B))


def hitung(kal_a, kal_b, n=1):
    def ng(t):
        return t if n == 1 else [" ".join(t[i:i + n]) for i in range(len(t) - n + 1)]
    ca, cb, da, db = Counter(), Counter(), Counter(), Counter()
    for t in kal_a:
        g = ng(t); ca.update(g); da.update(set(g))
    for t in kal_b:
        g = ng(t); cb.update(g); db.update(set(g))
    semua = ca + cb
    na, nb, n0 = sum(ca.values()), sum(cb.values()), sum(semua.values())
    a0 = 500.0   # ukuran prior
    rows = []
    for w, c in semua.items():
        aw = a0 * c / n0
        ya, yb = ca[w], cb[w]
        d = np.log((ya + aw) / (na + a0 - ya - aw)) - np.log((yb + aw) / (nb + a0 - yb - aw))
        var = 1 / (ya + aw) + 1 / (yb + aw)
        rows.append((w, d / np.sqrt(var), ya, yb, da[w], db[w]))
    return pd.DataFrame(rows, columns=["bentuk", "z", "frek_AM", "frek_Toba", "kalimat_AM", "kalimat_Toba"])


uni = hitung(A.tk, B, 1)
# kata Indonesia yang tidak diterjemahkan: sering muncul juga di sisi Indonesia kalimat yang sama
cid = Counter(w for s in A.teks_id for w in tok(s))
uni["frek_di_sisi_Indonesia"] = uni.bentuk.map(lambda w: cid[w])
uni["kemungkinan_kata_Indonesia"] = uni.frek_di_sisi_Indonesia >= 0.3 * uni.frek_AM
uni["proporsi_kalimat_AM"] = uni.kalimat_AM / (uni.kalimat_AM + uni.kalimat_Toba)
uni["penanda_lama"] = uni.bentuk.isin(AM)
def wilson_bawah(k, n, z=1.96):
    p = k / n
    return (p + z * z / (2 * n) - z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n)
uni["keandalan"] = wilson_bawah(uni.kalimat_AM, uni.kalimat_AM + uni.kalimat_Toba)
kand = uni[(uni.kalimat_AM >= 15) & (uni.keandalan >= 0.7) & ~uni.kemungkinan_kata_Indonesia].sort_values(
    ["keandalan", "kalimat_AM"], ascending=False)

bi = hitung(A.tk, B, 2)
bi["proporsi_kalimat_AM"] = bi.kalimat_AM / (bi.kalimat_AM + bi.kalimat_Toba)
bi["memuat_penanda_lama"] = bi.bentuk.map(lambda f: bool(set(f.split()) & AM))
bi["keandalan"] = wilson_bawah(bi.kalimat_AM, bi.kalimat_AM + bi.kalimat_Toba)
frasa = bi[(bi.kalimat_AM >= 10) & (bi.keandalan >= 0.7) & ~bi.memuat_penanda_lama].sort_values(
    ["keandalan", "kalimat_AM"], ascending=False).head(40)

# ---------- bukti penutur asli ----------
bukti = {}
def catat(w, sumber, info=""):
    w = w.lower().strip()
    if not w:
        return
    b = bukti.setdefault(w, {"sumber": set(), "info": []})
    b["sumber"].add(sumber)
    if info:
        b["info"].append(info)
c2 = pd.read_excel(HL / "C2.xlsx", sheet_name="Kategori")
for r in c2[c2.kategori.isin(["AM_atau_Batak_lain", "keduanya"])].itertuples():
    for w in re.split(r"[,;/]+", str(r.kata_bermasalah)):
        w = w.strip().lower()
        if w and w != "nan" and len(w.split()) <= 3:
            catat(w, "C2")
c3 = pd.read_excel(HL / "C3.xlsx", sheet_name="Label")
c4 = pd.read_excel(HL / "C4.xlsx", sheet_name="Contoh")
catatan = list(c3.catatan.dropna()) + list(c4.catatan.dropna()) + list(c4.glos_inggris.dropna())
for teks in catatan:
    for m in re.finditer(r"[\"“]([^\"”]{2,30})[\"”]\s*\(([^)]{2,80})\)", str(teks)):
        catat(m.group(1), "C3/C4", m.group(2))
    for m in re.finditer(r"\b([a-z]{2,15}) = ([^;|]{2,80})", str(teks)):
        if "AM" in m.group(2):
            catat(m.group(1), "C4", m.group(2))
print("bentuk dengan bukti penutur:", len(bukti))


def ringkas(w):
    b = bukti.get(w)
    if not b:
        return "", ""
    return ", ".join(sorted(b["sumber"])), " | ".join(dict.fromkeys(b["info"]))[:160]


for df in (kand, frasa):
    df["bukti_penutur"], df["keterangan_penutur"] = zip(*df.bentuk.map(ringkas))
kand.round(3).to_csv(OUT / "kandidat_kata_am.csv", index=False)
frasa.round(3).to_csv(OUT / "kandidat_frasa_am.csv", index=False)
# bentuk yang hanya ditemukan penutur (tidak lolos ambang statistik)
hanya = sorted(w for w in bukti if w not in set(kand.bentuk) and w not in set(frasa.bentuk))
pd.DataFrame({"bentuk": hanya, "bukti_penutur": [ringkas(w)[0] for w in hanya],
              "keterangan_penutur": [ringkas(w)[1] for w in hanya],
              "kalimat_AM": [int(uni.set_index("bentuk").kalimat_AM.get(w, 0)) for w in hanya],
              "kalimat_Toba": [int(uni.set_index("bentuk").kalimat_Toba.get(w, 0)) for w in hanya]}
             ).to_csv(OUT / "bentuk_dari_penutur_saja.csv", index=False)
pd.set_option("display.width", 220)
print(len(kand), kand.penanda_lama.sum()); print(kand[["bentuk", "keandalan", "kalimat_AM", "kalimat_Toba", "penanda_lama", "keterangan_penutur"]].to_string())
print(frasa[["bentuk", "keandalan", "kalimat_AM", "kalimat_Toba"]].to_string())
print("hanya dari penutur:", len(hanya))
