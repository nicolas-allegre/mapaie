import sys
import glob
from pathlib import Path

LOG_FILE = "corpus.log"
OUT_FILE = "corpus.txt"
log_fp = open(LOG_FILE, "w")

corpus_file = open(OUT_FILE, "w", encoding="utf-8")

for fname in glob.glob("./txts/*.txt"):
    print(fname)
    try:
        f = open(fname, "r")

        print("**** *mapaie", file=corpus_file)
        print(f.read().strip(), file=corpus_file)
        
        f.close()
    except Exception as e:
        print(f"Err {fname}: {e}")
        pass

log_fp.close()
corpus_file.close()
