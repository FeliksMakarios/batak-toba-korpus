# Skema Kolom dan Taksonomi Genre

Dokumen ini menjelaskan struktur berkas korpus (`btb_multigenre.csv` dan `btb_bible.csv`) serta taksonomi genre yang digunakan.

## Skema kolom

Kedua berkas CSV menggunakan delapan kolom berikut.

| Kolom | Tipe | Deskripsi |
|---|---|---|
| `title` | teks | Judul atau penanda dokumen (misalnya judul cerita, nama kitab dan pasal). |
| `text_bt` | teks | Teks dalam Bahasa Batak Toba. |
| `text_id` | teks | Teks padanan dalam Bahasa Indonesia. |
| `genre` | kategori | Genre utama dokumen (lihat taksonomi di bawah). |
| `subgenre` | kategori | Sub-genre dokumen. |
| `source_link` | teks | Tautan (URL) atau penanda sumber asal teks. |
| `notes` | teks | Catatan tambahan, misalnya status terjemahan atau informasi edisi. |
| `is_parallel` | kategori | Penanda apakah baris merupakan pasangan paralel yang siap pakai (`yes` atau `no`). |

Catatan:

- Kolom `text_id` mengikuti kode bahasa ISO untuk Bahasa Indonesia (`id`), bukan singkatan dari "identifier".
- Tidak semua baris pada `btb_multigenre.csv` berlabel paralel. Sebagian baris dapat berisi teks Batak Toba saja atau masih dalam proses penerjemahan; status ini tercermin pada kolom `is_parallel` dan `notes`.
- Jumlah token dihitung dengan tokenisasi berbasis spasi dan bersifat perkiraan.

## Taksonomi genre

| Genre | Sub-genre |
|---|---|
| Historical/Traditional | manuskrip, cerita rakyat (folktales), torsa, turian |
| Literary | puisi, pantun, umpasa, umpama |
| Religious | doa Kristen, agenda ibadah HKBP (Bahasa Indonesia dan Batak Toba), Alkitab Batak Toba |
| Educational | ringkasan buku, abstrak artikel ilmiah |
| Contemporary Media | Wiki, artikel berita, artikel blog |

## Asal mula skema

Skema ini berakar dari template Google Sheet yang digunakan oleh narasumber dan anotator selama pengumpulan data, dengan kolom: Data Collected (Time), Title, Text in Bahasa Indonesia, Text in Batak Toba (BTB), Genre, Sub-Genre, Original Author, dan URL Link. Pada tahap praproses, kolom-kolom tersebut dipetakan ke skema final di atas untuk keperluan analisis dan pemodelan NLP.
