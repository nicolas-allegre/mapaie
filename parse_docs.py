import glob
import os
from tqdm import tqdm
import magic

from Parser import Parser

DATA_FOLDER = 'data'
LOG_FOLDER = "log/"
LOG_FILENAME = "parse.log"
LOG_FILE = os.path.join(LOG_FOLDER, LOG_FILENAME)
OUT_FOLDER = os.path.join(DATA_FOLDER, "txts")
DOCS_FOLDER = os.path.join(DATA_FOLDER, "docs")
CHARSET = 'UTF-8'

os.makedirs(OUT_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

log_fp = open(LOG_FILE, "w", encoding=CHARSET)

p = Parser(log_file=log_fp)

all_files = [f for f in glob.glob(f'{DOCS_FOLDER}/*')]

for i in tqdm(range(len(all_files))):
    fname = all_files[i]
    ftype = magic.from_file(fname, mime=True)

    if ftype == "text/html" or ftype == "text/xml":
        # this is a html file
        p.parse_html(fname)
    elif ftype == "application/pdf":
        # this is a pdf file
        p.parse_pdf(fname)
    else:
        print(f"ERR. NOT A RECOGNIZED FILETYPE: {fname}, {ftype}.", file=log_fp)

log_fp.close()
