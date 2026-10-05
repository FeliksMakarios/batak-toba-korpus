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

Angka sub-korpus multi-genre dihasilkan oleh notebook [pipeline v2](notebooks/pipeline_korpus_multigenre_v2.ipynb). Angka sub-korpus Alkitab dihitung dengan fungsi yang sama. Karena hasil hitungan bergantung pada perlakuan terhadap tanda baca, jumlah token dilaporkan dengan tiga metode:

- **Kata**: hanya urutan huruf atau angka. Tanda baca tidak dihitung.
- **Token berbasis spasi**: teks dipisah pada spasi. Tanda baca ikut menempel pada kata.
- **Token NLTK**: teks dijadikan huruf kecil, lalu dipecah dengan NLTK `word_tokenize`. Tanda baca dihitung sebagai token tersendiri. Ini metode yang dipakai pada analisis versi awal.

| Sub-korpus | Satuan | Batak Toba | Bahasa Indonesia |
|---|---|---|---|
| `btb_multigenre` | dokumen | 104 | 104 |
| `btb_multigenre` | kalimat atau baris | 4.429 | 4.447 |
| `btb_multigenre` | kata | 59.443 | 53.166 |
| `btb_multigenre` | token NLTK | 67.680 | 60.866 |
| `btb_bible` | pasal (ayat) | 66 (1.594) | 66 (1.594) |
| `btb_bible` | kata | 38.509 | 34.320 |
| `btb_bible` | token NLTK | 44.785 | 39.687 |
| Total | kata | 97.952 | 87.486 |
| Total | token berbasis spasi | 98.235 | 85.990 |
| Total | token NLTK | 112.465 | 100.553 |

Target proposal, yaitu minimal 100.000 token pada sisi Batak Toba, tercapai bila tanda baca dihitung sebagai token (112.465 token NLTK). Bila hanya kata yang dihitung, sisi Batak Toba berjumlah 97.952 kata, sekitar 2% di bawah target. Kedua angka dicantumkan agar pembaca dapat menilai sendiri.

Catatan perubahan angka: versi awal README mencantumkan 520 dokumen paralel untuk sub-korpus Alkitab. Angka itu berasal dari pengelompokan yang keliru pada notebook EDA lama. Jumlah sebenarnya adalah 66 pasal (1.594 ayat). Jumlah kalimat multi-genre kini dihitung dengan segmentasi pipeline v2, yang juga memecah per baris untuk puisi dan liturgi, sehingga berbeda dari angka 3.498 kalimat pada versi awal.

Sebaran genre dan sub-genre:

| Genre | Sub-genre | Dokumen | Kata Batak Toba |
|---|---|---|---|
| Historical/Traditional | Folktales | 2 | 1.796 |
| Literary | Peribahasa/Umpama | 46 | 356 |
| Literary | Poems | 7 | 741 |
| Religious | Prayers | 3 | 210 |
| Religious | Ritual Text (Agenda HKBP) | 6 | 35.097 |
| Religious | Alkitab (`btb_bible`) | 66 pasal | 38.509 |
| Educational | Book Summary | 8 | 4.120 |
| Educational | Abstract | 9 | 1.915 |
| Contemporary Media | Wiki | 7 | 6.246 |
| Contemporary Media | News Article | 9 | 3.884 |
| Contemporary Media | Blog Articles | 7 | 5.078 |

Domain keagamaan sangat dominan. Agenda HKBP, doa, dan Alkitab mencakup sekitar 75% kata Batak Toba, dan Agenda HKBP saja mencakup 59% sub-korpus multi-genre. Penyeimbangan domain menjadi bagian dari rencana lanjutan.

### Struktur repositori

```
batak-toba-korpus/
├── README.md              Dokumen ini (dwibahasa)
├── LICENSE                Lisensi data (CC BY 4.0)
├── LICENSE-CODE           Lisensi skrip dan notebook (MIT)
├── CITATION.cff           Informasi sitasi
├── .gitignore
├── data/                  Berkas korpus (CSV)
│   ├── README.md
│   ├── btb_multigenre.csv Korpus multi-genre versi 2
│   └── experimental/      Korpus paralel tingkat kalimat (pending IAA)
├── notebooks/             Notebook pipeline (Google Colab)
│   ├── README.md
│   ├── pipeline_korpus_multigenre_v2.ipynb
│   └── panduan_anotator_BTB.ipynb
├── metadata/
│   └── skema-kolom.md     Definisi kolom dan taksonomi genre
└── docs/
    ├── laporan-teknis.md  Laporan teknis (luaran penelitian)
    ├── panduan-pipeline-v2.md  Panduan pemakaian notebook pipeline
    ├── panduan-review-anotator.md  Panduan pengisian lembar review
    ├── pengumpulan-data.md  Metode pengumpulan dan kurasi data
    └── pernyataan-data.md   Pernyataan asal, lisensi, dan etika data
```

