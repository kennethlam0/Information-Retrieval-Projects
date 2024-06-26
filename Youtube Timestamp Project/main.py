import json
import re
import hardcodes
import math
import sys
from porter_stemmer import PorterStemmer
from vsm import VSM
from within_textIDF import within_textIDF
from within_doc_termweights import within_doc_termweights
from queryvec import calculate_query_vector
from doc_term_weights import doc_term_weights
from links_database import links_database

# function that takes in a string and cleans it
def cleanAToken(token):
    # set cleaned string to token
    cleaned_string = token
    # if token of length -1 is a comma
    if token[len(token)-1] == ',':
        # remove trailing comma
        cleaned_string = cleaned_string[:-1]
    # use regex to remove any unwanted characters
    cleaned_string = re.sub('[\(\)\[\]\\\.\,\/\=\?\:\=\$]','', cleaned_string)
    # return
    return cleaned_string

# function that takes in a string and tokenizes it HELPER
def tokenize_helper(text):
    # split the text into tokens
    dirty_tokens = text.split()
    # create a list to store the clean tokens
    clean_tokens = []


    # loop through the tokens
    for token in dirty_tokens:
        # set clean to true
        clean = True
        # set token to cleaned token
        token = cleanAToken(token)

        # if the token is empty, skip
        if len(token) == 0:
            continue

        # delete numbers
        if token.isdigit():
            # set clean to false
            clean = False

        # remove stopwords
        if token in hardcodes.stopwords:
            # set clean to false
            clean = False
        
        # handle contractions case
        # if token is in the contractions dictionary
        if token in hardcodes.contractions_dict.keys():
            # split the token into a list of words
            new_tokens = hardcodes.contractions_dict[token].split(' ')
            # loop through the new tokens
            for i in range(len(new_tokens)):
                # append the new tokens to the clean tokens
                clean_tokens.append(new_tokens[i])
            clean = False # already appended to clean tokens, no need to add again
        
        # if the token is clean
        if clean:
            # append the token to the clean tokens  
            clean_tokens.append(token) 

    return clean_tokens


# function that takes in a string and tokenizes it
def tokenize(text):
    # call the helper function to tokenize the text
    full_tokens = tokenize_helper(text)
    # create a list to store the filtered tokens
    filtered_tokens = [token for token in full_tokens if re.match(r'^[a-zA-Z\-\&]+$', token)]
    
    # create a list to store the stemmed tokens
    clean_tokens = []
    # create a stemmer object
    stemmer = PorterStemmer()
    # loop through the filtered tokens
    for word in filtered_tokens:
        # stem the word
        stemmed_word = stemmer.stem(word, 0, len(word) - 1)
        # append the stemmed word to the clean tokens
        clean_tokens.append(stemmed_word)
    
    return clean_tokens

# function that loads the document text
def load_doc_text():
    # create a dictionary to store the document text
    doc_text_local_for_load = {}
    # open the youtube-transcriptions.jsonl file
    with open('youtube-transcriptions.jsonl', 'r') as f:
        # loop through the lines in the file
        for line in f:
            # load the line as a json object
            line = json.loads(line)
            # tokenize the text
            tokens = tokenize(line['text'])

            # if the title is not in the dictionary
            if doc_text_local_for_load.get(line['title'], 0) == 0:
                # add the title to the dictionary
                doc_text_local_for_load[line['title']] = tokens 
                # if the title is in the dictionary
            else:
                # append the tokens to the title in the dictionary
                doc_text_local_for_load[line['title']] += (tokens)
    
    #print(doc_text_local_for_load)
    # If the youtube video collection gets updated then uncomment
    # the line below to generate a new text file for vsm
    #page(doc_text_local_for_load)

# function that loads the within document text
def load_within_doc_text():
    # create a dictionary to store the within document text
    within_doc_for_load = {}
    # open the youtube-transcriptions.jsonl file
    with open('youtube-transcriptions.jsonl', 'r') as f:
        # loop through the lines in the file
        for line in f:
            # load the line as a json object
            line = json.loads(line)
            # tokenize the text
            tokens = tokenize(line['text'])
            # if the title is not in the dictionary
            if within_doc_for_load.get(line['title'], 0) == 0:
                # add the title to the dictionary
                within_doc_for_load[line['title']] = {} 
            # if the title is in the dictionary
            within_doc_for_load[line['title']][line['start']] = tokens 
    #print(within_doc_for_load)
    return within_doc_for_load

#input = one query vector
#output = the top 10 most relevant videos for that query
#function that finds the most relevant videos for a given query
def find_relevant_videos(query_vector):

    #in main_pr.py
    #finds the cosine similarity between the query vector and the document term weights
    cosine_similarity = find_similarity(query_vector, doc_term_weights)

    #sorts from most to least relevant
    #top 10 most relevant videos
    top_10_docs = dict(sorted(cosine_similarity.items(), key=lambda item: item[1], reverse=True)[:10])
    return top_10_docs


