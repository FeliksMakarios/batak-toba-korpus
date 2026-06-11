# Pernyataan Data

Dokumen ini menjelaskan asal usul, status lisensi, pertimbangan etika, dan tujuan penggunaan korpus Bahasa Batak Toba. Tujuannya adalah menjamin transparansi dan penggunaan kembali yang bertanggung jawab.

## Komposisi korpus

Korpus terdiri atas dua sub-korpus:

1. `btb_multigenre`: teks multi-genre yang dikurasi manual dari berbagai sumber daring.
2. `btb_bible`: teks paralel Alkitab Batak Toba dan Bahasa Indonesia.

## Asal data dan lisensi per sumber

### Sub-korpus Alkitab

Teks Alkitab berasal dari repositori `erwindosianipar/beeble` dan memuat terjemahan Batak Toba tahun 1894. Terjemahan ini terbit lebih dari 130 tahun lalu dan karena usianya berada dalam domain publik. Meskipun demikian, repositori sumber tetap dikreditkan sebagai bentuk penghargaan.

Pada versi ini, sub-korpus Alkitab baru memuat satu pasal per kitab, bukan seluruh pasal. Cakupan parsial ini disebabkan keterbatasan teknis pada saat pengumpulan. Versi dengan pasal penuh disiapkan sebagai pembaruan terpisah pada rilis mendatang.

### Sub-korpus multi-genre

Teks multi-genre berasal dari beragam sumber daring yang dicatat per baris pada kolom `source_link` dan `notes`. Karena sebagian teks bersumber dari materi daring yang dapat memiliki pemilik hak cipta, pengguna disarankan memeriksa kembali status hak masing-masing sumber sebelum penggunaan komersial atau redistribusi dalam skala besar. Bila ditemukan materi yang seharusnya tidak disertakan, materi tersebut akan dihapus atas permintaan yang wajar.

## Lisensi rilis

Data korpus dirilis di bawah Creative Commons Attribution 4.0 International (CC BY 4.0), dengan tetap menghormati hak pemilik sumber asli sebagaimana dicatat pada kolom sumber. Skrip dan notebook dirilis di bawah lisensi MIT.

## Pertimbangan etika

Pengumpulan data melibatkan dua narasumber penutur Bahasa Batak Toba yang berkontribusi dalam penyalinan dan penerjemahan teks. Keterlibatan penutur asli ditujukan untuk menjaga keberterimaan dan validitas linguistik korpus. Penelitian menghindari pengumpulan data pribadi yang sensitif, dan teks yang dihimpun berasal dari materi yang tersedia untuk publik.

## Tujuan penggunaan yang dimaksudkan

Korpus ini ditujukan untuk penelitian NLP bahasa sumber rendah, kajian linguistik korpus, dan upaya pelestarian Bahasa Batak Toba. Korpus ini merupakan sumber daya tahap awal dan belum dilengkapi anotasi linguistik lanjutan.

## Keterbatasan yang perlu diketahui pengguna

1. Domain keagamaan relatif dominan, sehingga distribusi leksikal dapat condong ke kosakata religius.
2. Tokenisasi yang digunakan berbasis spasi dan jumlah token bersifat perkiraan.
3. Belum tersedia data lisan.
4. Sub-korpus Alkitab baru mencakup satu pasal per kitab.

## Permintaan koreksi

Permintaan koreksi, penghapusan sumber, atau pertanyaan terkait hak cipta dapat disampaikan kepada penyusun korpus melalui kontak yang tercantum pada README.
