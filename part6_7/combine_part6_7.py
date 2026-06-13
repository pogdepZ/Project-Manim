#!/usr/bin/env python3
"""
Combine Manim video scenes and narration audio for Part 6 & Part 7.
Run: python combine_part6_7.py

Requires: ffmpeg installed
"""

import subprocess
import os
import shutil
from pathlib import Path

try:
    import av
except ImportError:
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "av"])
    import av

# Configuration
RESOLUTION = "1080p60"
OUTPUT_DIR = f"media/videos/scene_part6_7/{RESOLUTION}"
NARRATION_DIR = "narration_part6_7"
SEGMENT_DIR = Path("temp_segments_part6_7")
LOCAL_FFMPEG = Path(__file__).parent / ".venv" / "bin" / "ffmpeg"
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = str(LOCAL_FFMPEG) if LOCAL_FFMPEG.exists() else "ffmpeg"

scenes = [
    ("S6_01_CNNFailure", f"{NARRATION_DIR}/scene1.mp3"),
    ("S6_02_FeatureReconstruction", f"{NARRATION_DIR}/scene2.mp3"),
    ("S6_03_ViTArchitecture", f"{NARRATION_DIR}/scene3.mp3"),
    ("S6_04_DINOSAURModel", f"{NARRATION_DIR}/scene4.mp3"),
    ("S6_05_SSLComparison", f"{NARRATION_DIR}/scene5.mp3"),
    ("S6_06_EncoderUpgradeChallenge", f"{NARRATION_DIR}/scene6.mp3"),
    ("S6_07_OpticalFlowDepth", f"{NARRATION_DIR}/scene7.mp3"),
    ("S6_08_AdaSlot", f"{NARRATION_DIR}/scene8.mp3"),
    ("S6_09_VideoSaur", f"{NARRATION_DIR}/scene9.mp3"),
    ("S6_10_Part6Summary", f"{NARRATION_DIR}/scene10.mp3"),
    ("S7_01_SlotDecodingDilemma", f"{NARRATION_DIR}/scene11.mp3"),
    ("S7_02_PixelIndependence", f"{NARRATION_DIR}/scene12.mp3"),
    ("S7_03_TwoDirections", f"{NARRATION_DIR}/scene13.mp3"),
    ("S7_04_MLPvsTransformer", f"{NARRATION_DIR}/scene14.mp3"),
    ("S7_05_SLATEDecoder", f"{NARRATION_DIR}/scene15.mp3"),
    ("S7_06_DiffusionLSD", f"{NARRATION_DIR}/scene16.mp3"),
    ("S7_07_DORSAL3D", f"{NARRATION_DIR}/scene17.mp3"),
    ("S7_08_ObSuRF", f"{NARRATION_DIR}/scene18.mp3"),
    ("S7_09_OSRT", f"{NARRATION_DIR}/scene19.mp3"),
    ("S7_10_SysBinder", f"{NARRATION_DIR}/scene20.mp3"),
    ("S7_11_MoToK", f"{NARRATION_DIR}/scene21.mp3"),
    ("S7_12_CoSA", f"{NARRATION_DIR}/scene22.mp3"),
    ("S7_13_ISA", f"{NARRATION_DIR}/scene23.mp3"),
    ("S7_14_DiffFAE", f"{NARRATION_DIR}/scene24.mp3"),
    ("S7_15_PaLME", f"{NARRATION_DIR}/scene25.mp3"),
    ("S7_16_ThreeParadigms", f"{NARRATION_DIR}/scene26.mp3"),
    ("S7_17_Part7Summary", f"{NARRATION_DIR}/scene27.mp3"),
]

def run_cmd(cmd):
    printable = " ".join(str(p) for p in cmd)
    print(f"▶ {printable}")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def get_duration(path):
    with av.open(str(path)) as container:
        if container.duration is None:
            return 0.0
        return float(container.duration / av.time_base)

def create_concat_file(segment_files):
    print("\n📝 Creating concat file...")
    content = ""
    for seg in segment_files:
        content += f"file '{seg.as_posix()}'\n"
    with open("concat_part6_7.txt", "w") as f:
        f.write(content)
    print("✓ concat_part6_7.txt created")
    return content

