# python -m pip install langdetect

import os
import sys

from langdetect import detect
from langdetect import detect_langs

LOG_FOLDER = 'log/'
LOG_FILENAME = 'corpus_lang.log'
LOG_FILE = os.path.join(LOG_FOLDER, LOG_FILENAME)
CHARSET = 'UTF-8'
DEFAULT_FOLDER_PREPROCESSED = 'data/preprocessed/'


def normalise_folder(path: str) -> str:
    """Change le chemin en format UNIX (/) et ajoute le / final si inexistant.

    :param str path: Chemin de dossier à normaliser
    :return str: le chemin remis en forme
    """
    path = path.replace('\\', '/')
    if (path[-1] != '/'):
        path = path + '/'
    # end if
    return path
# end def normalise_folder


data_folder = DEFAULT_FOLDER_PREPROCESSED
if len(sys.argv) > 1:
    data_folder = sys.argv[1]

data_folder = normalise_folder(data_folder)
if not os.path.exists(data_folder):
    print("Dossier inexistant !", file=sys.stderr)
    sys.exit(-1)

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
log_fp = open(LOG_FILE, "w", encoding=CHARSET)

for root, dirs, files in os.walk(data_folder):
    for file_name in files:
        data = None
        lang_detect = '-'
        langs_detect = '-'
        file_path = os.path.join(root, file_name)
        if os.path.getsize(file_path) <= 2:  # fichier vide
            print(f"{file_name} : Fichier vide", file=log_fp)
            continue
        with open(file_path, 'r', encoding=CHARSET) as file:
            data = file.read()
            lang_detect = detect(data)
            langs_detect = detect_langs(data)
            print(f"{file_name} : {lang_detect} ({langs_detect})", file=log_fp)
            # end if
        # end with
    # end for
# end for

log_fp.close()
