import json
import re
import hardcodes
from porter_stemmer import PorterStemmer
from collections import defaultdict
import math
def cleanAToken(token):
    cleaned_string = token
    if token[len(token)-1] == ',':
        cleaned_string = cleaned_string[:-1]
    cleaned_string = re.sub('[\(\)\[\]\\\.\,\/\=\?\:\=\$]','', cleaned_string)
    return cleaned_string

def tokenize_helper(text):
    dirty_tokens = text.split()
    clean_tokens = []

    for token in dirty_tokens:
        clean = True
        token = cleanAToken(token)
        if len(token) == 0:
            continue

        # delete numbers
        if token.isdigit():
            clean = False

        # remove stopwords
        if token in hardcodes.stopwords:
            clean = False
        
        # handle contractions case
        if token in hardcodes.contractions_dict.keys():
            new_tokens = hardcodes.contractions_dict[token].split(' ')
            for i in range(len(new_tokens)):
                clean_tokens.append(new_tokens[i])
            clean = False # already appended to clean tokens, no need to add again

        if clean:
            clean_tokens.append(token) 

    return clean_tokens

def tokenize(text):
    full_tokens = tokenize_helper(text)
    filtered_tokens = [token for token in full_tokens if re.match(r'^[a-zA-Z\-]+$', token)]
    
    clean_tokens = []
    stemmer = PorterStemmer()
    for word in filtered_tokens:
        stemmed_word = stemmer.stem(word, 0, len(word) - 1)
        clean_tokens.append(stemmed_word)
    
    return clean_tokens

def load_doc_text():
    doc_text_local_for_load = {}
    with open('youtube-transcriptions.jsonl', 'r') as f:
        for line in f:
            line = json.loads(line)
            tokens = tokenize(line['text'])

            if doc_text_local_for_load.get(line['title'], 0) == 0:
                doc_text_local_for_load[line['title']] = tokens 
            else:
                doc_text_local_for_load[line['title']] += (tokens)
    
    print(doc_text_local_for_load)

def load_within_doc_text():
    within_doc_for_load = {}
    with open('youtube-transcriptions.jsonl', 'r') as f:
        for line in f:
            line = json.loads(line)
            tokens = tokenize(line['text'])

            if within_doc_for_load.get(line['title'], 0) == 0:
                within_doc_for_load[line['title']] = {} 
            
            within_doc_for_load[line['title']][line['start']] = tokens 
    return within_doc_for_load

def indexDocument(within_doc_text):
    invertedIndex = defaultdict(dict)
    tfIDFtext = defaultdict(dict)
    for title in within_doc_text.keys():
        for timestamps in within_doc_text[title]:
            text = within_doc_text[title][timestamps]
            for word in text:
                count = text.count(word)
                invertedIndex[word][" ".join(text)] = count
    DF = defaultdict(int)
    for word,content in invertedIndex.items():
        DF[word] = len(content)
    IDF = defaultdict(float)
    for word in invertedIndex.keys():
        doc_Frequency = DF[word]
        IDF[word] = math.log((208619+1)/(doc_Frequency+1),10)
    for title in within_doc_text.keys():
        for timestamps in within_doc_text[title]:
            text = within_doc_text[title][timestamps]
            for word in text:
                weight = IDF[word] * invertedIndex[word][" ".join(text)]
                tfIDFtext[word][" ".join(text)] = weight
    return tfIDFtext

if __name__ == '__main__':
    # leaving these two function calls commented out as they only need 
    # to be ran once to get the data in a clean format
    # load_doc_text()
    within_doc_text = load_within_doc_text()
    print(indexDocument(within_doc_text))
    