from __future__ import annotations

import logging
import shutil
from pathlib import Path

from utils import run_command


QUALITY_FLAGS = {
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
}


def render_manim(scene_file: Path, class_name: str, quality: str, project_root: Path) -> Path:
    flag = QUALITY_FLAGS[quality]
    command = ["manim", flag, str(scene_file), class_name]
    run_command(command, cwd=project_root)
    rendered = find_rendered_video(project_root / "media" / "videos", scene_file.stem, quality)
    logging.info("Rendered Manim video: %s", rendered)
    return rendered


def copy_rendered_video(rendered_file: Path, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(rendered_file, output_file)


def find_rendered_video(media_videos_dir: Path, scene_stem: str, quality: str) -> Path:
    if not media_videos_dir.exists():
        raise FileNotFoundError(f"Manim media directory not found: {media_videos_dir}")
    candidates = sorted(media_videos_dir.rglob("GeneratedVideo.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        candidates = sorted(media_videos_dir.rglob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No rendered mp4 found under {media_videos_dir} for {scene_stem} ({quality})")
    return candidates[0]
