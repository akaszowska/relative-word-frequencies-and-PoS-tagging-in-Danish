# Relative word frequencies and PoS tagging (in Danish)
Summary: Code for working with texts; calculating LIX score, comparing text content against corpora, tagging words with individual frequencies, and GUI for manually tagging words with part of speech/manually confirming tagging results. 

This respository allows the user to semi-automate text analysis. There are two separate pipelines for this:
- the **FLEXIKON** pipeline: target text is broken down into words; lemma identification is done based on [Flexikon](https://korpus.dsl.dk/resources/details/flexikon.html) matching; relative frequency tagging is done based on [relative frequency of lemmas in Danish corpus](https://korpus.dsl.dk/resources/details/freq-lemmas.html). There is no automated part of speech tagging in this pipeline.
- the **NLP** pipeline: target text is broken down into words; lemma identification and part of speech tagging is automated through [spacy](https://spacy.io/) with [da_core_news_md model](https://spacy.io/models/da); relative frequency tagging is done based on [relative frequency of lemmas in Danish corpus](https://korpus.dsl.dk/resources/details/freq-lemmas.html).

Both pipelines produce input for **manual annotation GUI**, where the user interacts with a simple interface to review automated part of speech tagging by the NLP pipeline or to manually tag part of speech for the flexikon pipeline. 

The following code could work with any language, but has been tested specifically on Danish and relies on external resources below. It should be possible to use the code to work with other languages, assuming that similar resources with identical formatting are available in those languages. 

## Prerequisites
- Python 3.5+ (code last tested on Python 3.12) with following repositores: [pandas](https://pandas.pydata.org/)
- the **NLP** pipeline relies on [spacy](https://spacy.io/) with [da_core_news_md model](https://spacy.io/models/da)
- the **FLEXIKON** pipeline relies on [Flexikon](https://korpus.dsl.dk/resources/details/flexikon.html), a word list containing more than 80.000 lemmas, each lemma form including information on all possible inflectional forms. In the code, each individual word from target text is matched with the inflectional form in Flexikon, and then tagged with the corresponding lemma.
- both pipelines rely on [Relative frequency of lemmas in Danish corpus](https://korpus.dsl.dk/resources/details/freq-lemmas.html), a list of most frequently used lemmas in Danish language, including their relative frequencies. In the code, each lemma identified with help of flexikon is searched for in this corpus, and tagged with the corresponding relative frequency.

Note: Flexikon and Corpus files are **not** included in the repository due to copyright and use conditions. Users will need to acquire the files directly from [DSL](https://korpus.dsl.dk/resources/index.html) or use a different corpus. 

## FLEXIKON PROCESSING PIPELINE
### Step 1: format Flexikon file (code: _convert_flexikon.py_) from list to table
This step needs to be performed only once, and the formatted flexikon file will be used in all subsequent steps. 

original/input format:

![image](https://github.com/akaszowska/relative-word-frequencies-and-PoS-tagging-in-Danish/assets/48135520/1d010486-55c1-46d3-820f-2fecd12a1022)

formatted/output format (three columns, tab separated: part of speech tag, lemma, inflectional form):

![image](https://github.com/akaszowska/relative-word-frequencies-and-PoS-tagging-in-Danish/assets/48135520/42af09cf-44a1-4fa7-9805-3f24c6a600ca)

### Step 2: analyze text (code: _analyze_text_FLEXIKON.py_)
inputs: 
- target text (in .txt format), formatted Flexikon file, frequency corpus file (three colums, tab separated: part of speech tag, lemma, relative frequency).

outputs: 
- analysis_summary.txt: includes original text file name, reference files, output files, and date and time analysis was conducted.
- identified_words.txt: four columns, tab separated; lemma, inflectional form (header conjugation), part of speech, and relative frequency. **Note** that the flexikon pipelline _does not_ automate part of speech tagging for individual words. Instead, the output file lists _all possible parts of speech_ that match a specific word, independent of context. For example, _dansk_ could be an adjective or a noun depending on context: the output will list both options, and you will have to manually choose the correct option in step 3. 
- missing_words.txt: list of words that were not identified either in flexikon or corpus.

### Step 3: manual annotation/checking (code: _annotate_pos_allWords.py_ or _annotate_pos_conflictWords.py_)
There are two options for manual annotation: 
- **allWords**: user goes word by word and tags all words, including the words with only one possibility for tagging
- **conflictWords**: user only manually tags words where the text analysis indicated several possible parts of speech; all words with only one identified options are tagged automatically. 

## Processing pipeline for relying on NLP LALALA



