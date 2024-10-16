import argparse
import numpy
import sys
import glob
from pathlib import Path
from nltk.corpus import stopwords
from tqdm import tqdm
import ujson as json
import os

DATA_FOLDER = 'data'
LOG_FOLDER = "log/"
LOG_FILENAME = "corpus.log"
LOG_FILE = os.path.join(LOG_FOLDER, LOG_FILENAME)
OUT_FILENAME = "corpus.txt"
CHARSET = 'UTF-8'

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

log_fp = open(LOG_FILE, "w", encoding=CHARSET)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data")
parser.add_argument("-m", "--method", choices=["iramuteq", "cortext"])
parser.add_argument("-t", "--themes")
# parser.add_argument("-d", "--destination", choices=["iramuteq", "cortext"])

args = parser.parse_args()
print(args)

# Keywords
keywords = json.load(open(args.themes, encoding=CHARSET))

filt_crit = lambda x, kw_list: all(x)

iramuteq = False
cortext = False

folder_name = os.path.join(DATA_FOLDER, f'corpus_{args.method}')
if args.method == "iramuteq":
    iramuteq = True
elif args.method == "cortext":
    cortext = True

    for t in keywords:
        os.makedirs(os.path.join(folder_name, t), exist_ok=True)
else:
    iramuteq = True
    folder_name = os.path.join(DATA_FOLDER, f'corpus_iramuteq')

os.makedirs(folder_name, exist_ok=True)
corpus_file = open(os.path.join(folder_name, OUT_FILENAME), "w", encoding=CHARSET)

# Counting docs per theme
nb_docs = 0
doc_counts = { k: 0 for k, v in keywords.items() }
doc_occurrences = {}

for i, fname in enumerate(tqdm(glob.glob(f"./{args.data}/*.txt"))):
    nb_docs += 1
    doc_occurrences[i] = {}

    try:
        f = open(fname, "r", encoding=CHARSET)
        contents = f.read().strip().lower()
        doc_occurrences[i]["contents"] = contents

        for topic, kw_list in keywords.items():
            if filt_crit([ kw for kw in kw_list if kw in contents ], kw_list):
            # if any([ kw in contents for kw in kw_list ]):
                doc_occurrences[i][topic] = sum([contents.count(x) for x in kw_list])
        
        f.close()
    except Exception as e:
        print(f"Err {fname}: {e}", file=log_fp)
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
    
    # Corpus Iramuteq
    if iramuteq:
        print("**** " + " ".join(topics), file=corpus_file)
        print(doc_occurrences[i]["contents"], file=corpus_file)

    # Corpus cortext
    if cortext:
        for t in topics:
            # Creer dir topics
            if t.strip("*") != "mapaie":
                file = open(os.path.join(folder_name, f"{t.strip('*')}/{i}.txt"), "w", encoding=CHARSET)
                print(doc_occurrences[i]["contents"], file=file) 

# regarder aussi les co-occurrences de thèmes
print("Summary stats", file=log_fp)
for k, v in doc_counts.items():
    tmp = '-'
    if nb_docs != 0:
        tmp = v / nb_docs * 100
    print(f"{k}: {v} ({tmp}%)", file=log_fp) 

log_fp.close()
corpus_file.close()
