download:
	rm -rf pdfs/; mkdir pdfs/
	python dl_pdfs.py
parse:
	rm -rf txts/; mkdir txts/
	python parse_pdfs.py

all: | download parse
	echo "done."
clean:
	rm -f *.log
