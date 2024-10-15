import glob
import os
from tqdm import tqdm
import magic

from Parser import Parser

LOG_FOLDER = "log/"
LOG_FILENAME = "parse.log"
LOG_FILE = os.path.join(LOG_FOLDER, LOG_FILENAME)
OUT_FOLDER = "./txts"
CHARSET = 'UTF-8'

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
log_fp = open(LOG_FILE, "w", encoding=CHARSET)

p = Parser(log_file=log_fp)

# Create output directory if it does not exist
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

all_files = [f for f in glob.glob("./docs/*")]

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
