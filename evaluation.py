import math
import re
from bsbi import BSBIIndex
from compression import VBEPostings, EliasGammaPostings

######## >>>>> sebuah IR metric: RBP p = 0.8

def rbp(ranking, p = 0.8):
  """ menghitung search effectiveness metric score dengan 
      Rank Biased Precision (RBP)

      Parameters
      ----------
      ranking: List[int]
         vektor biner seperti [1, 0, 1, 1, 1, 0]
         gold standard relevansi dari dokumen di rank 1, 2, 3, dst.
         Contoh: [1, 0, 1, 1, 1, 0] berarti dokumen di rank-1 relevan,
                 di rank-2 tidak relevan, di rank-3,4,5 relevan, dan
                 di rank-6 tidak relevan
        
      Returns
      -------
      Float
        score RBP
  """
  score = 0.
  for i in range(1, len(ranking)):
    pos = i - 1
    score += ranking[pos] * (p ** (i - 1))
  return (1 - p) * score

def dcg(ranking):
  """ menghitung score Discounted Cumulative Gain """
  score = 0.
  for i in range(len(ranking)):
    score += ranking[i] / math.log2(i + 2)
  return score

def ndcg(ranking):
  """ menghitung score Normalized Discounted Cumulative Gain """
  score = dcg(ranking) 

  ideal_ranking = sorted(ranking, reverse=True)
  ideal_score = dcg(ideal_ranking)

  if ideal_score == 0:
    return 0.0
  
  return score / ideal_score

def prec(ranking):
  score = 0.
  ranking_length = len(ranking)
  for i in range(1, ranking_length):
    score += ranking[i]
  return score / ranking_length

def ap(ranking):
  """ menghitung score Average Precision """
  score = 0.
  relevant_docs_found = 0

  R = sum(ranking)

  if R == 0:
    return 0.0


  for i in range(1, len(ranking)):
    if ranking[i] == 1:
      relevant_docs_found += 1

      precision_at_k = relevant_docs_found / (i + 1)
      score += precision_at_k

  return score / R

######## >>>>> memuat qrels

def load_qrels(qrel_file = "qrels.txt", max_q_id = 30, max_doc_id = 1033):
  """ memuat query relevance judgment (qrels) 
      dalam format dictionary of dictionary
      qrels[query id][document id]

      dimana, misal, qrels["Q3"][12] = 1 artinya Doc 12
      relevan dengan Q3; dan qrels["Q3"][10] = 0 artinya
      Doc 10 tidak relevan dengan Q3.

  """
  qrels = {"Q" + str(i) : {i:0 for i in range(1, max_doc_id + 1)} \
                 for i in range(1, max_q_id + 1)}
  with open(qrel_file) as file:
    for line in file:
      parts = line.strip().split()
      qid = parts[0]
      did = int(parts[1])
      qrels[qid][did] = 1
  return qrels

######## >>>>> EVALUASI !

def eval(qrels, scoring_mode="tfidf", query_file="queries.txt", k=1000):
  """ 
    loop ke semua 30 query, hitung score di setiap query,
    lalu hitung MEAN SCORE over those 30 queries.
    untuk setiap query, kembalikan top-1000 documents
  """
  BSBI_instance = BSBIIndex(data_dir = 'collection', \
                          postings_encoding = EliasGammaPostings, \
                          output_dir = 'index')

  with open(query_file) as file:
    rbp_scores = []
    dcg_scores = []
    ndcg_scores = []
    ap_scores = []
    for qline in file:
      parts = qline.strip().split()
      qid = parts[0]
      query = " ".join(parts[1:])

      # HATI-HATI, doc id saat indexing bisa jadi berbeda dengan doc id
      # yang tertera di qrels
      ranking = []
      if scoring_mode == "tfidf":
          results = BSBI_instance.retrieve_tfidf(query, k=k)
      elif scoring_mode == "bm25":
          results = BSBI_instance.retrieve_bm25(query, k=k)
      else:
          results = BSBI_instance.retrieve_bm25_wand(query, k=k)
          
      for (score, doc) in results:
          did = int(re.search(r'\/.*\/.*\/(.*)\.txt', doc).group(1))
          ranking.append(qrels[qid][did])
          
      rbp_scores.append(rbp(ranking))
      dcg_scores.append(dcg(ranking))
      ndcg_scores.append(ndcg(ranking))
      ap_scores.append(ap(ranking))

  print(f"\n[Hasil Evaluasi - Algoritma: {scoring_mode.upper()}] terhadap 30 queries")
  print(f"RBP score  = {sum(rbp_scores) / len(rbp_scores):.4f}")
  print(f"DCG score  = {sum(dcg_scores) / len(dcg_scores):.4f}")
  print(f"NDCG score = {sum(ndcg_scores) / len(ndcg_scores):.4f}")
  print(f"MAP score  = {sum(ap_scores) / len(ap_scores):.4f}")

if __name__ == '__main__':
  qrels = load_qrels()

  assert qrels["Q1"][166] == 1, "qrels salah"
  assert qrels["Q1"][300] == 0, "qrels salah"

  print("Pilih metode scoring yang akan dievaluasi:")
  print("1. TF-IDF")
  print("2. BM25 (Exhaustive)")
  print("3. BM25 (WAND Top-K)")
  print("4. Bandingkan Semua")
  
  mode_input = input("Masukkan pilihan (1/2/3/4) [default: 1]: ").strip()
  
  if mode_input == "2":
      eval(qrels, scoring_mode="bm25")
  elif mode_input == "3":
      eval(qrels, scoring_mode="wand")
  elif mode_input == "4":
      print("\n>>> Evaluasi TF-IDF")
      eval(qrels, scoring_mode="tfidf")
      print("\n>>> Evaluasi BM25 (Exhaustive)")
      eval(qrels, scoring_mode="bm25")
      print("\n>>> Evaluasi BM25 (WAND)")
      eval(qrels, scoring_mode="wand")
  else:
      eval(qrels, scoring_mode="tfidf")