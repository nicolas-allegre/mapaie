rule all:
    input:
        "pdfs/",
    output:
        "txts/"
    shell:
        "python parse_pdfs.py"
