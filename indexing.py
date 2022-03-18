

import json
 
# Opening JSON file
f = open('shakespeare-scenes.json')
 
# returns JSON object as a dictionary
data = json.load(f)['corpus']
 

print(data)
 
# Closing file
f.close()