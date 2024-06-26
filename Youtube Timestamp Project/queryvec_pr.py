from math import log10
from document_freq_pr import document_freq_pr
from collections import Counter

# Calculate the query vector for a given query
def calculate_query_vector(query_terms, N, query_type='t'):
    # Calculate the term frequency for each term in the query
    query_terms = Counter(query_terms)
    # Calculate max tf for normalization, if necessary
    max_tf = max(query_terms.values()) if query_type == 'n' else 1
    # Initialize the query vector
    query_vector = {}
    # Calculate the vector value for each term in the query
    for term, tf in query_terms.items():
        # Calculate Term Frequency (TF)
        if query_type == 'n':  # Normalized for short queries
            normalized_tf = 0.5 + (0.5 * tf / max_tf)
        elif query_type == 't':  # Direct TF for longer queries
            normalized_tf = tf        
        # Calculate Document Frequency (DF)
        df = 1# n in document frequency weighting schemes
        # this value for df can vary. we can use df = 1, use standard log(N / df), or use log(1 + N / df+1), or try
        # our own scheme we made, log(1+N) / (1+df)
        # Vector value for the term (TF * DF, since no normalization with query length is applied)
        query_vector[term] = normalized_tf * df
    return query_vector



