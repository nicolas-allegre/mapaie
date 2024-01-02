import sys
import glob
from pathlib import Path
from nltk.corpus import stopwords
from tqdm import tqdm

LOG_FILE = "corpus.log"
OUT_FILE = "corpus.txt"
log_fp = open(LOG_FILE, "w")

corpus_file = open(OUT_FILE, "w", encoding="utf-8")


for fname in tqdm(glob.glob(f"./{sys.argv[1]}/*.txt")):
    topics = ["*mapaie"]

    try:
        f = open(fname, "r")
        contents = f.read().strip()
        if "fairness" in contents:
            topics.append("*fairness")

        print("**** " + " ".join(topics), file=corpus_file)
        print(contents, file=corpus_file)
        
        f.close()
    except Exception as e:
        print(f"Err {fname}: {e}")
        pass

log_fp.close()
corpus_file.close()
