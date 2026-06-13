from __future__ import annotations

import argparse
import logging
from pathlib import Path

from manim_generator import generate_manim_scene
from merger import add_pause_to_audio, concat_mp4_files, merge_mp3_files, merge_video_audio
from render import copy_rendered_video, render_manim
from splitter import SceneSpec, split_into_scenes
from subtitle import build_srt
from text_cleaner import clean_script
from timing import assign_scene_timings, audio_duration
from tts import synthesize_text_sync
from utils import check_executable, clear_dir, ensure_dir, setup_logging, write_json, write_text


DEFAULT_VOICE = "vi-VN-HoaiMyNeural"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a long Manim video from a script with per-scene rendering.")
    parser.add_argument("--input", default="input/script.txt", help="Input script file")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="edge-tts voice")
    parser.add_argument("--scene-duration", type=int, default=60, help="Target narration seconds per scene")
    parser.add_argument("--max-chars", type=int, default=800, help="Maximum characters per edge-tts chunk")
    parser.add_argument("--rate", default="+0%", help='Voice rate, e.g. "+0%%"')
    parser.add_argument("--volume", default="+0%", help='Voice volume, e.g. "+0%%"')
    parser.add_argument("--quality", choices=["low", "medium", "high"], default="medium", help="Manim render quality")
    parser.add_argument("--resume", action="store_true", help="Skip scenes that already have completed outputs")
    parser.add_argument("--force", action="store_true", help="Rebuild selected scenes even if outputs already exist")
    parser.add_argument("--only-scene", type=int, help="Only process one 1-based scene index")
    parser.add_argument("--from-scene", type=int, help="Process from this 1-based scene index")
    parser.add_argument("--to-scene", type=int, help="Process through this 1-based scene index")
    parser.add_argument("--clean", action="store_true", help="Delete previous output before running")
    parser.add_argument("--no-render", action="store_true", help="Only generate scene assets and Manim code")
    parser.add_argument("--no-tts", action="store_true", help="Skip TTS and build animation timings from text estimates")
    parser.add_argument("--keep-code", action="store_true", help="Keep existing Manim code files instead of overwriting them")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--retries", type=int, default=3, help="Retries per TTS chunk")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    setup_logging(args.verbose)

    project_root = Path.cwd()
    input_file = Path(args.input)
    output_dir = Path(args.output)
    scenes_root = output_dir / "scenes"
    final_dir = output_dir / "final"
    manim_root = project_root / "manim_scenes"

    if not _validate_args(args, input_file):
        return 1
    if not _check_tools(args):
        return 1

    if args.clean:
        clear_dir(output_dir)
    for directory in (scenes_root, final_dir, manim_root):
        ensure_dir(directory)

    cleaned = clean_script(input_file.read_text(encoding="utf-8"))
    scenes = split_into_scenes(
        cleaned.body,
        cleaned.tts_text,
        max_chars=args.max_chars,
        scene_duration=args.scene_duration,
    )
    if not scenes:
        logging.error("No scenes were produced from input")
        return 1

    logging.info("Title: %s", cleaned.title or "(none)")
    logging.info("Created %s renderable scenes", len(scenes))

    manifest = [_scene_to_manifest(scene, output_dir, manim_root) for scene in scenes]
    _refresh_existing_statuses(manifest, args)
    _write_manifest(final_dir, manifest)

    selected_indexes = _selected_scene_indexes(len(scenes), args)
    if not selected_indexes:
        logging.error("Scene selection is empty")
        return 1

    for scene in scenes:
        entry = manifest[scene.scene_index - 1]
        if scene.scene_index not in selected_indexes:
            continue
        if _scene_complete(entry) and args.resume and not args.force:
            logging.info("Scene %03d already complete; skipping", scene.scene_index)
            continue

        try:
            _process_scene(scene, entry, project_root, args)
            _write_manifest(final_dir, manifest)
        except Exception as exc:
            entry["status"] = "error"
            entry["error"] = str(exc)
            _write_manifest(final_dir, manifest)
            logging.exception("Stopped at scene %03d: %s", scene.scene_index, exc)
            return 1

    _refresh_existing_statuses(manifest, args)
    _write_manifest(final_dir, manifest)
    if not args.no_render:
        _build_final_outputs(manifest, final_dir, args)
    logging.info("Done")
    return 0


def _validate_args(args: argparse.Namespace, input_file: Path) -> bool:
    if not input_file.exists():
        logging.error("Input file does not exist: %s", input_file)
        return False
    if args.scene_duration < 10:
        logging.error("--scene-duration must be at least 10 seconds")
        return False
    if args.max_chars < 200:
        logging.error("--max-chars must be at least 200")
        return False
    return True