# function that finds the cosine similarity between the query vector and the document term weights
def find_similarity(query_vector, weights_data_struct):
    # init our dict
    cosine_similarity = {}

    # calculate cumulative weight of the query vector
    query_cumul_weight = 0
    # calculate cumulative weight of the document vector
    for value in query_vector.values():
        # sum of the squares of the weights
        query_cumul_weight += value * value

    for title, weights_dict in weights_data_struct.items():
        # reset the dot prod (sum_vals -> changed this var name since sum is a python function too) and document cumulative weight for each document
        # sum of the dot product of the weights
        sum_vals = 0
        # sum of the squares of the weights
        doc_cumul_weight = 0

        # compute the dot product for terms present in both the query and the document
        for query_word, query_weight in query_vector.items():
            # if the query word is in the document
            if query_word in weights_dict:
                # add the dot product of the weights to the sum
                sum_vals += weights_dict[query_word] * query_weight

        # compute cumulative weight for the document vector
        for weight in weights_dict.values():
            # sum of the squares of the weights
            doc_cumul_weight += weight * weight
        # if the query and document have weights
        if query_cumul_weight > 0 and doc_cumul_weight > 0:
            # compute cosine similarity and store it
            cosine_similarity[title] = sum_vals / math.sqrt(query_cumul_weight * doc_cumul_weight)
        # else the cosine similarity is not available set to 0
        else:
            # no division by zero!!!
            cosine_similarity[title] = 0

    return cosine_similarity

#function that finds the most relevant section of a video
def find_most_relevant_section(video_title, query_vector):
    # find the cosine similarity between the query vector and the within document term weights
    cosine_similarity = find_similarity(query_vector, within_doc_termweights[video_title])

    #sorts from most to least relevant
    top_start_time = dict(sorted(cosine_similarity.items(), key=lambda item: item[1], reverse=True)[:1])
    #return the most relevant section
    return list(top_start_time.keys())[0]

# Used for UI
def run_search(query):
    query_tokens = tokenize(query)
    query_vector = calculate_query_vector(query_tokens, len(doc_term_weights))
    
    # find top 10 most relevant videos
    top_10_docs = find_relevant_videos(query_vector)
    
    #find most relevant part of the video
    for key, value in top_10_docs.items():
        # byte_key = key.encode('utf-8')
        byte_key = key.encode('iso-8859-1')
        most_relevant_section = find_most_relevant_section(byte_key, query_vector)
        most_relevant_section = math.floor(most_relevant_section)
        
        # key = key.encode('utf-8')
        top_10_docs[key] = links_database[byte_key]+"&t="+str(most_relevant_section)
    return top_10_docs

if __name__ == '__main__':
    # leaving these two function calls commented out as they only need 
    # to be ran once to get the data in a clean format
    #Within document output - Kenneth
    #print(within_textIDF(load_within_doc_text()))
    #a = output.term_weights
    # print(output.term_weights[(b'Training and Testing an Italian BERT - Transformers From Scratch #4', 0.0, 'Hi')])
    #for key, value in a.items():
    #    print(key, value)
    # dictionary of term weights for each word e.g documentTermWeights[video title][token] = 0.798654   
    #documentTermWeights, littleN = VSM()
    #print(littleN)   
    #Example to use within_doc_termweights print(within_doc_termweights[b'Training and Testing an Italian BERT - Transformers From Scratch #4'][0.0]['Hi'])
    # calculate query vector
    
    #read in the queries from the query file
    file_name = sys.argv[1]
    #open the file
    with open(file_name, 'r') as f:
        #reads in each query
        for line in f:
            #tokenizes query
            query_tokens = tokenize(line)

            #within queryvec.py
            query_vector = calculate_query_vector(query_tokens, len(doc_term_weights))

            #in main
            top_10_docs = find_relevant_videos(query_vector)
            
            #find most relevant part of the video
            for key, value in top_10_docs.items():
                # byte_key = key.encode('utf-8')
                byte_key = key.encode('iso-8859-1')
                #find the most relevant section of the video
                most_relevant_section = find_most_relevant_section(byte_key, query_vector)
                #round to the nearest second
                most_relevant_section = math.floor(most_relevant_section)
                
                # key = key.encode('utf-8')
                top_10_docs[key] = links_database[byte_key]+"&t="+str(most_relevant_section)
                #print the query and the top 10 most relevant videos
            print(f'@Query {line}')
            #print the top 10 most relevant videos
            for key, value in top_10_docs.items():
                # print the video title and the link to the most relevant section
                print(f'{key}:', value)
                #print the video title and the link to the most relevant section
            print()
            
