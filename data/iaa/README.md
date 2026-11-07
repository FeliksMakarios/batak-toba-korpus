# data/iaa/

Hasil kesepakatan antaranotator (IAA) dan adjudikasi korpus paralel tingkat kalimat, dihasilkan oleh notebook [`alur_lengkap_korpus_batak_toba.ipynb`](../../notebooks/alur_lengkap_korpus_batak_toba.ipynb).

| Berkas | Isi | Tahap |
|---|---|---|
| `laporan_iaa.json` | Kappa skenario utama beserta interval kepercayaan 95%, kappa biner, kesepakatan per prioritas, sebaran keputusan, dan hasil pemeriksaan rekonsiliasi label | 7 |
| `sensitivitas.csv` | Kesepakatan dan kappa untuk empat skenario rekonsiliasi label | 7 |
| `matriks_konfusi.csv` | Keputusan penilai A (baris) dibandingkan dengan penilai B (kolom) | 7 |
| `keputusan_emas.csv` | Keputusan akhir dan teks final untuk 145 pasangan, beserta sumber keputusannya | 8 |
| `verifikasi_korpus_paralel.json` | Pemeriksaan bahwa korpus final identik dengan `korpus_utama_FINAL_v3`, pemetaan `doc_id`, dan pembaruan label genre | 9 |
| `statistik_korpus_paralel.json`, `statistik_per_genre_paralel.csv` | Statistik korpus paralel final | 10 |

Kedua penilai berbeda dari dua narasumber yang menerjemahkan korpus. Satu pasangan (`doc_0000_s013`) diterjemahkan ulang oleh peneliti setelah adjudikasi; perubahan ini tercatat di `keputusan_emas.csv` dengan sumber `koreksi_pasca_adjudikasi`.
