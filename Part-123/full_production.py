#!/usr/bin/env python3
"""Run the full render, narration, and combine pipeline for one project."""

import argparse
import subprocess
import sys

from project_config import BASE_DIR, PROJECTS, get_project

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Run full video production.")
    parser.add_argument(
        "--project",
        default="object_centric_learning",
        choices=sorted(PROJECTS),
        help="Project key from project_config.py.",
    )
    parser.add_argument(
        "--skip-tts",
        action="store_true",
        help="Use existing narration files instead of regenerating them.",
    )
    parser.add_argument(
        "--quality",
        default="h",
        choices=["l", "m", "h", "k"],
        help="Render quality passed to render_all.py.",
    )
    return parser.parse_args()


def run_step(cmd, label):
    print("\n" + "=" * 70)
    print(label)
    print("=" * 70)
    subprocess.run(cmd, cwd=BASE_DIR, check=True)


def main():
    args = parse_args()
    project = get_project(args.project)

    print(f"Full production pipeline: {project['title']} ({args.project})")

    run_step(
        [
            sys.executable,
            "render_all.py",
            "--project",
            args.project,
            "--quality",
            args.quality,
        ],
        "Step 1/3: Render Manim scenes",
    )

    if not args.skip_tts:
        run_step(
            [sys.executable, "generate_narration.py", "--project", args.project],
            "Step 2/3: Generate narration",
        )
    else:
        print("\nStep 2/3: Generate narration skipped")

    run_step(
        [sys.executable, "combine_video_audio.py", "--project", args.project],
        "Step 3/3: Combine video and audio",
    )

    print("\nDone.")
    print(f"Output: {project['final_output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
