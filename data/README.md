# data/

| Berkas | Isi | Status |
|---|---|---|
| `btb_multigenre.csv` | Korpus multi-genre, 104 dokumen paralel Batak Toba dan Indonesia | Versi 2, dihasilkan oleh [`../notebooks/pipeline_korpus_multigenre_v2.ipynb`](../notebooks/pipeline_korpus_multigenre_v2.ipynb) dari `Combined Annotator.xlsx` |
| `btb_bible.csv` | Korpus paralel Alkitab Batak Toba (1894) dan Bahasa Indonesia, satu pasal per kitab | Belum disertakan. Menunggu notebook pengolahan tersendiri dan pemeriksaan izin terjemahan Indonesianya |
| `btb_parallel_sentence.csv` | Korpus paralel tingkat kalimat, 1.542 pasangan (182 divalidasi manusia) | Dihasilkan oleh notebook alur lengkap, tahap 9 |
| `iaa/` | Laporan kesepakatan antaranotator, matriks konfusi, analisis sensitivitas, keputusan emas 145 pasangan, dan statistik korpus paralel | Dihasilkan oleh notebook alur lengkap, tahap 7 sampai 10 |
| `experimental/` | Korpus paralel v1 (1.505 pasangan) dan buku kerja audit penyelarasan | Input beku untuk tahap 6 notebook alur lengkap |

Perubahan `btb_multigenre.csv` versi 2 dibanding versi sebelumnya:

1. Kolom `doc_id` ditambahkan.
2. Dua belas label genre atau sub-genre diperbaiki sesuai panduan anotator: tiga ulasan buku menjadi `Educational/Book Summary`, dan sembilan abstrak artikel jurnal menjadi `Educational/Abstract` (sebelumnya `News Article`).
3. Label `Historical/ Traditional` diseragamkan menjadi `Historical/Traditional`.
4. Metadata contoh dari templat Google Sheet dikosongkan, dan dua tautan sumber yang hilang dipulihkan.
5. Teks dirapikan secara teknis (Unicode, spasi, akhir baris) tanpa mengubah kata. Jumlah token berbasis spasi tidak berubah.

Kolom `btb_parallel_sentence.csv`: `pair_id` (akhiran `__rNN` menandai unit hasil pemecahan saat adjudikasi), `doc_id` (sama dengan `btb_multigenre.csv`), `doc_id_v1`, `genre`, `sub_genre`, `method`, `alignment_type` (tipe blok penyelarasan awal), `toba_final`, `indo_final`, `source`, `review_status` (`not_flagged`, `accepted`, `revised`, `revised_split`), `gold_decision`, dan `validasi_manusia`.

Definisi kolom dan taksonomi genre ada di [../metadata/skema-kolom.md](../metadata/skema-kolom.md).

---

| File | Contents | Status |
|---|---|---|
| `btb_multigenre.csv` | Multi-genre corpus, 104 parallel Batak Toba and Indonesian documents | Version 2, produced by the pipeline notebook from `Combined Annotator.xlsx` |
| `btb_bible.csv` | Parallel Batak Toba (1894) and Indonesian Bible corpus, one chapter per book | Not yet included, pending its own processing notebook and a permission check for the Indonesian translation |
| `btb_parallel_sentence.csv` | Sentence-level parallel corpus, 1,542 pairs (182 human-validated) | Produced by the full-flow notebook, stage 9 |
| `iaa/` | Inter-annotator agreement report, confusion matrix, sensitivity analysis, gold decisions for 145 pairs, and parallel corpus statistics | Produced by the full-flow notebook, stages 7 to 10 |
| `experimental/` | Parallel corpus v1 (1,505 pairs) and alignment audit workbook | Frozen input for stage 6 of the full-flow notebook |

Version 2 adds a `doc_id` column, corrects twelve genre or sub-genre labels to match the annotator guide, normalises the `Historical/Traditional` label, removes template placeholder metadata, restores two missing source links, and applies technical text cleanup without changing any words.
