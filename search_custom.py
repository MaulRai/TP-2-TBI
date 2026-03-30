import sys
import time
from compression import EliasGammaPostings
from bsbi import BSBIIndex


def prompt_choice(prompt, choices, default=None):
    opts = "/".join(choices)
    txt = f"{prompt} ({opts})"
    if default is not None:
        txt += f" [default: {default}]"
    txt += ": "
    val = input(txt).strip()
    if val == "" and default is not None:
        return default
    return val


def run():
    print("Loading index (this will read term/doc maps from index folder)...")
    start_load = time.time()
    idx = BSBIIndex(data_dir='collection', postings_encoding=EliasGammaPostings, output_dir='index')
    try:
        idx.load()
    except Exception:
        # If dictionaries are not present, BSBIIndex methods will lazy-load or build;
        # just continue but notify the user.
        print("Warning: failed to load saved dictionaries; if index isn't built, retrieval may fail.")
    load_time = time.time() - start_load
    print(f"Index ready (load time: {load_time:.3f}s). Enter queries (empty query to quit).\n")

    while True:
        try:
            query = input("Query> ").strip()
        except (KeyboardInterrupt, EOFError):
            print('\nExiting.')
            break

        if query == "":
            print("Goodbye.")
            break

        scoring = prompt_choice("Choose scoring [1=tfidf,2=bm25,3=bm25_wand]", ["1","2","3"], default="2")
        k_raw = input("Top-K (default 10): ").strip()
        try:
            k = int(k_raw) if k_raw else 10
        except ValueError:
            k = 10

        # Time the retrieval
        t0 = time.time()
        if scoring == "1":
            results = idx.retrieve_tfidf(query, k=k)
        elif scoring == "3":
            results = idx.retrieve_bm25_wand(query, k=k)
        else:
            results = idx.retrieve_bm25(query, k=k)
        qtime = time.time() - t0

        if results:
            print(f"Retrieved {len(results)} results in {qtime:.4f}s")

        if not results:
            print("No results.")
            continue

        print(f"Top {len(results)} results:")
        for i, (score, doc) in enumerate(results, start=1):
            print(f"{i}. {doc} \t(score={score:.6f})")


if __name__ == '__main__':
    run()
