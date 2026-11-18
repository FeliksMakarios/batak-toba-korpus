"""Membuat lembar kerja penutur asli untuk revisi naskah (C1 sampai C4).

Pemakaian: python buat_lembar.py <repo> <folder_paket_keluaran> <folder_keluaran>
"""
import json, re, sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

REPO, PAKET, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
RL = REPO / "riset-lanjutan"
OUT.mkdir(parents=True, exist_ok=True)
AM = set("inda madung kehe akkon angkon anso harana bope giot doma milas mur pade halai adaboru oppot ngen juo tai "
         "sannari soni sattak napedo abope unjung deges sarupo copat satiop manyogot natuari tarimokasih".split())
tok = lambda s: re.findall(r"\w+", str(s).lower())
KUNING = PatternFill("solid", fgColor="FFF2CC")


def lembar(wb, judul, petunjuk, df, lebar, isian, pilihan=None):
    ws0 = wb.active if wb.active.title == "Sheet" else wb.create_sheet()
    ws0.title = "Petunjuk"
    for i, b in enumerate(petunjuk, 1):
        ws0.cell(row=i, column=1, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    ws0.column_dimensions["A"].width = 110
    ws = wb.create_sheet(judul)
    ws.append(list(df.columns))
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in df.itertuples(index=False):
        ws.append(list(r))
    for j, col in enumerate(df.columns, 1):
        huruf = ws.cell(row=1, column=j).column_letter
        ws.column_dimensions[huruf].width = lebar.get(col, 14)
        for i in range(2, len(df) + 2):
            ws.cell(row=i, column=j).alignment = Alignment(wrap_text=True, vertical="top")
            if col in isian:
                ws.cell(row=i, column=j).fill = KUNING
    if pilihan:
        for col, opsi in pilihan.items():
            j = list(df.columns).index(col) + 1
            huruf = ws.cell(row=1, column=j).column_letter
            dv = DataValidation(type="list", formula1='"' + ",".join(opsi) + '"', allow_blank=True)
            ws.add_data_validation(dv)
            dv.add(f"{huruf}2:{huruf}{len(df) + 1}")
    ws.freeze_panes = "A2"
    return ws


# ---------- C1: pemeriksaan acak 100 pasangan yang tidak ditandai audit ----------
p = pd.read_csv(REPO / "data/btb_parallel_sentence.csv")
tak = p[p.review_status == "not_flagged"].sample(n=100, random_state=2026).reset_index(drop=True)
c1 = pd.DataFrame({"no": range(1, 101), "pair_id": tak.pair_id, "genre": tak.genre,
                   "teks_toba": tak.toba_final, "teks_indonesia": tak.indo_final,
                   "keputusan": "", "perbaikan_toba": "", "perbaikan_indonesia": "", "catatan": ""})
wb = Workbook()
lembar(wb, "Periksa", [
    "Pemeriksaan acak 100 pasangan kalimat yang TIDAK ditandai oleh audit otomatis (dipilih acak dari 1.360 pasangan, benih 2026).",
    "Tujuan: memperkirakan berapa persen pasangan yang lolos audit ternyata masih bermasalah. Hasilnya dilaporkan di naskah.",
    "Untuk setiap baris, pilih satu keputusan di kolom 'keputusan' (kolom kuning), memakai enam kategori yang sama dengan anotasi sebelumnya:",
    "accept = pasangan sudah benar; revise_alignment = penjajaran salah (kalimat terpotong, tergabung, atau tidak sepadan);",
    "revise_translation = terjemahan perlu diperbaiki; needs_source = perlu melihat dokumen sumber untuk memutuskan;",
    "fragment_policy = potongan kalimat (judul, daftar, atau baris puisi) yang perlu aturan khusus; exclude = sebaiknya dibuang.",
    "Bila memilih revise_translation, tulis perbaikannya di kolom perbaikan. Masalah variasi bahasa (misalnya kata Angkola-Mandailing) dicatat di kolom 'catatan'.",
    "Kerjakan sendiri tanpa berdiskusi dengan anotator lain. Perkiraan waktu: 2 sampai 3 jam.",
], c1, {"no": 5, "pair_id": 18, "genre": 16, "teks_toba": 55, "teks_indonesia": 55, "keputusan": 20,
        "perbaikan_toba": 35, "perbaikan_indonesia": 35, "catatan": 30},
       {"keputusan", "perbaikan_toba", "perbaikan_indonesia", "catatan"},
       {"keputusan": ["accept", "revise_alignment", "revise_translation", "needs_source", "fragment_policy", "exclude"]})
wb.save(OUT / "C1_periksa_acak_100_pasangan.xlsx")

# ---------- C2: memecah tag [VARIETY] ----------
e = pd.read_csv(RL / "data/esa_anonim.csv")
d = e[(e.arah == "id2bbc") & ((e.variety_A == 1) | (e.variety_B == 1))].copy()
d["penanda_AM_otomatis"] = d.terjemahan.map(lambda t: ", ".join(sorted(set(tok(t)) & AM)))
d = d.sample(frac=1, random_state=7).reset_index(drop=True)   # urutan acak, nama sistem disembunyikan
c2 = pd.DataFrame({"no": range(1, len(d) + 1), "item_id": d.item_id, "sumber_indonesia": d.sumber,
                   "terjemahan_batak": d.terjemahan, "penanda_AM_otomatis": d.penanda_AM_otomatis,
                   "kategori": "", "kata_bermasalah": "", "catatan": ""})
wb = Workbook()
lembar(wb, "Kategori", [
    f"Memecah tag [VARIETY] dari evaluasi ESA. Berisi {len(c2)} keluaran id->bbc yang ditandai [VARIETY] oleh minimal satu penilai.",
    "Nama sistem sengaja disembunyikan dan urutan diacak.",
    "Isi kolom 'kategori' (kuning) dengan satu pilihan:",
    "AM_atau_Batak_lain = ada kata Angkola-Mandailing atau bahasa Batak lain (bukan Toba);",
    "serapan_Indonesia = hanya ada kata bahasa Indonesia yang tidak diterjemahkan atau diserap;",
    "keduanya = ada kata Angkola-Mandailing atau Batak lain DAN serapan Indonesia;",
    "bahasa_lain = ada kata dari bahasa lain, misalnya Minangkabau, Melayu, atau Inggris;",
    "tidak_ada = menurut Anda tidak ada masalah variasi bahasa.",
    "Kolom 'penanda_AM_otomatis' hanya bantuan dari daftar penanda leksikal; boleh tidak disetujui. Tulis kata yang bermasalah di kolom 'kata_bermasalah'.",
    "Perkiraan waktu: 1,5 sampai 2 jam.",
], c2, {"no": 5, "item_id": 11, "sumber_indonesia": 50, "terjemahan_batak": 55, "penanda_AM_otomatis": 16,
        "kategori": 22, "kata_bermasalah": 25, "catatan": 25},
       {"kategori", "kata_bermasalah", "catatan"},
       {"kategori": ["AM_atau_Batak_lain", "serapan_Indonesia", "keduanya", "bahasa_lain", "tidak_ada"]})
wb.save(OUT / "C2_pecah_tag_variety.xlsx")

# ---------- C3: presisi penanda AM pada rujukan NusaTranslation ----------
nt = pd.read_csv(PAKET / "s02_nusatranslation.csv", keep_default_na=False)
nt["penanda"] = nt.teks_bbc.map(lambda t: ", ".join(sorted(set(tok(t)) & AM)))
am = nt[nt.penanda != ""].sample(n=50, random_state=2026).reset_index(drop=True)
c3 = pd.DataFrame({"no": range(1, 51), "id": am.uji_id, "kalimat_batak": am.teks_bbc, "penanda_terdeteksi": am.penanda,
                   "label": "", "catatan": ""})
wb = Workbook()
lembar(wb, "Label", [
    "Memeriksa ketepatan (presisi) daftar penanda leksikal Angkola-Mandailing. Berisi 50 kalimat acak dari NusaTranslation btk yang memuat minimal satu penanda.",
    "Untuk setiap kalimat, isi kolom 'label' (kuning):",
    "AM = kalimat ini Angkola-Mandailing atau jelas memuat unsur Angkola-Mandailing;",
    "Toba = kalimat ini Batak Toba yang wajar, penanda itu keliru menandainya;",
    "Batak_lain = varian Batak lain (misalnya Simalungun, Karo, Pakpak);",
    "ragu = tidak bisa memutuskan.",
    "Bila memilih Toba, tulis di 'catatan' mengapa penanda itu juga dipakai dalam Batak Toba (misalnya dialek daerah tertentu). Perkiraan waktu: 45 menit.",
], c3, {"no": 5, "id": 16, "kalimat_batak": 70, "penanda_terdeteksi": 18, "label": 14, "catatan": 35},
       {"label", "catatan"}, {"label": ["AM", "Toba", "Batak_lain", "ragu"]})
wb.save(OUT / "C3_presisi_penanda_AM.xlsx")

# ---------- C4: periksa contoh kualitatif ----------
contoh = ["kami-doc_0014_s000", "kami-doc_0001_s000", "kami-doc_0080_s053_c"]
SIS = {"MADLAD-400 3B": "madlad3b_zeroshot", "FT NusaTranslation": "ft_nusatranslation_s42",
       "FT ours + NusaTranslation": "ft_kami+nusatranslation_s42",
       "GoTo-AI 27B, retrieval": "llm_gemma3-27b-cpt-gotoai-v3-instruct_few_shot_retrieval"}
uji = pd.read_csv(PAKET / "s05_uji.csv", keep_default_na=False).set_index("uji_id")
pred = {}
for nama, s in SIS.items():
    L = (RL / f"prediksi/{s}/kami.id2bbc.jsonl").read_text(encoding="utf-8").splitlines()[1:]
    pred[nama] = {json.loads(l)["uji_id"]: json.loads(l)["hipotesis"] for l in L}
baris = []
for k, i in enumerate(contoh, 1):
    baris.append({"contoh": k, "jenis": "Sumber (Indonesia)", "teks": uji.loc[i, "teks_id"], "penanda_AM": "", "glos_inggris": "", "catatan": ""})
    baris.append({"contoh": k, "jenis": "Rujukan (Toba)", "teks": uji.loc[i, "teks_bbc"], "penanda_AM": "", "glos_inggris": "", "catatan": ""})
    for nama in SIS:
        t = pred[nama][i]
        baris.append({"contoh": k, "jenis": nama, "teks": t, "penanda_AM": ", ".join(sorted(set(tok(t)) & AM)),
                      "glos_inggris": "", "catatan": ""})
c4 = pd.DataFrame(baris)
wb = Workbook()
lembar(wb, "Contoh", [
    "Tabel contoh kualitatif untuk naskah: tiga kalimat uji, rujukan Toba, dan keluaran empat sistem.",
    "Mohon periksa: (1) apakah kata di kolom 'penanda_AM' memang bukan Batak Toba; (2) tulis glos bahasa Inggris singkat untuk kata yang ditebalkan di naskah",
    "(kata Angkola-Mandailing dan kata Indonesia yang tidak diterjemahkan), misalnya 'giot = want (AM; Toba naeng)';",
    "(3) catat bila ada hal lain yang menonjol dari keluaran itu. Perkiraan waktu: 20 menit.",
], c4, {"contoh": 8, "jenis": 26, "teks": 80, "penanda_AM": 16, "glos_inggris": 35, "catatan": 30},
       {"glos_inggris", "catatan"})
wb.save(OUT / "C4_periksa_contoh_kualitatif.xlsx")
print("C1", len(c1), "C2", len(c2), "C3", len(c3), "C4", len(c4))
