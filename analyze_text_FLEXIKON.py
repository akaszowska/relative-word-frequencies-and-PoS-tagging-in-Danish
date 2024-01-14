def analyze_text_FLEXIKON(text_file,flexikon_rows_file,corpus_file):
    """
    Parameters
    ----------
    text_file : str: 'filename.txt'
        .txt file containing text to analyze.
    flexikon_rows_file : str: 'filename.txt'
        Flexikon file formatted as rows using convert_flexikon().
        https://korpus.dsl.dk/resources/details/flexikon.html
    corpus_file : str: 'filename.txt'
        Corpus file containing lemmas and their relative frequency.
        https://korpus.dsl.dk/resources/details/freq-lemmas.html

    Returns
    -------
    .csv file containing all words from text identified in flexikon, with relative frequencies from corpus
    .csv file containing all words from text missing from flexikon and corpus
    
    Function
    -------
    Find words in text, check for their presence in flexikon, annotate with relative frequencies from corpus.
    If word not in flexikon but in corpus, add to identified word list too.
    
    Examples
    --------
    analyze_text_FLEXIKON("SAMPLE_TEXT.txt", "flexikon_rows.txt", "lemma-30k-2017.txt")
    
    @AUTHOR: Aleksandra Kaszowska, 14/01/2024
    
    version update from 05/10/2023: 
        - fixed how punctuation is removed from words to allow for multiple paragraphs in target text file.
    """
    
    import pandas as pd
    import re 
    from datetime import datetime
        
    # %%% set up references: corpus and flexikon
    
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
    
    
    # %%% separate textfile words using regex
    
    with open(text_file,'r', encoding='utf-8') as file_object:
        contents = file_object.read()
    
    sentenceList = re.split("[//.|//!|//?|\n|\r]", contents) # separate into sentences on> . ! ?
    wordList = list()
    
    for eachSentence in sentenceList:
        if eachSentence == '':
            pass
        else: 
            noPunctuation = re.sub(r'[^\w\s]','',eachSentence) # remove punctuation from individual words
            words = re.split(' ', noPunctuation)
            for eachWord in words:
                if eachWord == '':
                    pass
                else: 
                    wordList.append(eachWord.lower())
            
    # %%% try and match conjugated words from text with all options in flexikon, create two dataframes (missing and identified)
    
    identified = pd.DataFrame(columns=['part_of_speech_tag','lemma','conjugation','part_of_speech'])
    corpusOnly = pd.DataFrame(columns=['part_of_speech_tag','lemma','relative_frequency','part_of_speech'])
    
    missingWords = set()
    identifiedWords = []
    corpusOnlyWords = []
    
    for word in wordList:
        a = flexikon.loc[flexikon['conjugation'] == word]
        c = corpus.loc[corpus['lemma'] == word.capitalize()]
        d = corpus.loc[corpus['lemma'] == word]
        if len(a) == 0 and len(c) == 0 and len(d) == 0:
            missingWords.add(word)
        elif len(a) == 0 and len(c) != 0 and len(d) == 0:
            corpusOnly = pd.concat([corpusOnly, c], ignore_index=True, sort=False)
            corpusOnlyWords.append(word)
        elif len(a) == 0 and len(c) == 0 and len(d) != 0:
            corpusOnly = pd.concat([corpusOnly, d], ignore_index=True, sort=False)
            corpusOnlyWords.append(word)
        else:
            identified = pd.concat([identified, a], ignore_index=True, sort=False)
            identifiedWords.append(word)
    
    # %%% match identified words with relative frequencies from corpus; 
    # provide dataframe of all possible lemma/word/part of speech identifications
    
    storyname = text_file[:-4]        

    identified = identified.drop('part_of_speech_tag', axis=1)
    corpusOnly = corpusOnly.drop('part_of_speech_tag', axis=1)
    
    corpusOnly.insert(1, 'conjugation', corpusOnly['lemma']) # for words directly from corpus, lemma = conjugation
    corpusOnly['conjugation'] = corpusOnly['conjugation'].apply(lambda x: x.lower() if isinstance(x, str) else x)

    final = pd.DataFrame(columns=['lemma','conjugation','part_of_speech','relative_frequency'])
    
    identified = identified.drop('part_of_speech', axis=1)
    
    x = identified.merge(corpus, on=['lemma'])
    x = x.drop_duplicates()
    x = x.drop('part_of_speech_tag',axis=1)
    
    for word in identifiedWords:
        b = x.loc[x['conjugation'] == word]
        if len(b) != 0:
            final = pd.concat([final,b], ignore_index=True, sort=False)
        else:
            missingWords.add(word)

    
    final = pd.concat([final,corpusOnly], ignore_index=True, sort=False)     
    final = final.drop_duplicates()
        
    final.to_csv(f'{storyname}_identifiedWords_FLEXIKON.txt', sep='\t', encoding='utf-8', index=False)  
    
    with open(f'{storyname}_missingWords_FLEXIKON.txt', 'w') as file:
        for word in missingWords:
            file.write(f'{word}\n')

    # %%% create summary file

    with open(f'{storyname}_analysis_summary_FLEXIKON.txt', 'w') as file:
        file.write(f'original text analyzed: {text_file}\n')
        file.write(f'flexikon reference file: {flexikon_rows_file}\n')
        file.write(f'corpus reference file: {corpus_file}\n')
        file.write(f'output files: {storyname}_missingWords_FLEXIKON.txt, {storyname}_identifiedWords_FLEXIKON.txt\n')
        
        now = datetime.now()
        format_date = now.strftime("%A, %B %d, %Y - %H:%M:%S")
        
        file.write(f'analysis conducted on: {format_date}')     