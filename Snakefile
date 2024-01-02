rule parse:
    input:
        "pdfs/",
    output:
        "txts/"
    shell:
        "python parse_docs.py"

rule download:
    output:
        directory("pdfs/")
    shell:
        "python dl_docs.py"
