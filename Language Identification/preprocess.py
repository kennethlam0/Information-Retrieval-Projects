import re
import string
import sys
import os 
from collections import defaultdict
#Function that removes the SGML tags from the input string. input string output string
def removeSGML(text):
    pattern = re.compile(r'<.*?>')
    clean = re.sub(pattern,'',text)
    return clean

contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}


#Function that tokenizes the text input string output list
def tokenizeText(text):
    tokens = text.strip().split()
    processed_tokens = list()
    #tokenization of . (do not tokenize acronyms, abbreviations, numbers) acronyms handled numbers handled 
    #tokenization of ' (expand when needed, e.g., I’m -> I am; tokenize the possessive,e.g., Sunday’s -> Sunday ‘s; etc.) handled
    #tokenization of dates (keep dates together)  handled 
    #tokenization of - (keep texts separated by - together) handled
    #tokenization of , (do not tokenize numbers) handled
    acronymPattern = re.compile(r'\b(?:[a-zA-Z]\.){2,}')
    numberPattern = re.compile(r'(?:^|\s)(?=.)((?:0|(?:[1-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[1-9])?)(?!\S)')
    hyphenPattern = re.compile(r'\b\w*[-]\w*\b')
    possessivePattern = re.compile(r"\b\w+'s\b")
    datePattern = re.compile(r"\d{1,2}\/\d{1,2}\/\d{2,4}")

    for token in tokens:
        curr_token = token.lower()
        if re.search(acronymPattern,curr_token):
            processed_tokens.append(curr_token)
    
        elif re.search(numberPattern,curr_token):
            processed_tokens.append(curr_token)
        
        elif re.search(hyphenPattern, curr_token):
            processed_tokens.append(curr_token)
        
        elif curr_token in contractions:
            processed_tokens.append(contractions[curr_token])

        elif re.search(possessivePattern,curr_token):
            processed_tokens.append(curr_token[:-2])
            processed_tokens.append('\'s')

        elif re.search(datePattern,curr_token):
            processed_tokens.append(curr_token)
        else:
            processed_tokens.append(curr_token.translate(str.maketrans('','',string.punctuation)))

    return processed_tokens

def word_freq(tokens):
    char_freq = {}
    for token in tokens:
            if token not in char_freq:
                char_freq[token] = 1
            else:
                char_freq[token]+=1
    return char_freq

def char_freq(word_freq):
    vocab = []
    for word in word_freq.keys():
        for letter in word:
            if letter not in vocab:
                vocab.append(letter)
    return vocab

def get_pair_freq(parts,word_frequency):
    pairs = {}
    for word,freq in word_frequency.items():
        part = parts[word]
        if len(part)==1:
            continue
        for i in range(len(part)-1):
            pair = (part[i],part[i+1])
            current_freq = pairs.get(pair,0)
            pairs[pair] = current_freq + freq
    return pairs

def merge_most_common_pair(prev,next,parts,word_freq):
    for word in word_freq:
        part = parts[word]
        if len(part)==1:
            continue
        i=0
        while i < len(part) -1:
            if part[i] == prev and part[i+1]==next:
                part = part[:i] + [prev+next] + part[i+2:]
            else:
                i+=1
        parts[word] = part
    return parts


def calc_min_BPE(merged_list_vocab,sorted_word_freq_all):
    N = len(merged_list_vocab)
    x=0.25*N
    num = 0
    curr_sum = 0
    for i in range(len(sorted_word_freq_all)):
        curr_sum+=sorted_word_freq_all[i][1]
        num+=1
        if curr_sum>=x:
            break
    return num   

#Function that performs Byte-Pair Encoding tokenization. Input: list of tokens vocab size Output list(of subword tokens), list of merge rules 
def BPE(tokens,vocabSize):
    word_frequency = word_freq(tokens)
    vocab = char_freq(word_frequency)
    parts = {word:[c for c in word] for word in word_frequency.keys()}
    merge_rules = []
    while len(vocab) < vocabSize:
        pairs = get_pair_freq(parts,word_frequency)
        if not pairs:
            break
        best_pair = max(pairs,key=pairs.get)
        best_pair_freq = max(pairs.values())
        parts = merge_most_common_pair(*best_pair,parts,word_frequency)
        merge_rules.append(('(' + best_pair[0] + ',' + best_pair[1] + ')',best_pair[0] + best_pair[1]))
        vocab.append((best_pair[0] + best_pair[1]))
    return merge_rules,vocab

folderName = sys.argv[1]
vocabSize = sys.argv[2]
data_folder = os.path.join(os.getcwd(),folderName)
merge_rules = []
vocab = []
for root,folders,files in os.walk(data_folder):
    for file in files:
        path = os.path.join(root,file)
        with open(path, encoding = "ISO-8859-1") as inf:
            inf = removeSGML(inf.read())
            tokens = tokenizeText(inf)
            bpe = BPE(tokens,int(vocabSize))
            if bpe[0]:
                merge_rules.append(bpe[0])
            if bpe[1]:
                vocab.append(bpe[1])
merged_list_rules = [a for b in merge_rules for a in b]
merged_list_vocab = [a for b in vocab for a in b]

#Total number of BPE tokens
print("Total number of BPE tokens:",len(merged_list_vocab))
#Total number of merge rules
print("Total number of merge rules:",len(merged_list_rules))
#First 20 merge rules
"""print("First 20 merge rules:")
for i in range(20):
    print(merged_list_rules[i])"""
#Top 50 tokens 
word_freq_all = defaultdict(int)
for root,folders,files in os.walk(data_folder):
    for file in files:
        path = os.path.join(root,file)
        with open(path, encoding = "ISO-8859-1") as inf:
            inf = removeSGML(inf.read())
            tokens = tokenizeText(inf)  
            for token in tokens:
                if token in merged_list_vocab:
                        word_freq_all[token]+=1
sorted_word_freq_all = sorted(word_freq_all.items(),key=lambda x:x[1],reverse=True)
"""print("Top 50 tokens:")
for i in range(50):
    print(sorted_word_freq_all[i])"""
print("Mininum number of BPE tokens accounting for 25% of total BPE tokens:",calc_min_BPE(merged_list_vocab,sorted_word_freq_all))