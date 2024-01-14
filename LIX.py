def LIX(filename):
    """
    Parameters
    ----------
    filename : str ('filename.txt')
        .txt file containing text to analyze

    Returns
    -------
    int
        LIX score, rounded.
        
    Function
    -------
    Calculates LIX score for text.  
    https://en.wikipedia.org/wiki/Lix_(readability_test)        
    
    @AUTHOR: Aleksandra Kaszowska, 02/10/2023
    """
        
    import re
    
    with open(filename,'r', encoding='utf-8') as file_object:
        contents = file_object.read()
    
    sentenceList = re.split("[//.|//!|//?]", contents)
    sentenceCounter = 0
    sentenceLenCounter = 0
    wordsLongerThanSix = 0

    for eachSentence in sentenceList:
        if eachSentence == '':
            pass
        else:
            sentenceCounter += 1
            noPunctuation = re.sub("-|,|;|:|(|)]",'',eachSentence)
            words = re.split(' ', noPunctuation)
            for eachWord in words:
                if eachWord == '':
                    pass
                else: 
                    sentenceLenCounter += 1
                    if len(eachWord) > 6:
                        wordsLongerThanSix += 1
                
                #print(f"number of sentences: {sentenceCounter}")
                #print(f"number of words: {sentenceLenCounter}")
                #print(f"number of words longer than 6 characters: {wordsLongerThanSix}")

    averageSentenceLen = sentenceLenCounter / sentenceCounter
    #print(f"average sentence length: {averageSentenceLen}")

    wordsLongerProp = wordsLongerThanSix / sentenceLenCounter * 100
    #print(f"proportion of long words: {wordsLongerProp}")

    LIX = averageSentenceLen + wordsLongerProp
    #print(f"LIX score for the passage: {round(LIX)}")
    
    return round(LIX)

