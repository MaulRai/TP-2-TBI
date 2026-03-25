from bsbi import BSBIIndex
from compression import EliasGammaPostings

# sebelumnya sudah dilakukan indexing
# BSBIIndex hanya sebagai abstraksi untuk index tersebut
BSBI_instance = BSBIIndex(data_dir = 'collection', \
                          postings_encoding = EliasGammaPostings, \
                          output_dir = 'index')

queries = ["alkylated with radioactive iodoacetate", \
           "psychodrama for disturbed children", \
           "lipid metabolism in toxemia and normal pregnancy"]

print("Pilih metode scoring untuk pencarian:")
print("1. TF-IDF")
print("2. BM25 (Exhaustive)")
print("3. BM25 (WAND Top-K)")
mode_input = input("Masukkan pilihan (1/2/3) [default: 3]: ").strip()

scoring_mode = "wand"  # default
if mode_input == "1":
    scoring_mode = "tfidf"
elif mode_input == "2":
    scoring_mode = "bm25"
elif mode_input == "3":
    scoring_mode = "wand"
           
for query in queries:
    print("Query  : ", query)
    print("Results:")
    if scoring_mode == "tfidf":
        results = BSBI_instance.retrieve_tfidf(query, k = 10)
    elif scoring_mode == "bm25":
        results = BSBI_instance.retrieve_bm25(query, k = 10)
    else:
        results = BSBI_instance.retrieve_bm25_wand(query, k = 10)
        
    for (score, doc) in results:
        print(f"{doc:30} {score:>.3f}")
    print()