from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from utils import run_command


def add_pause_to_audio(input_file: Path, output_file: Path, pause_ms: int) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if pause_ms <= 0:
        output_file.write_bytes(input_file.read_bytes())
        return

    delay = pause_ms / 1000
    run_command(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_file),
            "-af",
            f"apad=pad_dur={delay}",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(output_file),
        ]
    )


def merge_mp3_files(audio_files: list[Path], output_mp3: Path) -> None:
    if not audio_files:
        raise ValueError("No audio files to merge")

    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        concat_file = Path(handle.name)
        for audio_file in audio_files:
            safe_path = str(audio_file.resolve()).replace("'", "'\\''")
            handle.write(f"file '{safe_path}'\n")

    try:
        logging.info("Merging %s mp3 files into %s", len(audio_files), output_mp3)
        try:
            run_command(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(concat_file),
                    "-c",
                    "copy",
                    str(output_mp3),
                ]
            )
        except RuntimeError:
            logging.warning("Stream-copy concat failed; retrying with mp3 re-encode")
            run_command(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(concat_file),
                    "-c:a",
                    "libmp3lame",
                    "-q:a",
                    "2",
                    str(output_mp3),
                ]
            )
    finally:
        concat_file.unlink(missing_ok=True)


def concat_mp4_files(video_files: list[Path], output_mp4: Path) -> None:
    if not video_files:
        raise ValueError("No video files to concat")

    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        concat_file = Path(handle.name)
        for video_file in video_files:
            safe_path = str(video_file.resolve()).replace("'", "'\\''")
            handle.write(f"file '{safe_path}'\n")

    try:
        logging.info("Concatenating %s videos into %s", len(video_files), output_mp4)
        try:
            run_command(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(concat_file),
                    "-c",
                    "copy",
                    str(output_mp4),
                ]
            )
        except RuntimeError:
            logging.warning("Stream-copy video concat failed; retrying with mp4 re-encode")
            run_command(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(concat_file),
                    "-c:v",
                    "libx264",
                    "-preset",
                    "veryfast",
                    "-crf",
                    "20",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    str(output_mp4),
                ]
            )
    finally:
        concat_file.unlink(missing_ok=True)


def convert_mp3_to_wav(input_mp3: Path, output_wav: Path) -> None:
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    run_command(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_mp3),
            "-ar",
            "48000",
            "-ac",
            "2",
            str(output_wav),
        ]
    )
    logging.info("Wrote audio: %s", output_wav)


def merge_video_audio(video_file: Path, audio_file: Path, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    run_command(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_file),
            "-i",
            str(audio_file),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            str(output_file),
        ]
    )
    logging.info("Wrote final video: %s", output_file)
