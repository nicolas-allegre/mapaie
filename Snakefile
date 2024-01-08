rule parse:
    input:
        "docs/",
    output:
        directory("txts/")
    shell:
        "python parse_docs.py"

rule download:
    output:
        directory("docs/")
    shell:
        "python dl_docs.py"

rule clean:
    shell:
        "rm  -rf docs txts preprocessed"
