import os
import subprocess
from pathlib import Path
import re

BASE_DIR = Path("/home/pognova/SkillManim")
BUILDER_DIR = BASE_DIR / "manim-video-builder"

def get_duration(file_path):
    if not file_path.exists(): return 0
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)]
    try:
        res = subprocess.check_output(cmd).decode().strip().split('\n')
        return float(res[0])
    except: return 0

def render_batch(idx):
    py_path = BUILDER_DIR / f"manim_scenes/batch_{idx}.py"
    audio_path = BUILDER_DIR / f"output/final/batch_{idx}_audio.mp3"
    
    # 1. Render base
    cmd = [str(BASE_DIR / ".venv/bin/manim"), "-qm", "--flush_cache", "--media_dir", str(BASE_DIR), str(py_path), f"Batch{idx}"]
    print(f"Rendering Batch {idx} (base)...")
    subprocess.run(cmd, capture_output=True)
    
    v_path = BASE_DIR / f"videos/batch_{idx}/720p30/Batch{idx}.mp4"
    v_dur = get_duration(v_path)
    a_dur = get_duration(audio_path)
    
    if a_dur > v_dur:
        diff = a_dur - v_dur + 0.5
        content = py_path.read_text()
        insert_idx = content.rfind("self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)")
        if insert_idx != -1:
            pad_code = f"\n        self.wait({diff:.3f}) # Pad for audio\n        "
            new_content = content[:insert_idx] + pad_code + content[insert_idx:]
            py_path.write_text(new_content)
            
            print(f"Rerendering Batch {idx} with {diff:.3f}s padding...")
            subprocess.run(cmd, capture_output=True)
            v_dur = get_duration(v_path)
    
    # Merge with audio
    out_video = BUILDER_DIR / f"output/final/batch_{idx}_final.mp4"
    merge_cmd = ["ffmpeg", "-y", "-i", str(v_path), "-i", str(audio_path), "-c:v", "copy", "-c:a", "aac", "-shortest", str(out_video)]
    subprocess.run(merge_cmd, capture_output=True)
    print(f"Batch {idx} completed: {out_video} (V:{v_dur:.2f}, A:{a_dur:.2f})")

for i in range(1, 6):
    render_batch(i)

# Final concatenation
final_list = BUILDER_DIR / "output/final/final_list.txt"
with open(final_list, "w") as f:
    for i in range(1, 6):
        f.write(f"file '{BUILDER_DIR}/output/final/batch_{i}_final.mp4'\n")

final_video = BUILDER_DIR / "output/final/full_video_consolidated.mp4"
concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(final_list), "-c", "copy", str(final_video)]
subprocess.run(concat_cmd, capture_output=True)
print(f"All done! Final video at {final_video}")
