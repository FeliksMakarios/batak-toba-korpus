"""Lembar kerja tahap 2: pemeriksaan penuh pasangan korpus yang belum pernah diperiksa penutur asli.

Yang dimasukkan: pasangan di korpus versi terbaru yang belum dinilai di lembar mana pun (kolom
`pemeriksaan_penutur` kosong) dan tidak ditinjau saat adjudikasi IAA (`review_status` = not_flagged).

Pemakaian (dari akar repo):
  python riset-lanjutan/skrip/buat_lembar_tahap2.py riset-lanjutan/data/draf_berbantuan_ai/btb_parallel_sentence_v1.1_draf.csv <keluaran.xlsx>
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

# bantuan untuk anotator: bentuk Angkola-Mandailing dari leksikon AM (draf)
leks = pd.read_csv(RL / "data/draf_berbantuan_ai/leksikon_am_draf.csv")
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
    "SEBELUM MULAI, baca empat lembar contoh (sekitar 20 menit):",
    "   'Contoh_perbaikan'   = 17 perbaikan dari pemeriksaan set uji, dengan kata yang diubah dan alasannya;",
    "   'Contoh_sudah_benar' = terjemahan yang tidak perlu diubah, dan contoh 'fragmen';",
    "   'Contoh_Toba_asli'   = kalimat yang aslinya ditulis dalam Batak Toba, sebagai acuan susunan kalimat yang wajar;",
    "   'Padanan_AM_Toba'    = kata Angkola-Mandailing yang sering muncul dan padanan Tobanya.",
    "   Contoh ini ACUAN, BUKAN ATURAN. Bila Anda yakin ada pilihan yang lebih tepat atau lebih wajar, ikuti penilaian Anda sebagai penutur.",
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

# ---------------- lembar contoh (acuan, bukan aturan) ----------------
# Semua contoh berasal dari pasangan yang sudah diperiksa penutur asli: set uji (C6), pemeriksaan acak (C1),
# atau adjudikasi IAA. Dokumen set uji tidak muncul di lembar A dan B (pembagian tingkat dokumen).
import difflib

C6 = pd.read_csv(RL / "data/draf_berbantuan_ai/set_uji_kami_koreksi_draf.csv", keep_default_na=False).set_index("uji_id")
KV = pd.read_csv(P_KORPUS, keep_default_na=False).set_index("pair_id")
CONTOH_PERBAIKAN = ["doc_0080_s025", "doc_0091_s000", "doc_0091_s030", "doc_0077_s070", "doc_0091_s012", "doc_0077_s026",
                    "doc_0080_s011_b", "doc_0090_s003", "doc_0069_s002",
                    "doc_0089_s000", "doc_0091_s021", "doc_0080_s049", "doc_0077_s004", "doc_0061_s021", "doc_0080_s024",
                    "doc_0080_s013_b", "doc_0080_s068"]
CONTOH_BENAR = ["doc_0077_s016", "doc_0080_s002", "doc_0080_s004", "doc_0090_s001", "doc_0091_s001_a", "doc_0069_s003"]
CONTOH_FRAGMEN = ["doc_0053_s019", "doc_0082_s049", "doc_0084_s037", "doc_0082_s022"]
CONTOH_TOBA = ["doc_0000_s003", "doc_0000_s012__r01", "doc_0000_s024", "doc_0000_s026_b", "doc_0000_s037", "doc_0000_s045_b",
               "doc_0000_s048", "doc_0000_s060", "doc_0000_s071", "doc_0000_s079__r02",
               "doc_0014_s000", "doc_0017_s000", "doc_0045_s000", "doc_0046_s000"]


def beda(a, b):
    ta, tb_ = re.findall(r"[\w-]+", a), re.findall(r"[\w-]+", b)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, [x.lower() for x in ta], [x.lower() for x in tb_]).get_opcodes():
        if op == "replace":
            out.append(f"{' '.join(ta[i1:i2])} → {' '.join(tb_[j1:j2])}")
        elif op == "delete":
            out.append(f"{' '.join(ta[i1:i2])} → (dihapus)")
        elif op == "insert":
            out.append(f"(ditambah) → {' '.join(tb_[j1:j2])}")
    return "; ".join(out)


def lembar(nama, kolom, baris, lebar, judul):
    ws = wb.create_sheet(nama)
    ws.append([judul]); ws["A1"].font = Font(bold=True, italic=True)
    ws.append(kolom)
    for c in ws[2]:
        c.font = Font(bold=True)
    for b in baris:
        ws.append(b)
    for j, w in enumerate(lebar, 1):
        huruf = ws.cell(row=2, column=j).column_letter
        ws.column_dimensions[huruf].width = w
        for i in range(3, len(baris) + 3):
            ws.cell(row=i, column=j).alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A3"


rows = []
for pid in CONTOH_PERBAIKAN:
    r = C6.loc["kami-" + pid]
    rows.append([r.keputusan, r.genre, r.teks_id_lama, r.teks_bbc_lama, r.teks_bbc_baru, beda(r.teks_bbc_lama, r.teks_bbc_baru),
                 r.catatan_anotator])
lembar("Contoh_perbaikan", ["keputusan", "genre", "indonesia (asli)", "toba_sebelum", "toba_sesudah", "yang_diubah", "alasan"],
       rows, [15, 14, 45, 45, 45, 40, 50],
       "Contoh perbaikan dari pemeriksaan set uji. Perhatikan bahwa perubahan dibuat seperlunya dan susunan kalimat yang sudah benar dipertahankan.")
rows = [[C6.loc["kami-" + p].genre, C6.loc["kami-" + p].teks_id_lama, C6.loc["kami-" + p].teks_bbc_lama] for p in CONTOH_BENAR]
rows += [["fragmen: " + KV.loc[p, "sub_genre"], KV.loc[p, "indo_final"], KV.loc[p, "toba_final"]] for p in CONTOH_FRAGMEN]
lembar("Contoh_sudah_benar", ["jenis", "indonesia (asli)", "toba"], rows, [24, 60, 60],
       "Contoh terjemahan yang dinilai sudah benar (tidak diubah), dan contoh 'fragmen' (judul, butir daftar, baris puisi). Tidak semua kalimat perlu diubah.")
rows = [[KV.loc[p, "sub_genre"], KV.loc[p, "toba_final"], KV.loc[p, "indo_final"]] for p in CONTOH_TOBA]
lembar("Contoh_Toba_asli", ["jenis", "toba (teks asli)", "indonesia (terjemahan)"], rows, [20, 65, 65],
       "Kalimat yang aslinya ditulis dalam Batak Toba (cerita rakyat dan umpama), sudah diperiksa penutur. Dapat dipakai sebagai acuan susunan kalimat Toba yang wajar. Ejaan sumber dibiarkan apa adanya.")
x = leks[(leks.kekuatan_penanda == "kuat") & (leks.jenis == "kata")].sort_values("kalimat_AM", ascending=False).head(25)
rows = [[r.bentuk, r.arti_Indonesia, r.padanan_Toba] for r in x.itertuples()]
lembar("Padanan_AM_Toba", ["bentuk Angkola-Mandailing", "arti", "padanan Batak Toba"], rows, [26, 34, 30],
       "Kata Angkola-Mandailing yang paling sering muncul dan padanan Tobanya, dari verifikasi kosakata sebelumnya (C5).")
URUTAN = ["Petunjuk", "Contoh_perbaikan", "Contoh_sudah_benar", "Contoh_Toba_asli", "Padanan_AM_Toba", "A_asli_Indonesia", "B_asli_Toba"]
wb._sheets = [wb[n] for n in URUTAN]
wb.active = URUTAN.index("Petunjuk")
wb.save(OUT)
print("A_asli_Indonesia", len(ind), "paket", -(-len(ind) // UKURAN_PAKET), "| bertanda AM", int((ind.penanda_AM != "").sum()),
      "| B_asli_Toba", len(tb), "| bertanda AM", int((tb.penanda_AM != "").sum()))
print(k.groupby(["arah_asli", "genre"]).size().to_string())
