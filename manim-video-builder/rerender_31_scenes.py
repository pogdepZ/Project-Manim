import json
import re
import subprocess
from pathlib import Path
import os
import sys

# Define base directory
BASE_DIR = Path("/home/pognova/SkillManim")
BUILDER_DIR = BASE_DIR / "manim-video-builder"

# Add src to path
sys.path.append(str(BUILDER_DIR / "src"))
try:
    from merger import merge_video_audio, concat_mp4_files
except ImportError:
    print("Could not import merger. Ensure you are running from the correct directory or PYTHONPATH is set.")
    sys.exit(1)

def update_scene_file(file_path, voice, duration):
    if not file_path.exists():
        return
    content = file_path.read_text(encoding="utf-8")
    
    # Update voice
    voice_pattern = r"voice\s*=\s*'.*?'"
    if not re.search(voice_pattern, content, re.DOTALL):
        # Try double quotes
        voice_pattern = r'voice\s*=\s*".*?"'
        
    # We use repr() to handle escaping and newlines
    new_voice = f"voice={repr(voice)}"
    content = re.sub(voice_pattern, new_voice, content, flags=re.DOTALL)
    
    # Update duration
    duration_pattern = r"duration\s*=\s*[\d\.]+"
    new_duration = f"duration={duration:.3f}"
    content = re.sub(duration_pattern, new_duration, content)
    
    file_path.write_text(content, encoding="utf-8")

def main():
    manifest_path = BUILDER_DIR / "output/final/manifest.json"
    if not manifest_path.exists():
        print(f"Manifest not found at {manifest_path}!")
        return

    manifest = json.loads(manifest_path.read_text())
    completed_videos = []

    # Ensure output directories exist
    (BUILDER_DIR / "output/scenes").mkdir(parents=True, exist_ok=True)

    for entry in manifest:
        idx = entry["scene_index"]
        if idx > 31:
            break
            
        scene_name = f"scene_{idx:03d}"
        py_file = BUILDER_DIR / f"manim_scenes/{scene_name}.py"
        
        if not py_file.exists():
            print(f"Skipping {scene_name}, file not found at {py_file}.")
            continue
            
        print(f"\n--- Processing {scene_name} (Index: {idx}) ---", flush=True)
        
        # Render
        # Using -qm (Medium Quality) for balance. 
        # Using --flush_cache to ignore cached data.
        cmd = [
            str(BASE_DIR / ".venv/bin/manim"), "-qm",
            "--flush_cache",
            "--media_dir", str(BASE_DIR),
            str(py_file), "GeneratedVideo"
        ]
        print(f"Running: {' '.join(cmd)}", flush=True)
        result = subprocess.run(cmd, capture_output=True, text=True) # Capture output to log errors better
        
        if result.returncode != 0:
            print(f"Error rendering {scene_name}:")
            print(result.stderr)
            continue

        # Manim output path
        rendered_vid = BASE_DIR / f"videos/{scene_name}/720p30/GeneratedVideo.mp4"

        if not rendered_vid.exists():
            # Try with media/ prefix just in case
            rendered_vid = BASE_DIR / f"media/videos/{scene_name}/720p30/GeneratedVideo.mp4"

        if not rendered_vid.exists():
            print(f"Error: Could not find rendered video for {scene_name}")
            continue
            
        out_dir = BUILDER_DIR / f"output/scenes/{scene_name}"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        vid_no_audio = out_dir / "video_no_audio.mp4"
        vid_no_audio.write_bytes(rendered_vid.read_bytes())
        
        # Audio path in manifest is relative to BUILDER_DIR
        audio_rel_path = entry["audio_file"]
        audio = BUILDER_DIR / audio_rel_path
        vid_with_audio = out_dir / "video_with_audio.mp4"
        
        if audio.exists():
            print(f"Merging with audio: {audio}", flush=True)
            merge_video_audio(vid_no_audio, audio, vid_with_audio)
        else:
            print(f"Warning: No audio found for {scene_name} at {audio}", flush=True)
            # If no audio, just use the video as is
            vid_with_audio.write_bytes(vid_no_audio.read_bytes())
            
        print(f"SCENE_COMPLETED: {scene_name}")
        completed_videos.append(vid_with_audio)

    if completed_videos:
        final_out = BUILDER_DIR / "output/final/final_video_upgraded.mp4"
        final_out_audio = BUILDER_DIR / "output/final/final_video_upgraded_with_audio.mp4"
        final_out.parent.mkdir(parents=True, exist_ok=True)
        print(f"\nConcatenating {len(completed_videos)} videos...")
        concat_mp4_files(completed_videos, final_out)
        print(f"Done! Final video is at {final_out}")
        
        narration_file = BUILDER_DIR / "output/final/narration.mp3"
        if narration_file.exists():
            print(f"Merging final video with narration: {narration_file}")
            merge_video_audio(final_out, narration_file, final_out_audio)
            print(f"Done! Final video with audio is at {final_out_audio}")
        else:
            print("Warning: output/final/narration.mp3 not found. Final video will not have audio.")
    else:
        print("No videos were rendered.")

if __name__ == "__main__":
    main()
