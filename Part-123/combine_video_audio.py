#!/usr/bin/env python3
"""Combine rendered Manim scenes with narration for one project."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import av

from project_config import BASE_DIR, PROJECTS, get_project

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RESOLUTION = "1080p60"
LOCAL_FFMPEG = BASE_DIR / ".venv" / "bin" / "ffmpeg"
FFMPEG = str(LOCAL_FFMPEG) if LOCAL_FFMPEG.exists() else "ffmpeg"


def parse_args():
    parser = argparse.ArgumentParser(description="Combine project video and audio.")
    parser.add_argument(
        "--project",
        default="object_centric_learning",
        choices=sorted(PROJECTS),
        help="Project key from project_config.py.",
    )
    parser.add_argument("--speed", type=float, default=1.0, help="Final playback speed.")
    return parser.parse_args()


def run_command(cmd):
    print(" ".join(str(part) for part in cmd))
    subprocess.run(cmd, check=True)


def get_duration(path):
    with av.open(str(path)) as container:
        if container.duration is None:
            return 0.0
        return float(container.duration / av.time_base)


def create_concat_file(segment_files, concat_file):
    concat_file.write_text(
        "".join(f"file '{segment_file.as_posix()}'\n" for segment_file in segment_files),
        encoding="utf-8",
    )


def build_inputs(project_key, project):
    video_dir = BASE_DIR / "media" / "videos" / project["manim_output_name"] / RESOLUTION
    narration_dir = BASE_DIR / "narration" / project_key
    narration_keys = project.get("narration_keys", [])

    if not narration_keys:
        raise SystemExit(f"Project '{project_key}' has no narration_keys configured.")

    if len(project["scenes"]) != len(narration_keys):
        raise SystemExit(
            f"Project '{project_key}' has {len(project['scenes'])} scenes but "
            f"{len(narration_keys)} narration keys."
        )

    return [
        (scene_name, video_dir / f"{scene_name}.mp4", narration_dir / f"{key}.mp3")
        for scene_name, key in zip(project["scenes"], narration_keys)
    ]


def validate_inputs(inputs):
    missing = []
    for _, video_file, audio_file in inputs:
        if not video_file.exists():
            missing.append(video_file)
        if not audio_file.exists():
            missing.append(audio_file)

    if missing:
        print("Missing inputs:")
        for path in missing:
            print(f"  {path.relative_to(BASE_DIR)}")
        return False
    return True


def create_scene_segments(project_key, inputs):
    segment_dir = BASE_DIR / "temp_segments" / project_key
    segment_dir.mkdir(parents=True, exist_ok=True)
    segment_files = []

    for index, (scene_name, video_file, audio_file) in enumerate(inputs, 1):
        segment_file = segment_dir / f"{index:02d}_{scene_name}.mp4"
        video_duration = get_duration(video_file)
        audio_duration = get_duration(audio_file)
        target_duration = max(video_duration, audio_duration)
        pad_duration = abs(video_duration - audio_duration)

        print(
            f"{index}. {scene_name}: video={video_duration:.2f}s, "
            f"audio={audio_duration:.2f}s"
        )

        if audio_duration > video_duration + 0.05:
            cmd = [
                FFMPEG,
                "-y",
                "-i",
                str(video_file),
                "-i",
                str(audio_file),
                "-filter_complex",
                f"[0:v]tpad=stop_mode=clone:stop_duration={pad_duration:.3f}[v]",
                "-map",
                "[v]",
                "-map",
                "1:a",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-t",
                f"{target_duration:.3f}",
                str(segment_file),
            ]
        elif video_duration > audio_duration + 0.05:
            cmd = [
                FFMPEG,
                "-y",
                "-i",
                str(video_file),
                "-i",
                str(audio_file),
                "-filter_complex",
                f"[1:a]apad=pad_dur={pad_duration:.3f}[a]",
                "-map",
                "0:v",
                "-map",
                "[a]",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-t",
                f"{target_duration:.3f}",
                str(segment_file),
            ]
        else:
            cmd = [
                FFMPEG,
                "-y",
                "-i",
                str(video_file),
                "-i",
                str(audio_file),
                "-map",
                "0:v",
                "-map",
                "1:a",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-shortest",
                str(segment_file),
            ]

        run_command(cmd)
        segment_files.append(segment_file)

    return segment_dir, segment_files


def combine_segments(segment_files, output_file, speed):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    concat_file = output_file.parent / f"{output_file.stem}_concat.txt"
    create_concat_file(segment_files, concat_file)

    if speed == 1.0:
        cmd = [
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            str(output_file),
        ]
    else:
        pts_factor = 1.0 / speed
        cmd = [
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-filter_complex",
            f"[0:v]setpts={pts_factor:.4f}*PTS[v];[0:a]atempo={speed}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            str(output_file),
        ]

    run_command(cmd)
    concat_file.unlink(missing_ok=True)


def validate_output(output_file):
    with av.open(str(output_file)) as container:
        duration = 0.0 if container.duration is None else container.duration / av.time_base
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"Created {output_file.relative_to(BASE_DIR)}")
    print(f"Duration: {duration:.2f}s")
    print(f"Size: {size_mb:.2f} MB")


def main():
    args = parse_args()
    project = get_project(args.project)
    inputs = build_inputs(args.project, project)

    print("=" * 70)
    print(f"Combining project: {project['title']} ({args.project})")
    print("=" * 70)

    if not validate_inputs(inputs):
        print("Run render_all.py and generate_narration.py for this project first.")
        return 1

    segment_dir, segment_files = create_scene_segments(args.project, inputs)
    try:
        combine_segments(segment_files, project["final_output"], args.speed)
        validate_output(project["final_output"])
    finally:
        shutil.rmtree(segment_dir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
