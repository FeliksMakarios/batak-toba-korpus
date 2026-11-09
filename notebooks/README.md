# notebooks/

## `alur_lengkap_korpus_batak_toba.ipynb` (notebook utama)

Notebook Google Colab tunggal yang menampilkan seluruh pengolahan korpus dari awal sampai akhir, termasuk peta alur dan riwayat keputusan selama penelitian.

| Bagian | Isi |
|---|---|
| 0 | Peta alur dan riwayat keputusan |
| A | Persiapan, daftar input, dan konfigurasi |
| B (tahap 1 sampai 5) | Korpus multi-genre: validasi, koreksi label, pembersihan, segmentasi, statistik |
| C (tahap 6 sampai 9) | Korpus paralel: korpus v1, rekonsiliasi label dan IAA, keputusan emas dari adjudikasi, penerapan ke korpus |
| D (tahap 10) | Statistik akhir dan paket rilis |
| E | Ringkasan dan keterbatasan |

Diagram alurnya juga tersedia sebagai [`../docs/peta-alur-korpus.svg`](../docs/peta-alur-korpus.svg).

Notebook ini tidak membutuhkan GPU. Hasil tahap 9 diverifikasi sama persis dengan `korpus_utama_FINAL_v3`.

## `agenda_hkbp_segmentasi.ipynb`

Langkah pertama sub-korpus paralel religius: segmentasi kalimat enam bagian Agenda HKBP (`mg_054` sampai `mg_059` di `btb_multigenre.csv`). Setiap unit diberi keterangan struktur (bagian, subbagian, butir, label peran) dan jenis unit (isi, instruksi, rujukan ayat, formula, dan lainnya), sebagai jangkar untuk penyelarasan berikutnya. Koreksi OCR sisi Indonesia hanya untuk pola yang jelas dan daftar kata eksplisit, dan teks aslinya tetap disimpan.

| Tahap | Isi |
|---|---|
| a01 | Muat dan validasi Agenda (sidik SHA-256 berkas masukan diperiksa) |
| a02 | Struktur baris: judul, subjudul, label peran, penanda butir, penggabungan baris |
| a03 | Segmentasi kalimat |
| a04 | Normalisasi OCR terbatas dan jenis unit |
| a05 | Pemeriksaan keutuhan teks, kesejajaran bagian, pembanding segmentasi lama, dan sampel pemeriksaan |

Penyelarasan, deduplikasi, dan pembagian train/dev/test belum dikerjakan di notebook ini. Keluarannya memuat teks Agenda HKBP yang izin redistribusinya belum dipastikan, jadi simpan hanya di Google Drive tim. Notebook ini tidak membutuhkan GPU.

## `eksperimen_mt_batak_toba.ipynb` (eksperimen naskah tahap 2)

Notebook Google Colab untuk eksperimen terjemahan mesin Batak Toba dan Indonesia pada korpus paralel tingkat kalimat. Isinya: audit varietas, pembagian data berbasis dokumen, *baseline copy-source*, NLLB-200 dan MADLAD-400 *zero-shot*, *fine-tuning* NLLB-200 pada lima konfigurasi data, LLM *zero-shot* dan *few-shot*, evaluasi otomatis per arah penerjemahan asli, lembar ESA untuk dua penilai, serta paket hasil untuk naskah. Notebook butuh GPU (A100 disarankan). Setiap tahap menyimpan *checkpoint* di Google Drive, dan pelatihan serta penerjemahan dapat dilanjutkan setelah sesi terputus.

Sebelum menjalankan notebook, periksa dan lengkapi [`../metadata/arah_penerjemahan_periksa.xlsx`](../metadata/arah_penerjemahan_periksa.xlsx), lalu unggah ke folder `input/` notebook.

## `pipeline_korpus_multigenre_v2.ipynb` (arsip)

Versi sebelumnya. Tahap 1 sampai 5-nya sama dengan notebook utama. Tahap 6 sampai 10-nya berisi eksperimen penyelarasan ulang dengan LaBSE yang tidak dipakai, karena anotasi manusia akhirnya dilakukan pada korpus paralel v1. Panduannya ada di [`../docs/panduan-pipeline-v2.md`](../docs/panduan-pipeline-v2.md).

## `panduan_anotator_BTB.ipynb`

Panduan kerja untuk kedua anotator, berisi definisi teks, target sebaran genre, dan daftar sumber yang ditugaskan kepada setiap anotator. Daftar sumber ini menjadi dasar koreksi label di Tahap 2 notebook pipeline.

---

## `alur_lengkap_korpus_batak_toba.ipynb` (main notebook)

A single Google Colab notebook showing the whole corpus processing from start to finish, including a flow map and a record of decisions made during the research: the multi-genre corpus (stages 1 to 5), the sentence-level parallel corpus with inter-annotator agreement and adjudication (stages 6 to 9), and the release package (stage 10). No GPU is needed. Stage 9 output is verified to be identical to `korpus_utama_FINAL_v3`.

`pipeline_korpus_multigenre_v2.ipynb` is kept as an archive of the unused LaBSE realignment experiment.

## `panduan_anotator_BTB.ipynb`

Working guide for the two annotators, with the text definition, target genre distribution, and the source list assigned to each annotator. This source list is the basis for the label corrections in Stage 2.
