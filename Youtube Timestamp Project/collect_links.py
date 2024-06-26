import json

links_database = {}
with open('youtube-transcriptions.jsonl', 'r') as f:
    for line in f:
        line = json.loads(line)
        links_database[line['title'].encode('utf-8')] = line['url']
print(links_database)