def validate_inputs():
    print("\n🔎 Checking video and audio files...")
    all_ok = True
    for scene_name, audio_file in scenes:
        video_file = Path(OUTPUT_DIR) / f"{scene_name}.mp4"
        if not video_file.exists():
            print(f"❌ Missing video: {video_file}")
            all_ok = False
        if not os.path.exists(audio_file):
            print(f"❌ Missing audio: {audio_file}")
            all_ok = False

    if all_ok:
        print("✓ All input files found")
    return all_ok

def create_scene_segments():
    print("\n🎬 Step 1: Creating synced scene segments...")
    SEGMENT_DIR.mkdir(exist_ok=True)
    segment_files = []

    for index, (scene_name, audio_file) in enumerate(scenes, 1):
        video_file = Path(OUTPUT_DIR) / f"{scene_name}.mp4"
        segment_file = SEGMENT_DIR / f"{index:02d}_{scene_name}.mp4"
        video_dur = get_duration(video_file)
        audio_dur = get_duration(audio_file)
        target_dur = max(video_dur, audio_dur)
        pad_dur = abs(video_dur - audio_dur)

        print(f"  {index}. {scene_name}: video={video_dur:.2f}s, audio={audio_dur:.2f}s")

        if audio_dur > video_dur + 0.05:
            cmd = [
                FFMPEG, "-y",
                "-i", str(video_file),
                "-i", audio_file,
                "-filter_complex",
                f"[0:v]tpad=stop_mode=clone:stop_duration={pad_dur:.3f}[v]",
                "-map", "[v]", "-map", "1:a",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-t", f"{target_dur:.3f}",
                str(segment_file),
            ]
        elif video_dur > audio_dur + 0.05:
            cmd = [
                FFMPEG, "-y",
                "-i", str(video_file),
                "-i", audio_file,
                "-filter_complex",
                f"[1:a]apad=pad_dur={pad_dur:.3f}[a]",
                "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac",
                "-t", f"{target_dur:.3f}",
                str(segment_file),
            ]
        else:
            cmd = [
                FFMPEG, "-y",
                "-i", str(video_file),
                "-i", audio_file,
                "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac",
                "-shortest",
                str(segment_file),
            ]

        if not run_cmd(cmd):
            return None
        segment_files.append(segment_file)

    print("✓ Synced scene segments created")
    return segment_files

def combine_segments(segment_files):
    print("\n▶️  Step 2: Combining synced segments...")
    create_concat_file(segment_files)
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", "concat_part6_7.txt",
        "-c", "copy",
        "final_part6_7.mp4",
    ]
    if not run_cmd(cmd):
        return False
    print("✓ final_part6_7.mp4 created")
    return True

def validate_output():
    print("\n✅ Validating output...")
    if not os.path.exists("final_part6_7.mp4"):
        print("❌ Output file not found!")
        return False

    with av.open("final_part6_7.mp4") as container:
        dur = 0.0 if container.duration is None else container.duration / av.time_base
        print(f"✓ Duration: {dur:.2f} seconds")
        print(f"✓ Streams: {len(container.streams)}")

    size_mb = os.path.getsize("final_part6_7.mp4") / (1024 * 1024)
    print(f"\n✓ Output file size: {size_mb:.2f} MB")
    return True

def cleanup():
    print("\n🧹 Cleaning up temporary files...")
    for f in ["concat_part6_7.txt"]:
        if os.path.exists(f):
            os.remove(f)
            print(f"✓ Removed {f}")
    if SEGMENT_DIR.exists():
        shutil.rmtree(SEGMENT_DIR)
        print(f"✓ Removed {SEGMENT_DIR}")

def main():
    print("=" * 70)
    print("Video + Narration Combiner — Part 6 & Part 7")
    print("=" * 70)

    print("\n📋 Scenes to process:")
    for i, (scene, audio) in enumerate(scenes, 1):
        print(f"  {i}. {scene} + {audio}")

    if not validate_inputs():
        print("\n❌ Missing inputs. Run render_part6_7.py and generate_narration_part6_7.py first.")
        return False

    segment_files = create_scene_segments()
    if not segment_files:
        return False

    if not combine_segments(segment_files):
        return False

    if not validate_output():
        return False

    cleanup()

    print("\n" + "=" * 70)
    print("✓ SUCCESS! Video ready:")
    print("  📹 final_part6_7.mp4")
    print("=" * 70)
    print("\n📺 Open with: VLC, Windows Media Player, or browser")
    print("📤 Upload to: YouTube, TikTok, Instagram Reels")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
