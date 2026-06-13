from __future__ import annotations

import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clear_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def check_executable(name: str) -> bool:
    return shutil.which(name) is not None


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_command(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    logging.debug("Running command: %s", " ".join(args))
    completed = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        logging.error("Command failed: %s", " ".join(args))
        if completed.stdout:
            logging.error("stdout:\n%s", completed.stdout)
        if completed.stderr:
            logging.error("stderr:\n%s", completed.stderr)
        raise RuntimeError(f"Command failed: {' '.join(args)}")
    return completed


def ffprobe_duration(path: Path) -> float:
    result = run_command(
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
    )
    try:
        return round(float(result.stdout.strip()), 3)
    except ValueError as exc:
        raise RuntimeError(f"Invalid ffprobe duration for {path}: {result.stdout!r}") from exc
