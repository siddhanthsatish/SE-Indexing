import matplotlib.pyplot as plt
from audioop import avg
from cmath import inf
import json
from typing import final
import time
from sympy import sfield


#API
def create_inverted_index(data):
    inverted_index = {}
    for file in data:
        text = file['text'].split()
        for word in text:
            if word not in inverted_index.keys():
                inverted_index[word] = {}
            if file['sceneId'] not in inverted_index[word].keys():
                inverted_index[word][file['sceneId']] = [text.index(word)]
                text[text.index(word)] = ""
            else:
                inverted_index[word][file['sceneId']].append(text.index(word))
                text[text.index(word)] = ""
    return inverted_index


def number_of_documents_containing_word(inverted_index, word):
    count = 0
    if word in inverted_index.keys(): #if word in the dcoument
        for doc in inverted_index[word]: #for each document in the inverted index of that word
            count += len(inverted_index[word][doc]) #count the length of the number of scenes the word appears
    return count

def plays_from_scenes(scenes):
    plays = set()
    for scene in scenes:
        l = scene.split(":")
        plays.add(l[0])
    plays = list(plays)
    return plays



def consecutive_words_scenes(inverted_index, word1, word2):
    scenes = {}
    docs = inverted_index[word1]
    for doc in docs:
        pos1 = inverted_index[word1][doc]
        if doc in inverted_index[word2]:
            pos2 = inverted_index[word2][doc]

            for p1 in pos1:
                for p2 in pos2:
                    if p2 -p1 == 1:
                        if doc not in scenes.keys():
                            scenes[doc] = [p2]
                        else:
                            scenes[doc].append(p2)
                        break    
    return scenes




def phrase_detect(inverted_index, sen, fname):
    sen = sen.split(" ")
    scenes  = []
    final_scenes= {}
    for ind, word in enumerate(sen):
        if(ind< len(sen)-1):
            scenes.append(consecutive_words_scenes(inverted_index, sen[ind], sen[ind+1]))


    for ind in range(len(scenes)):
        if ind == 0:
            for scene in scenes[ind]:
                if scene not in final_scenes:
                    final_scenes[scene] = [scenes[ind][scene]]
                else:
                    final_scenes[scene].append(scenes[ind][scene])
        else:
            for scene in scenes[ind]:
                if scene in final_scenes:
                    final_scenes[scene].append(scenes[ind][scene])

    print(final_scenes)
    
    f1 = open(fname, "w")
    

    result = []
    for scene in final_scenes:
        first_seq = final_scenes[scene][0]
        
        for ind1 in first_seq:
            flag = True
            for ind2 in range(1, len(final_scenes[scene])):
                if ind1 + 1 not in final_scenes[scene][ind2]:
                    flag = False
                    break
                ind1 += 1
            if flag == True:
                result.append(scene)
                f1.write(scene + "\n")
                break
    # print(result)
    f1.close()
    return result

def stats(data):
    max_scene_len = 0
    max_play_len = 0
    max_len_scene = ""
    min_scene_len = 100000000000
    max_len_play = ""
    word_len = 0
    scenes = set()
    plays = {}
    for scene in data:
        word_len += len(scene["text"].split(" "))
        scenes.add(scene["sceneId"])
        if(len(scene["text"].split(" ")) > max_scene_len):
            max_scene_len = len(scene["text"].split(" "))
            max_len_scene = scene['sceneId']
        if(len(scene["text"].split(" ")) < min_scene_len):
            min_scene_len = len(scene["text"].split(" "))
            min_len_scene = scene['sceneId']
        if plays_from_scenes([scene['sceneId']])[0] not in plays:
            plays[plays_from_scenes([scene['sceneId']])[0]] = len(scene["text"].split(" "))
        else:
            plays[plays_from_scenes([scene['sceneId']])[0]] += len(scene["text"].split(" "))

    max_len_play = max(plays, key=plays.get)
    min_len_play = min(plays, key=plays.get)
    avg_scene_len = word_len / len(scenes)


    return avg_scene_len, min_len_scene, max_len_scene, min_len_play, max_len_play, min_scene_len, max_scene_len

#driver code
file = open('shakespeare-scenes.json')
data = json.load(file)['corpus']
inverted_index = create_inverted_index(data)
file.close()

times = []


# terms0.txt
f0 = open("terms0.txt", "w")
i = 1
theethou_counts = []
you_counts = []
scene_num = []
scenes = []
start = time.time()
for document in data:
    temp_index = create_inverted_index([document]) #create inverted index for each document
    count1 = number_of_documents_containing_word(temp_index, 'thee')
    count2 = number_of_documents_containing_word(temp_index, 'thou')
    count3 = number_of_documents_containing_word(temp_index, 'you')
    if count3 < count1 or count3 < count2:
        scenes.append(document['sceneId'])
    theethou_counts.append(count1+count2)
    you_counts.append(count3)
    scene_num.append(i)
    i+=1
end = time.time()
times.append(end-start)
plt.plot(scene_num, theethou_counts, label= 'thee or thou')
plt.plot(scene_num, you_counts, label= 'you')
plt.xlabel("sceneNum")
plt.ylabel("Frequency")
plt.title("Thee or Thou vs You")
plt.legend()
plt.show()
scenes.sort()
print(scenes)
for scene in scenes:
    f0.write(scene + "\n")
# print(scenes)
print(len(scenes))
f0.close()

# terms1.txt
start = time.time()
scenes = []
scenes.extend(inverted_index['venice'].keys())
scenes.extend(inverted_index['denmark'].keys())
scenes.extend(inverted_index['rome'].keys())
scenes = list(set(scenes))
end = time.time()
times.append(end - start)
scenes.sort()
f1 = open("terms1.txt", "w")
for scene in scenes:
    f1.write(scene + "\n")
f1.close()
print(scenes)
print(len(scenes))    


#terms2.txt
start = time.time()
scenes = inverted_index['goneril'].keys()
plays = plays_from_scenes(scenes)
end = time.time()
times.append(end - start)
plays.sort()
f2 = open("terms2.txt", "w")
for each in plays:
    f2.write(each + '\n')
f2.close()
print(scenes)
print(plays)

# terms3.txt
start = time.time()
scenes = inverted_index['soldier'].keys()
plays = plays_from_scenes(scenes)
end = time.time()
times.append(end - start)
plays.sort()
f3 = open("terms3.txt", "w")
for each in plays:
    f3.write(each + '\n')
f3.close()
print(scenes)
print(plays)
print(len(plays))



# # phrase0.txt
start = time.time()
print(phrase_detect(inverted_index, "poor yorick", "phrase0.txt"))
end = time.time()
times.append(end - start)

# # phrase1.txt
start = time.time()
print(phrase_detect(inverted_index, "wherefore art thou romeo", "phrase1.txt"))
end = time.time()
times.append(end - start)

# # phrase2.txt
start = time.time()
print(phrase_detect(inverted_index, "let slip", "phrase2.txt"))
end = time.time()
times.append(end - start)


avg_scene_len, min_len_scene, max_len_scene, min_len_play, max_len_play, min_scene_len, max_scene_len = stats(data)

print("Average Scene Length: ", avg_scene_len)
print("Minimmum Length Scene: ",min_len_scene," ", min_scene_len)
print("Maximmum Length Scene: ", max_len_scene," ",  max_scene_len)
print("Minimmum Length Play: ", min_len_play)
print("Maximmum Length Play: ", max_len_play)

print("Runtime of each query:", times)