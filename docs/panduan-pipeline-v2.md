# Panduan Pemakaian Notebook Pipeline v2

Dokumen ini merangkum cara memakai notebook [`notebooks/pipeline_korpus_multigenre_v2.ipynb`](../notebooks/pipeline_korpus_multigenre_v2.ipynb): tahapannya, data yang dipakai di setiap tahap, lokasi file, dan status semua file lama.

**Inti yang perlu diingat:** notebook hanya butuh **satu** file dari Anda, yaitu `Combined Annotator.xlsx`. Semua file lain dibuat sendiri oleh notebook.

## 1. Tahapan notebook dan data yang dipakai

| Tahap | Yang dikerjakan | Masukan | Keluaran (otomatis di `keluaran/`) |
|---|---|---|---|
| 1. Muat dan validasi | Membaca file anotator, memberi `doc_id` (`mg_001` sampai `mg_104`), memeriksa teks kosong dan teks yang terpotong | **`input/Combined Annotator.xlsx`** (dari Anda) | `s01_dokumen_mentah.csv`, `s01_validasi.json` |
| 2. Koreksi metadata | Memperbaiki 12 label, mengosongkan isian contoh templat, memulihkan tautan sumber | Keluaran tahap 1 | `s02_dokumen.csv`, `s02_log_koreksi.csv` |
| 3. Pembersihan ringan | Merapikan Unicode dan spasi tanpa mengubah kata | Keluaran tahap 2 | `s03_btb_multigenre.csv` (berkas rilis) |
| 4. Segmentasi kalimat | Memecah dokumen menjadi kalimat atau baris | Keluaran tahap 3 | `s04_kalimat.csv` |
| 5. Statistik | Menghitung kata dan token dengan tiga metode | Keluaran tahap 3 dan 4 | `s05_statistik.json`, tabel untuk README |
| 6. Penyelarasan | Memasangkan kalimat Toba dan Indonesia dengan aturan 1:1 atau LaBSE (butuh GPU) | Keluaran tahap 3 dan 4 | `s06_penyelarasan.csv` |
| 7. Audit otomatis | Memberi tanda, prioritas, dan status pada setiap pasangan | Keluaran tahap 6 | `s07_paralel_utama.csv`, `s07_paralel_liturgi.csv` |
| 8. Lembar review | Menyusun dua lembar Excel identik untuk dua anotator | Keluaran tahap 7 | `s08_review_anotator_A.xlsx` dan `s08_review_anotator_B.xlsx` |
| 9. IAA | Menghitung Cohen's kappa dan menyusun lembar adjudikasi | **`review_terisi/review_anotator_A.xlsx` dan `review_anotator_B.xlsx`** (diisi anotator) | `s09_laporan_iaa.json`, `s09_adjudikasi.xlsx` |
| 10. Paket rilis | Menyalin berkas final, membandingkan dengan v1, menulis manifest | Keluaran tahap sebelumnya, ditambah **`input/btb_parallel_sentence_v1.csv`** (opsional) | Folder `rilis/` |

Anda hanya menyiapkan file pada tiga kesempatan:

1. Di awal: `Combined Annotator.xlsx` untuk Tahap 1.
2. Setelah anotator selesai mengisi lembar review: dua lembar terisi untuk Tahap 9.
3. Opsional: file korpus paralel v1 untuk perbandingan di Tahap 10.

## 2. Susunan folder di Google Drive

```
MyDrive/Datasets/btb-pipeline-v2/
├── input/
│   ├── Combined Annotator.xlsx         (wajib)
│   └── btb_parallel_sentence_v1.csv    (opsional, unduh dari GitHub)
├── review_terisi/                      (diisi setelah anotator selesai)
├── keluaran/                           (dibuat notebook)
└── rilis/                              (dibuat notebook)
```

Folder `keluaran/`, `review_terisi/`, dan `rilis/` dibuat otomatis saat notebook pertama kali dijalankan. Anda cukup membuat folder `input/` dan mengisinya.

## 3. Langkah menjalankan

