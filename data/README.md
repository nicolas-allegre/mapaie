## Data folder

This folder contain results and data for mapaie project.

- `data/docs/` : contain downloaded fairness manisfesto of mapaie (PDF & HTML)
- `data/txts/` : contain parsed data in text form of docs files (same filename)
- `data/preprocessed/`: contain cleaned data of txts files (same filename)
- *`data/corpus_iramuteq/corpus.txt`* : contain analysed and classified corpus from preprocessed file by IRAMUTEQ method
- `data/corpus_cortex/` : contain analysed and classified corpus from preprocessed file by CORTEX method
  - `category_x/` : contain originals files from txts files which has been classified in this category by CORTEX method
- *`data/corpus_lang.csv`* : contain lang detection for each file of `txts/`
- *`data/corpus_lang_preprocessing.csv`* : contain lang detection for each file of `preprocessed/`
- *`data/mapaie-metadata.csv`* : contain remainder of title of each file of `txts` (from all_manifestos.csv)
- `data/amr` : contain amr analysed file of `txt`
  - *`key_penmans.amr`* : contain penman syntax in AMR form of each sentences in txts files having 'fearness'
  - `id_n.png` : graph of an AMR sentences in `key_penmans.amr` for a specific filename (txts)
