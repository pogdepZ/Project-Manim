#!/usr/bin/env python3
"""
The Part 6/7 scenes are now hand-built in scene_part6_7.py.

The old version of this file regenerated scene_part6_7.py with text-only
slides, which would remove the visual diagrams from S6_05 through S7_17.
Keep this guard so accidental runs do not overwrite the production scene file.
"""

from pathlib import Path


SCENE_FILE = Path("scene_part6_7.py")


def main():
    if not SCENE_FILE.exists():
        raise SystemExit(f"Missing {SCENE_FILE}.")

    print(f"{SCENE_FILE} already contains the illustrated Manim scenes.")
    print("No files were changed.")


if __name__ == "__main__":
    main()
