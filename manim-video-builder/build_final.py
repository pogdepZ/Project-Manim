import json
import os
import subprocess
from pathlib import Path
import sys

# Ensure src module is in path
sys.path.append(str(Path(__file__).parent / "src"))
from merger import merge_video_audio, concat_mp4_files

def get_batch(index):
    if index <= 5: return 1
    elif index <= 10: return 2
    elif index <= 15: return 3
    elif index <= 20: return 4
    elif index <= 25: return 5
    else: return 6

def main():
    manifest_path = Path("output/final/manifest.json")
    if not manifest_path.exists():
        print("Manifest not found!")
        return

    manifest = json.loads(manifest_path.read_text())
    completed_videos = []

    for entry in manifest:
        idx = entry["scene_index"]
        scene_name = f"Scene{idx:03d}"
        batch = get_batch(idx)
        duration = entry["duration"]
        
        print(f"--- Rendering {scene_name} (Duration: {duration}s) ---")
        os.environ["TARGET_DURATION"] = str(duration)
        
        cmd = [
            "../.venv/bin/manim", "-ql", 
            f"manim_scenes/scenes_obj_batch_{batch}.py", 
            scene_name
        ]
        subprocess.run(cmd, check=True)
        
        rendered_vid = Path(f"media/videos/scenes_obj_batch_{batch}/480p15/{scene_name}.mp4")
        out_dir = Path(f"output/scenes/scene_{idx:03d}")
        out_dir.mkdir(parents=True, exist_ok=True)
        
        vid_no_audio = out_dir / "video_no_audio.mp4"
        vid_no_audio.write_bytes(rendered_vid.read_bytes())
        
        audio = Path(entry["audio_file"])
        vid_with_audio = out_dir / "video_with_audio.mp4"
        
        if audio.exists():
            merge_video_audio(vid_no_audio, audio, vid_with_audio)
        else:
            print(f"Warning: No audio found for {scene_name}")
            vid_no_audio.rename(vid_with_audio)
            
        completed_videos.append(vid_with_audio)

    final_out = Path("output/final/final_video_with_audio.mp4")
    concat_mp4_files(completed_videos, final_out)
    print(f"Done! Final video is at {final_out}")

if __name__ == "__main__":
    main()