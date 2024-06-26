#Kenneth Lam lamken
import sys
import re
import os
from collections import defaultdict
from collections import Counter
import string
import math
import collections
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

acronymPattern = re.compile(r'\b(?:[a-zA-Z]\.){2,}')
numberPattern = re.compile(r'(?:^|\s)(?=.)((?:0|(?:[1-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[1-9])?)(?!\S)')
hyphenPattern = re.compile(r'\b\w*[-]\w*\b')
possessivePattern = re.compile(r"\b\w+'s\b")
datePattern = re.compile(r"\d{1,2}\/\d{1,2}\/\d{2,4}")
#Function that tokenizes the text input string output list
def process(text):
    tokens = text.strip().split()
    processed_tokens = list()
    #tokenization of . (do not tokenize acronyms, abbreviations, numbers) acronyms handled numbers handled 
    #tokenization of ' (expand when needed, e.g., I’m -> I am; tokenize the possessive,e.g., Sunday’s -> Sunday ‘s; etc.) handled
    #tokenization of dates (keep dates together)  handled 
    #tokenization of - (keep texts separated by - together) handled
    #tokenization of , (do not tokenize numbers) handled

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


def trainNaiveBayes(training,test,jokeDict, num_jokes,num_nonjokes,trainingFilesCount):
    if test.startswith('joke'):
        num_jokes-=1 
    if test.startswith('non-joke'):
        num_nonjokes-=1
    TextJokes = [] 
    TextNonJokes = [] 
    probability_joke = num_jokes / trainingFilesCount
    probability_nonjoke = num_nonjokes / trainingFilesCount
    conditionalProbabilitiesJokes = defaultdict(int)
    conditionalProbabilitiesNonJokes = defaultdict(int)
    for file in training: 
        if file.startswith('joke'):
            TextJokes.extend(jokeDict[file])
        elif file.startswith('non-joke'):
            TextNonJokes.extend(jokeDict[file])
    vocab = TextJokes + TextNonJokes
    vocabSize = len(vocab)
    num_words_jokes = len(TextJokes)
    num_words_nonjokes = len(TextNonJokes) 
    wordCountJokes = collections.Counter(TextJokes)
    wordCountNonJokes = collections.Counter(TextNonJokes)
    for word in vocab:
        conditionalProbabilitiesJokes[word] = (wordCountJokes[word] + 1)/ (num_words_jokes + vocabSize)
        conditionalProbabilitiesNonJokes[word] = (wordCountNonJokes[word] + 1)/ (num_words_nonjokes + vocabSize)
    return probability_joke, probability_nonjoke, vocabSize, conditionalProbabilitiesJokes, conditionalProbabilitiesNonJokes, num_words_jokes, num_words_nonjokes



def testNaiveBayes(text, probability_joke, probability_nonjoke, vocabSize, conditionalProbabilitiesJoke, conditionalProbabilitiesNonJoke,num_words_jokes,num_words_nonjokes):
    joke_prob = math.log(probability_joke)
    non_joke_prob = math.log(probability_nonjoke)
    for word in text:
        if word in conditionalProbabilitiesJoke:
            joke_prob+=math.log(conditionalProbabilitiesJoke[word])
        else:
            joke_prob+=math.log(1/(num_words_jokes+vocabSize))
        if word in conditionalProbabilitiesNonJoke:
            non_joke_prob+=math.log(conditionalProbabilitiesNonJoke[word])
        else:
            non_joke_prob+=math.log(1/(num_words_nonjokes+vocabSize))
    if joke_prob > non_joke_prob:
        return 'joke'
    else:
        return 'non-joke'

folderName = sys.argv[1]  
jokeIDs = []
jokeDict = {}
num_files = 0
num_jokes = 0
num_nonjokes = 0

for root,folders,files in os.walk(folderName):
    for file in files:
        path = os.path.join(root,file)
        with open(path, encoding = "ISO-8859-1") as inf:
            jokeID = file.split(".")[0]
            jokeIDs.append(jokeID)
            content = process(inf.read())
            jokeDict[jokeID] = content
            num_files+=1
            if jokeID.startswith('joke'):
                num_jokes+=1
            elif jokeID.startswith('non-joke'):
                num_nonjokes+=1

trainingFilesCount = num_files-1
#repeat n times
pattern = re.compile(r'[0-9]')
correct = 0 

for i in range(len(jokeIDs)):
    test = jokeIDs[i]
    training = jokeIDs[:i] + jokeIDs[i+1:]
    #training 
    results = trainNaiveBayes(training,test,jokeDict, num_jokes,num_nonjokes,trainingFilesCount)
    probability_joke = results[0]
    probability_nonjoke = results[1]
    vocabSize = results[2]
    conditionalProbabilitiesJokes = results[3]
    conditionalProbabilitiesNonJokes = results[4]
    num_words_jokes = results[5]
    num_words_nonjokes = results[6]
    identification = testNaiveBayes(jokeDict[test],probability_joke,probability_nonjoke,vocabSize,conditionalProbabilitiesJokes,conditionalProbabilitiesNonJokes,num_words_jokes,num_words_nonjokes)
    print(test,identification)
    without_number = re.sub(pattern,'',test)
    if without_number == identification:
        correct+=1


accuracy = correct / num_files
print("Accuracy: ", accuracy)


#for answers output
"""
sortedConditionalJokes = sorted(conditionalProbabilitiesJokes.items(), key = lambda x:x[1], reverse= True)
for i in range(10):
    print(sortedConditionalJokes[i])
sortedConditionalNonJokes = sorted(conditionalProbabilitiesNonJokes.items(), key=lambda x:x[1], reverse = True)
print()
for i in range(10):
    print(sortedConditionalNonJokes[i])
"""