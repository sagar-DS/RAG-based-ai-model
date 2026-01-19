# How to use this RAG AI Teaching assistant on your own data
## Step 1 - Collect your videos
Move all your video files to the videos folder

## Step 2 - Convert to audio
Convert all the video files to mp3 by ruunning video_to_audio (make sure that you have created audio folder)


## Step 3 - Convert audio to json 
Convert all the mp3(audio) files to json by ruunning audio_to_json(make sure to have a folder named jsons)
Here don't forget to replace your actual Groq api key with the text in the variable API_KEY at line 10.

## Step 4 - Convert the json files to Vectors
Use the file text_to_vector to convert the json files to a dataframe with Embeddings and save it as a joblib pickle

## Step 5 - Prompt generation and feeding to LLM

Read the joblib file and load it into the memory. Then create a relevant prompt as per the user query and feed it to the LLM. For this use query_processing file.


