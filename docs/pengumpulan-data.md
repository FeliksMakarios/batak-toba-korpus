# Metode Pengumpulan dan Kurasi Data

Dokumen ini merinci alur kerja pengumpulan data korpus Bahasa Batak Toba, dari penentuan sumber hingga pemeriksaan kualitas. Penjelasan metode yang lebih ringkas tersedia pada [laporan-teknis.md](laporan-teknis.md).

## Prinsip umum

Pengumpulan data menekankan tiga prinsip: kurasi manual, keterlibatan penutur asli, dan dokumentasi metadata yang konsisten. Pendekatan ini dipilih agar korpus awal yang dihasilkan bersih, teranotasi baik, dan kaya metadata, meskipun berukuran relatif kecil.

## Sumber data

Dokumen dikumpulkan dari beragam sumber daring, antara lain perpustakaan digital, arsip komunitas, situs gereja, blog pribadi, Wiki, artikel berita, dan dataset terbuka berbentuk CSV. Setiap teks dicatat sumbernya pada kolom `source_link` dan `notes`.

Teks Alkitab bersumber dari repositori `erwindosianipar/beeble`, memuat terjemahan Batak Toba tahun 1894 beserta padanannya dalam Bahasa Indonesia. Detail status lisensi sumber dijelaskan pada [pernyataan-data.md](pernyataan-data.md).

## Klasifikasi genre

Sebelum pengumpulan, peneliti menyusun taksonomi genre untuk menjaga keragaman bahasa. Lima genre dan sub-genrenya didokumentasikan pada [../metadata/skema-kolom.md](../metadata/skema-kolom.md).

## Template pencatatan

Seluruh narasumber dan anotator menggunakan satu template Google Sheet dengan kolom: Data Collected (Time), Title, Text in Bahasa Indonesia, Text in Batak Toba (BTB), Genre, Sub-Genre, Original Author, dan URL Link. Template ini menjaga konsistensi pencatatan sekaligus menjadi kerangka metadata.

## Digitalisasi dokumen

Untuk dokumen berbentuk PDF atau hasil pindai, teks dikonversi menggunakan Optical Character Recognition (OCR) seperti Tesseract. Hasil OCR diperiksa secara manual untuk mengurangi kesalahan pengenalan karakter, terutama pada nama diri, istilah khusus, dan kosakata Batak Toba.

## Penerjemahan oleh narasumber

Dua narasumber penutur kompeten Bahasa Batak Toba bertugas menyalin dokumen terkurasi, menerjemahkan teks Batak Toba ke Bahasa Indonesia, dan menerjemahkan teks Bahasa Indonesia ke Batak Toba bila relevan. Peneliti memberikan panduan gaya bahasa, konsistensi istilah, dan prinsip kesepadanan terjemahan agar hasil tetap alami namun setia pada teks sumber.

## Pemeriksaan kualitas

Kualitas dijaga melalui pemeriksaan acak (spot-check) terhadap sejumlah entri, dengan membandingkan teks sumber dan terjemahan serta mengklarifikasi bagian yang meragukan bersama narasumber.

## Perubahan dari rencana awal

Rencana awal pada proposal menggunakan web crawling dan scraping berskala besar (Scrapy, BeautifulSoup, dan Twitter API). Dalam pelaksanaan, pendekatan dipersempit menjadi penelusuran manual dan kurasi terarah karena pertimbangan etis, perizinan hak cipta, kualitas data, dan keterbatasan waktu. Implikasinya, korpus tahap ini berukuran lebih kecil tetapi lebih terkurasi dan terdokumentasi.
