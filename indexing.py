

import json
 
# Opening JSON file
f = open('shakespeare-scenes.json')
 
# returns JSON object as a dictionary
data = json.load(f)['corpus']
# print(data)

inverted_index = {}
for file in data:
    text = file['text'].split()
    for word in text:
        if word not in inverted_index.keys():
            inverted_index[word] = {}
        if file['sceneId'] not in inverted_index[word].keys():
            inverted_index[word][file['sceneId']] = [text.index(word)]
        # if word in inverted_index.keys() and file['sceneId'] in inverted_index[word].keys():
        else:
            inverted_index[word][file['sceneId']].append(text.index(word)) 
print(inverted_index['fool'])



# Closing file
f.close()