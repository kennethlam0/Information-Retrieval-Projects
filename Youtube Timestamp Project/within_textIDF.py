#Kenneth Lam 
from collections import defaultdict
import math
#function that calculates the tfIDF for each word in the text
def within_textIDF(within_doc_text):
    #create inverted index dictionary of dictionaries
    invertedIndex = defaultdict(dict)
    #Dictionary tdIDFtext indexed by title, timestamp, word 
    tfIDFtext = {}
    #loop through title, timestamps, word
    for title in within_doc_text.keys():
        #loop through timestamps in within_doc_text
        for timestamps in within_doc_text[title]:
            #get text from within_doc_text
            text = within_doc_text[title][timestamps]
            #loop through words in text
            for word in text:
                #count words in text 
                count = text.count(word)
                #set count in inverted index
                invertedIndex[word][" ".join(text)] = count
    #calcualte document frequency of words
    DF = defaultdict(int)
    #loop through word, content in inverted index to find document frequency of each word
    for word,content in invertedIndex.items():
        #set document frequency of word
        DF[word] = len(content)
    #Calculate IDF fo each word from inverted index
    IDF = defaultdict(float)
    #Calculate IDF fo each word from inverted index 
    for word in invertedIndex.keys():
        #set document frequency of word
        doc_Frequency = DF[word]
        #set IDF of word
        IDF[word] = math.log((208619+1)/(doc_Frequency+1),10)
    #loop through title, timestamps, word 
    for title in within_doc_text.keys():
        #set title in tfIDFtext
        tfIDFtext[title.encode("utf-8")] = {}
        #loop through timestamps in within_doc_text
        for timestamps in within_doc_text[title]:
            #get text from within_doc_text
            text = within_doc_text[title][timestamps]
            #set timestamps in tfIDFtext
            tfIDFtext[title.encode("utf-8")][timestamps] = {}
            #calculate tfIDF for each word and set weight in dictionary 
            for word in text:
                #set weight of word
                weight = IDF[word] * invertedIndex[word][" ".join(text)]
                #set weight of word in tfIDFtext
                tfIDFtext[title.encode("utf-8")][timestamps][word]= weight
    return tfIDFtext

