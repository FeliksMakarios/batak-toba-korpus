# Korpus Bahasa Batak Toba

Korpus teks awal Bahasa Batak Toba (bbc) dan Bahasa Indonesia (ind), hasil penelitian Skema Penelitian Dosen Pemula (PDP) di Universitas Pelita Harapan, tahun 2025.

An initial Batak Toba (bbc) and Indonesian (ind) text corpus, produced under the Beginning Lecturer Research Scheme (PDP) at Universitas Pelita Harapan, 2025.

Pilih bahasa / Choose a language: [Bahasa Indonesia](#bahasa-indonesia) | [English](#english)

---

## Bahasa Indonesia

### Tentang

Repositori ini memuat korpus teks awal Bahasa Batak Toba beserta padanannya dalam Bahasa Indonesia, yang disusun sebagai luaran penelitian berjudul "Digitalisasi dan Praproses Korpus Bahasa Batak Toba sebagai Fondasi Pengembangan Model Bahasa Lokal Berbasis Deep Learning".

Bahasa Batak Toba adalah bahasa daerah Austronesia dengan lebih dari satu juta penutur di Sumatera Utara, namun nyaris tidak memiliki sumber daya digital untuk pemrosesan bahasa alami (NLP). Korpus ini disusun untuk menjadi fondasi awal bagi penelitian NLP dan pelestarian bahasa Batak Toba.

Korpus terdiri atas dua sub-korpus:

1. `btb_multigenre`: korpus multi-genre yang dikurasi secara manual dari berbagai sumber daring.
2. `btb_bible`: korpus paralel Alkitab Batak Toba dan terjemahannya dalam Bahasa Indonesia.

### Isi korpus

Statistik diperoleh dari tahap analisis data eksploratif (EDA). Jumlah token bersifat perkiraan dan dihitung dengan tokenisasi berbasis spasi.

| Sub-korpus | Satuan | Batak Toba | Bahasa Indonesia |
|---|---|---|---|
| `btb_multigenre` | kalimat | 3.498 | 3.539 |
| `btb_multigenre` | token (perkiraan) | 67.680 | 60.866 |
| `btb_bible` | dokumen paralel | 520 | 520 |
| `btb_bible` | token (perkiraan) | 44.660 | 39.687 |
| Total | token (perkiraan) | 112.340 | 100.553 |

Sisi Batak Toba melampaui 112.000 token, memenuhi target minimal 100.000 token yang ditetapkan dalam proposal. Rata-rata panjang kalimat berada pada kisaran 17 sampai 24 token, dengan rasio panjang Batak Toba dan Indonesia yang mendekati 1:1.

Korpus mencakup lima genre:

| Genre | Sub-genre |
|---|---|
| Historical/Traditional | manuskrip, cerita rakyat (folktales), torsa, turian |
| Literary | puisi, pantun, umpasa, umpama |
| Religious | doa Kristen, agenda ibadah HKBP (Indonesia dan Batak Toba), Alkitab Batak Toba |
| Educational | ringkasan buku, abstrak artikel ilmiah |
| Contemporary Media | Wiki, artikel berita, artikel blog |

Domain keagamaan masih relatif dominan pada versi awal ini. Penyeimbangan domain dan penambahan data lisan menjadi bagian dari rencana lanjutan.

### Struktur repositori

```
batak-toba-korpus/
├── README.md              Dokumen ini (dwibahasa)
├── LICENSE                Lisensi data (CC BY 4.0)
├── LICENSE-CODE           Lisensi skrip dan notebook (MIT)
├── CITATION.cff           Informasi sitasi
├── .gitignore
├── data/                  Berkas korpus (CSV)
│   └── README.md
├── notebooks/             Notebook pipeline (Google Colab)
│   └── README.md
├── metadata/
│   └── skema-kolom.md     Definisi kolom dan taksonomi genre
└── docs/
    ├── laporan-teknis.md  Laporan teknis (luaran penelitian)
    ├── pengumpulan-data.md  Metode pengumpulan dan kurasi data
    └── pernyataan-data.md   Pernyataan asal, lisensi, dan etika data
```

### Skema data

Kedua berkas CSV menggunakan skema kolom yang sama: `title`, `text_bt`, `text_id`, `genre`, `subgenre`, `source_link`, `notes`, `is_parallel`. Penjelasan lengkap setiap kolom dan taksonomi genre tersedia pada [metadata/skema-kolom.md](metadata/skema-kolom.md).

### Cara menggunakan

```python
import pandas as pd

multigenre = pd.read_csv("data/btb_multigenre.csv")
bible = pd.read_csv("data/btb_bible.csv")

# Mengambil hanya pasangan yang berlabel paralel
pasangan_paralel = multigenre[multigenre["is_parallel"] == "yes"]
```

### Status luaran penelitian

| Luaran yang dijanjikan | Status |
|---|---|
| Korpus dengan minimal 100.000 token Batak Toba | Tercapai (112.340 token) |
| Cakupan sumber tradisional | Tercapai |
| Cakupan sumber modern tertulis | Tercapai |
| Cakupan sumber religius | Tercapai |
| Cakupan sumber lisan | Belum tercapai, menjadi rencana lanjutan |
| Laporan teknis | Tercapai ([docs/laporan-teknis.md](docs/laporan-teknis.md)) |

### Keterbatasan dan rencana lanjutan

Versi awal ini memiliki beberapa keterbatasan yang disengaja dicatat secara terbuka:

1. Domain keagamaan masih dominan. Penambahan teks non-religius akan dilakukan untuk menyeimbangkan domain.
2. Sub-korpus Alkitab pada versi ini baru memuat satu pasal per kitab. Versi pasal penuh disiapkan sebagai pembaruan mendatang.
3. Korpus belum dilengkapi anotasi linguistik lanjutan (tokenisasi baku, POS tagging, morfologi, dependency parsing). Pengayaan anotasi direncanakan untuk menjadikannya sumber daya gold-standard. Penelitian berikutnya akan berfokus pada pedoman anotasi awal dengan Universal Dependencies versi 2.

### Lisensi

Data korpus berada di bawah lisensi Creative Commons Attribution 4.0 International (CC BY 4.0). Skrip dan notebook berada di bawah lisensi MIT. Lihat [LICENSE](LICENSE) dan [LICENSE-CODE](LICENSE-CODE).

### Cara mensitasi

Lihat berkas [CITATION.cff](CITATION.cff). Sitasi singkat:

> Samosir, F. V. P. (2025). Korpus Bahasa Batak Toba. Universitas Pelita Harapan. https://github.com/FeliksMakarios/batak-toba-korpus

### Penghargaan

Terima kasih kepada dua narasumber sekaligus anotator penutur Bahasa Batak Toba yang berkontribusi dalam pengumpulan dan penerjemahan teks. Penelitian ini didanai melalui Skema Penelitian Dosen Pemula Universitas Pelita Harapan.

Teks Alkitab bersumber dari repositori `erwindosianipar/beeble` (terjemahan tahun 1894). Sumber teks multi-genre lainnya dicatat pada kolom `source_link` di setiap baris data.

### Kontak

Feliks Victor Parningotan Samosir, Program Studi Informatika, Fakultas AI and Data Science, Universitas Pelita Harapan.

---

## English

### About

This repository contains an initial Batak Toba text corpus together with its Indonesian translation, produced as a research deliverable titled "Digitalisation and Preprocessing of a Batak Toba Language Corpus as a Foundation for Deep Learning Based Local Language Models".

Batak Toba is an Austronesian regional language with more than one million speakers in North Sumatra, yet it has almost no digital resources for natural language processing (NLP). This corpus is intended as an early foundation for Batak Toba NLP research and language preservation.

The corpus consists of two sub-corpora:

1. `btb_multigenre`: a multi-genre corpus manually curated from various online sources.
2. `btb_bible`: a parallel corpus of the Batak Toba Bible and its Indonesian translation.

### Corpus contents

Statistics were obtained during exploratory data analysis (EDA). Token counts are approximate and based on whitespace tokenisation.

| Sub-corpus | Unit | Batak Toba | Indonesian |
|---|---|---|---|
| `btb_multigenre` | sentences | 3,498 | 3,539 |
| `btb_multigenre` | tokens (approx.) | 67,680 | 60,866 |
| `btb_bible` | parallel documents | 520 | 520 |
| `btb_bible` | tokens (approx.) | 44,660 | 39,687 |
| Total | tokens (approx.) | 112,340 | 100,553 |

The Batak Toba side exceeds 112,000 tokens, meeting the minimum target of 100,000 tokens set in the proposal. Average sentence length ranges from 17 to 24 tokens, with a Batak Toba to Indonesian length ratio close to 1:1.

The corpus spans five genres:

| Genre | Sub-genres |
|---|---|
| Historical/Traditional | manuscripts, folktales, torsa, turian |
| Literary | poetry, pantun, umpasa, umpama |
| Religious | Christian prayers, HKBP liturgical agenda (Indonesian and Batak Toba), Batak Toba Bible |
| Educational | book summaries, academic article abstracts |
| Contemporary Media | Wiki, news articles, blog articles |

The religious domain remains relatively dominant in this initial version. Domain balancing and the addition of spoken data are part of the planned follow-up work.

### Repository structure

```
batak-toba-korpus/
├── README.md              This document (bilingual)
├── LICENSE                Data license (CC BY 4.0)
├── LICENSE-CODE           Script and notebook license (MIT)
├── CITATION.cff           Citation metadata
├── .gitignore
├── data/                  Corpus files (CSV)
│   └── README.md
├── notebooks/             Pipeline notebooks (Google Colab)
│   └── README.md
├── metadata/
│   └── skema-kolom.md     Column definitions and genre taxonomy
└── docs/
    ├── laporan-teknis.md  Technical report (research deliverable)
    ├── pengumpulan-data.md  Data collection and curation method
    └── pernyataan-data.md   Data provenance, license, and ethics statement
```

### Data schema

Both CSV files share the same column schema: `title`, `text_bt`, `text_id`, `genre`, `subgenre`, `source_link`, `notes`, `is_parallel`. A full description of each column and the genre taxonomy is available in [metadata/skema-kolom.md](metadata/skema-kolom.md).

### How to use

```python
import pandas as pd

multigenre = pd.read_csv("data/btb_multigenre.csv")
bible = pd.read_csv("data/btb_bible.csv")

# Keep only rows marked as parallel pairs
parallel_pairs = multigenre[multigenre["is_parallel"] == "yes"]
```

### Research deliverable status

| Promised deliverable | Status |
|---|---|
| Corpus with at least 100,000 Batak Toba tokens | Achieved (112,340 tokens) |
| Coverage of traditional sources | Achieved |
| Coverage of modern written sources | Achieved |
| Coverage of religious sources | Achieved |
| Coverage of spoken sources | Not yet achieved, planned as follow-up |
| Technical report | Achieved ([docs/laporan-teknis.md](docs/laporan-teknis.md)) |

### Limitations and future work

This initial version has several limitations that are recorded openly:

1. The religious domain is still dominant. Non-religious texts will be added to balance the domains.
2. The Bible sub-corpus in this version contains only one chapter per book. A full-chapter version is being prepared as a future update.
3. The corpus is not yet enriched with advanced linguistic annotation (standardised tokenisation, POS tagging, morphology, dependency parsing). Annotation enrichment is planned to develop it into a gold-standard resource. The next research will focus on the initial annotation guidelines with Universal Dependencies version 2.

### License

The corpus data is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0). Scripts and notebooks are released under the MIT License. See [LICENSE](LICENSE) and [LICENSE-CODE](LICENSE-CODE).

### How to cite

See [CITATION.cff](CITATION.cff). Short citation:

> Samosir, F. V. P. (2025). Batak Toba Language Corpus. Universitas Pelita Harapan. https://github.com/FeliksMakarios/batak-toba-korpus

### Acknowledgments

Thanks to the two Batak Toba speaking informants and annotators who contributed to text collection and translation. This research was funded through the Beginning Lecturer Research Scheme of Universitas Pelita Harapan.

The Bible text is sourced from the `erwindosianipar/beeble` repository (1894 translation). Other multi-genre source texts are recorded in the `source_link` column of each data row.

### Contact

Feliks Victor Parningotan Samosir, Informatics Study Program, Faculty of AI and Data Science, Universitas Pelita Harapan.
