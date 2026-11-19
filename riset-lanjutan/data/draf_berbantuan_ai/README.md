# Draf berbantuan AI (belum terverifikasi)

Folder ini memuat hasil lembar kerja revisi naskah (C1 sampai C6) dan turunannya. Setelah hasil tahap 2 masuk, ditemukan tanda bahwa lembar-lembar itu diisi jauh lebih cepat daripada kerja manual yang wajar, dan sebagian berkasnya terakhir disimpan oleh program. Anotator kemudian menyatakan bahwa **sebagian isian dibuat dengan bantuan AI**. Karena tidak bisa dipastikan baris mana saja, seluruh isi folder ini diperlakukan sebagai **usulan**, bukan penilaian penutur asli.

| Berkas | Isi | Asal |
|---|---|---|
| `set_uji_kami_koreksi_draf.csv` | Set uji `kami` dengan rujukan lama dan usulan koreksi (172 rujukan Toba, 4 rujukan Indonesia) | C6 |
| `btb_parallel_sentence_v1.1_draf.csv` | Draf korpus versi 1.1: versi 1.0 ditambah usulan koreksi C1 dan C6 (210 pasangan) | C1, C6 |
| `leksikon_am_draf.csv` | 153 bentuk kandidat penanda Angkola-Mandailing dengan kategori dan padanan Toba | C5 |
| `anotasi/` | Arsip stand-off lembar C1 sampai C6 | C1 sampai C6 |

Rencana verifikasi: setiap usulan diperiksa ulang oleh penutur asli tanpa alat bantu, dengan pilihan memakai teks lama, memakai usulan, atau menulis sendiri. Versi usulan dan versi lama ditampilkan dalam urutan acak tanpa label, sehingga penutur tidak tahu mana yang berasal dari usulan. Sebagian butir juga akan diperiksa secara buta oleh penutur kedua. Setelah verifikasi, berkas yang lolos dipindah keluar dari folder ini dengan nama baru.

Versi resmi korpus tetap 1.0 (`../../../data/btb_parallel_sentence.csv`). Angka di `../../hasil/v3/*_terkoreksi.csv` dan `../../hasil/tabel/c6_*.csv` memakai rujukan draf ini dan hanya bersifat sementara.

---

**English summary.** This folder holds the outputs of the revision worksheets (C1 to C6) and derived files. The annotator stated that part of the entries were produced with AI assistance, and the affected rows cannot be identified. All files here are therefore treated as unverified suggestions, pending blind re-verification by a native speaker without AI tools. The official corpus remains version 1.0.
