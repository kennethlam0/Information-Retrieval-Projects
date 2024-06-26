#Halle Frey (hallefr)

import sys #dont need to install
import string #dont need to install
import os #dont need to install
import re #dont need to install
from collections import defaultdict
import numpy as np
import glob


#gets the reljudge documents for each query aka the videos that were labeled as relevant
relevant = defaultdict(list)
with open("youtube.reljudge", 'r', encoding = 'latin-1') as f:
    #loops through each line 
    for line in f:
        input = line

        #gets the number of the query
        queryNum = int(input[0])

        #gets the title of the relevant videos
        title = input[2:]

        #adds the title of the relevant video to the list at the query number key
        relevant[queryNum].append(title[:-1])

#will store the outputted videos
answer = defaultdict(list)

#read in the output with query number and title
with open("output_pr.txt", 'r', encoding = 'latin-1') as f: 
   #loops through the 4 query outputs
   for i in range(4):
        
        #loops through the 13 lines of output for each query because of spacing
        for j in range(13):

            #gets each line from the file
            for line in f:

                #when j is 0, the query is being read in
                if j == 0:
                    query = line
                    break

                #when j is 1 or 12, an empty line is being read in
                if j == 1 or j == 12:
                    junk = line
                    break

                #when j is between 1 and 12, the relevant videos are being read in
                if j > 1 and j != 12:
                    #read in the relevant video with title and link
                    input = line

                    #finds the index where the title ends
                    index = input.find(": http")

                    #modifies the string so it is just the title
                    input = input[:index]
                    
                    #adds the title to the list at the query number key
                    answer[i+1].append((input))
                    break
#print("relevant")
#print(relevant)
#print("answer")
#print(answer)       


#top 1 precision and recall for tfc.tfx
#n is query number
n = 1
recall1 = 0
precision1 = 0

#while we are within the 4 queries
while n < 5:
    numerator = 0
    counter = 0
 
    #loops through each relevant document from reljudge at that query
    for item in answer[n]:

        #adds one to the set of retrieved and relevant if that document is in the documents I retrieved
        if item in relevant[n]:
            numerator += 1
        
        #only checks the first one
        counter+=1
        if(counter==1):
            break
    
    #calculates recall based on set of retrieved and relevant/number of relevant
    recall1 += numerator/len(relevant[n])

    #calculates precision based on set of retrieved and relevant/number of retrieved
    precision1 += numerator/1

    #increments query
    n+=1

#top 5 precision and recall for tfc.tfx
n = 1
recall5 = 0
precision5 = 0

#while we are within the 4 queries
while n < 5:
    numerator = 0
    counter = 0
 
    #loops through each relevant document from reljudge at that query
    for item in answer[n]:

        #adds one to the set of retrieved and relevant if that document is in the documents I retrieved
        if item in relevant[n]:
            numerator += 1
        
        #only checks the first one
        counter+=1
        if(counter==5):
            break
    
    #calculates recall based on set of retrieved and relevant/number of relevant
    recall5 += numerator/len(relevant[n])

    #calculates precision based on set of retrieved and relevant/number of retrieved
    precision5 += numerator/5

    #increments query
    n+=1


#top 10 precision and recall for tfc.tfx
n = 1
recall10 = 0
precision10 = 0

#while we are within the 4 queries
while n < 5:
    numerator = 0
    counter = 0
 
    #loops through each relevant document from reljudge at that query
    for item in answer[n]:

        #adds one to the set of retrieved and relevant if that document is in the documents I retrieved
        if item in relevant[n]:
            numerator += 1
        
        #only checks the first 10
        counter+=1
        if(counter==10):
            break

    #calculates recall based on set of retrieved and relevant/number of relevant
    recall10 += numerator/len(relevant[n])

    #calculates precision based on set of retrieved and relevant/number of retrieved
    precision10 += numerator/10

    #increments query
    n+=1


print("MAP 1 " + str(precision1/4))
print("MAR 1 " + str(recall1/4))

print("MAP 5 " + str(precision5/4))
print("MAR 5 " + str(recall5/4))

print("MAP 10 " + str(precision10/4))
print("MAR 10 " + str(recall10/4))
