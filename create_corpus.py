import sys
import glob
from pathlib import Path
from nltk.corpus import stopwords
from tqdm import tqdm

LOG_FILE = "corpus.log"
OUT_FILE = "corpus.txt"
log_fp = open(LOG_FILE, "w")

corpus_file = open(OUT_FILE, "w", encoding="utf-8")
nb_docs = 0

# Keywords
keywords = {
    "fairness": ["fair", "fairness"],
    "accountability": ["accountability", "accountable"],
    "xai": ["xai", "explainability", "explainable"],
    "transparency": ["transparency", "transparent"]
}

# Counting docs per theme
doc_counts = { k: 0 for k, v in keywords.items() }

for fname in tqdm(glob.glob(f"./{sys.argv[1]}/*.txt")):
    topics = ["*mapaie"]
    nb_docs += 1

    try:
        f = open(fname, "r")
        contents = f.read().strip().lower()
        for topic, kw_list in keywords.items():
            if any([ kw in contents for kw in kw_list ]):
                topics.append(f"*{topic}")
                doc_counts[topic] += 1

        print("**** " + " ".join(topics), file=corpus_file)
        print(contents, file=corpus_file)
        
        f.close()
    except Exception as e:
        print(f"Err {fname}: {e}")
        pass

log_fp.close()
corpus_file.close()

# regarder aussi les co-occurrences de thèmes
print("Summary stats")
for k, v in doc_counts.items():
    print(f"{k}: {v} ({v/nb_docs*100}%)") 
