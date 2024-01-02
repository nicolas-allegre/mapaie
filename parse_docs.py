from PyPDF2 import PdfReader
import sys
import glob
import os
from pathlib import Path
from tqdm import tqdm

LOG_FILE = "parse.log"
OUT_FOLDER = "./txts"
log_fp = open(LOG_FILE, "w")

# Create output directory if it does not exist
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

all_files = [f for f in glob.glob("./pdfs/*.pdf")]

for i in tqdm(range(len(all_files))):
    fname = all_files[i]

    try:
        f = open(fname, "rb")
        reader = PdfReader(f)
        words = set()
        txt_file = open(f"txts/{Path(fname).stem}.txt", "w+", encoding="utf-8")
        
        for page in reader.pages:
            page_contents = page.extract_text()
            page_contents = page_contents.replace("-\n", "")
            page_contents = page_contents.replace("\n", " ")
            print(page_contents, file=txt_file)
            words = words.union(set(page_contents.split(" ")))
        
        f.close()
        txt_file.close()
        print(fname, len(words), file=log_fp)
    except Exception as e:
        print(f"Err {fname}: {e}", file=log_fp)
        pass

log_fp.close()
