import requests
import sys
import os
from random import choice
from tqdm import tqdm


URL_FILE = "list_pdfs.txt"
UA_FILE = "user_agents.txt"
OUT_FOLDER = "./pdfs"
LOG_FILE = "dl_pdfs.log"
log_fp = open(LOG_FILE, "w")

list_of_urls = [ x.strip() for x in open(URL_FILE).readlines() ]
user_agents = [ x.strip() for x in open(UA_FILE).readlines() ] 

if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

for i in tqdm(range(len(list_of_urls))):
    url = list_of_urls[i]
    try:
        headers = { "User-Agent": choice(user_agents) }
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {url}, {e}", file=log_fp)

    if response.status_code == 200:
        print(f"{url},OK", file=log_fp)
        with open(f"{OUT_FOLDER}/{i}.pdf", "wb") as f:
            f.write(response.content)

log_fp.close()
