# Panduan Review Pasangan Kalimat untuk Anotator

Panduan ini untuk dua anotator yang mengisi `s08_review_anotator_A.xlsx` dan `s08_review_anotator_B.xlsx`, keluaran Tahap 8 notebook [`pipeline_korpus_multigenre_v2.ipynb`](../notebooks/pipeline_korpus_multigenre_v2.ipynb).

Bagian 1 sampai 9 boleh dibagikan kepada anotator. **Lampiran untuk peneliti** di akhir dokumen tidak dibagikan kepada anotator.

## 1. Tujuan

Setiap baris di lembar review berisi satu pasangan teks: satu unit Batak Toba dan padanannya dalam Bahasa Indonesia. Pasangan ini dibuat secara otomatis oleh komputer, sehingga sebagian bisa saja salah. Tugas Anda adalah menilai apakah setiap pasangan sudah benar.

Dua anotator menilai baris yang **sama persis** secara terpisah. Hasil keduanya kemudian dibandingkan untuk mengukur seberapa konsisten penilaiannya (kesepakatan antaranotator, IAA). Karena itu, **bekerjalah sendiri** dan jangan berdiskusi dengan anotator lain sampai kedua lembar selesai.

## 2. Berkas yang Anda terima

Berkas berisi 675 baris dan tiga lembar (sheet):

| Lembar | Isi |
|---|---|
| `Review` | Tempat Anda bekerja |
| `Panduan` | Ringkasan panduan ini, termasuk urutan memutuskan |
| `Info` | Versi berkas dan label anotator. Jangan diubah |

## 3. Kolom di lembar `Review`

| Kolom | Yang Anda lakukan |
|---|---|
| `nomor` | Jangan diubah |
| `pair_id` | Jangan diubah. Ini kode unik pasangan |
| `teks_bt` | Baca. Teks Batak Toba |
| `teks_id` | Baca. Teks Bahasa Indonesia |
| `keputusan` | **Wajib diisi.** Pilih satu kategori dari daftar pilihan (dropdown) |
| `koreksi_bt` | Isi hanya bila sisi Batak Toba perlu diperbaiki |
| `koreksi_id` | Isi hanya bila sisi Indonesia perlu diperbaiki |
| `catatan` | Opsional. Tulis alasan bila ragu, atau hal lain yang perlu diketahui peneliti |
| `konteks_sebelum_bt`, `konteks_sebelum_id` | Baca. Pasangan tepat sebelum baris ini di dokumen yang sama |
| `konteks_sesudah_bt`, `konteks_sesudah_id` | Baca. Pasangan tepat sesudah baris ini di dokumen yang sama |

Urutan baris sengaja diacak. Baris yang berdekatan di lembar belum tentu berasal dari dokumen yang sama. Kalau butuh konteks, gunakan kolom konteks.

## 4. Enam keputusan

| Keputusan | Kapan dipakai | Kolom koreksi |
|---|---|---|
| `terima` | Pasangan sudah benar. Batas unit tepat di kedua sisi dan maknanya sepadan | Kosongkan |
| `perbaiki_penyelarasan` | Teks kedua sisi benar, tetapi batasnya salah. Misalnya sisi Indonesia memuat sebagian kalimat yang sebenarnya milik baris sebelum atau sesudahnya, atau sebagian kalimat Toba tidak punya padanan di baris ini | Isi versi yang benar untuk sisi yang batasnya salah |
| `perbaiki_terjemahan` | Batas unit sudah benar, tetapi terjemahannya keliru, ada makna yang hilang, atau ada tambahan yang tidak ada di teks sumber | Isi terjemahan yang benar di sisi yang merupakan terjemahan |
| `fragmen` | Pasangan sepadan, tetapi unitnya bukan kalimat utuh. Contohnya judul, nama diri, nama marga, butir daftar, atau pengantar ujaran seperti "Ninna ibana:" | Kosongkan |
| `perlu_sumber` | Anda tidak bisa memutuskan tanpa melihat teks asli atau konteks yang lebih luas | Kosongkan. Jelaskan alasannya di `catatan` |
| `keluarkan` | Pasangan tidak layak masuk korpus: kedua sisi sama sekali tidak berpadanan, kedua sisi berbahasa sama padahal bukan nama diri, atau unit tidak berisi kata sama sekali (hanya nomor atau tanda baca) | Kosongkan. Jelaskan alasannya di `catatan` |

### Sisi mana yang merupakan terjemahan?

Ini penting untuk `perbaiki_terjemahan`:

- Untuk teks yang aslinya berbahasa Batak Toba (cerita rakyat, puisi, umpasa dan umpama, doa), terjemahannya ada di sisi **Indonesia**. Perbaikan ditulis di `koreksi_id`.
- Untuk teks yang aslinya berbahasa Indonesia (artikel berita, Wiki, blog, ringkasan buku, abstrak jurnal), terjemahannya ada di sisi **Batak Toba**. Perbaikan ditulis di `koreksi_bt`.

Kalau ragu sisi mana yang asli, tulis keraguan itu di `catatan`.

## 5. Urutan memutuskan

Ajukan pertanyaan berikut **secara berurutan** dan berhenti pada jawaban "ya" yang pertama.

1. Apakah kedua sisi sama sekali tidak berpadanan, berbahasa sama padahal bukan nama diri, atau tidak berisi kata sama sekali? Kalau ya, pilih **`keluarkan`**.
2. Apakah saya tidak bisa memutuskan tanpa melihat teks asli atau konteks yang lebih luas? Kalau ya, pilih **`perlu_sumber`**.
3. Apakah ada bagian kalimat yang seharusnya milik baris sebelum atau sesudahnya? Kalau ya, pilih **`perbaiki_penyelarasan`**.
4. Apakah ada makna yang hilang, berlebih, atau keliru? Kalau ya, pilih **`perbaiki_terjemahan`**.
5. Apakah unit ini bukan kalimat utuh? Kalau ya, pilih **`fragmen`**.
6. Kalau semua jawaban di atas "tidak", pilih **`terima`**.

Setiap baris hanya mendapat **satu** keputusan. Bila dua masalah muncul bersamaan, pilih yang paling atas dalam urutan ini.

## 6. Kasus khusus

| Situasi | Keputusan |
|---|---|
| Nama diri, judul, atau nama marga yang sama persis di kedua sisi (misalnya "Ugamo Malim" dan "Ugamo Malim") | `fragmen`, bukan `keluarkan` |
| Unit hanya berisi nomor butir atau tanda baca (misalnya "1." dan "1.") | `keluarkan` |
| Beberapa baris puisi atau umpasa digabung menjadi satu unit, tetapi maknanya lengkap dan sepadan | `terima` |
| Terjemahan bebas atau berbeda gaya, tetapi maknanya sepadan | `terima`. Perbedaan gaya bukan alasan untuk memperbaiki |
| Variasi ejaan Batak Toba yang lazim (misalnya "ndang" dan "dang") | `terima` |
| Salah ketik yang tidak mengubah makna, misalnya dua kata menempel ("ibanamangoli") | Putuskan berdasarkan padanan maknanya, lalu tulis salah ketik itu di `catatan` |
| Salah satu sisi hanya berisi sebagian kalimat dan sisanya ada di baris konteks | `perbaiki_penyelarasan` |
| Pasangan yang sama persis muncul lebih dari sekali di lembar | Nilai setiap baris seperti biasa |

## 7. Cara mengisi kolom koreksi

1. Tulis **versi lengkap yang benar** untuk sisi yang diperbaiki, bukan hanya kata yang diubah.
2. Isi hanya sisi yang memang perlu diperbaiki. Sisi yang sudah benar dibiarkan kosong.
3. Untuk `perbaiki_penyelarasan`, tulis unit dengan batas yang benar. Bagian yang seharusnya pindah ke baris lain cukup dijelaskan di `catatan`, misalnya "kalimat terakhir sisi Indonesia milik baris sesudahnya". Peneliti akan merapikannya saat adjudikasi.

## 8. Hal yang tidak boleh dilakukan

1. Menghapus, menambah, atau mengurutkan ulang baris.
2. Mengubah isi kolom `nomor`, `pair_id`, `teks_bt`, `teks_id`, atau kolom konteks.
3. Mengetik keputusan di luar daftar pilihan.
4. Melihat atau mendiskusikan lembar anotator lain sebelum kedua lembar selesai.
5. Menggunakan mesin penerjemah untuk memutuskan.

## 9. Setelah selesai

1. Pastikan kolom `keputusan` terisi di semua baris.
2. Simpan berkas dalam format `.xlsx` dengan nama `review_anotator_A.xlsx` atau `review_anotator_B.xlsx`, sesuai label Anda di lembar `Info`.
3. Kirim berkas kepada peneliti.

Perkiraan waktu: bila satu baris rata-rata memakan satu menit, 675 baris membutuhkan sekitar 11 jam kerja. Bagilah dalam beberapa sesi dan simpan berkas secara berkala.

---

## Lampiran untuk peneliti (tidak dibagikan kepada anotator)

### Mengapa tanda audit disembunyikan