1. Buka notebook di Colab lewat **File > Open notebook > GitHub**, lalu pilih repositori ini dan branch yang memuat notebook.
2. Pilih **Runtime > Change runtime type > T4 GPU**.
3. Jalankan **Runtime > Run all**. Izinkan Colab mengakses Google Drive saat diminta.
4. Bagikan `keluaran/s08_review_anotator_A.xlsx` dan `keluaran/s08_review_anotator_B.xlsx` kepada dua anotator. Mereka bekerja terpisah dan tidak saling melihat.
5. Simpan kedua lembar yang sudah diisi ke `review_terisi/` dengan nama `review_anotator_A.xlsx` dan `review_anotator_B.xlsx`.
6. Jalankan **Run all** sekali lagi. Tahap 1 sampai 8 diambil dari checkpoint, dan Tahap 9 menghitung IAA.

Jangan menjalankan sel secara acak. Notebook dirancang untuk dijalankan dari atas ke bawah.

## 4. Lokasi file di GitHub

| Lokasi di repositori | Isi |
|---|---|
| `notebooks/pipeline_korpus_multigenre_v2.ipynb` | Notebook pipeline multi-genre |
| `notebooks/panduan_anotator_BTB.ipynb` | Panduan dan daftar sumber untuk anotator. Daftar sumber ini menjadi dasar 12 koreksi label |
| `data/btb_multigenre.csv` | Korpus multi-genre versi 2, keluaran Tahap 3 |
| `data/experimental/btb_parallel_sentence_v1.csv` | Korpus paralel v1. Dipakai sebagai pembanding opsional di Tahap 10 |
| `data/experimental/audit_penyelarasan_v1.xlsx` | Buku kerja audit penyelarasan v1 |
| `data/experimental/doc_id_map.csv` | Pemetaan `doc_id` v1 |
| `docs/panduan-pipeline-v2.md` | Dokumen ini |

`Combined Annotator.xlsx` **tidak disimpan di GitHub**. Simpan baik-baik di Google Drive.

## 5. Status semua file lama

### Dipakai notebook multi-genre

| File | Peran |
|---|---|
| `Combined Annotator.xlsx` | Input utama Tahap 1 |
| `btb_parallel_sentence_v1.csv` (sama dengan `korpus_utama_revisi_penyelarasan_v1.csv`) | Pembanding opsional Tahap 10 |

### Arsip bukti asal data (tidak dipakai notebook)

| File | Keterangan |
|---|---|
| `Annotator_1.xlsx`, `Annotator_2-2.xlsx` | Hasil kerja masing-masing anotator. `Combined Annotator.xlsx` adalah gabungan persis keduanya |
| `audit_penyelarasan_toba_v1.xlsx` | Sudah ada di repositori sebagai `audit_penyelarasan_v1.xlsx` |
| `Annotator - BTB_Template.ipynb` | Sudah ada di repositori sebagai `panduan_anotator_BTB.ipynb` |

### Disisihkan untuk notebook Alkitab nanti

| File | Keterangan |
|---|---|
| `alkitab.csv` | Hasil scraping mentah, 12 versi Alkitab |
| `alkitab_bataktoba.csv` | Alkitab Batak Toba. Isinya identik dengan `alkitab_bataktoba_tokenized.csv`, jadi cukup simpan satu |
| `btb_bible.csv` | Korpus paralel Alkitab versi lama |
| `alkitab_bataktoba_wordcount.csv` | Daftar frekuensi kata |
| `dataset_alkitab_batak_toba.ipynb`, `toba_pl.zip`, `toba_pb.zip` | Scraping Alkitab Toba lengkap per kitab (belum selesai) |

### Tidak perlu lagi (sudah digantikan notebook v2)

| File | Keterangan |
|---|---|
| `combined_annotator_data.csv`, `combined_annotator_data-v1.1.csv`, `combined_annotator_data_norm.csv`, `combined_annotator_data_norm_clean.csv` | Turunan lama dari `Combined Annotator.xlsx` |
| `btb_multigenre.csv` versi lama | Gunakan `data/btb_multigenre.csv` di GitHub |
| `01_build-batak-toba-corpus.ipynb`, `01_build-batak-toba-corpus-v2.ipynb`, `02_eda-batak-toba-corpus.ipynb`, `Segmentasi_Kalimat_Batak_Toba.ipynb` | Notebook lama. Seluruh fungsinya untuk multi-genre sudah ada di notebook v2 |

**Peringatan keamanan:** `01_build-batak-toba-corpus-v2.ipynb` memuat token Hugging Face dalam teks polos. Cabut token tersebut di pengaturan akun Hugging Face, lalu hapus notebook itu atau hapus sel yang memuat token.
