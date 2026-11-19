"""Lembar verifikasi buta untuk koreksi set uji (C6) yang sebagian dibuat dengan bantuan AI.

Untuk setiap butir set uji `kami` yang rujukannya diubah, rujukan lama dan usulan koreksi ditampilkan
sebagai terjemahan A dan B dalam urutan acak (benih tetap), tanpa label. Butir yang tidak diubah
ditampilkan dengan satu terjemahan saja. Penutur memilih mana yang benar atau menulis sendiri.
Kunci urutan A/B dapat dibuat ulang dari benih yang sama (lihat fungsi `kunci`).

Pemakaian (dari akar repo):
  python riset-lanjutan/skrip/buat_verifikasi_c6.py <keluaran.xlsx> <kunci.csv>
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

AKAR = Path(__file__).resolve().parents[2]
RL = AKAR / "riset-lanjutan"
OUT, P_KUNCI = sys.argv[1], sys.argv[2]
BENIH = 20261119
KUNING = PatternFill("solid", fgColor="FFF2CC")

c6 = pd.read_csv(RL / "data/draf_berbantuan_ai/set_uji_kami_koreksi_draf.csv", keep_default_na=False)
doc = pd.read_csv(RL / "data/split_korpus_kami.csv").set_index("uji_id").doc_id
c6["dokumen"] = c6.uji_id.map(doc)
c6 = c6.sort_values("uji_id").reset_index(drop=True)          # urutan dokumen dan kalimat


def kunci(df):
    rng = np.random.RandomState(BENIH)
    rows = []
    for r in df.itertuples():
        toba = r.arah_asli == "asli_indonesia"                  # sisi yang diperiksa: terjemahan
        sumber = r.teks_id_lama if toba else r.teks_bbc_lama
        lama = r.teks_bbc_lama if toba else r.teks_id_lama
        usul = r.teks_bbc_baru if toba else r.teks_id_baru
        if lama == usul:
            a, b, a_adalah = lama, "", "lama"
        elif rng.rand() < 0.5:
            a, b, a_adalah = lama, usul, "lama"
        else:
            a, b, a_adalah = usul, lama, "usulan"
        rows.append({"uji_id": r.uji_id, "dokumen": r.dokumen, "genre": r.genre,
                     "sisi": "Toba" if toba else "Indonesia", "sumber": sumber, "A": a, "B": b,
                     "A_adalah": a_adalah, "dua_versi": lama != usul})
    return pd.DataFrame(rows)


K = kunci(c6)
K[["uji_id", "sisi", "A_adalah", "dua_versi"]].to_csv(P_KUNCI, index=False)

OPSI = ["A_benar", "B_benar", "A_dan_B_benar", "keduanya_salah", "ragu"]
wb = Workbook()
ws0 = wb.active
ws0.title = "Petunjuk"
petunjuk = [
    "VERIFIKASI TERJEMAHAN SET UJI",
    f"Berisi {len(K)} kalimat. Untuk {int(K.dua_versi.sum())} kalimat ada dua terjemahan (A dan B); untuk {int((~K.dua_versi).sum())} kalimat hanya ada satu terjemahan (A).",
    "Kolom 'sisi' menunjukkan bahasa terjemahan yang diperiksa: 'Toba' berarti sumbernya bahasa Indonesia dan terjemahannya Batak Toba;",
    "'Indonesia' berarti sumbernya Batak Toba dan terjemahannya bahasa Indonesia.",
    "",
    "Isi kolom 'keputusan' (kuning):",
    "  A_benar = terjemahan A tepat dan wajar (untuk baris dua versi: A lebih tepat daripada B);",
    "  B_benar = terjemahan B tepat dan wajar, dan lebih tepat daripada A;",
    "  A_dan_B_benar = keduanya sama-sama tepat dan wajar;",
    "  keduanya_salah = tidak ada yang tepat; tulis terjemahan yang benar secara LENGKAP di kolom 'terjemahan_sendiri'",
    "                   (untuk baris satu versi: A salah, tulis yang benar);",
    "  ragu = tidak yakin; jelaskan di 'catatan'.",
    "Bila memilih A_benar atau B_benar tetapi masih ada kesalahan kecil, pilih keduanya_salah dan tulis versi yang sudah dirapikan.",
    "",
    "PENTING:",
    "  1. Kerjakan sendiri, tanpa mesin penerjemah, ChatGPT, Gemini, atau alat AI lain, baik untuk memilih maupun untuk menulis.",
    "  2. Bila pada baris tertentu Anda tetap memakai alat bantu, itu tidak apa-apa asal ditandai: isi kolom 'dibantu_AI' dengan 'ya'.",
    "     Kejujuran di kolom ini jauh lebih penting daripada kecepatan.",
    "  3. Tidak ada jawaban yang diharapkan. A dan B bisa sama-sama benar atau sama-sama salah, dan urutan A dan B diacak.",
    "  4. Pakai Batak Toba baku yang wajar dipakai penutur Toba; kata serapan Indonesia yang lazim, nama, angka, dan istilah teknis boleh dipertahankan.",
    "  5. Catat jam mulai dan selesai setiap kali bekerja di lembar 'Catatan_waktu'.",
    "",
    "Baris diurutkan per dokumen sehingga kalimat bisa dibaca berurutan. Perkiraan waktu: 3 sampai 4 jam, boleh dicicil.",
]
for i, b in enumerate(petunjuk, 1):
    ws0.cell(row=i, column=1, value=b).alignment = Alignment(wrap_text=True, vertical="top")
ws0.column_dimensions["A"].width = 130

ws = wb.create_sheet("Verifikasi")
kolom = ["no", "uji_id", "dokumen", "genre", "sisi", "sumber", "terjemahan_A", "terjemahan_B", "keputusan",
         "terjemahan_sendiri", "dibantu_AI", "catatan"]
ws.append(kolom)
for c in ws[1]:
    c.font = Font(bold=True)
for i, r in enumerate(K.itertuples(), 1):
    ws.append([i, r.uji_id, r.dokumen, r.genre, r.sisi, r.sumber, r.A, r.B or "(hanya satu terjemahan)", "", "", "", ""])
lebar = [5, 22, 9, 14, 9, 45, 45, 45, 16, 45, 11, 30]
for j, w in enumerate(lebar, 1):
    huruf = ws.cell(row=1, column=j).column_letter
    ws.column_dimensions[huruf].width = w
    for i in range(2, len(K) + 2):
        sel = ws.cell(row=i, column=j)
        sel.alignment = Alignment(wrap_text=True, vertical="top")
        if kolom[j - 1] in ("keputusan", "terjemahan_sendiri", "dibantu_AI", "catatan"):
            sel.fill = KUNING
dv = DataValidation(type="list", formula1='"' + ",".join(OPSI) + '"', allow_blank=True)
dv2 = DataValidation(type="list", formula1='"tidak,ya"', allow_blank=True)
ws.add_data_validation(dv); ws.add_data_validation(dv2)
dv.add(f"I2:I{len(K) + 1}"); dv2.add(f"K2:K{len(K) + 1}")
ws.freeze_panes = "G2"

wt = wb.create_sheet("Catatan_waktu")
wt.append(["tanggal", "jam_mulai", "jam_selesai", "dari_baris_no", "sampai_baris_no", "catatan"])
for c in wt[1]:
    c.font = Font(bold=True)
for j, w in enumerate([14, 12, 12, 14, 16, 40], 1):
    wt.column_dimensions[wt.cell(row=1, column=j).column_letter].width = w
wb.save(OUT)
print(f"{len(K)} butir | dua versi {int(K.dua_versi.sum())} (A = usulan pada {int((K.A_adalah == 'usulan').sum())}) | "
      f"satu versi {int((~K.dua_versi).sum())} | per sisi {K.sisi.value_counts().to_dict()}")