### Skema data

Kedua berkas CSV menggunakan skema kolom yang sama: `title`, `text_bt`, `text_id`, `genre`, `subgenre`, `source_link`, `notes`, `is_parallel`. Berkas `btb_multigenre.csv` versi 2 menambahkan kolom `doc_id` di depan. Penjelasan lengkap setiap kolom dan taksonomi genre tersedia pada [metadata/skema-kolom.md](metadata/skema-kolom.md).

Berkas `btb_bible.csv` belum disertakan di repositori ini. Lihat [data/README.md](data/README.md).

### Cara menggunakan

```python
import pandas as pd

multigenre = pd.read_csv("data/btb_multigenre.csv")

# Mengambil hanya pasangan yang berlabel paralel
pasangan_paralel = multigenre[multigenre["is_parallel"] == "yes"]
```

### Status luaran penelitian

| Luaran yang dijanjikan | Status |
|---|---|
| Korpus dengan minimal 100.000 token Batak Toba | Tercapai menurut hitungan token NLTK yang menyertakan tanda baca (112.465 token). Tanpa tanda baca: 97.952 kata. |
| Cakupan sumber tradisional | Tercapai |
| Cakupan sumber modern tertulis | Tercapai |
| Cakupan sumber religius | Tercapai |
| Laporan teknis | Tercapai ([docs/laporan-teknis.md](docs/laporan-teknis.md)) |

### Keterbatasan dan rencana lanjutan

Versi awal ini memiliki beberapa keterbatasan yang disengaja dicatat secara terbuka:

1. Domain keagamaan sangat dominan (sekitar 75% kata Batak Toba). Penambahan teks non-religius akan dilakukan untuk menyeimbangkan domain.
2. Sub-korpus Alkitab pada versi ini baru memuat satu pasal per kitab dan berkasnya belum disertakan. Sisi Indonesianya memakai Terjemahan Baru (1974), sehingga izin redistribusinya perlu dipastikan lebih dulu. Versi pasal penuh disiapkan sebagai pembaruan mendatang.
3. Korpus belum dilengkapi anotasi linguistik lanjutan (tokenisasi baku, POS tagging, morfologi, dependency parsing). Pengayaan anotasi direncanakan untuk menjadikannya sumber daya gold-standard. Penelitian berikutnya akan berfokus pada pedoman anotasi awal dengan Universal Dependencies versi 2.
4. Korpus paralel tingkat kalimat pada [data/experimental/](data/experimental/) masih berstatus eksperimental. Inter-annotator agreement belum dilakukan, sehingga data tersebut belum dapat dianggap gold-standard dan tidak termasuk luaran resmi tahap ini.

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

Multi-genre figures are produced by the [v2 pipeline notebook](notebooks/pipeline_korpus_multigenre_v2.ipynb). Bible figures are computed with the same functions. Because counts depend on how punctuation is treated, token counts are reported with three methods:

- **Words**: letter or digit sequences only. Punctuation is not counted.
- **Whitespace tokens**: text split on spaces. Punctuation stays attached to words.
- **NLTK tokens**: lowercased text split with NLTK `word_tokenize`. Punctuation marks count as separate tokens. This is the method used in the initial analysis.

| Sub-corpus | Unit | Batak Toba | Indonesian |
|---|---|---|---|
| `btb_multigenre` | documents | 104 | 104 |
| `btb_multigenre` | sentences or lines | 4,429 | 4,447 |
| `btb_multigenre` | words | 59,443 | 53,166 |
| `btb_multigenre` | NLTK tokens | 67,680 | 60,866 |
| `btb_bible` | chapters (verses) | 66 (1,594) | 66 (1,594) |
| `btb_bible` | words | 38,509 | 34,320 |
| `btb_bible` | NLTK tokens | 44,785 | 39,687 |
| Total | words | 97,952 | 87,486 |
| Total | whitespace tokens | 98,235 | 85,990 |
| Total | NLTK tokens | 112,465 | 100,553 |

The proposal target of at least 100,000 Batak Toba tokens is met when punctuation marks are counted as tokens (112,465 NLTK tokens). Counting words only, the Batak Toba side has 97,952 words, about 2% below the target. Both figures are reported so that readers can judge for themselves.

