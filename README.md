# mapaie


## Creating a virtual environment

```
pip install virtualenv
virtualenv venv
```

## Getting started

Clone the repository, and make sure the python package virtualenv is installed.


```
cd mapaie
source venv/bin/activate
pip install -r requirements.txt
```

You can then run `make download` to download PDF files, `make parse` to download and extract their contents. PDF fiels are stored in `./pdfs`, and textual contents in ` ./txts/`.
