import numpy
import sys
import glob
from pathlib import Path
from nltk.corpus import stopwords
from tqdm import tqdm
import ujson as json

LOG_FILE = "corpus.log"
OUT_FILE = "corpus.txt"
log_fp = open(LOG_FILE, "w")

corpus_file = open(OUT_FILE, "w", encoding="utf-8")
nb_docs = 0

# Keywords
keywords = {
    "fairness": [" fairness ", " algorithmic fairness ", " demographic parity "],
    "accountability": ["accountability", "accountable"],
    "xai": [" xai ", " lime ", " shap "],
    "transparency": ["transparency", "transparent"],
    "agi": [" agi " ],
    "dignity": [" dignity "],
    "gen_ai": [" generative "]
}
# keywords = json.load(open("themes.json"))

filt_crit = lambda x, kw_list: all(x)

# Counting docs per theme
doc_counts = { k: 0 for k, v in keywords.items() }
doc_occurrences = {}

for i, fname in enumerate(tqdm(glob.glob(f"./{sys.argv[1]}/*.txt"))):
    nb_docs += 1
    doc_occurrences[i] = {}

    try:
        f = open(fname, "r")
        contents = f.read().strip().lower()
        doc_occurrences[i]["contents"] = contents

        for topic, kw_list in keywords.items():
            if filt_crit([ kw for kw in kw_list if kw in contents ], kw_list):
            # if any([ kw in contents for kw in kw_list ]):
                doc_occurrences[i][topic] = sum([contents.count(x) for x in kw_list])
        
        f.close()
    except Exception as e:
        print(f"Err {fname}: {e}")
        pass

# Write out topics
topics_counts = { x: [] for x in keywords.keys() }
topics_medians = { x: 0.0 for x in keywords.keys() }
for i in doc_occurrences:
    for t in keywords:
        topics_counts[t].append(doc_occurrences[i][t])

for t in topics_medians:
    topics_medians[t] = numpy.median(topics_counts[t])

for i in doc_occurrences:
    
    topics = ["*mapaie"]

    for t in keywords:
        # if doc_occurrences[i][t] > topics_medians[t]:
        filt_crit = [ x in doc_occurrences[i]["contents"] for x in keywords[t] ] 
        # doc_has_topic = any(filt_crit)
        doc_has_topic = len([x for x in filt_crit if x])/len(filt_crit) >= 0.6

        if doc_has_topic:
            topics.append(f"*{t}")
            doc_counts[t] += 1

    print("**** " + " ".join(topics), file=corpus_file)
    print(doc_occurrences[i]["contents"], file=corpus_file)

log_fp.close()
corpus_file.close()

# regarder aussi les co-occurrences de thèmes
print("Summary stats")
for k, v in doc_counts.items():
    print(f"{k}: {v} ({v/nb_docs*100}%)") 

