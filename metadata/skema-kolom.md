# Skema Kolom dan Taksonomi Genre

Dokumen ini menjelaskan struktur berkas korpus (`btb_multigenre.csv` dan `btb_bible.csv`) serta taksonomi genre yang digunakan.

## Skema kolom

| Kolom | Tipe | Deskripsi |
|---|---|---|
| `doc_id` | teks | Identitas dokumen yang tetap, berformat `mg_001` sampai `mg_104` sesuai urutan baris pada berkas anotator. Hanya ada di `btb_multigenre.csv` dan dipakai juga di `pair_id` korpus paralel. |
| `title` | teks | Judul atau penanda dokumen (misalnya judul cerita, nama kitab dan pasal). |
| `text_bt` | teks | Teks dalam Bahasa Batak Toba. |
| `text_id` | teks | Teks padanan dalam Bahasa Indonesia. |
| `genre` | kategori | Genre utama dokumen (lihat taksonomi di bawah). |
| `subgenre` | kategori | Sub-genre dokumen. |
| `source_link` | teks | Tautan (URL) atau penanda sumber asal teks. |
| `notes` | teks | Catatan tambahan dari anotator. |
| `is_parallel` | kategori | Penanda apakah baris memuat teks di kedua bahasa (`yes` atau `no`). |

Catatan:

- Kolom `text_id` mengikuti kode bahasa ISO untuk Bahasa Indonesia (`id`), bukan singkatan dari "identifier".
- Teks pada berkas rilis hanya dirapikan secara teknis (normalisasi Unicode NFC, akhir baris, spasi berlebih, karakter tak terlihat). Ejaan, kapitalisasi, dan tanda baca tidak diubah.
- Jumlah token dilaporkan dengan tiga metode yang dinyatakan eksplisit, yaitu kata tanpa tanda baca, token berbasis spasi, dan token NLTK yang menghitung tanda baca. Lihat README untuk angkanya.

## Taksonomi genre

Tabel berikut memuat sub-genre yang benar-benar ada di `btb_multigenre.csv` beserta jumlah dokumennya.

| Genre | Sub-genre | Dokumen |
|---|---|---|
| Historical/Traditional | Folktales (cerita rakyat) | 2 |
| Literary | Peribahasa/Umpama | 46 |
| Literary | Poems (puisi) | 7 |
| Religious | Prayers (doa Kristen) | 3 |
| Religious | Ritual Text (Agenda HKBP, enam bagian) | 6 |
| Educational | Book Summary (ringkasan dan ulasan buku) | 8 |
| Educational | Abstract (abstrak artikel jurnal) | 9 |
| Contemporary Media | Wiki | 7 |
| Contemporary Media | News Article (artikel berita) | 9 |
| Contemporary Media | Blog Articles (artikel blog) | 7 |

Sub-korpus Alkitab (`btb_bible.csv`) memakai genre `Religious` dengan sub-genre `scripture`.

## Asal mula skema

Skema ini berakar dari template Google Sheet yang digunakan oleh narasumber dan anotator selama pengumpulan data, dengan kolom: Column 1, Date Collected, Title, Text in Toba, Text in Bahasa Indonesia, Genre Category, Sub-Genre Category, Original Author (Publisher or Person), Source Link, dan Additional Notes (optional). Pemetaan ke skema di atas, beserta seluruh koreksi label dan metadata, dilakukan oleh notebook [`../notebooks/pipeline_korpus_multigenre_v2.ipynb`](../notebooks/pipeline_korpus_multigenre_v2.ipynb) dan tercatat di log koreksinya.
