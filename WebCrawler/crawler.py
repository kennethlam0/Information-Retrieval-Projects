#Kenneth Lam lamken
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import re
import numpy as np

headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"}
domains = ['eecs.umich.edu','eecs.engin.umich.edu','ece.engin.umich.edu','cse.engin.umich.edu']
edges = []


def extract_domain(url):

  pattern = r"(https?://)?(www\d?\.)?(?P<domain>[\w\.-]+\.\w+)(/\S*)?"
  match = re.match(pattern, url)
  if match:
    domain = match.group("domain")
    return domain
  else:
    return None
  
def crawl(url):
    try:
        response = requests.get(url,headers=headers,timeout=3) 
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, "html.parser")
        newLinks = []
        for link in soup.find_all("a", href=True):
            newUrl = urljoin(url, link["href"])
            if extract_domain(newUrl) not in domains:
               continue 
            if 'www.' in newUrl:
               continue
            if '.pdf' in newUrl:
               continue
            if '/cdn-cgi/l/email-protection' in newUrl:
                continue
            else:
                newLinks.append(newUrl)
        return newLinks

    except requests.exceptions.RequestException as e:
        return []

fileName = sys.argv[1]
maxUrls = sys.argv[2]
uniqueUrls = list()
seedUrls = open(fileName,'r').readlines()
for url in seedUrls:
    visited_urls = set()
    num_visited = 0 
    seed_url = url
    urls_to_visit = [seed_url]
    while urls_to_visit:
        uniqueUrls.extend(visited_urls)
        uniqueUrls.extend(urls_to_visit)
        if (len(set(list(visited_urls) + urls_to_visit))) >= int(maxUrls):
            break
        current_url = urls_to_visit.pop(0) 
        if current_url in visited_urls:
            continue

        if extract_domain(current_url) not in domains:
           continue

        try:
            response = requests.head(current_url,headers=headers,timeout=3)
            response.raise_for_status()
            if 'text/html' not in response.headers['content-type']:
               continue
        except requests.exceptions.RequestException as e:
           continue
        
        if '/cdn-cgi/l/email-protection' in current_url:
           continue
        new_links = crawl(current_url)
        edges.append((current_url,set(new_links)))
        visited_urls.add(current_url)
        num_visited+=1
        urls_to_visit.extend(new_links)

uniqueUrls = list(dict.fromkeys(uniqueUrls))
#for crawler.output


printed = 0 
for urls in uniqueUrls:
   if printed==2500:
      break
   try:
    print(urls)
    printed+=1
   except:
      continue
   
"""
for a in edges:
   for link in a[1]:
      try:
         print(a[0],link)
      except: 
         continue
"""