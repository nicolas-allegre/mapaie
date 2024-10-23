import os

CHARSET = 'UTF-8'


def loadData(data_folder: str) -> dict[str, list[str]]:
    """Load text in each file in a dict.
    
    :param str data_folder: Folder path where txt files are
    :return [filename]=str: Dict with key are filename and value file data
    """
    corpus: dict[str, list[str]] = {}
    
    for root, dirs, files in os.walk(data_folder):
        for file_name in files:
            data = None
            file_path = os.path.join(root, file_name)
            if os.path.getsize(file_path) <= 2:  # fichier vide
                print(f"{file_name} : Fichier vide")
                continue
            with open(file_path, 'r', encoding=CHARSET) as file:
                data = file.read()
                if len(data.strip()) == 0:
                    print(f"{file_name} : Fichier vide")
                    continue
                corpus[file_name] = data
                # end if
            # end with
        # end for
    # end for
    return corpus
# end def loadData