Lembar anotator sengaja tidak memuat `status_penyelarasan`, `prioritas_review`, `flag_audit`, maupun skor LaBSE. Bila anotator melihat bahwa mesin sudah menandai sebuah pasangan bermasalah, penilaian mereka cenderung mengikuti tanda itu, sehingga IAA tidak lagi mengukur penilaian manusia yang independen. Kunci yang menghubungkan setiap baris dengan tandanya ada di `s08_kunci_sampel.csv` dan dipakai di Tahap 9.

### Desain sampel review

Dari korpus utama (1.562 pasangan pada eksekusi Colab dengan LaBSE), lembar review memuat:

| Strata | Jumlah | Dasar pemilihan |
|---|---|---|
| Prioritas tinggi | 132 | Semua pasangan berprioritas tinggi |
| Prioritas sedang | 443 | Semua pasangan berprioritas sedang |
| Rutin | 100 | Sampel acak dari 987 pasangan rutin (10%, minimal 100, seed 42) |

Sampel rutin diperlukan agar kualitas pasangan yang lolos audit otomatis juga teruji.

### Status, prioritas, dan validasi

| Kolom | Nilai | Arti |
|---|---|---|
| `status_penyelarasan` | `perlu_review` | Pasangan berprioritas tinggi. Jangan dipakai untuk melatih atau menguji model sebelum diperiksa manusia |
| `status_penyelarasan` | `kandidat` | Lolos dari tanda prioritas tinggi, tetapi belum divalidasi manusia |
| `prioritas_review` | `tinggi` | Memiliki minimal satu tanda prioritas tinggi |
| `prioritas_review` | `sedang` | Memiliki minimal satu tanda lain |
| `prioritas_review` | `rutin` | Tidak memiliki tanda apa pun |
| `validasi_terjemahan` | `menunggu_manusia` | Berlaku untuk semua pasangan sampai adjudikasi selesai |

### Tanda audit (`flag_audit`)

| Tanda | Arti | Prioritas |
|---|---|---|
| `tipe_bukan_1_1` | Blok menggabungkan lebih dari satu kalimat di salah satu sisi (misalnya 2-1 atau 1-3) | tinggi |
| `sisi_identik` | Teks Toba dan Indonesia sama persis setelah dinormalisasi dan lebih dari 3 token, kemungkinan bukan terjemahan | tinggi |
| `rasio_karakter_ekstrem` | Rasio panjang karakter Toba terhadap Indonesia di luar rentang 0,4 sampai 2,5 | tinggi |
| `identik_pendek` | Sama persis tetapi maksimal 3 token, biasanya nama diri atau judul | sedang |
| `tanpa_huruf` | Salah satu sisi hanya berisi angka atau tanda baca | sedang |
| `rasio_token_ekstrem` | Jumlah token satu sisi minimal dua kali sisi lainnya | sedang |
| `unit_panjang` | Salah satu sisi lebih dari 45 token, sehingga batas kalimat mungkin terlewat | sedang |
| `sim_rendah` | Skor kemiripan LaBSE di bawah 0,2. LaBSE tidak dilatih khusus dengan Batak Toba, sehingga tanda ini paling tidak andal dan menjadi penyumbang terbesar prioritas sedang (293 pasangan) | sedang |
| `duplikat_persis` | Pasangan yang sama persis muncul lebih dari sekali | sedang |
| `tanya_tidak_cocok` | Hanya satu sisi yang diakhiri tanda tanya | sedang |
| `bersebelahan_tanpa_pasangan` | Bertetangga dengan kalimat yang tidak mendapat pasangan, sehingga batasnya mungkin bergeser | sedang |
| `fragmen` | Unit sangat pendek tanpa tanda baca akhir, atau seluruhnya huruf kapital | sedang |

### Metode dan tipe blok

| Kolom | Nilai | Arti |
|---|---|---|
| `metode` | `rule` | Pasangan 1:1 berdasarkan urutan, untuk doa dan umpama yang jumlah kalimatnya sama di kedua sisi |
| `metode` | `labse_alih` | Seharusnya `rule`, tetapi jumlah kalimatnya berbeda sehingga dialihkan ke LaBSE |
| `metode` | `labse` | Penyelarasan dengan LaBSE dan pemrograman dinamis |
| `tipe` | `1-1`, `2-1`, `1-3`, dan seterusnya | Jumlah kalimat Toba dan Indonesia yang digabung dalam satu blok |

### Catatan metodologis: penilai IAA berbeda dari penerjemah

Review untuk IAA dikerjakan oleh dua anotator yang **berbeda** dari dua narasumber yang menyalin dan menerjemahkan korpus. Dengan begitu, tidak ada penilai yang menilai terjemahannya sendiri, dan kesepakatan yang terukur mencerminkan penilaian independen terhadap kualitas pasangan. Hal ini layak disebutkan di bagian metodologi paper.
