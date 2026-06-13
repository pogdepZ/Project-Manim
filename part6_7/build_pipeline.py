import re
from pathlib import Path

content = Path("merged_script_content.txt").read_text(encoding="utf-8")
lines = content.split('\n')

scenes_data = []
current_scene_title = ""
current_scene_text = []

# Manual mapping to scene names
scene_names = [
    "S6_01_CNNFailure", "S6_02_FeatureReconstruction", "S6_03_ViTArchitecture", 
    "S6_04_DINOSAURModel", "S6_05_SSLComparison", "S6_06_EncoderUpgradeChallenge", 
    "S6_07_OpticalFlowDepth", "S6_08_AdaSlot", "S6_09_VideoSaur", "S6_10_Part6Summary",
    "S7_01_SlotDecodingDilemma", "S7_02_PixelIndependence", "S7_03_TwoDirections",
    "S7_04_MLPvsTransformer", "S7_05_SLATEDecoder", "S7_06_DiffusionLSD", "S7_07_DORSAL3D",
    "S7_08_ObSuRF", "S7_09_OSRT", "S7_10_SysBinder", "S7_11_MoToK", "S7_12_CoSA",
    "S7_13_ISA", "S7_14_DiffFAE", "S7_15_PaLME", "S7_16_ThreeParadigms", "S7_17_Part7Summary"
]

current_idx = -1
for line in lines:
    line = line.strip()
    if not line: continue
    if line.startswith("MỤC LỤC") or line.startswith("Lưu ý:") or line.startswith("TÀI LIỆU") or line.startswith("["):
        continue
        
    # Match headers like "6.1. " or "7.1. ", avoiding "6.7.1."
    match = re.match(r"^([67]\.\d+)\.(?!\d)\s*(.*)", line)
    if match:
        current_idx += 1
        current_scene_title = match.group(2)
        scenes_data.append({"name": scene_names[current_idx], "text": ""})
    elif line.startswith("PHẦN"):
        pass
    else:
        if current_idx >= 0 and current_idx < len(scene_names):
            scenes_data[current_idx]["text"] += line + " "

# Clean texts
for s in scenes_data:
    s["text"] = s["text"].strip()

# Generate generate_narration_part6_7.py
narration_code = '''#!/usr/bin/env python3
"""
Generate Vietnamese narration for Part 6 & Part 7 using Microsoft Edge TTS.
Run: python generate_narration_part6_7.py

Requires: pip install edge-tts pydub
"""

import asyncio
import subprocess
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts


narrations = {
'''

for i, s in enumerate(scenes_data):
    text = s["text"].replace('"', '\\"')
    narration_code += f'    "scene{i+1}": (\n        "{text}"\n    ),\n'

narration_code += '''}

VOICE = "vi-VN-HoaiMyNeural"
RATE = "+0%"


async def generate_narration(key, text, output_file):
    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        print(f"🎙️  Generating: {output_file}... attempt {attempt}/{max_attempts}")
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
            await communicate.save(output_file)
            if Path(output_file).stat().st_size == 0:
                raise RuntimeError("TTS returned an empty file")
            print(f"✓ {output_file} created ({len(text)} chars)")
            return
        except Exception as exc:
            if attempt == max_attempts:
                print(f"❌ Failed to generate {output_file} after {max_attempts} attempts.")
                raise
            sleep_time = 3 + attempt * 2
            print(f"  retrying after TTS error: {exc}. Waiting {sleep_time}s...")
            await asyncio.sleep(sleep_time)


async def main():
    print("=" * 60)
    print("Vietnamese Narration Generator — Part 6 & Part 7")
    print("=" * 60)

    output_dir = Path("narration_part6_7")
    output_dir.mkdir(exist_ok=True)

    print(f"\\n📁 Output directory: {output_dir}")
    print(f"🎤 Voice: {VOICE}\\n")

    for key, text in narrations.items():
        output_file = output_dir / f"{key}.mp3"
        await generate_narration(key, text, str(output_file))

    print("\\n" + "=" * 60)
    print("✓ All narration files generated!")
    print("=" * 60)
    print("\\nNext step: Run: python combine_part6_7.py")


if __name__ == "__main__":
    asyncio.run(main())
'''