def _check_tools(args: argparse.Namespace) -> bool:
    if not args.no_tts:
        for executable in ("ffmpeg", "ffprobe"):
            if not check_executable(executable):
                logging.error("%s is not available in PATH", executable)
                return False
    if not args.no_render:
        for executable in ("manim", "ffmpeg"):
            if not check_executable(executable):
                logging.error("%s is required for rendering", executable)
                return False
    return True


def _selected_scene_indexes(scene_count: int, args: argparse.Namespace) -> set[int]:
    if args.only_scene is not None:
        return {args.only_scene} if 1 <= args.only_scene <= scene_count else set()
    start = args.from_scene or 1
    end = args.to_scene or scene_count
    start = max(1, start)
    end = min(scene_count, end)
    if start > end:
        return set()
    return set(range(start, end + 1))


def _process_scene(scene: SceneSpec, entry: dict, project_root: Path, args: argparse.Namespace) -> None:
    scene_dir = Path(entry["scene_dir"])
    ensure_dir(scene_dir)
    if args.force:
        for key in ("video_no_audio", "video_with_audio", "audio_file"):
            path_value = entry.get(key)
            if path_value:
                Path(path_value).unlink(missing_ok=True)
    write_text(scene_dir / "voice_text.txt", scene.voice_text)
    entry["status"] = "processing"
    entry.pop("error", None)

    if args.no_tts:
        _estimate_scene_duration(scene, entry)
    else:
        _build_scene_tts(scene, entry, args)

    local_timing = dict(entry)
    local_timing["start"] = 0.0
    local_timing["end"] = float(entry["duration"])
    build_srt([local_timing], scene_dir / "subtitles.srt")

    manim_file = Path(entry["manim_file"])
    if args.keep_code and manim_file.exists():
        logging.info("Keeping existing Manim code: %s", manim_file)
    else:
        generate_manim_scene([entry], manim_file)
        logging.info("Wrote scene Manim code: %s", manim_file)

    if args.no_render:
        entry["status"] = "generated"
        return

    video_no_audio = Path(entry["video_no_audio"])
    video_with_audio = Path(entry["video_with_audio"])
    if video_with_audio.exists() and video_with_audio.stat().st_size > 0 and args.resume and not args.force:
        entry["status"] = "complete"
        return

    if video_no_audio.exists() and video_no_audio.stat().st_size > 0 and args.resume and not args.force:
        logging.info("Scene %03d silent render exists; reusing it", scene.scene_index)
    else:
        rendered = render_manim(manim_file, "GeneratedVideo", args.quality, project_root)
        copy_rendered_video(rendered, video_no_audio)

    if args.no_tts:
        copy_rendered_video(video_no_audio, video_with_audio)
    else:
        merge_video_audio(video_no_audio, Path(entry["audio_file"]), video_with_audio)
    entry["status"] = "complete"


def _build_scene_tts(scene: SceneSpec, entry: dict, args: argparse.Namespace) -> None:
    scene_dir = Path(entry["scene_dir"])
    chunks_dir = scene_dir / "chunks"
    audio_chunks_dir = scene_dir / "audio_chunks"
    paused_dir = scene_dir / ".paused_chunks"
    for directory in (chunks_dir, audio_chunks_dir, paused_dir):
        ensure_dir(directory)

    raw_chunk_audio_files: list[Path] = []
    paused_chunk_audio_files: list[Path] = []
    for chunk_index, chunk_text in enumerate(scene.chunks, start=1):
        stem = f"scene_{scene.scene_index:03}_chunk_{chunk_index:03}"
        chunk_text_file = chunks_dir / f"{stem}.txt"
        chunk_audio_file = audio_chunks_dir / f"{stem}.mp3"
        paused_audio_file = paused_dir / f"{stem}.mp3"
        write_text(chunk_text_file, chunk_text)

        if chunk_audio_file.exists() and chunk_audio_file.stat().st_size > 0 and args.resume and not args.force:
            logging.info("TTS chunk exists; reusing %s", chunk_audio_file)
        else:
            chunk_audio_file.unlink(missing_ok=True)
            ok = synthesize_text_sync(
                text=chunk_text,
                output_file=chunk_audio_file,
                voice=args.voice,
                rate=args.rate,
                volume=args.volume,
                retries=args.retries,
            )
            if not ok:
                raise RuntimeError(f"TTS failed for {chunk_audio_file}")

        if paused_audio_file.exists() and paused_audio_file.stat().st_size > 0 and args.resume and not args.force:
            logging.info("Paused TTS chunk exists; reusing %s", paused_audio_file)
        else:
            paused_audio_file.unlink(missing_ok=True)
            add_pause_to_audio(chunk_audio_file, paused_audio_file, pause_ms=220)

        raw_chunk_audio_files.append(chunk_audio_file)
        paused_chunk_audio_files.append(paused_audio_file)

    narration_file = Path(entry["audio_file"])
    if narration_file.exists() and narration_file.stat().st_size > 0 and args.resume and not args.force:
        logging.info("Scene narration exists; reusing %s", narration_file)
    else:
        narration_file.unlink(missing_ok=True)
        merge_mp3_files(paused_chunk_audio_files, narration_file)

    scene.audio_file = str(narration_file)
    scene.chunk_audio_files = [str(path) for path in raw_chunk_audio_files]
    scene.duration = audio_duration(narration_file)
    entry["chunk_audio_files"] = scene.chunk_audio_files
    entry["duration"] = scene.duration


