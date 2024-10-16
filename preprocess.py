import glob
from tqdm import tqdm
import numpy as np
import os

import nltk as nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

DATA_FOLDER = 'data'
OUT_FOLDER = os.path.join(DATA_FOLDER, "preprocessed")
TXT_FOLDER = os.path.join(DATA_FOLDER, "txts")
CHARSET = 'UTF-8'

os.makedirs(OUT_FOLDER, exist_ok=True)

corpus = []
stop_words = set(stopwords.words('english'))

print(f'Preprocessing...')
for i, filename in enumerate(tqdm(glob.glob(f'{TXT_FOLDER}/*.txt'))):
    name = os.path.basename(filename).split('.')[0]
    with open(filename, encoding=CHARSET) as f:
        lines = f.read().strip()
        # Tokenize
        tokens = word_tokenize(lines)
        # Remove tokens with length < 3, not a link and not in stop words
        tokens = (' ').join([t.lower() for t in tokens
            if len(t) >= 3 
            and (t.isalpha() or t in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
            and t.lower() not in stop_words 
            and not "http" in t.lower()
        ])

        # ngrams ?

        # Save tokens
        corpus.append(tokens)


# TF-IDF
def tfidf_filter(corpus):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    tfidf_values = np.array(X.mean(axis=0))[0]
    median_tfidf = np.quantile(tfidf_values, 0.5)
    mask = tfidf_values > median_tfidf
    words_to_keep = vectorizer.get_feature_names_out()[mask]
    print(type(words_to_keep))
    return words_to_keep

corpus_filt_tfidf = []
# words_to_keep = tfidf_filter(corpus)

for i, d in enumerate(tqdm(corpus)):
    words = d.split()
    # filt_words = [w for w in words if w in words_to_keep]
    # corpus_filt_tfidf.append(filt_words)
    f = open(f"{OUT_FOLDER}/{i}.txt", "w", encoding=CHARSET)
    f.write(" ".join(words) + "\n")
    f.close()

# with open('corpus_filt_tfidf.txt', 'w', encoding=CHARSET) as f:
#    for d in corpus_filt_tfidf:
#        doc = ' '.join(d)
#        f.write(doc + '\n')
