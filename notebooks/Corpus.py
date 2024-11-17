import itertools
import os

PATH_DATA_FOLDER = '../data'
PATH_LOG_FOLDER = '../log'
PATH_DATA_TXT = '../data/txts'
PATH_DATA_DOCS = '../data/docs'
PATH_DATA_PREPROCESSED = '../data/preprocessed'
PATH_DATA_CORTEX = '../data/corpus_cortext'
PATH_DATA_IRAMUTEQ = '../data/corpus_iramuteq'
FILENAME_DATA_IRAMUTEQ = 'corpus.txt'
FILENAME_DATA_LANG = 'corpus_lang.csv'
FILENAME_DATA_LANG_PREPRO = 'corpus_lang_preprocessing.csv'
PATH_DATA_FILE_LANG = os.path.join(PATH_DATA_FOLDER, FILENAME_DATA_LANG)
PATH_DATA_FILE_IRAMUTEQ = os.path.join(PATH_DATA_IRAMUTEQ, FILENAME_DATA_IRAMUTEQ)
TYPE_METHOD = ['cortex', 'iramuteq', 'txt']
CHARSET = 'UTF-8'


class Corpus():
    """Charge un corpus issu de diverse méthode pour une utilisation unique.

    Attributes:
        data dict[str, str]: pour chaque fichier (clés = nom de fichier), son contenu
        tags dict[str, list[str]] : pour chaque fichier (clés = nom de fichier), les tags suivant le découpage de la méthode
        type_model str: le model/méthode dont sont issu les données (txt, cortex, iramuteq)

    Methods:
        load(self, type_method: str) -> None
        get_corpus(self) -> str
        get_filename(self) -> list[str]
        get_tags(self) -> set[str]
    """

    data: dict[str, str] = {}
    tags: dict[str, list[str]] = {}
    type_model: str = ''

    def __init__(self, type_method: str = TYPE_METHOD[2], load: bool = True):
        """Initialise la classe en chargant les données suivant la méthode.

        :param str type_method: charge les textes de la méthode fournie
            'cortex' => charge les fichiers issus de l'analyse CORTEX
            'iramuteq' => charge les fichiers issus de l'analyse IRAMUTEQ
            'txt' => [DEFAUT] charge les fichiers bruts TXT issus du parsing de PDF/HTML
        :param bool load: spécifie s'il faut charger les données [DEFAUT=True]
        """
        self.type_model = type_method
        if type_method not in (TYPE_METHOD[0], TYPE_METHOD[1]):
            self.type_model = TYPE_METHOD[2]  # 'txt'

        if load is True:
            self.load(self.type_model)

    def load(self, type_method: str) -> None:
        """Charge les textes en fonction de la méthode choisie.

        :param str type_method: charge les textes de la méthode fournie
            'cortex' => charge les fichiers issus de l'analyse CORTEX
            'iramuteq' => charge les fichiers issus de l'analyse IRAMUTEQ
            'txt' => charge les fichiers bruts TXT issus du parsing de PDF/HTML
        """
        if type_method == TYPE_METHOD[0]:  # 'cortex'
            self.load_cortex()
        elif type_method == TYPE_METHOD[1]:  # 'iramuteq'
            self.load_iramuteq()
        else:  # 'txt'
            self.load_txt()

    def load_cortex(self) -> None:
        """Charge les textes issus de l'analyse CORTEX."""
        self.data = {}
        self.tags = {}
        folder_cortex = [x for x in os.listdir(PATH_DATA_CORTEX) if os.path.isdir(os.path.join(PATH_DATA_CORTEX, x))]
        file_txt = [x for x in os.listdir(PATH_DATA_TXT) if x.endswith('.txt')]
        if file_txt == []:
            file_txt = [x for x in os.listdir(PATH_DATA_PREPROCESSED) if x.endswith('.txt')]

        self.data = dict.fromkeys(file_txt, '')
        self.tags = dict.fromkeys(file_txt, [])
        for tag in folder_cortex:
            for file in os.listdir(os.path.join(PATH_DATA_CORTEX, tag)):
                if file not in file_txt:  # Pas un fichier du corpus
                    continue
                self.tags[file].append(tag)
                if self.data[file] == '':  # ne charge qu'une seule fois le fichier
                    with open(os.path.join(PATH_DATA_CORTEX, tag, file), 'r', encoding=CHARSET) as f:
                        self.data[file] = f.read().strip()

    def load_iramuteq(self) -> None:
        """Charge les textes issus de l'analyse IRAMUTEQ."""
        self.data = {}
        self.tags = {}
        lines: list[str] = []
        with open(PATH_DATA_FILE_IRAMUTEQ, 'r', encoding=CHARSET) as f:
            lines = f.readlines()

        file_txt = [x for x in os.listdir(PATH_DATA_TXT) if x.endswith('.txt')]
        if file_txt == []:
            file_txt = [x for x in os.listdir(PATH_DATA_PREPROCESSED) if x.endswith('.txt')]

        nb_file = len(file_txt)
        i = 0
        for line in lines:
            if i > nb_file:
                file = str(i)
            else:
                file = file_txt[i]

            if line.startswith("****"):
                self.tags[file] = line.strip().split(' *')[1:]
            else:
                self.data[file] = line.strip()
                i += 1

    def load_txt(self) -> None:
        """Charge les fichiers bruts TXT issus du parsing de PDF/HTML."""
        self.data = {}
        self.tags = {}
        for file in os.listdir(PATH_DATA_TXT):
            if not file.endswith('.txt'):  # Pas un fichier du corpus
                continue
            with open(os.path.join(PATH_DATA_TXT, file), 'r', encoding=CHARSET) as f:
                self.data[file] = f.read().strip()
                self.tags[file] = []

    def get_corpus(self) -> str:
        """Retourne l'ensemble des textes concaténés.

        :return str: fusion du contenu des fichiers
        """
        return ''.join(self.data.values())

    def get_filename(self) -> list[str]:
        """Retourne la liste des noms de fichier.

        :return list[str]: liste des noms de fichiers
        """
        return list(self.data.keys())

    def get_tags(self) -> set[str]:
        """Retourne tout les tags utilisés par la méthode.

        :return set[str]: liste des tags de la méthode
        """
        return set(itertools.chain.from_iterable(self.tags.values()))
