#!/usr/bin/env python3
"""
Render script for Object-Centric Learning video
Run: python render_all.py
"""

import subprocess
import sys
import os
from pathlib import Path

os.environ["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"

# Configuration
RESOLUTION = "1080p60"  # Can change to 720p30, 480p15, etc
QUALITY = "h"  # h=high, m=medium, l=low
PREVIEW = False  # Keep disabled in headless/Linux shell; preview needs xdg-open.
OUTPUT_DIR = "media/videos"

scenes = [
    "SlotAttentionIntro",
    "PixelsToObjects", 
    "SlotAttentionMechanism",
    "AlphaChannelBlending",
    "CausalIntervention",
    "EndingScene"
]

print("=" * 60)
print("Object-Centric Learning - Manim Render Script")
print("=" * 60)

for i, scene in enumerate(scenes, 1):
    print(f"\n[{i}/{len(scenes)}] Rendering: {scene}")
    print("-" * 60)
    
    flags = f"-{'p' if PREVIEW else ''}q{QUALITY}"
    cmd = [sys.executable, "-m", "manim", flags, "scene.py", scene]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✓ {scene} rendered successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error rendering {scene}: {e}")
        exit(1)

print("\n" + "=" * 60)
print("All scenes rendered successfully!")
print("=" * 60)
print("\nNext steps:")
print("1. Create narration MP3 files using TTS")
print("2. Run: python combine_video_audio.py")
print("3. Output: final_video_with_narration.mp4")
