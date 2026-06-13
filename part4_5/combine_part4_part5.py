#!/usr/bin/env python3
"""Sync each rebuilt scene with its narration, then concatenate final video."""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path


RESOLUTION = "720p30"
VIDEO_DIR = Path("media/videos/scene_part4_part5") / RESOLUTION
AUDIO_DIR = Path("narration_part4_part5_12_15min")
PAIR_DIR = Path("media/part4_part5_12_15min_synced_pairs")
CONCAT_FILE = Path("concat_part4_part5_12_15min_synced.txt")
OUTPUT = "final_part4_part5_with_narration.mp4"
FPS = "30"
AUDIO_RATE = "48000"
SYNC_WARNING_SECONDS = 0.5

SCENES = [
    ("Part04BridgeFromSlotAttention", AUDIO_DIR / "p4_00_bridge_slot_attention.mp3"),
    ("Part04SyntheticVsRealOverview", AUDIO_DIR / "p4_01_synthetic_real_gap.mp3"),
    ("Part04RealWorldComplexity", AUDIO_DIR / "p4_02_real_world_hard.mp3"),
    ("Part04RGBReconstructionProblem", AUDIO_DIR / "p4_03_rgb_reconstruction.mp3"),
    ("Part04ResearchQuestionBeyondRGB", AUDIO_DIR / "p4_05_core_question.mp3"),
    ("Part05BeyondRGBOverview", AUDIO_DIR / "p5_00_beyond_rgb_overview.mp3"),
    ("Part05OpticalFlowMotionCue", AUDIO_DIR / "p5_01_optical_flow.mp3"),
    ("Part05MotionLimitations", AUDIO_DIR / "p5_02_motion_limits.mp3"),
    ("Part05DepthLidarGeometryCue", AUDIO_DIR / "p5_03_depth_lidar_waymo.mp3"),
    ("Part05DinosaurFeatureReconstruction", AUDIO_DIR / "p5_04_dinosaur_features.mp3"),
    ("Part05FinalSynthesisToEncoder", AUDIO_DIR / "p5_05_synthesis_encoder_bridge.mp3"),
]

SILENT_AUDIO_SCENES = set()


def ffmpeg_exe():
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which("ffmpeg") or "ffmpeg"


def ffprobe_exe():
    ffmpeg = Path(ffmpeg_exe())
    local = ffmpeg.with_name("ffprobe.exe" if os.name == "nt" else "ffprobe")
    return str(local) if local.exists() else (shutil.which("ffprobe") or "ffprobe")


def run(cmd):
    print(" ".join(str(part) for part in cmd))
    subprocess.run([str(part) for part in cmd], check=True)


def duration_seconds(path):
    cmd = [ffprobe_exe(), "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return float(json.loads(result.stdout)["format"]["duration"])
    except Exception:
        result = subprocess.run([ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True)
        match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr + result.stdout)
        if not match:
            raise RuntimeError(f"Could not determine duration for {path}")
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)


def video_path(scene_name):
    return VIDEO_DIR / f"{scene_name}.mp4"


def validate_inputs():
    missing = []
    for scene_name, audio_path in SCENES:
        if not video_path(scene_name).exists():
            missing.append(str(video_path(scene_name)))
        if scene_name not in SILENT_AUDIO_SCENES and not Path(audio_path).exists():
            missing.append(str(audio_path))
    if missing:
        print("Missing inputs:")
        for item in missing:
            print(f"  {item}")
        return False
    return True


def collect_duration_report():
    report = []
    print("\nScene duration report")
    print("-" * 108)
    print(f"{'Scene':38} | {'video':>8} | {'audio':>8} | {'delta':>8} | action")
    print("-" * 108)
    for scene_name, audio_path in SCENES:
        vdur = duration_seconds(video_path(scene_name))
        if scene_name in SILENT_AUDIO_SCENES:
            adur = vdur
        else:
            adur = duration_seconds(audio_path)
        delta = adur - vdur
        if delta > SYNC_WARNING_SECONDS:
            action = f"pad video +{delta:.2f}s"
        elif delta < -SYNC_WARNING_SECONDS:
            action = f"pad audio +{-delta:.2f}s"
        else:
            action = "already close"
        print(f"{scene_name:38} | {vdur:8.2f} | {adur:8.2f} | {delta:8.2f} | {action}")
        report.append((scene_name, audio_path, vdur, adur))
    print("-" * 108)
    return report


def synced_pair_path(index, scene_name):
    return PAIR_DIR / f"{index:02d}_{scene_name}.mp4"


def merge_scene_pair(index, item):
    scene_name, audio_path, vdur, adur = item
    PAIR_DIR.mkdir(exist_ok=True, parents=True)
    out = synced_pair_path(index, scene_name)
    target = max(vdur, adur)
    video_filter = f"fps={FPS},format=yuv420p"
    if adur > vdur:
        video_filter += f",tpad=stop_mode=clone:stop_duration={adur - vdur:.3f}"
    video_filter += f",trim=duration={target:.3f},setpts=PTS-STARTPTS[v]"

    if scene_name in SILENT_AUDIO_SCENES:
        cmd = [
            ffmpeg_exe(), "-y",
            "-i", video_path(scene_name),
            "-f", "lavfi", "-t", f"{target:.3f}", "-i", f"anullsrc=channel_layout=stereo:sample_rate={AUDIO_RATE}",
            "-filter_complex", f"[0:v]{video_filter};[1:a]atrim=duration={target:.3f},asetpts=PTS-STARTPTS[a]",
            "-map", "[v]", "-map", "[a]",
            "-r", FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-ar", AUDIO_RATE, "-ac", "2", "-b:a", "160k",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", out,
        ]
    else:
        audio_filter = "aresample=48000"
        if vdur > adur:
            audio_filter += f",apad=pad_dur={vdur - adur:.3f}"
        audio_filter += f",atrim=duration={target:.3f},asetpts=PTS-STARTPTS,pan=stereo|c0=c0|c1=c0[a]"
        cmd = [
            ffmpeg_exe(), "-y",
            "-i", video_path(scene_name), "-i", audio_path,
            "-filter_complex", f"[0:v]{video_filter};[1:a]{audio_filter}",
            "-map", "[v]", "-map", "[a]",
            "-r", FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-ar", AUDIO_RATE, "-ac", "2", "-b:a", "160k",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", out,
        ]
    run(cmd)
    return out


def concatenate(paths):
    CONCAT_FILE.write_text("".join(f"file '{path.resolve().as_posix()}'\n" for path in paths), encoding="utf-8")
    run([
        ffmpeg_exe(), "-y", "-f", "concat", "-safe", "0", "-i", CONCAT_FILE,
        "-r", FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-ar", AUDIO_RATE, "-ac", "2", "-b:a", "160k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUTPUT,
    ])


def main():
    if not validate_inputs():
        return 1
    report = collect_duration_report()
    outputs = [merge_scene_pair(i, item) for i, item in enumerate(report, start=1)]
    concatenate(outputs)
    dur = duration_seconds(OUTPUT)
    size_mb = Path(OUTPUT).stat().st_size / (1024 * 1024)
    print(f"Created {OUTPUT} ({size_mb:.2f} MB, {dur:.2f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
