#!/usr/bin/env python3
"""Render one registered Manim project.

Examples:
  python render_all.py --project object_centric_learning
  python render_all.py --project autonomous_driving --quality m
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from project_config import BASE_DIR, PROJECTS, get_project

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


QUALITY_FLAGS = {
    "l": "ql",
    "m": "qm",
    "h": "qh",
    "k": "qk",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Render a registered Manim project.")
    parser.add_argument(
        "--project",
        default="object_centric_learning",
        choices=sorted(PROJECTS),
        help="Project key from project_config.py.",
    )
    parser.add_argument(
        "--quality",
        default="h",
        choices=sorted(QUALITY_FLAGS),
        help="Manim quality: l=480p15, m=720p30, h=1080p60, k=4k.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Open each rendered scene after rendering. Avoid this on headless servers.",
    )
    parser.add_argument(
        "--scene",
        action="append",
        dest="scenes",
        help="Render only this scene class. Can be passed multiple times.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    project = get_project(args.project)
    scenes = args.scenes or project["scenes"]

    env = os.environ.copy()
    env["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{env.get('PATH', '')}"
    env["PYTHONPATH"] = f"{BASE_DIR}{os.pathsep}{env.get('PYTHONPATH', '')}"

    flags = f"-{'p' if args.preview else ''}{QUALITY_FLAGS[args.quality]}"

    print("=" * 70)
    print(f"Rendering project: {project['title']} ({args.project})")
    print(f"Scene file: {project['scene_file'].relative_to(BASE_DIR)}")
    print(f"Scenes: {', '.join(scenes)}")
    print("=" * 70)

    for index, scene in enumerate(scenes, 1):
        print(f"\n[{index}/{len(scenes)}] Rendering {scene}")
        cmd = [
            sys.executable,
            "-m",
            "manim",
            flags,
            str(project["scene_file"].relative_to(BASE_DIR)),
            scene,
        ]
        subprocess.run(cmd, cwd=BASE_DIR, env=env, check=True)

    print("\nDone.")
    print("Manim output is under Video/media/ and should stay out of git.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
