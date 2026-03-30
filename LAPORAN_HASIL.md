## **Laporan Evaluasi Indexing BSBI**

### **1. Ringkasan Hasil Eksperimen**
Pengujian dilakukan terhadap 11 blok dokumen menggunakan algoritma **Blocked Sort-Based Indexing (BSBI)**.

| Metode Kompresi | Waktu Indexing (detik) | Ukuran Index (MB) | Efisiensi Ruang (%) |
| :--- | :---: | :---: | :---: |
| **StandardPostings** | **2.7730** | 2.21 | 0% (Baseline) |
| **VBEPostings** | 2.8644 | 1.49 | ~32.5% |
| **EliasGammaPostings** | 2.9454 | **1.45** | **~34.4%** |



---

### **2. Analisis Performa**

#### **A. Efisiensi Ruang Penyimpanan**
* **EliasGammaPostings** memberikan hasil kompresi paling optimal (1.45 MB), sedikit lebih unggul dibandingkan VBE. Hal ini dikarenakan Elias-Gamma bekerja pada level bit sehingga sangat efisien untuk angka-angka kecil (hasil dari *gap encoding*).
* **VBEPostings** memberikan pengurangan ukuran yang signifikan dari *Standard* (dari 2.21 MB ke 1.49 MB) dengan hanya menggunakan algoritma berbasis *byte*.
* **StandardPostings** (tanpa kompresi) menghasilkan ukuran berkas terbesar karena setiap integer disimpan menggunakan alokasi memori tetap (4 byte).

#### **B. Waktu Pemrosesan (*Indexing Time*)**
* **StandardPostings** adalah yang tercepat (2.77 detik) karena tidak membutuhkan beban komputasi tambahan untuk melakukan encoding bit atau manipulasi byte.
* Terdapat *trade-off* (timbal balik) antara kecepatan dan ukuran: Semakin kompleks algoritma kompresinya (**Elias-Gamma**), waktu yang dibutuhkan sedikit lebih lama (2.94 detik) karena adanya proses kalkulasi *prefix* dan manipulasi *bitstring*.

---

### **3. Kesimpulan**
Jika prioritas sistem adalah **penghematan ruang penyimpanan**, maka **Elias-Gamma** adalah pilihan terbaik untuk koleksi ini. Namun, jika prioritas adalah **kecepatan indexing**, **StandardPostings** tetap unggul. **VBE** menjadi titik tengah (*sweet spot*) yang baik karena memberikan kompresi tinggi dengan waktu yang hampir secepat metode tanpa kompresi.

Berikut adalah laporan singkat hasil evaluasi efektivitas pencarian menggunakan metode **TF-IDF** dan **BM25** (Exhaustive & WAND) pada lingkungan index **BSBI** dengan kompresi **EliasGammaPostings**.

---

## **Laporan Evaluasi Efektivitas Retrieval**

*Catatan: Lingkungan eksperimen bagian ini dilakukan dengan indexing metode BSBI dan kompresi EliasGammaPostings*

### **1. Tabel Perbandingan Performa**
Evaluasi dilakukan terhadap 30 query menggunakan metrik standar Information Retrieval (RBP, DCG, NDCG, dan MAP).

| Algoritma | RBP (p=0.8) | DCG | NDCG | MAP |
| :--- | :---: | :---: | :---: | :---: |
| **TF-IDF** | 0.6494 | 5.8206 | 0.8149 | 0.4188 |
| **BM25 (Exhaustive)** | **0.6818** | 5.9600 | **0.8351** | **0.4483** |
| **BM25 (WAND)** | **0.6818** | **5.9601** | **0.8351** | **0.4483** |

---

### **2. Analisis Hasil**

#### **A. BM25 vs TF-IDF**
* **Superioritas BM25**: Algoritma BM25 secara konsisten mengungguli TF-IDF di semua metrik. Hal ini terlihat dari kenaikan skor **MAP** (~7%) dan **NDCG** (~2.5%).
* **Normalisasi Panjang Dokumen**: Keunggulan BM25 didorong oleh kemampuannya melakukan normalisasi terhadap panjang dokumen (*length normalization*) melalui parameter $avgdl$ (rata-rata panjang dokumen) yang telah di-precompute sebelumnya, sehingga dokumen panjang tidak mendominasi skor secara tidak adil.

#### **B. Exhaustive vs WAND (Weak AND)**
* **Efektivitas Identik**: Skor antara BM25 Exhaustive dan WAND hampir tidak memiliki perbedaan signifikan (NDCG dan MAP identik).
* **Optimasi Tanpa Penurunan Kualitas**: Hasil ini membuktikan bahwa algoritma **WAND** berhasil melakukan optimasi pemangkasan (*pruning*) dokumen yang tidak relevan selama proses retrieval tanpa mengorbankan kualitas dokumen Top-K yang dihasilkan.

---

### **3. Kesimpulan Teknikal**
Penggunaan **EliasGammaPostings** pada tahap indexing terbukti mampu menjaga integritas data postings list dan TF. Meskipun data dikompresi hingga ke level bit untuk menghemat ruang penyimpanan, sistem tetap mampu melakukan *decoding* dengan akurat untuk menghitung skor statistik yang tinggi (NDCG > 0.8). 
