import json
from pathlib import Path
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Ensure src module is in path
sys.path.append(str(Path(__file__).parent / "src"))
from merger import concat_mp4_files

def finalize():
    manifest_path = Path("output/final/manifest.json")
    if not manifest_path.exists():
        logging.error("Manifest not found at %s", manifest_path)
        return

    try:
        manifest = json.loads(manifest_path.read_text())
    except Exception as e:
        logging.error("Failed to parse manifest: %s", e)
        return

    video_files = []
    for entry in manifest:
        idx = entry["scene_index"]
        # Use the video_with_audio path from manifest, or construct it
        vid_path = Path(entry.get("video_with_audio", f"output/scenes/scene_{idx:03d}/video_with_audio.mp4"))
        
        if not vid_path.exists():
            logging.warning("Video for scene %d not found at %s", idx, vid_path)
            # Try alternative if it exists in the output/scenes folder
            alt_path = Path(f"output/scenes/scene_{idx:03d}/video_with_audio.mp4")
            if alt_path.exists():
                vid_path = alt_path
            else:
                logging.error("Missing video for scene %d. Aborting.", idx)
                return

        video_files.append(vid_path)
        logging.info("Added scene %d: %s", idx, vid_path)

    output_file = Path("output/final/final_video_with_audio.mp4")
    logging.info("Concatenating %d scenes into %s", len(video_files), output_file)
    
    try:
        concat_mp4_files(video_files, output_file)
        logging.info("Final video successfully created at %s", output_file)
    except Exception as e:
        logging.error("Failed to concatenate videos: %s", e)

if __name__ == "__main__":
    finalize()
