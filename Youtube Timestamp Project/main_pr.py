import json
import re
import hardcodes
import math
import sys
from porter_stemmer import PorterStemmer
from vsm_pr import VSM
from within_textIDF_pr import within_textIDF
from within_doc_termweights_pr import within_doc_termweights_pr
from queryvec_pr import calculate_query_vector
from subset_term_weights import subset_term_weights
from links_database import links_database

# function that cleans a token using regex
def cleanAToken(token):
    # set our cleaned string to the token
    cleaned_string = token
    # remove trailing commas
    if token[len(token)-1] == ',':
        # remove the last character
        cleaned_string = cleaned_string[:-1]
    # remove any of the following characters from the token
    cleaned_string = re.sub('[\(\)\[\]\\\.\,\/\=\?\:\=\$]','', cleaned_string)
    # return the cleaned string
    return cleaned_string

# function that tokenizes a string helper
def tokenize_helper(text):
    # split the text into tokens
    dirty_tokens = text.split()
    # create a list to store the clean tokens
    clean_tokens = []

    # loop through the tokens
    for token in dirty_tokens:
        # set clean to true
        clean = True
        # clean the token
        token = cleanAToken(token)
        # if the token is empty, skip it
        if len(token) == 0:
            # skip this token
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
        if token in hardcodes.contractions_dict.keys():
            # split the contraction into its parts
            new_tokens = hardcodes.contractions_dict[token].split(' ')
            # loop through the new tokens
            for i in range(len(new_tokens)):
                # add the new token to the clean tokens
                clean_tokens.append(new_tokens[i])
            clean = False # already appended to clean tokens, no need to add again

        # if the token is clean, add it to the clean tokens
        if clean:
            # add the token to the clean tokens
            clean_tokens.append(token) 
    # return the clean tokens
    return clean_tokens


# function that tokenizes a string
def tokenize(text):
    # tokenize the text using the helper function
    full_tokens = tokenize_helper(text)
    # filter out tokens that don't match the regex
    filtered_tokens = [token for token in full_tokens if re.match(r'^[a-zA-Z\-\&]+$', token)]
    
    # create a list to store the clean tokens
    clean_tokens = []
    # create a stemmer
    stemmer = PorterStemmer()
    # loop through the filtered tokens
    for word in filtered_tokens:
        # stem the word
        stemmed_word = stemmer.stem(word, 0, len(word) - 1)
        # add the stemmed word to the clean tokens
        clean_tokens.append(stemmed_word)
    # return the clean tokens
    return clean_tokens

# to genearate document into tokenized version
# comment out everything in main and call this function
# in the command line, use output redirection to save into a file
# we used it to create document_text.py
def load_doc_text():
    # create a dictionary to store the document text
    doc_text_local_for_load = {}
    # open the file
    with open('youtube-transcription-for-precision-and-recall.jsonl.jsonl', 'r') as f:
        # loop through the lines in the file
        for line in f:
            # load the line as a json object
            line = json.loads(line)
            # tokenize the text
            tokens = tokenize(line['text'])
            
            # if the title is not in the dictionary, add it
            if doc_text_local_for_load.get(line['title'], 0) == 0:
                # add the title to the dictionary
                doc_text_local_for_load[line['title']] = tokens 
                #else add the tokens to the existing title
            else:
                # add the tokens to the existing title
                doc_text_local_for_load[line['title']] += (tokens)
    
    #print(doc_text_local_for_load)
    # If the youtube video collection gets updated then uncomment
    # the line below to generate a new text file for vsm
    #page(doc_text_local_for_load)

# to genearate document into tokenized version
# comment out everything in main and call this function
# in the command line, use output redirection to save into a file
# we used it to create within_doc_text.py
def load_within_doc_text():
    # create a dictionary to store the within document text
    within_doc_for_load = {}
    # open the file
    with open('youtube-transcription-for-precision-and-recall.jsonl.jsonl', 'r') as f:
        # loop through the lines in the file
        for line in f:
            # load the line as a json object
            line = json.loads(line)
            # tokenize the text
            tokens = tokenize(line['text'])
            # if the title is not in the dictionary, add it
            if within_doc_for_load.get(line['title'], 0) == 0:
                # add the title to the dictionary
                within_doc_for_load[line['title']] = {} 
            # add the tokens to the dictionary
            within_doc_for_load[line['title']][line['start']] = tokens 
    # return the dictionary
    return within_doc_for_load

#input = one query vector
#output = the top 10 most relevant videos for that query
def find_relevant_videos(query_vector):

    #in main_pr.py
    # calculate cosine similarity between query vector and all document vectors
    cosine_similarity = find_similarity(query_vector, subset_term_weights)

    #sorts from most to least relevant
    # get the top 10 most relevant documents
    top_10_docs = dict(sorted(cosine_similarity.items(), key=lambda item: item[1], reverse=True)[:10])
    # return the top 10 most relevant documents
    return top_10_docs

