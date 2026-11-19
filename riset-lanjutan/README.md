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
| [`metadata/arah_penerjemahan_periksa.xlsx`](metadata/arah_penerjemahan_periksa.xlsx) | Lembar kerja pemeriksaan label bahasa asli, versi yang sudah diperiksa peneliti |
| [`data/split_korpus_kami.csv`](data/split_korpus_kami.csv) | Pembagian 1.542 pasangan korpus ini: 1.081 latih, 151 validasi, 310 uji (tingkat dokumen) |
| [`data/set_uji.csv`](data/set_uji.csv) | Daftar butir keempat set uji beserta label bahasa asli, genre, dan varietas rujukan |
| [`data/set_validasi.csv`](data/set_validasi.csv) | Daftar butir set validasi yang dipakai selama *fine-tuning* |
| [`data/esa_anonim.csv`](data/esa_anonim.csv) | 480 butir anotasi ESA dari dua penilai, tanpa identitas penilai dan tanpa catatan bebas |
| [`prediksi/`](prediksi/) | Keluaran 22 sistem untuk semua set uji dan kedua arah (132 berkas `.jsonl`) |
| [`hasil/tabel/`](hasil/tabel/) | Tabel hasil setiap tahap (S03 sampai S15), termasuk skor per kalimat |
| [`hasil/gambar/`](hasil/gambar/) | Gambar audit varietas, skor menurut bahasa asli, dan varietas keluaran |
| [`hasil/latex/`](hasil/latex/) | Tabel utama dan tabel bahasa asli dalam format LaTeX |
| [`hasil/_meta/`](hasil/_meta/) | Catatan *checkpoint* setiap tahap (parameter, sidik SHA-256 masukan dan keluaran), versi pustaka, dan manifest |
| [`skrip/holm_tabel3.py`](skrip/holm_tabel3.py) | Uji beda berpasangan ulang dengan 10.000 sampel *bootstrap* dan koreksi Holm atas 88 perbandingan (`hasil/tabel/tambahan_perbandingan_holm.csv`), serta selang kepercayaan 95% chrF++ menurut bahasa asli (`hasil/tabel/tambahan_tabel3_ik.csv`). Dijalankan di luar Colab, dari prediksi di `prediksi/` dan `s05_uji.csv` hasil S05 |
| [`skrip/analisis_revisi.py`](skrip/analisis_revisi.py) | Analisis untuk revisi naskah: statistik per genre, kovariat set uji menurut bahasa asli, rincian kesalahan ESA per penilai, selang kepercayaan alfa dan kappa, BLEU per sistem, dan *validation loss* per epoch (`hasil/tabel/revisi_*.csv`) |
| [`skrip/buat_lembar.py`](skrip/buat_lembar.py) | Pembuat lembar kerja penutur asli: pemeriksaan acak 100 pasangan, pemecahan tag [VARIETY], presisi penanda, dan pemeriksaan contoh kualitatif |
| [`skrip/buat_c6.py`](skrip/buat_c6.py), [`skrip/nilai_ulang_c6.py`](skrip/nilai_ulang_c6.py) | Lembar kerja perbaikan rujukan set uji (C6) dan penilaian ulang semua sistem dengan rujukan terkoreksi |
| [`skrip/leksikon_am.py`](skrip/leksikon_am.py), [`skrip/buat_c5.py`](skrip/buat_c5.py) | Kandidat kosakata penanda Angkola-Mandailing (analisis kontrastif kalimat AM dan Toba, diurutkan menurut batas bawah Wilson) dan lembar verifikasinya (C5) |
| [`data/anotasi_penutur/`](data/anotasi_penutur/) | Semua hasil pemeriksaan penutur asli dalam bentuk stand-off: penilaian dan koreksi 210 pasangan korpus ini, label varietas NusaTranslation dari penutur, label varietas otomatis seluruh NusaX dan NusaTranslation, dan rincian tag [VARIETY] ESA (lihat README di folder itu) |
| [`data/leksikon_am_terverifikasi.csv`](data/leksikon_am_terverifikasi.csv) | 153 kata dan frasa penanda Angkola-Mandailing (AM) yang diverifikasi penutur asli (C5): `kategori` (`AM_saja`, `AM_dan_Toba_perbatasan`, `juga_Toba_umum`, `bukan_Batak`), arti, padanan Toba, dan `kekuatan_penanda`. Aturan penyaringan yang disarankan: kalimat dianggap AM bila memuat satu bentuk `kuat`, atau dua bentuk `lemah` yang berbeda |
| [`data/set_uji_kami_terkoreksi.csv`](data/set_uji_kami_terkoreksi.csv) | Set uji `kami` (310 butir) dengan rujukan lama dan rujukan yang sudah dikoreksi penutur asli: 172 rujukan Toba dan 4 rujukan Indonesia diubah. Kolom `keputusan`: `benar`, `perbaiki_kata`, atau `perbaiki_makna` |
| [`hasil/v3/`](hasil/v3/) | Keluaran `skrip/jalankan_semua.py`: semua angka evaluasi untuk kedua versi rujukan (`*_lama.csv` dan `*_terkoreksi.csv`), audit varietas dengan daftar penanda 32 dan 26 kata, analisis ESA, statistik korpus, `verifikasi.csv`, dan `ringkasan.json` |
| [`hasil/tabel/c6_*.csv`](hasil/tabel/) | Penilaian ulang semua sistem dengan rujukan terkoreksi (dibuat oleh `skrip/nilai_ulang_c6.py`; kini juga direproduksi oleh `jalankan_semua.py`) |
| [`notebooks/reproduksi_tanpa_gpu.ipynb`](notebooks/reproduksi_tanpa_gpu.ipynb) | Notebook Colab (runtime CPU) yang menjalankan `jalankan_semua.py`, menampilkan verifikasi dan tabel utama, lalu menyimpan hasilnya |
| [`skrip/arsip_anotasi.py`](skrip/arsip_anotasi.py) | Membuat berkas di `data/anotasi_penutur/` dari lembar kerja C1 sampai C6 |
| [`skrip/bangun_versi_korpus.py`](skrip/bangun_versi_korpus.py) | Membangun versi baru korpus paralel dari versi sebelumnya dan berkas penilaian penutur asli (dipakai untuk `../data/btb_parallel_sentence_v1.1.csv`) |
| [`skrip/buat_lembar_tahap2.py`](skrip/buat_lembar_tahap2.py) | Lembar kerja pemeriksaan penuh untuk pasangan korpus yang belum pernah diperiksa penutur asli (tahap 2) |
| [`skrip/jalankan_semua.py`](skrip/jalankan_semua.py) | **Jalur reproduksi tanpa GPU.** Mengunduh NusaX dan NusaTranslation, menyusun set uji dalam dua versi rujukan, lalu menghitung ulang skor, selang kepercayaan, uji beda dengan koreksi Holm, Tabel 3, audit varietas, analisis ESA, dan statistik korpus. Angka versi rujukan lama dicocokkan otomatis dengan tabel di `hasil/tabel/` (`hasil/v3/verifikasi.csv`). Sekitar 2,5 menit di CPU |

