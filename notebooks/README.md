# notebooks/

## `pipeline_korpus_multigenre_v2.ipynb`

Notebook Google Colab tunggal yang mengolah sub-korpus multi-genre dari hasil kerja kedua anotator (`Combined Annotator.xlsx`) sampai korpus paralel tingkat kalimat yang siap diuji kesepakatan antaranotator (IAA).

| Tahap | Isi |
|---|---|
| 1 | Muat dan validasi input anotator |
| 2 | Koreksi metadata tercatat |
| 3 | Pembersihan ringan, menghasilkan `btb_multigenre.csv` |
| 4 | Segmentasi kalimat |
| 5 | Statistik korpus dengan tiga metode hitung token |
| 6 | Penyelarasan kalimat (aturan 1:1 atau LaBSE) |
| 7 | Audit otomatis dan pelabelan status |
| 8 | Lembar review untuk dua anotator |
| 9 | Penghitungan IAA (Cohen's kappa) dan lembar adjudikasi |
| 10 | Paket rilis, perbandingan dengan v1, manifest, dan changelog |

Setiap tahap menyimpan titik simpan (checkpoint) di Google Drive, sehingga saat dijalankan ulang hanya tahap yang masukan, parameter, atau kodenya berubah yang dihitung ulang. Petunjuk lengkap ada di sel pertama notebook.

Sub-korpus Alkitab tidak diolah di notebook ini.

Panduan pemakaian lengkap, termasuk data yang dipakai di setiap tahap dan status file lama, ada di [`../docs/panduan-pipeline-v2.md`](../docs/panduan-pipeline-v2.md).

## `panduan_anotator_BTB.ipynb`

Panduan kerja untuk kedua anotator, berisi definisi teks, target sebaran genre, dan daftar sumber yang ditugaskan kepada setiap anotator. Daftar sumber ini menjadi dasar koreksi label di Tahap 2 notebook pipeline.

---

## `pipeline_korpus_multigenre_v2.ipynb`

A single Google Colab notebook that processes the multi-genre sub-corpus from the two annotators' output (`Combined Annotator.xlsx`) to a sentence-level parallel corpus ready for inter-annotator agreement (IAA). It covers input validation, logged metadata corrections, light cleaning, sentence segmentation, corpus statistics, sentence alignment (rule-based 1:1 or LaBSE), automatic auditing, review sheets for two annotators, IAA computation, and a release package with a manifest. Every stage writes a checkpoint to Google Drive, so a rerun only recomputes stages whose inputs, parameters, or code changed. The Bible sub-corpus is processed separately.

A full usage guide is in [`../docs/panduan-pipeline-v2.md`](../docs/panduan-pipeline-v2.md).

## `panduan_anotator_BTB.ipynb`

Working guide for the two annotators, with the text definition, target genre distribution, and the source list assigned to each annotator. This source list is the basis for the label corrections in Stage 2 of the pipeline notebook.
