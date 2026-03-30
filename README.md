# Sistem Pencarian — Panduan Singkat (Bahasa Indonesia)

## Penggunaan

- **Indexing**: Jalankan `bsbi.py` untuk membangun indeks. Pilih mode indexing saat diminta:
  - `1` = BSBI (Blocked Sort-Based Indexing)
  - `2` = SPIMI (Single-Pass In-Memory Indexing)
  Saat proses, Anda juga akan diminta memilih metode kompresi (Standard / VBE / Elias-Gamma).

- **Tes pencarian & evaluasi**:
  - Jalankan `search.py` untuk menjalankan beberapa test-case pencarian bawaan.
  - Jalankan `evaluation.py` untuk menghitung metrik evaluasi dari hasil pencarian menggunakan `qrels.txt` dan `queries.txt`.

- **Pencarian kustom**:
  - Jalankan `search_custom.py` untuk membuka CLI interaktif di mana Anda dapat memasukkan query, memilih skema scoring (TF-IDF / BM25 / BM25 WAND) dan menentukan Top-K.


## Deliverables (Tugas)

- **Algoritma kompresi tambahan**: Elias-Gamma ditambahkan sebagai opsi kompresi bersama VBE dan Standard. (File: `compression.py`)

- **Scoring BM25**: BM25 tersedia sebagai fungsi ranking. Pre-komputasi panjang dokumen dan rata-rata panjang dokumen disiapkan/diolah oleh `precomp.py` dan digunakan saat retrieval untuk perhitungan BM25.

- **Metrik evaluasi tambahan**: NDCG, DCG, dan Average Precision (AP) ditambahkan pada modul evaluasi. Jalankan `evaluation.py` untuk melihat hasil metrik ini.

- **WAND Top-K Retrieval**: Implementasi WAND (Weak AND) untuk mempercepat retrieval top-K dengan pruning tersedia sebagai opsi `retrieve_bm25_wand` di `bsbi.py`.

- **Indexing dengan SPIMI**: Mode SPIMI didukung — pilih `2` saat menjalankan `bsbi.py` untuk menjalankan single-pass in-memory indexing per block.

- **Struktur dictionary efisien (Patricia Tree)**: Term-term pada dictionary disusun menggunakan struktur Patricia Tree untuk efisiensi prefix — lihat `util.py` (class `PatriciaTreeIdMap`).

