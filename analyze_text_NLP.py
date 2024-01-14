def analyze_text_NLP(text_file,corpus_file):
    """
    Parameters
    ----------
    text_file : str: 'filename.txt'
        .txt file containing text to analyze.
    corpus_file : str: 'filename.txt'
        Corpus file containing lemmas and their relative frequency.
        https://korpus.dsl.dk/resources/details/freq-lemmas.html

    Returns
    -------
    .csv file containing all words from text identified by spacy, with relative frequencies from corpus
    .csv file containing all words from text not identified by spacy
    
    Function
    -------
    Use Spacy (https://spacy.io/) and da_core_news_md (https://spacy.io/models/da) model 
    identify words in text and annotate them with relative frequencies from corpus.
    
    @AUTHOR: Aleksandra Kaszowska, 02/10/2023
    """
    
    import pandas as pd
    import spacy 
    from datetime import datetime
    
    nlp = spacy.load('da_core_news_md')
    
    textname = text_file[:-4]
    
    # %%% set up corpus reference
    
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
    corpus = corpus.drop('part_of_speech_tag', axis=1)
        
    # %%% text file setup
    
    text = open(text_file, 'r', encoding='utf-8').read()
    document = nlp(text)
    
    # tag parts of speech
    textTagged = pd.DataFrame(columns=['part_of_speech_tag','lemma','conjugation'])
    
    for token in document:
        datarow = [token.pos_, token.lemma_.lower(), token.text.lower()]
        textTagged.loc[len(textTagged)] = datarow
        
    textTagRecodeDict = {'ADJ':'ADJECTIVE',
                          'ADP':'ADPOSITION',
                          'ADV':'ADVERB',
                          'AUX':'AUXILIARY',
                          'CONJ':'CONJUNCTION',
                          'CCONJ':'COORDINATING_CONJUNCTION',
                          'DET':'DETERIMNER',
                          'INTJ':'INTERJECTION',
                          'NOUN':'NOUN',
                          'NUM':'NUMERAL',
                          'PART':'PARTICLE',
                          'PRON':'PRONOUN',
                          'PROPN':'PROPER_NOUN',
                          'PUNCT':'PUNCTUATION',
                          'SCONJ':'SUBORDINATING_CONJUNCTION',
                          'SYM':'SYMBOL',
                          'VERB':'VERB',
                          'X':'OTHER',
                          'SPACE':'SPACE'}
    
    textTagged = textTagged.assign(part_of_speech = textTagged.part_of_speech_tag.map(textTagRecodeDict))
    
    # drop punctuation
    textTagged = textTagged.drop(textTagged[textTagged['part_of_speech'] == 'PUNCTUATION'].index)
    
    # drop spaces
    textTagged = textTagged.drop(textTagged[textTagged['part_of_speech'] == 'SPACE'].index)
    
    # drop tag
    textTagged = textTagged.drop('part_of_speech_tag', axis=1)
    
    
    # %%% try and match identified lemmas with lemma30k, create two dataframes (missing lemmas and identified lemmas)
    
    currentLemmas = textTagged['lemma'].tolist()
    
    identified = pd.DataFrame(columns=['lemma','relative_frequency','part_of_speech'])
    
    missingWords = set()
    identifiedLemmas=[]
    
    for lemma in currentLemmas:
        a = corpus.loc[corpus['lemma'] == lemma]
        if len(a) == 0:
            missingWords.add(lemma)
        else:
            identified = pd.concat([identified, a], ignore_index=True, sort=False)
            identifiedLemmas.append(lemma)
    
    # %%% match identified words with relative frequencies; 
    # provide dataframe of all word identifications
         
    with open(f'{textname}_missingWords_NLP.txt', 'w') as file:
        for word in missingWords:
            file.write(f'{word}\n')
    
    final = pd.DataFrame(columns=['lemma','conjugation','part_of_speech','relative_frequency'])
    
    x = identified.merge(textTagged, on = ['lemma','part_of_speech'])
    x = x.drop_duplicates()
    
    identifiedWords = textTagged['conjugation'].tolist()
    
    for word in identifiedWords:
        b = x.loc[x['conjugation'] == word]
        final = pd.concat([final,b], ignore_index=True, sort=False)
        
    final = final.drop_duplicates()
    final.to_csv(f'{textname}_identifiedWords_NLP.txt', sep='\t', encoding='utf-8', index=False)
    
    # %%%
    with open(f'{textname}_analysis_summary_NLP.txt', 'w') as file:
        file.write(f'original text analyzed: {text_file}\n')
        file.write("reference model: spacy.load('da_core_news_md')\n")
        file.write(f'corpus reference file: {corpus_file}\n')
        file.write(f'output files: {textname}_missingWords_NLP.txt, {textname}_identifiedWords_NLP.txt\n')
            
        now = datetime.now()
        format_date = now.strftime("%A, %B %d, %Y - %H:%M:%S")
            
        file.write(f'analysis conducted on: {format_date}')     
