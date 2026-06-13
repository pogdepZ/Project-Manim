#!/usr/bin/env python3
"""Render the rebuilt Part 4 / Part 5 Manim scenes."""

import os
import subprocess
import sys
from pathlib import Path


SCENE_FILE = "scene_part4_part5.py"
QUALITY = "m"

SCENES = [
    "Part04BridgeFromSlotAttention",
    "Part04SyntheticVsRealOverview",
    "Part04RealWorldComplexity",
    "Part04RGBReconstructionProblem",
    "Part04ResearchQuestionBeyondRGB",
    "Part05BeyondRGBOverview",
    "Part05OpticalFlowMotionCue",
    "Part05MotionLimitations",
    "Part05DepthLidarGeometryCue",
    "Part05DinosaurFeatureReconstruction",
    "Part05FinalSynthesisToEncoder",
]


def build_env():
    env = os.environ.copy()
    try:
        import imageio_ffmpeg

        ffmpeg_dir = str(Path(imageio_ffmpeg.get_ffmpeg_exe()).parent)
        env["PATH"] = ffmpeg_dir + os.pathsep + env.get("PATH", "")
    except Exception:
        pass
    return env


def main():
    env = build_env()
    for index, scene in enumerate(SCENES, start=1):
        print(f"[{index}/{len(SCENES)}] {scene}")
        subprocess.run(["manim", f"-q{QUALITY}", SCENE_FILE, scene], check=True, env=env)
    print("All rebuilt Part 4 / Part 5 scenes rendered.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Render failed: {exc}", file=sys.stderr)
        raise SystemExit(exc.returncode)
