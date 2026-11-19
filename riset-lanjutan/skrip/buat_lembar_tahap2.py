"""Lembar kerja tahap 2: pemeriksaan penuh pasangan korpus yang belum pernah diperiksa penutur asli.

Yang dimasukkan: pasangan di korpus versi terbaru yang belum dinilai di lembar mana pun (kolom
`pemeriksaan_penutur` kosong) dan tidak ditinjau saat adjudikasi IAA (`review_status` = not_flagged).

Pemakaian (dari akar repo):
  python riset-lanjutan/skrip/buat_lembar_tahap2.py data/btb_parallel_sentence_v1.1.csv <keluaran.xlsx>
"""
import re, sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

AKAR = Path(__file__).resolve().parents[2]
RL = AKAR / "riset-lanjutan"
P_KORPUS, OUT = sys.argv[1], sys.argv[2]
KUNING, ABU, MERAH = PatternFill("solid", fgColor="FFF2CC"), PatternFill("solid", fgColor="E7F1FB"), PatternFill("solid", fgColor="F8D7DA")
OPSI = ["benar", "fragmen", "perbaiki_kata", "perbaiki_makna", "tidak_sejajar", "ragu"]
UKURAN_PAKET = 100

k = pd.read_csv(P_KORPUS, keep_default_na=False)
arah = pd.read_csv(RL / "metadata/arah_penerjemahan.csv").set_index("doc_id").arah_final
k["arah_asli"] = k.doc_id.map(arah)
k = k[(k.pemeriksaan_penutur == "") & (k.review_status == "not_flagged")].copy()

# bantuan untuk anotator: bentuk Angkola-Mandailing dari leksikon terverifikasi
leks = pd.read_csv(RL / "data/leksikon_am_terverifikasi.csv")
AM = set(leks[leks.kekuatan_penanda.isin(["kuat", "lemah"])].bentuk)
tok = lambda s: re.findall(r"\w+", str(s).lower())


def penanda(t):
    w = tok(t)
    g = set(w) | {" ".join(w[i:i + 2]) for i in range(len(w) - 1)}
    return ", ".join(sorted(g & AM))


k["penanda_AM"] = k.toba_final.map(penanda)


