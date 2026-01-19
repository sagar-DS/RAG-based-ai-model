import os
import json
import math
import time
from groq import Groq
import librosa
import soundfile as sf
from pydub import AudioSegment

API_KEY = "your api key" # use your api key of groq i have used mine here
CHUNK_LENGTH_MS = 2 * 60 * 1000  #(2 mins)

client = Groq(api_key=API_KEY)

def process_file(audio_file_path):
    filename = os.path.basename(audio_file_path)

    # 1. Load Audio
    audio, sr = librosa.load(audio_file_path, sr=None)
    total_duration_seconds = librosa.get_duration(y=audio, sr=sr)
    total_length = int(total_duration_seconds * 1000)  # Convert to ms
    num_chunks = math.ceil(total_length / CHUNK_LENGTH_MS)
    
    all_segments = []
    full_text_list = []
    segment_id_counter = 0

    # 2. Loop through chunks
    for i in range(num_chunks):
        start_ms = i * CHUNK_LENGTH_MS
        end_ms = min((i + 1) * CHUNK_LENGTH_MS, total_length)
        time_offset_seconds = start_ms / 1000.0
        
        # Create and save temp chunk
        start_sample = int((start_ms / 1000.0) * sr)
        end_sample = int((end_ms / 1000.0) * sr)
        chunk = audio[start_sample:end_sample]
        temp_wav = "temp_groq_chunk.wav"
        sf.write(temp_wav, chunk, sr)
        
        # Convert to MP3 for smaller file size
        temp_filename = "temp_groq_chunk.mp3"
        sound = AudioSegment.from_wav(temp_wav)
        sound.export(temp_filename, format="mp3", bitrate="64k")
        os.remove(temp_wav)
        
        # 3. Send to Groq API
        with open(temp_filename, "rb") as file:
            transcription = client.audio.translations.create(
                file=(temp_filename, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json", 
            )
        
        # Add delay to avoid rate limiting
        time.sleep(1)

        # 4. Fix Timestamps & Collect Data
        for segment in transcription.segments:
            adjusted_start = segment['start'] + time_offset_seconds
            adjusted_end = segment['end'] + time_offset_seconds
            
            all_segments.append({
                "id": segment_id_counter,
                "start": round(adjusted_start, 2),
                "end": round(adjusted_end, 2),
                "text": segment['text']
            })
            full_text_list.append(segment['text'])
            segment_id_counter += 1
        
        print(f" -> Chunk {i+1}/{num_chunks} done.")

    # Cleanup temp file
    if os.path.exists("temp_groq_chunk.mp3"):
        os.remove("temp_groq_chunk.mp3")

    # 5. Format Output
    parts = filename.split("_")
    lec_num = parts[0]
    # Simple logic to get title (assumes format: "01_Title.mp3")
    lec_name = parts[1].replace(".mp3", "") if len(parts) > 1 else filename.replace(".mp3", "")

    final_chunks = []
    for seg in all_segments:
        final_chunks.append({
            "number": lec_num,
            "title": lec_name,
            "id": seg['id'],
            "start": seg['start'],
            "end": seg['end'],
            "text": seg['text']
        })

    final_output = {
        "chunks": final_chunks,
        "text": "".join(full_text_list)
    }

    # 6. Save JSON
    output_path = os.path.join("jsons", filename.replace(".mp3", ".json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=4)
    
    print(f"Saved: {output_path}\n")

files = os.listdir("audios")
for file in files:
    # Minimal check just to ensure it's a file, not a subfolder
    if os.path.isfile(os.path.join("audios", file)):
        process_file(os.path.join("audios", file))

print("All Done!")