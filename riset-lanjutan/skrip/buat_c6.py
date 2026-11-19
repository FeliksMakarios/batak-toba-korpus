"""Lembar kerja C6: perbaikan rujukan set uji kita.

Pemakaian: python buat_c6.py <repo> <s05_uji.csv> <C1_terisi.xlsx> <keluaran.xlsx>
"""
import sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

REPO, P_UJI, P_C1, OUT = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
KUNING, ABU = PatternFill("solid", fgColor="FFF2CC"), PatternFill("solid", fgColor="E7F1FB")

u = pd.read_csv(P_UJI, keep_default_na=False)
k = u[u.set_uji == "kami"].copy()
k["pair_id"] = k.uji_id.str[5:]
p = pd.read_csv(REPO / "data/btb_parallel_sentence.csv")
k = k.merge(p[["pair_id", "doc_id"]], on="pair_id", how="left")
c1 = pd.read_excel(P_C1, sheet_name="Periksa")
c1 = c1[c1.keputusan == "revise_translation"].set_index("pair_id")
k["usulan_pemeriksaan_sebelumnya"] = k.pair_id.map(c1.perbaikan_toba).fillna("")
k["usulan_indonesia"] = k.pair_id.map(c1.perbaikan_indonesia).fillna("")
k = k.sort_values("uji_id").reset_index(drop=True)   # urutan dokumen dan kalimat

OPSI = ["benar", "perbaiki_kata", "perbaiki_makna", "tulis_ulang", "ragu"]


def isi_lembar(ws, df, kol_sumber, kol_rujukan, kol_usulan, judul_baru):
    kolom = ["no", "uji_id", "dokumen", "genre", "sumber", "rujukan_sekarang", "usulan_pemeriksaan_sebelumnya",
             "keputusan", judul_baru, "catatan"]
    ws.append(kolom)
    for c in ws[1]:
        c.font = Font(bold=True)
    for i, r in enumerate(df.itertuples(index=False), 1):
        ws.append([i, r.uji_id, r.doc_id, r.genre, getattr(r, kol_sumber), getattr(r, kol_rujukan),
                   getattr(r, kol_usulan), "", "", ""])
    lebar = {"no": 5, "uji_id": 24, "dokumen": 9, "genre": 14, "sumber": 50, "rujukan_sekarang": 50,
             "usulan_pemeriksaan_sebelumnya": 40, "keputusan": 16, judul_baru: 50, "catatan": 30}
    for j, nama in enumerate(kolom, 1):
        huruf = ws.cell(row=1, column=j).column_letter
        ws.column_dimensions[huruf].width = lebar[nama]
        for i in range(2, len(df) + 2):
            sel = ws.cell(row=i, column=j)
            sel.alignment = Alignment(wrap_text=True, vertical="top")
            if nama in ("keputusan", judul_baru, "catatan"):
                sel.fill = KUNING
            if nama == "usulan_pemeriksaan_sebelumnya" and sel.value:
                sel.fill = ABU
    dv = DataValidation(type="list", formula1='"' + ",".join(OPSI) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    huruf = ws.cell(row=1, column=kolom.index("keputusan") + 1).column_letter
    dv.add(f"{huruf}2:{huruf}{len(df) + 1}")
    ws.freeze_panes = "E2"


wb = Workbook()
ws0 = wb.active
ws0.title = "Petunjuk"
petunjuk = [
    "PERBAIKAN RUJUKAN SET UJI (C6)",
    "Tujuan: memperbaiki rujukan Batak Toba di set uji agar evaluasi mesin penerjemah memakai rujukan yang benar. Hasilnya menjadi 'set uji terkoreksi' di naskah.",
    "",
    "LEMBAR 1 'Rujukan_Toba' (wajib, 266 baris): kalimat yang aslinya ditulis dalam bahasa Indonesia, lalu diterjemahkan ke Batak Toba oleh penerjemah korpus.",
    "Periksa kolom 'rujukan_sekarang' (Batak Toba) terhadap kolom 'sumber' (Indonesia).",
    "LEMBAR 2 'Rujukan_Indonesia_opsional' (opsional, 44 baris): kalimat yang aslinya Batak Toba; periksa terjemahan Indonesianya. Kerjakan bila waktu masih ada.",
    "",
    "Isi kolom 'keputusan' (kuning) dengan salah satu pilihan:",
    "  benar = rujukan sudah tepat, tidak perlu diubah;",
    "  perbaiki_kata = makna sudah tepat, tetapi ada kata tidak baku, kata Angkola-Mandailing, atau kata Indonesia yang sebenarnya punya padanan Toba yang lazim;",
    "  perbaiki_makna = ada bagian yang salah arti, hilang, atau tertambah;",
    "  tulis_ulang = rujukan perlu ditulis ulang hampir seluruhnya;",
    "  ragu = tidak yakin; jelaskan di kolom 'catatan'.",
    "Bila keputusannya bukan 'benar', tulis rujukan yang sudah diperbaiki secara LENGKAP di kolom kuning berikutnya (bukan hanya kata yang diganti).",
    "",
    "Aturan perbaikan:",
    "  1. Ubah seperlunya saja. Jangan mengganti gaya atau susunan kalimat yang sudah benar.",
    "  2. Pakai Batak Toba baku yang wajar dipakai penutur Toba; hindari kata Angkola-Mandailing (misalnya inda, giot, tai, madung, ngen).",
    "  3. Nama orang, nama tempat, angka, dan istilah teknis yang memang tidak punya padanan Toba yang lazim boleh tetap dipakai.",
    "  4. Kata serapan Indonesia yang memang lazim dipakai penutur Toba boleh dipertahankan.",
    "  5. Kolom biru 'usulan_pemeriksaan_sebelumnya' berisi perbaikan dari pemeriksaan acak sebelumnya (9 baris). Boleh dipakai, diubah, atau diabaikan.",
    "  6. Jangan melihat keluaran mesin penerjemah apa pun selama mengerjakan lembar ini.",
    "",
    "Baris diurutkan per dokumen sehingga konteks antarkalimat bisa dibaca berurutan.",
    "Perkiraan waktu: 6 sampai 8 jam untuk lembar 1, boleh dicicil. Lembar 2 sekitar 1 jam.",
    "Sebaiknya dikerjakan oleh anotator yang sama dengan pemeriksaan acak sebelumnya (C1), agar ukurannya konsisten.",
]
for i, b in enumerate(petunjuk, 1):
    ws0.cell(row=i, column=1, value=b).alignment = Alignment(wrap_text=True, vertical="top")
ws0.column_dimensions["A"].width = 120

ind = k[k.arah_asli == "asli_indonesia"]
isi_lembar(wb.create_sheet("Rujukan_Toba"), ind, "teks_id", "teks_bbc", "usulan_pemeriksaan_sebelumnya", "rujukan_toba_baru")
tb = k[k.arah_asli == "asli_toba"]
isi_lembar(wb.create_sheet("Rujukan_Indonesia_opsional"), tb, "teks_bbc", "teks_id", "usulan_indonesia", "rujukan_indonesia_baru")
wb.save(OUT)
print("Rujukan_Toba", len(ind), "dengan usulan", (ind.usulan_pemeriksaan_sebelumnya != "").sum(),
      "| opsional", len(tb), "dengan usulan", (tb.usulan_indonesia != "").sum())