def _estimate_scene_duration(scene: SceneSpec, entry: dict) -> None:
    words = max(1, len(scene.voice_text.split()))
    duration = round(max(6.0, words / 2.35), 3)
    scene.duration = duration
    scene.audio_file = ""
    scene.chunk_audio_files = []
    entry["audio_file"] = ""
    entry["chunk_audio_files"] = []
    entry["duration"] = duration


def _scene_to_manifest(scene: SceneSpec, output_dir: Path, manim_root: Path) -> dict:
    scene_name = f"scene_{scene.scene_index:03}"
    scene_dir = output_dir / "scenes" / scene_name
    return {
        "scene_index": scene.scene_index,
        "title": scene.scene_title,
        "scene_title": scene.scene_title,
        "goal": scene.goal,
        "voice_text_raw": scene.voice_text_raw or scene.voice_text,
        "voice_text_tts_safe": scene.voice_text,
        "voice_text": scene.voice_text,
        "duration": scene.duration,
        "audio_file": str(scene_dir / "narration.mp3"),
        "manim_file": str(manim_root / f"{scene_name}.py"),
        "video_no_audio": str(scene_dir / "video_no_audio.mp4"),
        "video_with_audio": str(scene_dir / "video_with_audio.mp4"),
        "visual_hints": scene.visual_hints,
        "screen_formulas": scene.screen_formulas,
        "formula_speech": scene.formula_speech,
        "animation_pattern": scene.animation_pattern,
        "colors": scene.colors,
        "formulas": scene.formulas,
        "animation_type": scene.animation_type,
        "status": "pending",
        "scene_dir": str(scene_dir),
        "chunk_audio_files": scene.chunk_audio_files,
    }


def _refresh_existing_statuses(manifest: list[dict], args: argparse.Namespace) -> None:
    for entry in manifest:
        audio_file = Path(entry["audio_file"]) if entry.get("audio_file") else None
        video_with_audio = Path(entry["video_with_audio"])
        if audio_file and audio_file.exists() and not args.no_tts:
            entry["duration"] = audio_duration(audio_file)
        if video_with_audio.exists() and (args.no_tts or (audio_file and audio_file.exists())):
            entry["status"] = "complete"
        elif entry.get("status") not in {"error", "generated"}:
            entry["status"] = "pending"


def _scene_complete(entry: dict) -> bool:
    return entry.get("status") == "complete" and Path(entry["video_with_audio"]).exists()


def _write_manifest(final_dir: Path, manifest: list[dict]) -> None:
    timed_manifest = assign_scene_timings(manifest)
    write_json(final_dir / "manifest.json", timed_manifest)
    build_srt(timed_manifest, final_dir / "subtitles.srt")


def _build_final_outputs(manifest: list[dict], final_dir: Path, args: argparse.Namespace) -> None:
    completed = [entry for entry in manifest if _scene_complete(entry)]
    if len(completed) != len(manifest):
        logging.warning(
            "Skipping final concat: %s/%s scenes are complete",
            len(completed),
            len(manifest),
        )
        return

    concat_mp4_files([Path(entry["video_with_audio"]) for entry in completed], final_dir / "final_video.mp4")
    if not args.no_tts:
        merge_mp3_files([Path(entry["audio_file"]) for entry in completed], final_dir / "narration.mp3")
    build_srt(assign_scene_timings(manifest), final_dir / "subtitles.srt")
    write_json(final_dir / "manifest.json", manifest)


if __name__ == "__main__":
    raise SystemExit(main())
