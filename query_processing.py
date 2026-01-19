import pandas as pd
import numpy as np 
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import requests

def create_embeddings(text_list):
    r = requests.post("http://localhost:11434/api/embed",json ={
        "model" : "bge-m3",
        "input" : text_list
    })

    embedding = r.json()["embeddings"]
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate",json ={
        "model" : "llama3.2",
        "prompt" : prompt,
        "stream": False
    })

    model_response = r.json()
    return model_response
     


df = joblib.load('embeddings.joblib')

query = input("Ask a question :")
query_embed = create_embeddings(query)

similarities = cosine_similarity(np.vstack(df['embedding']), np.vstack(query_embed)).flatten()
top_results = 5
max_index = similarities.argsort()[ :: -1][ : top_results]
# print(max_index)
# print(similarities[max_index])

new_df = df.loc[max_index]

# for index,item in new_df.iterrows():
#     print(index, item['number'] , item['title'], item['start'], item['end'],item['text'])
prompt = f'''
This is a  Full python course taught by apna college. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

------------------------------------------------------

"{query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course.And give the time stamps in this particular (hour : minute : seconds) format.
'''

with open("prompt.txt", "w") as f:
    f.write(prompt)

output = inference(prompt)['response']
# print(output)

with open("response.txt", "w") as f:
    f.write(output)
