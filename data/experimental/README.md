# data/experimental/

> **Status: EKSPERIMENTAL, PENDING IAA.** Berkas di folder ini bukan bagian dari luaran resmi penelitian tahap 1 dan bukan korpus emas (gold standard). Inter-annotator agreement (IAA) belum dilakukan dan belum ada pasangan yang disahkan oleh penutur.

## Isi

| Berkas | Isi |
|---|---|
| `btb_parallel_sentence_v1.csv` | Korpus paralel Batak Toba dan Bahasa Indonesia pada tingkat kalimat atau segmen, versi kerja v1. |
| `audit_penyelarasan_v1.xlsx` | Buku kerja audit penyelarasan: panduan, korpus hasil revisi, antrean pemeriksaan (`Perlu_periksa`), jejak perubahan, data asli sebelum audit, dan kamus kolom. |
| `doc_id_map.csv` | Pemetaan `doc_id` ke judul, genre, dan jumlah pasangan per dokumen. |

## Ringkasan

| Ukuran | Nilai |
|---|---|
| Pasangan (baris) | 1.505 |
| Dokumen tercakup | 97 dari 99 |
| Token Batak Toba (berbasis spasi) | 23.820 |
| Token Bahasa Indonesia (berbasis spasi) | 21.050 |
| `alignment_status = candidate_1_1` | 1.275 |
| `alignment_status = structural_1_1_reviewed` | 141 |
| `alignment_status = needs_review` | 89 |
| `translation_validation = pending_human` | 1.505 (seluruh baris) |

Penyelarasan awal memakai LaBSE (1.446 baris) dan aturan (59 baris), lalu diaudit secara otomatis dan terarah. Audit hanya menilai batas unit dan label, bukan kesepadanan makna.

## Asal data

Korpus ini diturunkan dari sub-korpus multi-genre. Nilai `doc_id` mengikuti urutan dokumen pada versi kerja multi-genre v1.1, yaitu 99 dokumen dengan enam baris "Agenda HKBP - 1" sampai "Agenda HKBP - 6" pada `btb_multigenre.csv` digabung menjadi satu dokumen "Agenda Ibadah HKBP". Gunakan `doc_id_map.csv` untuk menelusuri judul dokumen.

Dua dokumen tidak tercakup: `doc_0009` (UMPAMA 6) dan `doc_0098` (Agenda Ibadah HKBP). Sub-korpus Alkitab tidak termasuk di sini.

## Aturan pemakaian

1. Jangan memakai baris `needs_review` untuk melatih atau menguji model.
2. Baris `candidate_1_1` dan `structural_1_1_reviewed` juga belum tervalidasi maknanya. Bila dipakai untuk eksperimen, laporkan sebagai data silver, bukan gold.
3. Jangan mengubah label `unresolved` menjadi `1-1` tanpa keputusan anotator yang tercatat.
4. Definisi setiap kolom ada pada lembar `Kamus_kolom` di buku kerja audit.

## Rencana validasi

1. Dua anotator mengisi lembar `Perlu_periksa` secara terpisah (kolom `annotator_decision`, `corrected_toba`, `corrected_indo`, `adjudication_note`).
2. Hitung IAA (misalnya Cohen's kappa) atas keputusan kedua anotator.
3. Adjudikasi ketidaksepakatan, perbarui korpus melalui `pair_id`, lalu terbitkan versi v2 dengan status validasi yang tercatat.

---

> **Status: EXPERIMENTAL, PENDING IAA.** Files in this folder are not part of the official phase 1 research deliverable and are not a gold-standard corpus. Inter-annotator agreement (IAA) has not been measured and no pair has been validated by speakers.

This folder holds a sentence or segment level Batak Toba to Indonesian parallel corpus (working version v1, 1,505 pairs from 97 of 99 multi-genre documents), together with its alignment audit workbook and a `doc_id` mapping. Initial alignment used LaBSE and rules, followed by automatic and targeted auditing of unit boundaries and labels only. Every row has `translation_validation = pending_human`; 89 rows are `needs_review` and must not be used for training or evaluation. Treat the remaining rows as silver data. `doc_id` follows the order of the 99-document multi-genre working version v1.1, in which the six "Agenda HKBP" rows of `btb_multigenre.csv` are merged into one document; see `doc_id_map.csv`. Column definitions are in the `Kamus_kolom` sheet of the audit workbook.
