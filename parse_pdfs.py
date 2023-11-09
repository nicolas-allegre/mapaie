from PyPDF2 import PdfReader
import sys
import glob
from pathlib import Path

LOG_FILE = "parse.log"
log_fp = open(LOG_FILE, "w")

for fname in glob.glob("./pdfs/*.pdf"):
    print(fname)
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
        print(f"Err {fname}: {e}")
        pass

log_fp.close()
