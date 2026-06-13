import subprocess
import json
from pathlib import Path

def get_duration(file_path):
    if not file_path.exists():
        return None
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None

base_dir = Path("/home/pognova/SkillManim/manim-video-builder")
for i in range(1, 32):
    scene_name = f"scene_{i:03d}"
    vid_path = base_dir / f"output/scenes/{scene_name}/video_no_audio.mp4"
    aud_path = base_dir / f"output/scenes/{scene_name}/narration.mp3"
    
    v_dur = get_duration(vid_path)
    a_dur = get_duration(aud_path)
    
    if v_dur is not None and a_dur is not None:
        diff = v_dur - a_dur
        if abs(diff) > 0.1:
            print(f"{scene_name}: Video {v_dur:.3f}s, Audio {a_dur:.3f}s, Diff {diff:.3f}s")
