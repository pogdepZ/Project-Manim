from __future__ import annotations

from pathlib import Path

from utils import ffprobe_duration


def audio_duration(path: Path) -> float:
    if not path.exists():
        return 0.0
    return ffprobe_duration(path)


def assign_scene_timings(manifest: list[dict]) -> list[dict]:
    cursor = 0.0
    for entry in manifest:
        duration = float(entry.get("duration", 0.0))
        entry["start"] = round(cursor, 3)
        cursor += duration
        entry["end"] = round(cursor, 3)
    return manifest