Teks NusaX dan NusaTranslation **tidak** disalin ke repositori ini. Berkas di `data/` dan `prediksi/` hanya memuat ID butirnya (`nx-...`, `nt-...`), sehingga teks sumber dan rujukannya perlu diambil dari repositori asli masing-masing (tautannya ada di `hasil/_meta/lingkungan.json`). Teks korpus ini sendiri ada di [`../data/btb_parallel_sentence.csv`](../data/btb_parallel_sentence.csv).

### Set uji (`data/set_uji.csv`)

| `set_uji` | Butir | Keterangan |
|---|---|---|
| `kami` | 310 | Bagian uji korpus ini |
| `nusax` | 400 | Seluruh set uji NusaX (`toba_batak`) |
| `nusatranslation` | 2.000 | Seluruh set uji NusaTranslation `btk` |
| `nusatranslation_toba` | 400 | Sampel acak set uji NusaTranslation yang rujukannya berlabel `Toba_saja` (ada penanda Toba, tanpa penanda Angkola-Mandailing), dipakai untuk LLM dan juga dinilai untuk sistem lain |

Kolom: `uji_id`, `set_uji`, `arah_asli` (`asli_toba` atau `asli_indonesia`), `genre`, `varietas_rujukan` (`Toba_saja`, `AM`, atau `tak_bertanda`, dari penanda leksikal), dan `validasi_manusia` (khusus set `kami`, sama dengan kolom `validasi_manusia` di korpus utama).