def isi(ws, df, sumber_asli):
    if sumber_asli == "indonesia":
        kolom = ["no", "paket", "pair_id", "dokumen", "genre", "teks_indonesia (asli)", "teks_toba (terjemahan)",
                 "penanda_AM", "keputusan", "toba_baru", "indonesia_baru", "catatan"]
        nilai = lambda r: [r.doc_id, r.genre, r.indo_final, r.toba_final]
    else:
        kolom = ["no", "paket", "pair_id", "dokumen", "genre", "teks_toba (asli)", "teks_indonesia (terjemahan)",
                 "penanda_AM", "keputusan", "toba_baru", "indonesia_baru", "catatan"]
        nilai = lambda r: [r.doc_id, r.genre, r.toba_final, r.indo_final]
    ws.append(kolom)
    for c in ws[1]:
        c.font = Font(bold=True)
    for i, r in enumerate(df.itertuples(index=False), 1):
        ws.append([i, (i - 1) // UKURAN_PAKET + 1, r.pair_id, *nilai(r), r.penanda_AM, "", "", "", ""])
    lebar = [5, 6, 20, 9, 14, 50, 50, 14, 16, 50, 40, 30]
    for j, w in enumerate(lebar, 1):
        huruf = ws.cell(row=1, column=j).column_letter
        ws.column_dimensions[huruf].width = w
        for i in range(2, len(df) + 2):
            sel = ws.cell(row=i, column=j)
            sel.alignment = Alignment(wrap_text=True, vertical="top")
            if kolom[j - 1] in ("keputusan", "toba_baru", "indonesia_baru", "catatan"):
                sel.fill = KUNING
            if kolom[j - 1] == "penanda_AM" and sel.value:
                sel.fill = MERAH
    dv = DataValidation(type="list", formula1='"' + ",".join(OPSI) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"I2:I{len(df) + 1}")
    ws.freeze_panes = "F2"


wb = Workbook()
ws0 = wb.active
ws0.title = "Petunjuk"
ind, tb = k[k.arah_asli == "asli_indonesia"], k[k.arah_asli == "asli_toba"]
petunjuk = [
    "PEMERIKSAAN PENUH KORPUS PARALEL (TAHAP 2)",
    f"Tujuan: memeriksa {len(k)} pasangan kalimat korpus yang belum pernah diperiksa penutur asli, agar korpus menjadi bersih dan layak menjadi dataset tolok ukur (benchmark).",
    "",
    f"LEMBAR 'A_asli_Indonesia' ({len(ind)} baris, PRIORITAS): teks aslinya bahasa Indonesia, lalu diterjemahkan ke Batak Toba.",
    "   Periksa terjemahan Toba terhadap teks Indonesia. Perbaikan ditulis di kolom 'toba_baru'.",
    f"LEMBAR 'B_asli_Toba' ({len(tb)} baris): teks aslinya Batak Toba, lalu diterjemahkan ke bahasa Indonesia.",
    "   Periksa terjemahan Indonesia terhadap teks Toba. Perbaikan ditulis di kolom 'indonesia_baru'.",
    "   Teks Toba asli JANGAN diubah, kecuali salah ketik yang jelas (tulis di 'toba_baru' dan jelaskan di 'catatan').",
    "",
    "Isi kolom 'keputusan' (kuning) dengan salah satu pilihan:",
    "  benar = terjemahan sudah tepat, tidak perlu diubah;",
    "  fragmen = pasangan berupa judul, butir daftar, atau baris puisi yang sudah sejajar dan tepat;",
    "  perbaiki_kata = makna sudah tepat, tetapi ada kata tidak baku, kata Angkola-Mandailing, atau kata Indonesia yang punya padanan Toba yang lazim;",
    "  perbaiki_makna = ada bagian yang salah arti, hilang, atau tertambah;",
    "  tidak_sejajar = kedua sisi tidak saling menerjemahkan (salah pasang, terpotong, atau tergabung); jelaskan di 'catatan';",
    "  ragu = tidak yakin; jelaskan di 'catatan'.",
    "Bila keputusannya perbaiki_kata atau perbaiki_makna, tulis kalimat yang sudah diperbaiki secara LENGKAP (bukan hanya kata yang diganti).",
    "",
    "Aturan perbaikan (sama dengan lembar C6):",
    "  1. Ubah seperlunya saja. Jangan mengganti gaya atau susunan kalimat yang sudah benar.",
    "  2. Pakai Batak Toba baku yang wajar dipakai penutur Toba; hindari kata Angkola-Mandailing.",
    "     Kolom merah 'penanda_AM' menunjukkan kata yang di daftar kita tercatat sebagai Angkola-Mandailing. Periksa apakah memang perlu diganti.",
    "  3. Nama orang, nama tempat, angka, dan istilah teknis yang tidak punya padanan Toba yang lazim boleh tetap dipakai.",
    "  4. Kata serapan Indonesia yang memang lazim dipakai penutur Toba boleh dipertahankan.",
    "  5. Jangan memakai mesin penerjemah atau alat AI untuk membuat terjemahan atau keputusan. Alat AI hanya boleh dipakai untuk mencari istilah di kolom catatan.",
    "",
    f"Baris diurutkan per dokumen sesuai urutan kalimat. Kolom 'paket' membagi pekerjaan menjadi kelompok {UKURAN_PAKET} baris; satu paket sekitar 2,5 sampai 3 jam.",
    "Silakan kirim per paket bila ingin dicicil. Perkiraan total: lembar A sekitar 23 jam, lembar B sekitar 4 jam.",
]
for i, b in enumerate(petunjuk, 1):
    ws0.cell(row=i, column=1, value=b).alignment = Alignment(wrap_text=True, vertical="top")
ws0.column_dimensions["A"].width = 130
isi(wb.create_sheet("A_asli_Indonesia"), ind, "indonesia")
isi(wb.create_sheet("B_asli_Toba"), tb, "toba")
wb.save(OUT)
print("A_asli_Indonesia", len(ind), "paket", -(-len(ind) // UKURAN_PAKET), "| bertanda AM", int((ind.penanda_AM != "").sum()),
      "| B_asli_Toba", len(tb), "| bertanda AM", int((tb.penanda_AM != "").sum()))
print(k.groupby(["arah_asli", "genre"]).size().to_string())