Path("generate_narration_part6_7.py").write_text(narration_code, encoding="utf-8")

# Generate render_part6_7.py
render_code = '''#!/usr/bin/env python3
"""
Render script for Object-Centric Learning Part 6 & Part 7 video.
Run: python render_part6_7.py
"""

import subprocess
import sys
import os
from pathlib import Path

os.environ["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"

# Configuration
RESOLUTION = "1080p60"  # Can change to 720p30, 480p15, etc
QUALITY = "h"  # h=high, m=medium, l=low
PREVIEW = False
SCENE_FILE = "scene_part6_7.py"

scenes = [
'''

for s in scenes_data:
    render_code += f'    "{s["name"]}",\n'

render_code += ''']

print("=" * 60)
print("OCL Part 6 & 7 — Manim Render Script")
print(f"Quality: {RESOLUTION} | File: {SCENE_FILE}")
print("=" * 60)

for i, scene in enumerate(scenes, 1):
    print(f"\\n[{i}/{len(scenes)}] Rendering: {scene}")
    print("-" * 60)

    flags = f"-{'p' if PREVIEW else ''}q{QUALITY}"
    cmd = [sys.executable, "-m", "manim", flags, SCENE_FILE, scene]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ {scene} rendered successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error rendering {scene}: {e}")
        exit(1)

print("\\n" + "=" * 60)
print("All scenes rendered successfully!")
print("=" * 60)
print("\\nNext steps:")
print("1. Generate narration: python generate_narration_part6_7.py")
print("2. Combine: python combine_part6_7.py")
print("3. Output: final_part6_7.mp4")
'''

Path("render_part6_7.py").write_text(render_code, encoding="utf-8")

# Generate combine_part6_7.py
combine_code = '''#!/usr/bin/env python3
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
'''

for i, s in enumerate(scenes_data):
    combine_code += f'    ("{s["name"]}", f"{{NARRATION_DIR}}/scene{i+1}.mp3"),\n'

combine_code += ''']

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
    print("\\n📝 Creating concat file...")
    content = ""
    for seg in segment_files:
        content += f"file '{seg.as_posix()}'\\n"
    with open("concat_part6_7.txt", "w") as f:
        f.write(content)
    print("✓ concat_part6_7.txt created")
    return content

def validate_inputs():
    print("\\n🔎 Checking video and audio files...")
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
    print("\\n🎬 Step 1: Creating synced scene segments...")
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
    print("\\n▶️  Step 2: Combining synced segments...")
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
    print("\\n✅ Validating output...")
    if not os.path.exists("final_part6_7.mp4"):
        print("❌ Output file not found!")
        return False

    with av.open("final_part6_7.mp4") as container:
        dur = 0.0 if container.duration is None else container.duration / av.time_base
        print(f"✓ Duration: {dur:.2f} seconds")
        print(f"✓ Streams: {len(container.streams)}")

    size_mb = os.path.getsize("final_part6_7.mp4") / (1024 * 1024)
    print(f"\\n✓ Output file size: {size_mb:.2f} MB")
    return True

def cleanup():
    print("\\n🧹 Cleaning up temporary files...")
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

    print("\\n📋 Scenes to process:")
    for i, (scene, audio) in enumerate(scenes, 1):
        print(f"  {i}. {scene} + {audio}")

    if not validate_inputs():
        print("\\n❌ Missing inputs. Run render_part6_7.py and generate_narration_part6_7.py first.")
        return False

    segment_files = create_scene_segments()
    if not segment_files:
        return False

    if not combine_segments(segment_files):
        return False

    if not validate_output():
        return False

    cleanup()

    print("\\n" + "=" * 70)
    print("✓ SUCCESS! Video ready:")
    print("  📹 final_part6_7.mp4")
    print("=" * 70)
    print("\\n📺 Open with: VLC, Windows Media Player, or browser")
    print("📤 Upload to: YouTube, TikTok, Instagram Reels")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
'''

Path("combine_part6_7.py").write_text(combine_code, encoding="utf-8")
print("Successfully generated all pipeline scripts for 27 scenes.")
