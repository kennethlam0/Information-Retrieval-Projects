from document_text import document_text

# dictionary for our document freq
document_freq_pr = {}

# for each title and list of words in document_text
for title, list_words in document_text.items():
    # for each word in the list of words
    for word in list_words:
        # if the word is not in the dictionary, add it
        document_freq_pr[word] = document_freq_pr.get(word, 0) + 1

#print(document_freq_pr)

