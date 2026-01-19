
import os
import subprocess

files = os.listdir("videos")

for file in files :
    lecture_no = file.split(" ： ")[0].split(" ")[1]
    lecture_name = file.split(" ： ")[1].split(" ｜ Python Full Course")[0]
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{lecture_no}_{lecture_name}.mp3"])
