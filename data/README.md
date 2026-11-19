# data/

| Berkas | Isi | Status |
|---|---|---|
| `btb_multigenre.csv` | Korpus multi-genre, 104 dokumen paralel Batak Toba dan Indonesia | Versi 2, dihasilkan oleh [`../notebooks/pipeline_korpus_multigenre_v2.ipynb`](../notebooks/pipeline_korpus_multigenre_v2.ipynb) dari `Combined Annotator.xlsx` |
| `btb_bible.csv` | Korpus paralel Alkitab Batak Toba (1894) dan Bahasa Indonesia, satu pasal per kitab | Belum disertakan. Menunggu notebook pengolahan tersendiri dan pemeriksaan izin terjemahan Indonesianya |
| `btb_parallel_sentence.csv` | Korpus paralel tingkat kalimat, 1.542 pasangan (182 divalidasi manusia) | Dihasilkan oleh notebook alur lengkap, tahap 9 |
| `btb_parallel_sentence_v1.1.csv` | Korpus paralel tingkat kalimat versi 1.1: 1.542 pasangan, 210 di antaranya diperbaiki penutur asli (206 sisi Toba, 5 sisi Indonesia) | Dibuat oleh [`../riset-lanjutan/skrip/bangun_versi_korpus.py`](../riset-lanjutan/skrip/bangun_versi_korpus.py) dari versi 1.0 dan [`../riset-lanjutan/data/anotasi_penutur/penilaian_korpus_kami.csv`](../riset-lanjutan/data/anotasi_penutur/penilaian_korpus_kami.csv) |
| `iaa/` | Laporan kesepakatan antaranotator, matriks konfusi, analisis sensitivitas, keputusan emas 145 pasangan, dan statistik korpus paralel | Dihasilkan oleh notebook alur lengkap, tahap 7 sampai 10 |
| `experimental/` | Korpus paralel v1 (1.505 pasangan) dan buku kerja audit penyelarasan | Input beku untuk tahap 6 notebook alur lengkap |

Perubahan `btb_multigenre.csv` versi 2 dibanding versi sebelumnya:

1. Kolom `doc_id` ditambahkan.
2. Dua belas label genre atau sub-genre diperbaiki sesuai panduan anotator: tiga ulasan buku menjadi `Educational/Book Summary`, dan sembilan abstrak artikel jurnal menjadi `Educational/Abstract` (sebelumnya `News Article`).
3. Label `Historical/ Traditional` diseragamkan menjadi `Historical/Traditional`.
4. Metadata contoh dari templat Google Sheet dikosongkan, dan dua tautan sumber yang hilang dipulihkan.
5. Teks dirapikan secara teknis (Unicode, spasi, akhir baris) tanpa mengubah kata. Jumlah token berbasis spasi tidak berubah.

Kolom `btb_parallel_sentence.csv`: `pair_id` (akhiran `__rNN` menandai unit hasil pemecahan saat adjudikasi), `doc_id` (sama dengan `btb_multigenre.csv`), `doc_id_v1`, `genre`, `sub_genre`, `method`, `alignment_type` (tipe blok penyelarasan awal), `toba_final`, `indo_final`, `source`, `review_status` (`not_flagged`, `accepted`, `revised`, `revised_split`), `gold_decision`, dan `validasi_manusia`.

Versi 1.1 (`btb_parallel_sentence_v1.1.csv`) dibanding versi 1.0:

1. Seluruh 310 pasangan set uji diperiksa penutur asli; 172 terjemahan Toba dan 4 terjemahan Indonesia diperbaiki.
2. Dari 100 pasangan acak yang sebelumnya tidak pernah ditandai, 34 pasangan di bagian latih dan validasi diperbaiki (pasangan di bagian uji mengikuti pemeriksaan set uji).
3. Kolom baru: `pemeriksaan_penutur` (lembar pemeriksaan: `C1` pemeriksaan acak, `C6` pemeriksaan set uji), `keputusan_penutur`, `dikoreksi_pada_versi`, dan `catatan_varietas` (tiga kalimat yang menurut penutur asli memuat unsur Angkola-Mandailing).
4. Versi 1.0 tetap disimpan apa adanya karena model di naskah riset lanjutan dilatih dengan versi itu. Pembagian latih, validasi, dan uji sama untuk kedua versi ([`../riset-lanjutan/data/split_korpus_kami.csv`](../riset-lanjutan/data/split_korpus_kami.csv)).
5. Sebanyak 1.002 pasangan belum pernah diperiksa penutur asli (kolom `pemeriksaan_penutur` kosong dan `review_status` = `not_flagged`). Pemeriksaan penuhnya sedang berjalan (tahap 2).

Definisi kolom dan taksonomi genre ada di [../metadata/skema-kolom.md](../metadata/skema-kolom.md).

---

| File | Contents | Status |
|---|---|---|
| `btb_multigenre.csv` | Multi-genre corpus, 104 parallel Batak Toba and Indonesian documents | Version 2, produced by the pipeline notebook from `Combined Annotator.xlsx` |
| `btb_bible.csv` | Parallel Batak Toba (1894) and Indonesian Bible corpus, one chapter per book | Not yet included, pending its own processing notebook and a permission check for the Indonesian translation |
| `btb_parallel_sentence.csv` | Sentence-level parallel corpus, 1,542 pairs (182 human-validated) | Produced by the full-flow notebook, stage 9 |
| `btb_parallel_sentence_v1.1.csv` | Sentence-level parallel corpus, version 1.1: 1,542 pairs, 210 of them corrected by a native speaker (206 Toba sides, 5 Indonesian sides) | Built by `../riset-lanjutan/skrip/bangun_versi_korpus.py` from version 1.0 and the native-speaker judgements |
| `iaa/` | Inter-annotator agreement report, confusion matrix, sensitivity analysis, gold decisions for 145 pairs, and parallel corpus statistics | Produced by the full-flow notebook, stages 7 to 10 |
| `experimental/` | Parallel corpus v1 (1,505 pairs) and alignment audit workbook | Frozen input for stage 6 of the full-flow notebook |

Version 2 adds a `doc_id` column, corrects twelve genre or sub-genre labels to match the annotator guide, normalises the `Historical/Traditional` label, removes template placeholder metadata, restores two missing source links, and applies technical text cleanup without changing any words.

Version 1.1 corrects all 310 test pairs after a full native-speaker check (172 Toba and 4 Indonesian translations) and 34 training or validation pairs from a random check of 100 previously unflagged pairs. It adds the columns `pemeriksaan_penutur`, `keputusan_penutur`, `dikoreksi_pada_versi` and `catatan_varietas`. Version 1.0 is kept unchanged because the models in the follow-up study were trained on it; the train, validation and test split is the same for both versions. 1,002 pairs have not yet been checked by a native speaker; a full check is in progress.
