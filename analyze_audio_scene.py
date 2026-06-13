from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def analyze_audio(audio_path):
    print(f"Analyzing {audio_path}...")
    audio = AudioSegment.from_mp3(audio_path)
    
    # Split audio on silence
    chunks = split_on_silence(
        audio, 
        min_silence_len=400, # 400ms silence
        silence_thresh=audio.dBFS-16, # Adjust threshold
        keep_silence=200
    )
    
    print(f"Found {len(chunks)} chunks.")
    for i, chunk in enumerate(chunks):
        duration = len(chunk) / 1000.0
        print(f"Chunk {i+1}: {duration:.3f}s")

if __name__ == "__main__":
    path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_001/narration.mp3"
    if os.path.exists(path):
        analyze_audio(path)
    else:
        print("Audio not found.")
