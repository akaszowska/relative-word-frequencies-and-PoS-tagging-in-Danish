'''
Usage in IPython:
from is_it_in import isitin as isin
isin("hus")

Simple function to check if words are included in flexikon or corpus files.

Aleksandra Kaszowska, 09/10/2023
'''

global flexikon
global corpus
global othercorpus

def load_all(flexikon_rows_file,corpus_file,other_corpus_file):
    """
    Parameters
    ----------
    flexikon_rows_file : str: 'filename.txt'
        Flexikon file formatted as rows using convert_flexikon().
        https://korpus.dsl.dk/resources/details/flexikon.html
    corpus_file : str: 'filename.txt'
        Corpus file containing lemmas and their relative frequency.
        https://korpus.dsl.dk/resources/details/freq-lemmas.html
    other_corpus_file: str: 'filename.txt'
        added to compare different versions of lemma corpus

    Returns
    -------
    dataframes for flexikon and corpus
    
    Function
    -------
    
    @AUTHOR: Aleksandra Kaszowska, 09/10/2023
    """
    import pandas as pd
    
    corpus = pd.read_csv(
        corpus_file, 
        sep='\t', 
        header=None, 
        names=['part_of_speech_tag','lemma','relative_frequency']
        )
    
    corpusRecodeDict = {'A':'ADJECTIVE',
                      'C':'CONJUNCTION',
                      'D':'ADVERB',
                      'I':'INTERJECTION',
                      'L':'NUMERAL',
                      'NC':'NOUN',
                      'NP':'PROPER_NOUN',
                      'P':'PRONOUN',
                      'T':'PREPOSITION',
                      'V':'VERB',
                      'U':'UNIQUE',
                      'NW':'POW_NOUN',
                      'LW':'POW_NUMERAL',
                      'M':'POW_MORPH_ITEM',
                      'EW':'POW_LEX_ITEM',
                      'AW':'NO_IDEA',
                      'DW':'NO_IDEA',
                      'TW':'NO_IDEA',
                      'PW':'NO_IDEA',
                      'IW':'NO_IDEA',
                      'VW':'NO_IDEA'}  
    
    corpus = corpus.assign(part_of_speech = corpus.part_of_speech_tag.map(corpusRecodeDict))
    
    ###
    
    flexikon = pd.read_csv(
        flexikon_rows_file, 
        sep='\t', 
        header=None, 
        names=['part_of_speech_tag','lemma','conjugation']
        )
    
    flexikonRecodeDict = {'S':'NOUN',
                        'A':'ADJECTIVE',
                        'V':'VERB',
                        'D':'ADVERB',
                        'F':'ABBREVIATION',
                        'K':'CONJUNCTION',
                        'L':'ONOMATOPEIC_WORD',
                        'O':'PRONOUN',
                        'P':'PROPER_NOUN',
                        'I':'PREFIX',
                        'Æ':'PREPOSITION',
                        'T':'NUMERAL',
                        'U':'INTERJECTION',
                        'X':'UNIDENTIFIED'}  
    
    flexikon = flexikon.assign(part_of_speech = flexikon.part_of_speech_tag.map(flexikonRecodeDict))

    othercorpus = pd.read_csv(
        other_corpus_file, 
        sep='\t', 
        header=None, 
        names=['part_of_speech_tag','lemma','relative_frequency']
        )
    
    othercorpus = othercorpus.assign(part_of_speech = othercorpus.part_of_speech_tag.map(corpusRecodeDict))    

    return flexikon, corpus, othercorpus

flexikon, corpus, othercorpus = load_all('flexikon_rows.txt','lemma-10k-2017-in.txt','lemma-30k-2017.txt')

def isitin(word):
    """
    Parameters
    ----------
    word: string
    
    Returns
    -------
    prints whether the word is contained in flexikon and corpus
    
    Function
    -------
    
    @AUTHOR: Aleksandra Kaszowska, 09/10/2023
    """
    
    a = flexikon.loc[flexikon['conjugation'] == word]
    b = corpus.loc[corpus['lemma'] == word]
    c = othercorpus.loc[othercorpus['lemma'] == word]
    
    if len(a) == 0:
        print(f'\n\nFLEXIKON does not contain word {word}')
    else:
        print('\n\nFLEXIKON:')
        print(a)
        
    if len(b) == 0:
        print(f'\n\nCORPUS-10k does not contain word {word}')
    else:
        print('\n\nCORPUS-10k:')
        print(b)
    
    if len(c) == 0:
        print(f'\n\nCORPUS-30k does not contain word {word}')
    else:
        print('\n\nCORPUS-30k:')
        print(c)
