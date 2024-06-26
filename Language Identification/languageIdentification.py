import sys
import os
import string
import re
import math
from collections import defaultdict
from collections import Counter


"""Input: string (the training text in a given language);
Output: two dictionaries: one dictionary with character-unigram frequencies collected from the
string; one dictionary with character-bigram frequencies collected from the string"""

def computeUnigramFreq(text):
    c = Counter()
    for line in text:
        c+=Counter(line)
    return c 

def computeBigramFreq(text):
    bigram_freq = {}
    text = text.lower()
    for i in range(len(text)-1):
        bigram = text[i:i+2]
        if bigram in bigram_freq:
            bigram_freq[bigram]+=1
        else:
            bigram_freq[bigram]=1
    return bigram_freq

def trainBigramLanguageModel(text):
    unigram_Freq = computeUnigramFreq(text)
    bigram_Freq = computeBigramFreq(text)
    return unigram_Freq, bigram_Freq


"""Input: string (the test text for which the language is to be identified); list of strings (each string
corresponding to a language name); list of dictionaries with unigram character frequencies (each
dictionary corresponding to the single character frequencies in a language); list of dictionaries with
bigram character frequencies (each dictionary corresponding to the bigram character frequencies in
a language)
Output: string (the name of the most likely language)."""


def identifyLanguage(text, languages, unigram_Freq,bigram_Freq):
    vocabulary_size = len(set(text))
    text = text.lower()
    def laplace_smoothed_probability(language,bigram):
        prev_word, current_word = bigram[0],bigram[1]
        prev_word_count = unigram_Freq[language][prev_word]
        count = bigram_Freq[language].get(bigram,0)
        probability = (count+1)/(prev_word_count + vocabulary_size)
        log_probability = math.log(probability)
        return log_probability
    language_probabilities = {}
    for language in languages:
        language_prob = 0
        for i in range(len(text)-1):
            bigram = text[i:i+2]
            language_prob += laplace_smoothed_probability(language,bigram)
        language_probabilities[language] = language_prob
    
    identified_language = max(language_probabilities, key=language_probabilities.get)
    return identified_language


data=[]
folderName = sys.argv[1]
data_folder = os.path.join(os.getcwd(),folderName)
for root,folders,files in os.walk(data_folder):
    for file in files:
        path = os.path.join(root,file)
        with open(path, encoding = "ISO-8859-1") as inf:
            data.append(inf.read())

languages = ["English","French","Italian"]
english_Training = data[0]
french_Training = data[1]
italian_Training = data[2]
english_Unigram, english_Bigram = trainBigramLanguageModel(english_Training)
french_Unigram, french_Bigram = trainBigramLanguageModel(french_Training)
italian_Unigram, italian_Bigram = trainBigramLanguageModel(italian_Training)
language_UnigramFreq = defaultdict(dict)
language_BigramFreq = defaultdict(dict)
language_UnigramFreq["English"] = english_Unigram
language_UnigramFreq["French"] = french_Unigram
language_UnigramFreq["Italian"] = italian_Unigram
language_BigramFreq["English"] = english_Bigram
language_BigramFreq["French"] = french_Bigram
language_BigramFreq["Italian"] = italian_Bigram
test = open("test", encoding = "ISO-8859-1")
line_num = 1
for line in test:
    identified_Language = identifyLanguage(line,languages,language_UnigramFreq,language_BigramFreq)
    print(line_num,identified_Language)
    line_num+=1
