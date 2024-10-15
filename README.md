# mapaie

## Getting started

### Rappel : Creating a virtual environment

```sh
pip install virtualenv
virtualenv venv
```

### Rappel : Creating a SSH key for GIT

1. Création de la clé SSH
```sh
ssh-keygen -t ed25519 -C "MS IA <prenom.nom> GITLAB_Telecom-Paris" -f GITLAB_ENST_SSHKey
```

2. Dépôt sur le GITLAB


3. Test de la connexion
```sh
ssh -i ..\..\..\GITLAB_ENST_SSHKey -T git@gitlab.enst.fr
```

### Getting project environment

1. Create virtual Python environment

```sh
virtualenv venv
source venv/bin/activate

# on Windows
.\venv\Scripts\activate
```

2. Clone the repository
```sh
git clone <URL>
```

3. Configuring GIT
```sh
cd mapaie
git config --local user.name "Prénom Nom"
git config --local user.email "prenom.nom@telecom-paris.fr"
git config --local core.sshCommand "ssh -i C:\\<Path_to_SSHey>\\GITLAB_ENST_SSHKey"
```
 - `--local` pour une configuration local d'un dépôt GIT (mapaie/.git/config)
 - `--global` pour une configuration user de GIT ($HOME/.config/git/config)
 - `--system` pour une configuration PC de GIT (<Path_to_GIT>/etc/gitconfig)

4. Install all requirement
```sh
python -m pip install -r mapaie\requirements.txt
python -m nltk.downloader stopwords
python -m nltk.downloader punkt_tab
```

5. Installation des dépendances externes (voir la doc sur [python-magic](https://pypi.org/project/python-magic/))
- Windows & Mac
```sh
python -m pip install python-magic-bin
```
- Linux (Debian/Ubuntu)
```sh
sudo apt-get install libmagic1
```

## Using

Snakemake should be installed on the side.

You can then run `snakemake -c4` to download PDF files and extract their contents. PDF files are stored in `./pdfs`, and textual contents in ` ./txts/`.

### Manually

Dans l'ordre : 
```sh
python dl_docs.py
python parse_docs.py
python preproccess.py
python create_corpus_before_lang.py
python create_corpus.py -t themes.json -d preprocessed/ -m iramuteq
python create_corpus.py -t themes.json -d preprocessed/ -m cortext
```