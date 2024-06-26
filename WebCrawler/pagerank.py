#Kenneth Lam lamken
import sys
from collections import defaultdict
import re

def read_links(file_path):
    links = []
    file = open(file_path,encoding = 'utf-16')
    lines = file.readlines()
    for line in lines:
        links.append((line.split()[0],line.split()[1]))
    file.close()
    return links

def find_pagerank(url_score,in_edges,out_edges,threshold):
    c = (1.0-0.85)/len(url_score)
    iteration = 0
    while True:
        for url in url_score:
            weight = sum(url_score[edge][iteration]/len(out_edges[edge]) for edge in in_edges.get(url,[]))
            new_score = c + 0.85*weight
            url_score[url].append(new_score)
        if all(abs(url_score[url][iteration]-url_score[url][iteration+1]) <=threshold for url in url_score):
            break
        iteration+=1
    return iteration,url_score

def initialize(links,url_score):
    for node1,node2 in links:
        for node in [node1,node2]:
            if node not in url_score:
                url_score[node] = [0.25]
        in_edges.setdefault(node2,[]).append(node1.strip())
        in_edges.setdefault(node1,[]).append(node2.strip())
        out_edges.setdefault(node1,[]).append(node2.strip())
        out_edges.setdefault(node2,[]).append(node1.strip())
    return url_score,in_edges,out_edges

threshold = 0.001
url_score = {}
in_edges = {}
out_edges = {}

crawler_output_file = sys.argv[1]
links_output_file = sys.argv[2]
convergence_threshold = float(sys.argv[3])
links = read_links(links_output_file)

url_score,in_edges, out_edges = initialize(links,url_score)
iterations,pageranks = find_pagerank(url_score,in_edges,out_edges,threshold)

pageranks_final = {url: pageranks[url][iterations] for url in pageranks}

sorted_pageranks = sorted(pageranks_final.items(), key=lambda x:x[1],reverse=True)

for pagerank in sorted_pageranks:
    print(pagerank[0],pagerank[1])
