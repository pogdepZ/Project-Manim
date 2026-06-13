from __future__ import annotations

import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCENES_DIR = BASE_DIR / "output/scenes"
MANIFEST_PATH = BASE_DIR / "output/final/manifest.json"
FPS = 30.0


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(args)
            + "\n\nstdout:\n"
            + completed.stdout
            + "\n\nstderr:\n"
            + completed.stderr
        )
    return completed


def duration(path: Path) -> float:
    result = run(
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
    return float(result.stdout.strip())


def frame_aligned_duration(audio_seconds: float) -> float:
    return math.ceil(audio_seconds * FPS) / FPS


def fit_video_to_audio(video_in: Path, audio_in: Path, video_out: Path) -> tuple[float, float]:
    audio_seconds = duration(audio_in)
    video_seconds = duration(video_in)
    target_seconds = frame_aligned_duration(audio_seconds)
    pad_seconds = max(0.0, target_seconds - video_seconds)

    filter_expr = (
        f"trim=duration={target_seconds:.6f},"
        "setpts=PTS-STARTPTS,"
        f"tpad=stop_mode=clone:stop_duration={pad_seconds:.6f}"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_in),
            "-vf",
            filter_expr,
            "-an",
            "-r",
            str(int(FPS)),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            str(video_out),
        ]
    )
    return video_seconds, audio_seconds


def mux(video_in: Path, audio_in: Path, output: Path) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_in),
            "-i",
            str(audio_in),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            str(output),
        ]
    )


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    rows: list[tuple[str, int, int, int]] = []

    for entry in manifest:
        idx = int(entry["scene_index"])
        scene_name = f"scene_{idx:03d}"
        scene_dir = SCENES_DIR / scene_name
        video_path = scene_dir / "video_no_audio.mp4"
        audio_path = BASE_DIR / entry["audio_file"]
        mux_path = scene_dir / "video_with_audio.mp4"

        if not video_path.exists() or not audio_path.exists():
            print(f"skip {scene_name}: missing video or audio")
            continue

        with tempfile.TemporaryDirectory(prefix=f"{scene_name}_fit_") as tmp:
            tmp_video = Path(tmp) / "video_no_audio.fit.mp4"
            old_video_seconds, audio_seconds = fit_video_to_audio(video_path, audio_path, tmp_video)
            shutil.move(str(tmp_video), video_path)
            mux(video_path, audio_path, mux_path)

        new_video_seconds = duration(video_path)
        rows.append(
            (
                scene_name,
                round(old_video_seconds * 1000),
                round(audio_seconds * 1000),
                round((new_video_seconds - audio_seconds) * 1000),
            )
        )

    print("scene,old_video_ms,audio_ms,new_video_minus_audio_ms")
    for scene_name, old_ms, audio_ms, diff_ms in rows:
        print(f"{scene_name},{old_ms},{audio_ms},{diff_ms:+d}")


if __name__ == "__main__":
    main()
