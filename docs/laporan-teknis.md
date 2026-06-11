# Laporan Teknis Korpus Bahasa Batak Toba

Laporan teknis ini merupakan salah satu luaran penelitian Skema Penelitian Dosen Pemula (PDP) Universitas Pelita Harapan tahun 2025, berjudul "Digitalisasi dan Praproses Korpus Bahasa Batak Toba sebagai Fondasi Pengembangan Model Bahasa Lokal Berbasis Deep Learning". Laporan ini mendeskripsikan setiap tahap penelitian, mulai dari pengumpulan hingga penyimpanan korpus, beserta statistik dan status ketercapaian luaran.

## 1. Latar belakang

Bahasa Batak Toba adalah bahasa daerah Austronesia yang digunakan oleh lebih dari satu juta penutur di Sumatera Utara, namun perlahan tergantikan oleh Bahasa Indonesia di wilayah perkotaan dan di kalangan perantau. Bahasa ini sangat minim representasi dalam teknologi bahasa modern, khususnya pemrosesan bahasa alami (NLP). Ketiadaan korpus digital yang memadai menjadi hambatan utama bagi pengembangan alat dan model bahasa Batak Toba.

Penelitian ini menjawab kebutuhan tersebut dengan menyusun korpus teks awal Batak Toba yang terstruktur, terdokumentasi, dan dapat dikembangkan kembali, sebagai fondasi bagi penelitian NLP dan pelestarian bahasa.

## 2. Tujuan

Tujuan penelitian pada tahap ini adalah menghasilkan korpus teks awal Bahasa Batak Toba dengan minimal 100.000 token, yang berasal dari beragam jenis sumber, beserta laporan teknis yang mendokumentasikan prosesnya.

## 3. Metode

Penelitian menggunakan pendekatan pengembangan korpus (corpus building) dengan penekanan pada kurasi manual, keterlibatan penutur asli, dan dokumentasi metadata yang sistematis. Alur penelitian terdiri atas lima tahap utama.

### 3.1 Perancangan skema genre dan template data

Peneliti menyusun klasifikasi genre untuk memandu pengumpulan dokumen dan menjamin keragaman penggunaan bahasa. Korpus dibagi ke dalam lima genre: Historical/Traditional, Literary, Religious, Educational, dan Contemporary Media. Untuk konsistensi pencatatan, disiapkan sebuah template Google Sheet dengan kolom: Data Collected (Time), Title, Text in Bahasa Indonesia, Text in Batak Toba (BTB), Genre, Sub-Genre, Original Author, dan URL Link. Template ini sekaligus menjadi kerangka metadata dasar korpus.

### 3.2 Pengumpulan dan digitalisasi dokumen

Pengumpulan dilakukan melalui penelusuran manual terhadap berbagai sumber, antara lain perpustakaan digital, arsip komunitas, situs gereja, blog pribadi, Wiki, artikel berita, dan dataset terbuka berbentuk CSV. Dokumen yang relevan dikurasi dan ditetapkan genre serta sub-genrenya, lalu sumbernya dicatat melalui kolom URL Link dan Original Author. Untuk dokumen berbentuk PDF atau hasil pindai, dilakukan digitalisasi dengan Optical Character Recognition (OCR) seperti Tesseract, yang hasilnya diperiksa secara manual untuk meminimalkan kesalahan pengenalan karakter, terutama pada nama diri dan kosakata khas Batak Toba.

### 3.3 Penerjemahan dan anotasi oleh narasumber

Penelitian melibatkan dua narasumber sekaligus anotator yang merupakan penutur kompeten Bahasa Batak Toba. Tugas mereka mencakup penyalinan dokumen terkurasi ke Google Sheet sesuai genre, penerjemahan teks Batak Toba ke Bahasa Indonesia, dan penerjemahan teks Bahasa Indonesia ke Batak Toba bila relevan untuk memperkaya korpus paralel. Setiap baris data merepresentasikan satu unit dokumen atau segmen yang memuat pasangan teks beserta metadata. Peneliti memberikan panduan gaya bahasa, konsistensi istilah, dan prinsip kesepadanan terjemahan, serta melakukan pemeriksaan acak (spot-check) untuk menjaga kualitas.

