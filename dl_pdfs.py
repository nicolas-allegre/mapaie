import requests
import sys
import os
from random import choice
from tqdm import tqdm


requests.packages.urllib3.disable_warnings()

URL_FILE = "list_urls.txt"
UA_FILE = "user_agents.txt"
OUT_FOLDER = "./pdfs"
LOG_FILE = "dl_pdfs.log"
log_fp = open(LOG_FILE, "w")

list_of_urls = [ x.strip() for x in open(URL_FILE).readlines() ]
user_agents = [ x.strip() for x in open(UA_FILE).readlines() ] 

# Create output directory if it does not exist
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

for i in tqdm(range(len(list_of_urls))):
    url = list_of_urls[i]
    try:
        headers = { "User-Agent": choice(user_agents), "Referer": "http://perdu.com" }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
    except requests.exceptions.RequestException as e:
        print(f"ERR: {url}, {e}", file=log_fp)

    if response.status_code == 200:
        print(f"{url},OK", file=log_fp)
        if ".pdf"[-4:] == ".pdf":
            with open(f"{OUT_FOLDER}/{i}.pdf", "wb") as f:
                f.write(response.content)
        else:
            with open(f"{OUT_FOLDER}/{i}.html", "wb") as f:
                f.write(response.content)

    else:
        # if we received any error http code
        print(f"ERR: {url},{response.status_code}", file=log_fp)

log_fp.close()
