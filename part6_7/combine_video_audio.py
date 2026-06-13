#!/usr/bin/env python3
"""
Combine Manim video scenes and narration audio
Run: python combine_video_audio.py

Requires: ffmpeg installed (download from ffmpeg.org or: choco install ffmpeg)
"""

import subprocess
import os
import shutil
from pathlib import Path

import av

# Configuration
RESOLUTION = "1080p60"
OUTPUT_DIR = f"media/videos/scene/{RESOLUTION}"
SEGMENT_DIR = Path("temp_segments")
LOCAL_FFMPEG = Path(__file__).parent / ".venv" / "bin" / "ffmpeg"
FFMPEG = str(LOCAL_FFMPEG) if LOCAL_FFMPEG.exists() else "ffmpeg"

scenes = [
    ("SlotAttentionIntro", "narration/scene1.mp3"),
    ("PixelsToObjects", "narration/scene2.mp3"),
    ("SlotAttentionMechanism", "narration/scene3.mp3"),
    ("AlphaChannelBlending", "narration/scene4.mp3"),
    ("CausalIntervention", "narration/scene5.mp3"),
    ("EndingScene", "narration/scene6.mp3")
]

def run_command(cmd):
    """Run shell command and return success status"""
    printable_cmd = " ".join(str(part) for part in cmd)
    print(f"▶ {printable_cmd}")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def get_duration(path):
    """Return media duration in seconds using PyAV."""
    with av.open(str(path)) as container:
        if container.duration is None:
            return 0.0
        return float(container.duration / av.time_base)

def create_concat_file(segment_files):
    """Create FFmpeg concat demuxer file"""
    print("\n📝 Creating concat file...")
    
    concat_content = ""
    for segment_file in segment_files:
        concat_content += f"file '{segment_file.as_posix()}'\n"
    
    with open("concat.txt", "w") as f:
        f.write(concat_content)
    
    print("✓ concat.txt created")
    return concat_content

def validate_inputs():
    """Check if all required video and audio files exist."""
    print("\n🔎 Checking video and audio files...")

    for scene_name, audio_file in scenes:
        video_file = Path(OUTPUT_DIR) / f"{scene_name}.mp4"
        if not video_file.exists():
            print(f"❌ Missing: {video_file}")
            return False
        if not os.path.exists(audio_file):
            print(f"❌ Missing: {audio_file}")
            return False

    print("✓ All input files found")
    return True

def create_scene_segments():
    """Create one synced video+audio segment per scene."""
    print("\n🎬 Step 1: Creating synced scene segments...")

    SEGMENT_DIR.mkdir(exist_ok=True)
    segment_files = []

    for index, (scene_name, audio_file) in enumerate(scenes, 1):
        video_file = Path(OUTPUT_DIR) / f"{scene_name}.mp4"
        segment_file = SEGMENT_DIR / f"{index:02d}_{scene_name}.mp4"
        video_duration = get_duration(video_file)
        audio_duration = get_duration(audio_file)
        target_duration = max(video_duration, audio_duration)
        pad_duration = abs(video_duration - audio_duration)

        print(
            f"  {index}. {scene_name}: video={video_duration:.2f}s, "
            f"audio={audio_duration:.2f}s"
        )

        if audio_duration > video_duration + 0.05:
            cmd = [
                FFMPEG, "-y",
                "-i", str(video_file),
                "-i", audio_file,
                "-filter_complex",
                f"[0:v]tpad=stop_mode=clone:stop_duration={pad_duration:.3f}[v]",
                "-map", "[v]",
                "-map", "1:a",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-t", f"{target_duration:.3f}",
                str(segment_file),
            ]
        elif video_duration > audio_duration + 0.05:
            cmd = [
                FFMPEG, "-y",
                "-i", str(video_file),
                "-i", audio_file,
                "-filter_complex",
                f"[1:a]apad=pad_dur={pad_duration:.3f}[a]",
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-t", f"{target_duration:.3f}",
                str(segment_file),
            ]
        else:
            cmd = [
                FFMPEG, "-y",
                "-i", str(video_file),
                "-i", audio_file,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(segment_file),
            ]

        if not run_command(cmd):
            return None

        segment_files.append(segment_file)

    print("✓ Synced scene segments created")
    return segment_files

def combine_segments(segment_files):
    """Combine synced scene segments using FFmpeg concat."""
    print("\n▶️  Step 2: Combining synced segments...")

    create_concat_file(segment_files)
    cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat.txt",
        "-c", "copy",
        "final_video_with_narration.mp4",
    ]
    if not run_command(cmd):
        return False

    print("✓ final_video_with_narration.mp4 created")
    return True

def add_background_music():
    """Optional: Add background music (lofi ambient)"""
    print("\n🎵 Optional: Adding background music (if available)...")
    
    if not os.path.exists("background_music.mp3"):
        print("⏭️  Skipping (background_music.mp3 not found)")
        return True
    
    cmd = [
        FFMPEG,
        "-i", "final_video_with_narration.mp4",
        "-i", "background_music.mp3",
        "-filter_complex", "[1:a]volume=0.1[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "final_video_with_music.mp4",
    ]
    if not run_command(cmd):
        return False
    
    print("✓ final_video_with_music.mp4 created")
    return True

def validate_output():
    """Validate output file"""
    print("\n✅ Validating output...")
    
    if not os.path.exists("final_video_with_narration.mp4"):
        print("❌ Output file not found!")
        return False
    
    with av.open("final_video_with_narration.mp4") as container:
        duration = 0.0 if container.duration is None else container.duration / av.time_base
        print(f"✓ Duration: {duration:.2f} seconds")
        print(f"✓ Streams: {len(container.streams)}")
    
    file_size = os.path.getsize("final_video_with_narration.mp4") / (1024 * 1024)
    print(f"\n✓ Output file size: {file_size:.2f} MB")
    return True

def cleanup():
    """Optional: Clean up temporary files"""
    print("\n🧹 Cleaning up temporary files...")
    
    temp_files = ["concat.txt"]
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"✓ Removed {f}")

    if SEGMENT_DIR.exists():
        shutil.rmtree(SEGMENT_DIR)
        print(f"✓ Removed {SEGMENT_DIR}")

def main():
    print("=" * 70)
    print("Video + Narration Combiner (FFmpeg)")
    print("=" * 70)
    
    print("\n📋 Scenes to process:")
    for i, (scene, audio) in enumerate(scenes, 1):
        print(f"  {i}. {scene} + {audio}")
    
    # Step 1: Validate video and audio files
    if not validate_inputs():
        print("\n❌ Missing inputs. Run render_all.py and generate_narration.py first.")
        return False

    # Step 2: Create synced scene segments
    segment_files = create_scene_segments()
    if not segment_files:
        return False

    # Step 3: Combine synced segments
    if not combine_segments(segment_files):
        return False
    
    # Step 6: Optionally add music
    # add_background_music()  # Uncomment if you have background_music.mp3
    
    # Step 7: Validate
    if not validate_output():
        return False
    
    # Step 8: Cleanup
    cleanup()
    
    print("\n" + "=" * 70)
    print("✓ SUCCESS! Video ready:")
    print("  📹 final_video_with_narration.mp4")
    print("=" * 70)
    print("\n📺 Open with: VLC, Windows Media Player, or browser")
    print("📤 Upload to: YouTube, TikTok, Instagram Reels")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
