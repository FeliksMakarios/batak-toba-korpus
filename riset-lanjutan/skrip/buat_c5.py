"""Tabel kandidat leksikon Angkola-Mandailing dan lembar verifikasi C5.

Pemakaian: python buat_c5.py <folder_leksikon> <s02_nusatranslation.csv> <keluaran_tabel.csv> <keluaran_C5.xlsx>
"""
import re, sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

L, P_NT, OUT_CSV, OUT_XLSX = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
AM_LAMA = ("inda madung kehe akkon angkon anso harana bope giot doma milas mur pade halai adaboru oppot ngen juo tai "
           "sannari soni sattak napedo abope unjung deges sarupo copat satiop manyogot natuari tarimokasih").split()
PERINGATAN = {"giot": "penutur: juga dipakai di Toba Silindung, Pahae, Tapanuli Utara ('giot hian')",
              "milas": "penutur: juga di Toba perbatasan Pahae dan Silindung, serta Simalungun dan Karo",
              "akkon": "penutur: juga muncul di Toba lisan (ikkon/akkon)",
              "sarupo": "juga kata Minangkabau; sumber salah tanda pada keluaran zero-shot"}
BUANG_FRASA = re.compile(r"jokowi|syahrini|cinta|orang tua|gara gara")

kata = pd.read_csv(L / "kandidat_kata_am.csv", keep_default_na=False)
frasa = pd.read_csv(L / "kandidat_frasa_am.csv", keep_default_na=False)
penutur = pd.read_csv(L / "bentuk_dari_penutur_saja.csv", keep_default_na=False)
penutur = penutur[penutur.keterangan_penutur.str.contains("Toba|AM") & (penutur.kalimat_Toba <= 5)]
frasa = frasa[~frasa.bentuk.str.contains(BUANG_FRASA)]

baris = []
for r in kata.itertuples():
    baris.append({"bentuk": r.bentuk, "jenis": "kata", "status": "penanda lama" if r.penanda_lama else "kandidat baru (statistik)",
                  "kalimat_AM": r.kalimat_AM, "kalimat_Toba": r.kalimat_Toba, "keandalan": r.keandalan,
                  "keterangan_penutur": r.keterangan_penutur})
for r in frasa.itertuples():
    baris.append({"bentuk": r.bentuk, "jenis": "frasa", "status": "kandidat baru (statistik)", "kalimat_AM": r.kalimat_AM,
                  "kalimat_Toba": r.kalimat_Toba, "keandalan": r.keandalan, "keterangan_penutur": r.keterangan_penutur})
for r in penutur.itertuples():
    baris.append({"bentuk": r.bentuk, "jenis": "frasa" if " " in r.bentuk else "kata", "status": "dari penutur asli",
                  "kalimat_AM": r.kalimat_AM, "kalimat_Toba": r.kalimat_Toba, "keandalan": "",
                  "keterangan_penutur": r.keterangan_penutur})
for w in AM_LAMA:   # penanda lama yang tidak muncul di data (angkon, bope)
    if w not in {b["bentuk"] for b in baris}:
        baris.append({"bentuk": w, "jenis": "kata", "status": "penanda lama", "kalimat_AM": 0, "kalimat_Toba": 0,
                      "keandalan": "", "keterangan_penutur": ""})
t = pd.DataFrame(baris).drop_duplicates("bentuk")
t["peringatan"] = t.bentuk.map(PERINGATAN).fillna("")
urut = {"penanda lama": 0, "kandidat baru (statistik)": 1, "dari penutur asli": 2}
t = t.sort_values(["status", "jenis"], key=lambda s: s.map(urut) if s.name == "status" else s).reset_index(drop=True)
t.to_csv(OUT_CSV, index=False)

# contoh kalimat dari NusaTranslation untuk setiap bentuk
nt = pd.read_csv(P_NT, keep_default_na=False)
low = nt.teks_bbc.str.lower()
def contoh(f):
    m = low[low.str.contains(r"\b" + re.escape(f) + r"\b", regex=True)]
    return nt.teks_bbc[m.index[0]][:220] if len(m) else ""
t["contoh_kalimat"] = t.bentuk.map(contoh)

