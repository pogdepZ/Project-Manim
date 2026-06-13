from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(args: list[str]) -> str:
    completed = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr)
    return completed.stdout


def duration(path: Path) -> float:
    return float(
        run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ]
        ).strip()
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a contact sheet for rendered scene layout QA.")
    parser.add_argument("--scenes-dir", type=Path, default=Path("output/scenes"))
    parser.add_argument("--output", type=Path, default=Path("output/final/layout_contact_sheet.jpg"))
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=320)
    parser.add_argument("--thumb-height", type=int, default=180)
    args = parser.parse_args()

    frames_dir = args.output.parent / "_layout_contact_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    scene_dirs = [p for p in sorted(args.scenes_dir.glob("scene_*")) if (p / "video_no_audio.mp4").exists()]
    if not scene_dirs:
        raise SystemExit(f"No rendered scenes found in {args.scenes_dir}")

    for scene_dir in scene_dirs:
        video = scene_dir / "video_no_audio.mp4"
        midpoint = duration(video) * 0.5
        image = frames_dir / f"{scene_dir.name}.jpg"
        run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{midpoint:.3f}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-vf",
                (
                    f"scale={args.thumb_width}:{args.thumb_height},"
                    f"drawtext=text='{scene_dir.name}':x=8:y=8:fontsize=18:"
                    "fontcolor=white:box=1:boxcolor=black@0.55"
                ),
                "-q:v",
                "3",
                str(image),
            ]
        )

    rows = (len(scene_dirs) + args.cols - 1) // args.cols
    args.output.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-pattern_type",
            "glob",
            "-i",
            str(frames_dir / "scene_*.jpg"),
            "-vf",
            f"tile={args.cols}x{rows}:padding=8:margin=8:color=0x202020",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(args.output),
        ]
    )
    print(args.output)


if __name__ == "__main__":
    main()