### 3.4 Praproses dan analisis data eksploratif (EDA)

Praproses dilakukan dengan Python dan pustaka seperti Pandas dan Regex, meliputi:

1. Pemeriksaan kelengkapan dan konsistensi metadata, serta penyeragaman label genre dan sub-genre.
2. Pembersihan teks dan normalisasi ringan, yaitu penghapusan karakter non-teks, penyeragaman spasi dan tanda baca dasar, serta perbaikan kesalahan teknis yang jelas, dengan tetap menjaga karakteristik alami Bahasa Batak Toba.
3. Deteksi dan penghapusan duplikasi eksak agar korpus tidak bias terhadap teks tertentu.
4. Analisis eksploratif berupa statistik deskriptif, distribusi genre dan sub-genre, serta pemeriksaan variasi leksikal.

### 3.5 Penyimpanan dan dokumentasi

Seluruh data disimpan dalam struktur berkas yang terorganisir berdasarkan genre dan format. Data dapat diekspor ke format CSV dan plaintext. Skema kolom, definisi genre, dan prosedur praproses didokumentasikan agar korpus dapat digunakan dan dikembangkan kembali.

### 3.6 Perubahan dari proposal

Pada proposal, direncanakan penggunaan web crawling dan scraping berskala besar (Scrapy, BeautifulSoup, dan Twitter API). Dalam pelaksanaannya, pendekatan tersebut dipersempit menjadi penelusuran manual dan kurasi terarah dengan pelibatan narasumber. Pertimbangan utamanya adalah aspek etis, perizinan hak cipta, kualitas data, dan keterbatasan waktu. Fokus tahap ini diarahkan pada korpus awal yang relatif kecil namun bersih, teranotasi baik, dan kaya metadata.

## 4. Hasil

Penelitian menghasilkan dua sub-korpus: korpus multi-genre (`btb_multigenre`) dan korpus Alkitab paralel Batak Toba dan Bahasa Indonesia (`btb_bible`).

| Sub-korpus | Satuan | Batak Toba | Bahasa Indonesia |
|---|---|---|---|
| `btb_multigenre` | kalimat | 3.498 | 3.539 |
| `btb_multigenre` | token (perkiraan) | 67.680 | 60.866 |
| `btb_bible` | dokumen paralel | 520 | 520 |
| `btb_bible` | token (perkiraan) | 44.660 | 39.687 |
| Total | token (perkiraan) | 112.340 | 100.553 |

Sisi Batak Toba korpus mencapai lebih dari 112.000 token, melampaui target minimal 100.000 token. Rata-rata panjang kalimat berada pada kisaran 17 sampai 24 token, dengan rasio panjang Batak Toba dan Indonesia mendekati 1:1, sehingga korpus layak diperlakukan sebagai data paralel yang seimbang.

Analisis eksploratif menunjukkan bahwa fungsi gramatikal Batak Toba (misalnya na, ni, do, di, jala, tu) dan leksikon religius muncul sangat sering pada kedua sub-korpus. Hal ini menandakan dominasi domain keagamaan, namun tetap menyisakan ruang variasi leksikal dari genre lain. Pipeline pembersihan dan analisis yang terdokumentasi di Google Colab dirancang agar dapat direplikasi.

## 5. Status ketercapaian luaran

Luaran yang dijanjikan pada proposal adalah korpus mentah Batak Toba minimal 100.000 token dari minimal tiga jenis sumber (tradisional, modern, dan lisan), serta laporan teknis.

