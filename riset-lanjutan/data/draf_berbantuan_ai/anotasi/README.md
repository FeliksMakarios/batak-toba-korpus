# Arsip lembar kerja revisi (stand-off), draf berbantuan AI

Isi lembar kerja revisi naskah (lembar C1 sampai C6), disimpan dengan ID butir. Teks NusaX dan NusaTranslation tidak disalin ke sini; labelnya dikaitkan lewat `uji_id` (ID posisi di riset ini, misalnya `nt-train-0123` adalah baris ke-123 berkas `nusa_kalimat-mt-btk-train.csv`) dan `id_asli` (ID resmi di rilis IndoNLP). Dibuat oleh [`../../skrip/arsip_anotasi.py`](../../skrip/arsip_anotasi.py).

| Berkas | Isi |
|---|---|
| `penilaian_korpus_kami.csv` | 410 penilaian pasangan korpus ini: 100 pasangan acak dari pasangan yang tidak pernah ditandai (C1: `accept`, `fragment_policy`, `revise_translation`) dan seluruh 310 pasangan set uji (C6: `benar`, `perbaiki_kata`, `perbaiki_makna`). Kolom `teks_*_baru` terisi bila teksnya diperbaiki |
| `penilaian_tahap2.csv` | Isian lembar tahap 2: 1.002 pasangan yang sebelumnya belum pernah diperiksa (keputusan, usulan teks, catatan). Formatnya sama dengan `penilaian_korpus_kami.csv`, lembar `T2`. Belum diterapkan ke draf korpus |
| `koreksi_korpus_kami.csv` | Koreksi akhir per pasangan, siap diterapkan ke korpus: 210 pasangan (176 uji, 33 latih, 1 validasi), dengan teks lama dan baru. Untuk butir uji, keputusan C6 berlaku |
| `putusan_am_korpus_kami.csv` | Putusan penutur atas 4 kalimat korpus ini yang memuat penanda Angkola-Mandailing (AM) |
| `label_varietas_nusatranslation_c3.csv` | Label penutur untuk 50 kalimat NusaTranslation bertanda AM (49 AM, 1 Toba) |
| `label_varietas_otomatis.csv` | Label varietas otomatis untuk seluruh 9.449 kalimat NusaTranslation dan 1.000 kalimat NusaX: `label_am32` (32 penanda naskah) dan `label_leksikon` (leksikon terverifikasi `../leksikon_am_draf.csv`: `AM` bila ada satu bentuk kuat atau dua bentuk lemah, `AM_lemah` bila hanya satu bentuk lemah). Dapat dipakai untuk menyaring subset Toba |
| `kategori_variety_esa_c2.csv` | Rincian 180 tag [VARIETY] ESA: `AM_atau_Batak_lain`, `serapan_Indonesia`, atau `keduanya`, dengan kata bermasalah. Gabungkan dengan `../../esa_anonim.csv` lewat `item_id` |
| `glos_contoh_kualitatif_c4.csv` | Glos bahasa Inggris dan catatan penutur untuk tiga contoh kualitatif di naskah |

Status: **belum terverifikasi**. Anotator menyatakan bahwa sebagian isian dibuat dengan bantuan AI, dan tidak bisa dipastikan baris mana saja. Semua isi folder ini diperlakukan sebagai usulan yang sedang diverifikasi ulang oleh penutur asli tanpa alat bantu (lihat `../README.md`).