Note on changed figures: the initial README listed 520 parallel documents for the Bible sub-corpus. That figure came from an incorrect grouping in the old EDA notebook; the actual count is 66 chapters (1,594 verses). Multi-genre sentence counts now come from the v2 segmentation, which also splits poems and liturgy by line, so they differ from the 3,498 sentences reported initially.

Genre and sub-genre distribution:

| Genre | Sub-genre | Documents | Batak Toba words |
|---|---|---|---|
| Historical/Traditional | Folktales | 2 | 1,796 |
| Literary | Peribahasa/Umpama | 46 | 356 |
| Literary | Poems | 7 | 741 |
| Religious | Prayers | 3 | 210 |
| Religious | Ritual Text (HKBP liturgical agenda) | 6 | 35,097 |
| Religious | Bible (`btb_bible`) | 66 chapters | 38,509 |
| Educational | Book Summary | 8 | 4,120 |
| Educational | Abstract | 9 | 1,915 |
| Contemporary Media | Wiki | 7 | 6,246 |
| Contemporary Media | News Article | 9 | 3,884 |
| Contemporary Media | Blog Articles | 7 | 5,078 |

The religious domain is strongly dominant. The HKBP agenda, prayers, and the Bible account for about 75% of Batak Toba words, and the HKBP agenda alone accounts for 59% of the multi-genre sub-corpus. Domain balancing is part of the planned follow-up work.

### Repository structure

```
batak-toba-korpus/
├── README.md              This document (bilingual)
├── LICENSE                Data license (CC BY 4.0)
├── LICENSE-CODE           Script and notebook license (MIT)
├── CITATION.cff           Citation metadata
├── .gitignore
├── data/                  Corpus files (CSV)
│   ├── README.md
│   ├── btb_multigenre.csv Multi-genre corpus, version 2
│   └── experimental/      Sentence-level parallel corpus (pending IAA)
├── notebooks/             Pipeline notebooks (Google Colab)
│   ├── README.md
│   ├── pipeline_korpus_multigenre_v2.ipynb
│   └── panduan_anotator_BTB.ipynb
├── metadata/
│   └── skema-kolom.md     Column definitions and genre taxonomy
└── docs/
    ├── laporan-teknis.md  Technical report (research deliverable)
    ├── panduan-pipeline-v2.md  Usage guide for the pipeline notebook
    ├── panduan-review-anotator.md  Guide for filling in the review sheets
    ├── pengumpulan-data.md  Data collection and curation method
    └── pernyataan-data.md   Data provenance, license, and ethics statement
```

### Data schema

Both CSV files share the same column schema: `title`, `text_bt`, `text_id`, `genre`, `subgenre`, `source_link`, `notes`, `is_parallel`. Version 2 of `btb_multigenre.csv` adds a leading `doc_id` column. A full description of each column and the genre taxonomy is available in [metadata/skema-kolom.md](metadata/skema-kolom.md).

`btb_bible.csv` is not yet included in this repository. See [data/README.md](data/README.md).

### How to use

```python
import pandas as pd

multigenre = pd.read_csv("data/btb_multigenre.csv")

# Keep only rows marked as parallel pairs
parallel_pairs = multigenre[multigenre["is_parallel"] == "yes"]
```

### Research deliverable status

| Promised deliverable | Status |
|---|---|
| Corpus with at least 100,000 Batak Toba tokens | Achieved when punctuation marks are counted as NLTK tokens (112,465 tokens). Without punctuation: 97,952 words. |
| Coverage of traditional sources | Achieved |
| Coverage of modern written sources | Achieved |
| Coverage of religious sources | Achieved |
| Technical report | Achieved ([docs/laporan-teknis.md](docs/laporan-teknis.md)) |

### Limitations and future work

This initial version has several limitations that are recorded openly:

1. The religious domain is strongly dominant (about 75% of Batak Toba words). Non-religious texts will be added to balance the domains.
2. The Bible sub-corpus in this version contains only one chapter per book, and its file is not yet included. Its Indonesian side uses the Terjemahan Baru (1974) translation, so redistribution permission must be confirmed first. A full-chapter version is being prepared as a future update.
3. The corpus is not yet enriched with advanced linguistic annotation (standardised tokenisation, POS tagging, morphology, dependency parsing). Annotation enrichment is planned to develop it into a gold-standard resource. The next research will focus on the initial annotation guidelines with Universal Dependencies version 2.
4. The sentence-level parallel corpus in [data/experimental/](data/experimental/) is still experimental. Inter-annotator agreement has not been measured, so it cannot be treated as gold-standard and is not part of the official deliverable of this phase.

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