KUNING, ABU = PatternFill("solid", fgColor="FFF2CC"), PatternFill("solid", fgColor="E7F1FB")
wb = Workbook(); ws0 = wb.active; ws0.title = "Petunjuk"
pet = [
    "VERIFIKASI KOSAKATA PENANDA ANGKOLA-MANDAILING (C5)",
    f"Berisi {len(t)} kata dan frasa yang diduga menandakan teks Angkola-Mandailing (AM). Hasilnya dipakai sebagai dasar menyaring data Batak Toba di kemudian hari,",
    "dan untuk menjawab pertanyaan reviewer tentang dialek Toba di daerah perbatasan seperti Silindung dan Pahae.",
    "",
    "Untuk setiap baris, isi kolom 'kategori' (kuning):",
    "  AM_saja = bentuk ini khas Angkola-Mandailing dan tidak dipakai penutur Toba;",
    "  AM_dan_Toba_perbatasan = khas AM, tetapi juga dipakai penutur Toba di daerah perbatasan (sebutkan daerahnya di 'catatan');",
    "  juga_Toba_umum = bentuk ini juga lazim dalam Batak Toba umum, jadi tidak bisa dipakai sebagai penanda;",
    "  bukan_Batak = kata Indonesia, nama, istilah, atau bahasa lain;",
    "  ragu = tidak yakin.",
    "Lalu isi 'arti_Indonesia' dan 'padanan_Toba' bila Anda tahu. Kolom biru berisi keterangan dari pemeriksaan sebelumnya; boleh dikoreksi.",
    "Kolom 'contoh_kalimat' hanya contoh pemakaian dari data NusaTranslation. Angka 'kalimat_AM' dan 'kalimat_Toba' menunjukkan berapa kalimat",
    "AM dan berapa kalimat Toba yang memuat bentuk itu; semakin kecil 'kalimat_Toba', semakin kuat dugaannya.",
    "Bagian pertama (status 'penanda lama') adalah 32 penanda yang sudah dipakai di naskah. Mohon perhatikan terutama apakah ada yang juga dipakai di Toba perbatasan.",
    "Perkiraan waktu: 1 sampai 1,5 jam. Kerjakan tanpa berdiskusi dengan orang lain.",
]
for i, b in enumerate(pet, 1):
    ws0.cell(row=i, column=1, value=b).alignment = Alignment(wrap_text=True, vertical="top")
ws0.column_dimensions["A"].width = 120
ws = wb.create_sheet("Verifikasi")
kol = ["no", "bentuk", "jenis", "status", "kalimat_AM", "kalimat_Toba", "keterangan_sebelumnya", "contoh_kalimat",
       "kategori", "arti_Indonesia", "padanan_Toba", "catatan"]
ws.append(kol)
for c in ws[1]:
    c.font = Font(bold=True)
for i, r in enumerate(t.itertuples(), 1):
    ket = "; ".join(x for x in [r.keterangan_penutur, r.peringatan] if x)
    ws.append([i, r.bentuk, r.jenis, r.status, r.kalimat_AM, r.kalimat_Toba, ket, r.contoh_kalimat, "", "", "", ""])
lebar = [5, 16, 7, 22, 10, 11, 35, 60, 22, 22, 18, 30]
for j, w in enumerate(lebar, 1):
    huruf = ws.cell(row=1, column=j).column_letter
    ws.column_dimensions[huruf].width = w
    for i in range(2, len(t) + 2):
        sel = ws.cell(row=i, column=j); sel.alignment = Alignment(wrap_text=True, vertical="top")
        if kol[j - 1] in ("kategori", "arti_Indonesia", "padanan_Toba", "catatan"):
            sel.fill = KUNING
        if kol[j - 1] == "keterangan_sebelumnya" and sel.value:
            sel.fill = ABU
dv = DataValidation(type="list", formula1='"AM_saja,AM_dan_Toba_perbatasan,juga_Toba_umum,bukan_Batak,ragu"', allow_blank=True)
ws.add_data_validation(dv); dv.add(f"I2:I{len(t) + 1}")
ws.freeze_panes = "C2"
wb.save(OUT_XLSX)
print(t.status.value_counts().to_dict(), t.jenis.value_counts().to_dict(), len(t))
