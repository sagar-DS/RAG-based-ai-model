import os 
import json
import requests
import pandas as pd
import joblib

def create_embeddings(text_list):
    r = requests.post("http://localhost:11434/api/embed",json ={
        "model" : "bge-m3",
        "input" : text_list
    })

    embedding = r.json()["embeddings"]
    return embedding

jsons = os.listdir("new_jsons")
my_dicts  = []

for json_file in jsons:
    with open(f"new_jsons/{json_file}") as f:
        content = json.load(f)
    print(f"Creating embeddings for {json_file}")
    embeddings = create_embeddings([c['text'] for c in content['chunks']])

    for i,chunk in enumerate(content['chunks']):
        chunk['embedding'] = embeddings[i]
        my_dicts.append(chunk)


df = pd.DataFrame.from_records(my_dicts)
print(df)

joblib.dump(df,'embeddings.joblib')