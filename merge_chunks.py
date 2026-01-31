import os
import math
import json

n = 5 #number of chunks to be merged

for file in os.listdir("jsons"):
    file_path = os.path.join("jsons", file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        new_jsons = []
        num_of_chunks = len(data['chunks'])
        num_groups = math.ceil(num_of_chunks/n)
        for i in range(num_groups):
            start_idx = i*n
            end_idx = min((i+1)*n, num_of_chunks)

            chunk_group = data['chunks'][start_idx : end_idx]

            new_jsons.append({
                "number" : data['chunks'][0]['number'],
                "title"  : data['chunks'][0]['title'],
                "id" : i ,
                "start": chunk_group[0]['start'],
                "end" : chunk_group[-1]['end'],
                "text" : " ".join(c['text'] for c in chunk_group)
            })
        
        #creating new json folder to store new merged chunks
        os.makedirs("new_jsons", exist_ok=True)
        with open(os.path.join("new_jsons", file), "w", encoding = "utf-8") as json_files:
            json.dump({"chunks" : new_jsons , "text" : data['text']}, json_files , indent=4)


        