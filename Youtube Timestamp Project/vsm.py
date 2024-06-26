
# Thomas Bates, trbates 

import os
import sys
import math
import re
from collections import defaultdict
from collections import Counter
from collections import OrderedDict

# function that does tfc weighting scheme
def tfc(bigN, invertIndex) :
    #creating the dictionary of lists for the tfidf values
    tfIdf = defaultdict(list)
    #creating the dictionary of the little n values
    littleN = Counter()
    # for each document in the inverted index
    for document in invertIndex :
      #creating the dictionary of the words in the document
      wordDict = {}
      #for each token in the document
      for token in invertIndex[document] :
        # set the value of the token in the dictionary to 0
        wordDict[token] = 0
        #if the token is not in the little n dictionary, add it
        if token not in littleN :
          #set the value of the token to 1
          littleN[token] = 1
          #otherwise, increment the value of the token
        else :
          #increment the value of the token
          littleN[token] += 1   
          #set the value of the token in the dictionary to the value of the token in the inverted index
      tfIdf[document] = wordDict
    #creating the vector of tokens and weights,  
    #making the vectors of tokens with weights
    docVecs = []  
    #for each document in the inverted index

    for document in invertIndex:
         #creating the dictionary of the weights of the tokens
         docWeights = defaultdict(list)
         #for each token in the document
         for token in invertIndex[document] :
            #calculating the term frequency of the token
            tf = invertIndex[document][token]
            #calculating the weight of the token
            weight = bigN / littleN[token]
            #calculating the log of the weight
            weight = math.log(weight)
            #calculating the weight of the token
            weight = weight * tf
            #setting the value of the token in the dictionary to the weight
            docWeights[token] = weight
            #setting the value of the token in the dictionary to the weight
            tfIdf[document][token] = weight
            #appending the dictionary of the weights of the tokens to the vector of tokens and weights
         docVecs.append(docWeights)

    #normalizing the vectors
    for page in tfIdf :
         #determining the sum for the normalization factor
         squareRootSum = 0
         #determining the sum for the normalization factor
         for token in tfIdf[page]:
            #calculating the weight of the token
            weight = tfIdf[page][token]**2
            #incrementing the sum of the squares of the weights
            squareRootSum += weight 
            #calculating the square root of the sum of the squares of the weights
         squareRootSum = math.sqrt(squareRootSum)
         #determines the values of the numerator and denominator for the cosine 
         for tokens in tfIdf[page]:
            #have complete weight here -->v
            tfIdf[page][tokens] = tfIdf[page][tokens]/squareRootSum

    return tfIdf, littleN

# function that writes the video texts to a file
def page(videoText) :
    #writing the video texts to a file
    with open("videos_texts", 'w+') as output_file:
       #for each line in the video text
       for line in videoText:
          #writing the line to the file
          output_file.write(line)
          #writing a new line to the file
          output_file.write("\n")
          #writing the line to the file
          for word in videoText[line]:
            #writing the word to the file
            output_file.write(word)
            #writing a space to the file
            output_file.write(" ")
            #writing the word to the file
          output_file.write("\n")
       
    return

# function that reads the video texts from a file
def VSM() :
  #creating the dictionary of the vectors
   vectors = {}
   #reading the video texts from a file
   with open("videos_texts", encoding='iso-8859-1') as f:
     #creating the list of the elements
     elts = []
     #creating the title of the video
     title = ""
     #for each line in the file
     for line in f:  
       #appending the line to the list of elements
       elts.append(line)
       #if the index of the line is 0 or the index of the line is even
     for line in elts :
       # if the index of the line is 0 or the index of the line is even
       if elts.index(line) == 0 or elts.index(line) % 2 == 0 :
         #setting the title to the line
         title = re.sub("\n", "", line)
         #otherwise
       else :
          #setting the value of the title in the dictionary to the line
          vectors[title] = line.split()

  #creating the dictionary of the vectors
   bigN = len(vectors)   
   #preprocessing the query and assigning term frequency
   #when project query file is ready replace file below with that file name

  # create dictionary for i inverted index
   invertIndex = {}
   #for each vector in the vectors
   for vector in vectors :
      #creating the counter of the vector
      counter = Counter(vectors[vector]) 
      #setting the value of the vector in the dictionary to the counter
      invertIndex[vector] = counter 

   return tfc(bigN, invertIndex)
   

def main() :
    #calling the VSM function
    VSM()

#main()