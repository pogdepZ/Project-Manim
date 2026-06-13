from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
import sys

def get_sentence_timings(mp3_path):
    try:
        audio = AudioSegment.from_mp3(mp3_path)
    except Exception as e:
        print(f"Error loading {mp3_path}: {e}")
        return

    # Find non-silent chunks. Silence is usually defined as < -40dBFS for at least 500ms
    # But TTS pauses between sentences might be shorter, like 300ms.
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=300, silence_thresh=-40)
    
    print(f"Timings for {mp3_path}:")
    for i, (start, end) in enumerate(nonsilent_ranges):
        print(f"Segment {i+1}: Start: {start/1000.0:.3f}s - End: {end/1000.0:.3f}s")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_sentence_timings(sys.argv[1])
    else:
        for i in range(16, 32):
            get_sentence_timings(f"output/scenes/scene_{i:03d}/narration.mp3")
            print("-" * 40)