### Prediksi (`prediksi/<sistem>/<set_uji>.<arah>.jsonl`)

Baris pertama adalah *header* berisi `sidik` dan `parameter` (model, benih, pengaturan dekode, atau kondisi *prompt*). Setiap baris berikutnya berisi `uji_id` dan `hipotesis`. Arah `id2bbc` berarti Indonesia ke Batak Toba, sedangkan `bbc2id` sebaliknya. Nama sistem: `copy_source`, `nllb600m_zeroshot`, `nllb1.3b_zeroshot`, `nllb3.3b_zeroshot`, `madlad3b_zeroshot`, `ft_<data>_s<benih>` (NLLB-200 600M yang di-*fine-tune*), dan `llm_<model>_<kondisi>` dengan kondisi `zero_shot`, `few_shot_acak`, atau `few_shot_retrieval`.

### Anotasi ESA (`data/esa_anonim.csv`)

| Kolom | Isi |
|---|---|
| `item_id`, `arah`, `uji_id`, `sistem` | Identitas butir. Urutan butir diacak berbeda untuk setiap penilai, dan nama sistem disembunyikan dari penilai |
| `sumber`, `terjemahan` | Kalimat sumber dari set uji `kami` dan keluaran sistem yang dinilai |
| `skor_A`, `skor_B` | Skor 0 sampai 100 dari penilai A dan B |
| `kesalahan_mayor_*`, `kesalahan_minor_*` | Rentang teks yang ditandai salah, dipisah ` \| ` |
| `variety_*` | Khusus `id2bbc`: 1 bila penilai menilai terjemahan memakai kata yang benar maknanya tetapi bukan Batak Toba, 0 bila tidak |

## Menjalankan ulang

**Tanpa GPU (semua angka evaluasi):** buka `notebooks/reproduksi_tanpa_gpu.ipynb` di Colab, atau dari akar repositori jalankan `pip install pandas numpy scipy openpyxl sacrebleu==2.6.0`, lalu `python riset-lanjutan/skrip/jalankan_semua.py`. Hasilnya ada di `hasil/v3/`; periksa `verifikasi.csv`.

**Dengan GPU (seluruh eksperimen, termasuk pelatihan):**

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

The experiments use the Phase 1 sentence-level parallel corpus (1,542 pairs) to study data quality and variety, the original language of texts, existing models, the value of the corpus as training data and as in-context examples, and the validity of automatic metrics against two native-speaker raters. Key results: only 0.26% of our Batak sentences carry Angkola-Mandailing markers (24.55% in the NusaTranslation test references); into Batak, no zero-shot NLLB-200, MADLAD-400 or Qwen2.5-7B system beats a copy-source baseline, and only GoTo-AI 27B does; adding our 1,081 training pairs to NusaX improves chrF++ on every out-of-domain test set by 1.3 to 3.0 points; retrieved in-context examples beat random ones; and chrF++ agrees only weakly with raters into Batak. The notebook [`notebooks/eksperimen_mt_batak_toba.ipynb`](notebooks/eksperimen_mt_batak_toba.ipynb) records every stage with its original outputs and observations. The folder also releases the data split (`data/split_korpus_kami.csv`), test-set item lists with original-language and reference-variety labels (`data/set_uji.csv`), outputs of all 22 systems (`prediksi/`), result tables, figures and stage checkpoints (`hasil/`), and 480 anonymised ESA judgements from two native-speaker raters (`data/esa_anonim.csv`). NusaX and NusaTranslation texts are not redistributed; only their item IDs are included.
