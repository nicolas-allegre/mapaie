rule lang:
    input:
        "data/txts/",
    output:
        "data/corpus_lang.csv"
    shell:
        "python create_corpus_before_lang.py"

rule corpus_iramuteq:
    input:
        "data/preprocessed/",
    output:
        directory("data/corpus_iramuteq/")
    shell:
        "python create_corpus.py -t themes.json -d data/preprocessed/ -m iramuteq"

rule corpus_cortex:
    input:
        "data/preprocessed/",
    output:
        directory("data/corpus_cortex/")
    shell:
        "python create_corpus.py -t themes.json -d data/preprocessed/ -m cortext"

rule preprocess:
    input:
        "data/txts/",
    output:
        directory("data/preprocessed/")
    shell:
        "python preprocess.py"

rule parse:
    input:
        "data/docs/",
    output:
        directory("data/txts/")
    shell:
        "python parse_docs.py"

rule download:
    output:
        directory("data/docs/")
    shell:
        "python dl_docs.py"

rule clean:
    shell:
        "rm  -rf docs txts preprocessed"
