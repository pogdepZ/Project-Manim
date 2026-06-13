
import json
import subprocess
from pathlib import Path

def merge_video_audio(video_file, audio_file, output_file):
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_file),
        "-i", str(audio_file),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        str(output_file)
    ]
    subprocess.run(cmd, check=True)

def main():
    base_dir = Path("/home/pognova/SkillManim")
    builder_dir = base_dir / "manim-video-builder"
    
    scenes_to_fix = [16, 22, 24, 31]
    
    for idx in scenes_to_fix:
        scene_name = f"scene_{idx:03d}"
        print(f"Updating {scene_name}...")
        
        rendered_vid = base_dir / f"videos/{scene_name}/720p30/GeneratedVideo.mp4"
        if not rendered_vid.exists():
            print(f"Error: {rendered_vid} not found")
            continue
            
        out_dir = builder_dir / f"output/scenes/{scene_name}"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        vid_no_audio = out_dir / "video_no_audio.mp4"
        vid_no_audio.write_bytes(rendered_vid.read_bytes())
        
        audio_file = out_dir / "narration.mp3"
        if not audio_file.exists():
            # Try to find it via manifest if it's not in out_dir
            manifest_path = builder_dir / "output/final/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            for entry in manifest:
                if entry["scene_index"] == idx:
                    audio_file = builder_dir / entry["audio_file"]
                    break
        
        vid_with_audio = out_dir / "video_with_audio.mp4"
        if audio_file.exists():
            print(f"Merging with {audio_file}")
            merge_video_audio(vid_no_audio, audio_file, vid_with_audio)
        else:
            print(f"Warning: Audio not found for {scene_name}")
            vid_with_audio.write_bytes(vid_no_audio.read_bytes())

if __name__ == "__main__":
    main()
