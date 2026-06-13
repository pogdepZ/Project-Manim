#!/usr/bin/env python3
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
    "S6_01_CNNFailure",
    "S6_02_FeatureReconstruction",
    "S6_03_ViTArchitecture",
    "S6_04_DINOSAURModel",
    "S6_05_SSLComparison",
    "S6_06_EncoderUpgradeChallenge",
    "S6_07_OpticalFlowDepth",
    "S6_08_AdaSlot",
    "S6_09_VideoSaur",
    "S6_10_Part6Summary",
    "S7_01_SlotDecodingDilemma",
    "S7_02_PixelIndependence",
    "S7_03_TwoDirections",
    "S7_04_MLPvsTransformer",
    "S7_05_SLATEDecoder",
    "S7_06_DiffusionLSD",
    "S7_07_DORSAL3D",
    "S7_08_ObSuRF",
    "S7_09_OSRT",
    "S7_10_SysBinder",
    "S7_11_MoToK",
    "S7_12_CoSA",
    "S7_13_ISA",
    "S7_14_DiffFAE",
    "S7_15_PaLME",
    "S7_16_ThreeParadigms",
    "S7_17_Part7Summary",
]

print("=" * 60)
print("OCL Part 6 & 7 — Manim Render Script")
print(f"Quality: {RESOLUTION} | File: {SCENE_FILE}")
print("=" * 60)

for i, scene in enumerate(scenes, 1):
    print(f"\n[{i}/{len(scenes)}] Rendering: {scene}")
    print("-" * 60)

    flags = f"-{'p' if PREVIEW else ''}q{QUALITY}"
    cmd = [sys.executable, "-m", "manim", flags, "--disable_caching", SCENE_FILE, scene]

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
print("1. Generate narration: python generate_narration_part6_7.py")
print("2. Combine: python combine_part6_7.py")
print("3. Output: final_part6_7.mp4")