| Luaran | Status | Keterangan |
|---|---|---|
| Korpus minimal 100.000 token | Tercapai | 112.340 token pada sisi Batak Toba |
| Sumber tradisional | Tercapai | cerita rakyat, umpasa/umpama, teks historis budaya |
| Sumber modern tertulis | Tercapai | puisi kontemporer, artikel berita dan blog, materi pendidikan |
| Sumber religius | Tercapai | Alkitab Batak Toba, doa, dan teks ibadah pendek |
| Sumber lisan | Belum tercapai | direncanakan pada tahap berikutnya |
| Laporan teknis | Tercapai | dokumen ini |

## 6. Keterbatasan

1. Belum tersedia data lisan dari rekaman baru.
2. Domain keagamaan masih relatif dominan.
3. Sub-korpus Alkitab pada versi ini baru memuat satu pasal per kitab. Versi pasal penuh disiapkan sebagai pembaruan mendatang.
4. Korpus belum dilengkapi anotasi linguistik lanjutan.

## 7. Rekomendasi dan rencana lanjutan

1. Menambah sumber lisan melalui perekaman wawancara, cerita rakyat, khotbah, atau percakapan, beserta transkripsi dan terjemahannya.
2. Menyeimbangkan domain dengan menambah teks non-religius.
3. Memperkaya anotasi di atas korpus mentah, misalnya tokenisasi baku, POS tagging, anotasi morfologi, dan dependency parsing, untuk menuju sumber daya gold-standard.
4. Mengembangkan baseline pemodelan bahasa (misalnya n-gram language model dan evaluasi perplexity lintas domain) untuk mengukur kontribusi korpus multi-genre.
5. Menyiapkan versi pembaruan korpus Alkitab dengan pasal penuh.

Catatan: butir-butir pada bagian ini merupakan rencana lanjutan, bukan luaran yang dijanjikan pada tahap penelitian ini.

## 8. Daftar pustaka

Daftar pustaka berikut dikutip pada laporan akhir penelitian.

[1] P. Joshi, S. Santy, A. Budhiraja, K. Bali, dan M. Choudhury, "The State and Fate of Linguistic Diversity and Inclusion in the NLP World," Proceedings of the 58th Annual Meeting of the ACL, hlm. 6282 sampai 6293, 2020.

[2] M. A. Hedderich, L. Lange, H. Adel, J. Strotgen, dan D. Klakow, "A Survey on Recent Approaches for Natural Language Processing in Low-Resource Scenarios," Proceedings of NAACL-HLT 2021, hlm. 2545 sampai 2568, 2021.

[3] A. F. Aji dkk., "One Country, 700+ Languages: NLP Challenges for Underrepresented Languages and Dialects in Indonesia," Proceedings of the 60th Annual Meeting of the ACL, hlm. 7226 sampai 7249, 2022.

[4] G. I. Winata dkk., "NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages," Proceedings of the 17th Conference of the European Chapter of the ACL, hlm. 815 sampai 834, 2023.

[5] S. Cahyawijaya dkk., "NusaCrowd: Open Source Initiative for Indonesian NLP Resources," Findings of the Association for Computational Linguistics: ACL 2023, hlm. 13745 sampai 13818, 2023.

[6] B. Tahir, M. Azam, A. N. Mahmood, dan K. M. Malik, "Corpulyzer: A Novel Framework for Building Low Resource Language Corpora," IEEE Access, vol. 9, hlm. 17865 sampai 17880, 2021.

[7] E. M. Bender, T. Gebru, A. McMillan-Major, dan S. Shmitchell, "On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?," Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, hlm. 610 sampai 623, 2021.

[8] T. Blevins dkk., "Breaking the Curse of Multilinguality with Cross-lingual Expert Language Models," Proceedings of EMNLP 2024, hlm. 10822 sampai 10837, 2024.

[9] M. D. Al Kautsar dkk., "What Do Indonesians Really Need from Language Technology?," Proceedings of EMNLP 2025, 2025 (draf pra-cetak).

[10] S. Poria dkk., "A Survey for Low-Resourced Languages in South Asia," pra-cetak arXiv, 2025.
