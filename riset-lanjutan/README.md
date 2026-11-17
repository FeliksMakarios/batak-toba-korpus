# Riset lanjutan: eksperimen terjemahan mesin Batak Toba dan Indonesia

> **Status.** Folder ini berada **di luar luaran PDP Tahap 1**. Isinya adalah pengembangan untuk naskah jurnal yang sedang disiapkan (target: *Language Resources and Evaluation*). Folder ini disimpan di branch tersendiri dan baru digabung ke `main` setelah naskah dikirim.

Riset ini memakai korpus paralel tingkat kalimat dari Tahap 1 ([`../data/btb_parallel_sentence.csv`](../data/btb_parallel_sentence.csv), 1.542 pasangan) untuk menjawab enam pertanyaan: mutu dan varietas data, pengaruh bahasa asli teks, kemampuan model yang sudah ada, nilai korpus sebagai data latih, manfaatnya sebagai contoh *in-context* untuk LLM, dan validitas metrik otomatis terhadap penilaian manusia.

## Temuan utama

| RQ | Temuan |
|---|---|
| RQ1 mutu data | Hanya 0,26% kalimat Batak korpus ini yang bertanda Angkola-Mandailing, dibanding 24,55% pada rujukan uji NusaTranslation (`btk`). |
| RQ2 bahasa asli | Teks yang aslinya berbahasa Toba jauh lebih sulit dipahami: skor manusia ke arah Indonesia turun sekitar 40 poin. Ke arah Batak, chrF++ meremehkan mutu terjemahan pada teks ini. |
| RQ3 model yang ada | Ke arah Batak, NLLB-200 (sampai 3,3B), MADLAD-400 3B, dan Qwen2.5-7B *zero-shot* tidak melampaui *copy-source*. Hanya GoTo-AI 27B yang melampauinya secara *zero-shot*. |
| RQ4 nilai data latih | Menambahkan 1.081 pasangan latih korpus ini ke NusaX menaikkan chrF++ secara signifikan di semua set uji di luar domainnya (+1,3 sampai +3,0). Model yang dilatih dengan NusaTranslation menulis Angkola-Mandailing pada 58 sampai 66% keluarannya untuk rujukan Toba. |
| RQ5 contoh *prompt* | Contoh hasil *retrieval* dari korpus ini lebih baik daripada contoh acak (+1,4 sampai +4,3 chrF++ ke arah Batak untuk GoTo-AI 27B). |
| RQ6 evaluasi | Dua penilai penutur asli sangat sepakat (alfa Krippendorff 0,85 dan 0,92). chrF++ hanya lemah sejalan dengan penilai ke arah Batak (Kendall tau 0,27 di antara sistem *fine-tuned*). |

Rincian setiap angka, beserta keluaran asli dan observasinya, ada di notebook.

## Isi folder

| Berkas atau folder | Isi |
|---|---|
| [`notebooks/eksperimen_mt_batak_toba.ipynb`](notebooks/eksperimen_mt_batak_toba.ipynb) | Rekaman eksekusi lengkap tahap S01 sampai S15: kode, keluaran asli dari empat sesi Colab, dan sel "Hasil dan observasi" setelah setiap tahap |
| [`metadata/arah_penerjemahan.csv`](metadata/arah_penerjemahan.csv) | Label bahasa asli per dokumen (lihat skema di bawah) |
| [`metadata/arah_penerjemahan_periksa.xlsx`](metadata/arah_penerjemahan_periksa.xlsx) | Lembar kerja pemeriksaan label bahasa asli |
| `data/` | Pembagian data latih, validasi, dan uji, serta anotasi ESA tanpa identitas penilai (menyusul) |
| `prediksi/` | Keluaran 22 sistem untuk semua set uji dan kedua arah (menyusul) |
| `hasil/` | Tabel skor, uji beda, varietas keluaran, analisis ESA, dan gambar (menyusul) |

## Menjalankan ulang

1. Buka notebook di Google Colab dan pilih runtime GPU. A100 dipakai untuk S06, S07, dan S09; L4 untuk S08.
2. Bila label bahasa asli sudah diperiksa, unggah `arah_penerjemahan_periksa.xlsx` ke folder `input/` di Drive. Korpus, NusaX, dan NusaTranslation diunduh otomatis.
3. Jalankan sel dari atas ke bawah. Setiap tahap menyimpan *checkpoint* di Google Drive, sehingga sesi yang terputus bisa dilanjutkan tanpa mengulang dari awal.
4. Simpan token Hugging Face di menu *Secrets* Colab dengan nama `HF_TOKEN`. Jangan menulis token di sel.

## Skema label bahasa asli (`metadata/arah_penerjemahan.csv`)

Satu baris per dokumen multi-genre (104 dokumen). Kolom berakhiran `_otomatis` diisi dari `source_link`, sedangkan kolom berakhiran `_final` diisi peneliti.

| Kolom | Isi |
|---|---|
| `doc_id`, `judul`, `genre`, `subgenre` | Sama dengan `btb_multigenre.csv` |
| `n_pasangan_paralel`, `di_korpus_paralel` | Jumlah pasangan dokumen ini di `btb_parallel_sentence.csv` |
| `domain_sumber`, `source_link_asli` | Tautan sumber. Tautan pengalihan Google sudah dibuka menjadi URL aslinya |
| `arah_otomatis`, `keyakinan`, `alasan_otomatis` | Tebakan otomatis beserta tingkat keyakinan dan alasannya |
| `arah_final` | Label terperiksa: `asli_toba` (teks asli Batak Toba, sisi Indonesia terjemahan) atau `asli_indonesia` (sebaliknya) |
| `penerjemah_otomatis`, `penerjemah_final` | Penulis sisi terjemahan: `narasumber`, `sumber_asli`, atau `tidak_diketahui` |

## Keterbatasan utama

1. Bahasa asli bercampur dengan genre: seluruh 44 pasangan uji asli Toba bergenre sastra atau sejarah.
2. Penanda varietas bersifat leksikal dan heuristik, sehingga persentase Angkola-Mandailing adalah batas bawah.
3. *Fine-tuning* hanya pada NLLB-200 600M. GoTo-AI 27B dijalankan dalam 4-bit, sedangkan Qwen2.5-7B dalam `bfloat16`.
4. Evaluasi manusia memakai dua penilai dan 60 kalimat per arah.

---

# Follow-up research: Batak Toba-Indonesian machine translation experiments

> **Status.** This folder is **not a PDP Phase 1 deliverable**. It holds the work behind a journal manuscript in preparation (target: *Language Resources and Evaluation*) and lives on a separate branch until the manuscript is submitted.

The experiments use the Phase 1 sentence-level parallel corpus (1,542 pairs) to study data quality and variety, the original language of texts, existing models, the value of the corpus as training data and as in-context examples, and the validity of automatic metrics against two native-speaker raters. Key results: only 0.26% of our Batak sentences carry Angkola-Mandailing markers (24.55% in the NusaTranslation test references); into Batak, no zero-shot NLLB-200, MADLAD-400 or Qwen2.5-7B system beats a copy-source baseline, and only GoTo-AI 27B does; adding our 1,081 training pairs to NusaX improves chrF++ on every out-of-domain test set by 1.3 to 3.0 points; retrieved in-context examples beat random ones; and chrF++ agrees only weakly with raters into Batak. The notebook [`notebooks/eksperimen_mt_batak_toba.ipynb`](notebooks/eksperimen_mt_batak_toba.ipynb) records every stage with its original outputs and observations.