#def find_similarity(query_vector_orig, weights_data_struct):
#    cosine_similarity = {}
#    for title, weights in weights_data_struct.items():
#        query_vector = query_vector_orig
#       all_keys = set(weights.keys()).union(set(query_vector.keys()))
        # Creating full sparce vectors with 0 for missing terms
#        doc_full = {key: weights.get(key, 0.0) for key in all_keys}
#        query_full = {key: query_vector.get(key, 0.0) for key in all_keys}

        # Creating list representations of vectors
#        doc_vector = [doc_full[key] for key in sorted(all_keys)]
#        query_vector = [query_full[key] for key in sorted(all_keys)]

 #       dot_product = sum(d * q for d, q in zip(doc_vector, query_vector))
  #      doc_norm = math.sqrt(sum(d ** 2 for d in doc_vector))
  #      query_norm = math.sqrt(sum(q ** 2 for q in query_vector))

      #  cosine_similarity[title] = dot_product / (doc_norm * query_norm) if doc_norm and query_norm else 0.0
   # return cosine_similarity

# calculate cosine similarity between query vector and all document vectors
def find_similarity(query_vector, weights_data_struct):
    # init our dict
    cosine_similarity = {}

    # calculate cumulative weight of the query vector
    query_cumul_weight = 0
    # calculate the cumulative weight of the query vector
    for value in query_vector.values():
        # add the square of the value to the cumulative weight
        query_cumul_weight += value * value

    for title, weights_dict in weights_data_struct.items():
        # reset the dot prod (sum_vals -> changed this var name since sum is a python function too) and document cumulative weight for each document
        # set the dot product to 0
        sum_vals = 0
        # set the document cumulative weight to 0
        doc_cumul_weight = 0

        # compute the dot product for terms present in both the query and the document
        for query_word, query_weight in query_vector.items():
            # if the query word is in the weights dictionary
            if query_word in weights_dict:
                # add the product of the weights to the sum_vals
                sum_vals += weights_dict[query_word] * query_weight

        # compute cumulative weight for the document vector
        for weight in weights_dict.values():
            # add the square of the weight to the document cumulative weight
            doc_cumul_weight += weight * weight

        # if the query cumulative weight and the document cumulative weight are both greater than 0
        if query_cumul_weight > 0 and doc_cumul_weight > 0:
            # compute cosine similarity and store it
            cosine_similarity[title] = sum_vals / math.sqrt(query_cumul_weight * doc_cumul_weight)
            # else set the cosine similarity to 0
        else:
            # no division by zero!!!
            cosine_similarity[title] = 0

    return cosine_similarity

# find the most relevant section of the video
def find_most_relevant_section(video_title, query_vector):
    # calculate the cosine similarity between the query vector and the document term weights
    cosine_similarity = find_similarity(query_vector, within_doc_termweights_pr[video_title])

    #sorts from most to least relevant
    top_start_time = dict(sorted(cosine_similarity.items(), key=lambda item: item[1], reverse=True)[:1])
    # return the most relevant section
    return list(top_start_time.keys())[0]

if __name__ == '__main__':
    # leaving these two function calls commented out as they only need 
    # to be ran once to get the data in a clean format
    #Within document output - Kenneth use output redirection to make files
    #print(within_textIDF(load_within_doc_text()))
    #a = output.term_weights
    #print(output.term_weights[(b'Training and Testing an Italian BERT - Transformers From Scratch #4', 0.0, 'Hi')])
    #for key, value in a.items():
        #print(key, value)
    # dictionary of term weights for each word e.g documentTermWeights[video title][token] = 0.798654   
    #documentTermWeights, littleN = VSM()
    #print(littleN)   
    #Example to use within_doc_termweights print(within_doc_termweights[b'Training and Testing an Italian BERT - Transformers From Scratch #4'][0.0]['Hi'])
    # calculate query vector
    
    #read in the queries from the query file
    
    # get the file name from the command line arguments
    file_name = sys.argv[1]
    # open the file
    with open(file_name, 'r') as f:
        #reads in each query
        for line in f:
            #tokenizes query
            query_tokens = tokenize(line)

            #within queryvec.py
            query_vector = calculate_query_vector(query_tokens, len(subset_term_weights))

            #in main
            top_10_docs = find_relevant_videos(query_vector)
            
            #find most relevant part of the video
            for key, value in top_10_docs.items():
                # byte_key = key.encode('utf-8')
                byte_key = key.encode('iso-8859-1')
                # find the most relevant section
                most_relevant_section = find_most_relevant_section(byte_key, query_vector)
                # round the most relevant section
                most_relevant_section = math.floor(most_relevant_section)
                
                # key = key.encode('utf-8')
                top_10_docs[key] = links_database[byte_key]+"&t="+str(most_relevant_section)
                # print the results
            print(f'@Query {line}')
            # print the top 10 most relevant documents
            for key, value in top_10_docs.items():
                # print the key and value
                print(f'{key}:', value)
                # print a newline
            print()
            
            