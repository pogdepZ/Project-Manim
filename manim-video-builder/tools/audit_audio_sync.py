from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


FORBIDDEN_SOURCE_PATTERNS = [
    "FadeOut(Group(*self.mobjects))",
    "FadeOut(*self.mobjects)",
    "self.clear(",
]


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


def run_capture_all(args: list[str]) -> str:
    completed = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr)
    return completed.stdout + completed.stderr


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


def black_ratio(video: Path, timestamp: float) -> float:
    output = run_capture_all(
        [
            "ffmpeg",
            "-hide_banner",
            "-ss",
            f"{max(0.0, timestamp):.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            "blackframe=amount=98:threshold=32",
            "-f",
            "null",
            "-",
        ]
    )
    marker = "pblack:"
    if marker not in output:
        return 0.0
    return float(output.rsplit(marker, 1)[1].split()[0])


def audit_source(scene_files: list[Path]) -> list[str]:
    issues: list[str] = []
    for path in scene_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN_SOURCE_PATTERNS:
            if pattern in text:
                issues.append(f"{path}: forbidden pattern `{pattern}`")
    return issues


def audit_outputs(scenes_dir: Path) -> list[str]:
    issues: list[str] = []
    for video in sorted(scenes_dir.glob("scene_*/video_no_audio.mp4")):
        scene_dir = video.parent
        audio = scene_dir / "narration.mp3"
        if not audio.exists():
            continue
        video_ms = round(duration(video) * 1000)
        audio_ms = round(duration(audio) * 1000)
        diff_ms = video_ms - audio_ms
        if abs(diff_ms) > 500:
            issues.append(f"{scene_dir.name}: duration diff {diff_ms:+d}ms exceeds 500ms")
        # Probe just before the scene ends. A nearly black frame is a strong
        # signal that the visual vanished before narration completed.
        ratio = black_ratio(video, duration(video) - 0.10)
        if ratio >= 98.0:
            issues.append(f"{scene_dir.name}: final frame is near-black ({ratio:.1f}%)")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit obvious audio/visual sync violations.")
    parser.add_argument("--scene-glob", default="manim_scenes/scene_*.py")
    parser.add_argument("--scenes-dir", type=Path, default=Path("output/scenes"))
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()

    scene_files = sorted(Path(".").glob(args.scene_glob))
    issues = audit_source(scene_files)
    if not args.source_only:
        issues.extend(audit_outputs(args.scenes_dir))

    if issues:
        print("AUDIO SYNC AUDIT FAILED")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)

    print("AUDIO SYNC AUDIT PASSED")


if __name__ == "__main__":
    main()
