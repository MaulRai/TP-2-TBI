import math

import os
import pickle

def precompute_len_doc(target_dir_path, output_path):
    """
    Menghitung jumlah token untuk setiap dokumen di seluruh koleksi.
    
    Parameters
    ----------
    target_dir_path: str
        Path ke folder 'collection' yang berisi sub-folder (blok).
    output_path: str
        Path (termasuk nama file) untuk menyimpan hasil pickle (misal: 'index/doc_lengths.dict').
    """
    doc_lengths = {}

    blocks = sorted(next(os.walk(target_dir_path))[1])

    for block in blocks:
        block_path = os.path.join(target_dir_path, block)
        for filename in next(os.walk(block_path))[2]:
            doc_path = os.path.join(block_path, filename)
            
            with open(doc_path, "r", encoding="utf8", errors="surrogateescape") as f:
                tokens = f.read().split()
                doc_lengths[doc_path] = len(tokens)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(doc_lengths, f)
    
    print(f"Selesai! Panjang {len(doc_lengths)} dokumen disimpan di {output_path}")

def precompute_mean_len_doc(precomputed_path, output_path):
    """
    Menghitung rata-rata panjang dokumen (avgdl) dari data yang sudah di-precompute.
    
    Parameters
    ----------
    precomputed_path: str
        Path ke file pickle hasil precompute_len_doc.
    output_path: str
        Path untuk menyimpan nilai rata-rata (misal: 'index/avg_doc_length.txt').
    """
    with open(precomputed_path, 'rb') as f:
        doc_lengths = pickle.load(f)

    if not doc_lengths:
        return 0.0

    total_docs = len(doc_lengths)
    total_tokens = sum(doc_lengths.values())
    mean_length = total_tokens / total_docs

    with open(output_path, 'w') as f:
        f.write(str(mean_length))
    
    print(f"Rata-rata panjang dokumen: {mean_length:.4f} (Total: {total_tokens} token dari {total_docs} dokumen)")
    return mean_length

if __name__ == "__main__":
    precompute_len_doc(target_dir_path='collection', output_path='index/doc_lengths.dict')
    precompute_mean_len_doc(precomputed_path='index/doc_lengths.dict', output_path='index/avg_doc_length.txt')