#!/usr/bin/env python3
"""Generate Vietnamese narration for the rebuilt 12-15 minute Part 4 / Part 5 video."""

import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path


try:
    import edge_tts
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts


VOICE = "vi-VN-HoaiMyNeural"
RATE = "+0%"
MAX_RETRIES = 3
CHUNK_CHAR_LIMIT = 1300
SCRIPT_PATH = Path("NARRATION_SCRIPT_12_15min.md")
OUTPUT_DIR = Path("narration_part4_part5_12_15min")

SCENE_AUDIO = [
    ("p4_00_bridge_slot_attention", "Part04BridgeFromSlotAttention", "p4_00_bridge_slot_attention"),
    ("p4_01_synthetic_real_gap", "Part04SyntheticVsRealOverview", "p4_01_synthetic_real_gap"),
    ("p4_02_real_world_hard", "Part04RealWorldComplexity", "p4_02_real_world_hard"),
    ("p4_03_rgb_reconstruction", "Part04RGBReconstructionProblem", "p4_03_rgb_reconstruction"),
    ("p4_05_core_question", "Part04ResearchQuestionBeyondRGB", "p4_05_core_question"),
    ("p5_00_beyond_rgb_overview", "Part05BeyondRGBOverview", "p5_00_beyond_rgb_overview"),
    ("p5_01_optical_flow", "Part05OpticalFlowMotionCue", "p5_01_optical_flow"),
    ("p5_02_motion_limits", "Part05MotionLimitations", "p5_02_motion_limits"),
    ("p5_03_depth_lidar_waymo", "Part05DepthLidarGeometryCue", "p5_03_depth_lidar_waymo"),
    ("p5_04_dinosaur_features", "Part05DinosaurFeatureReconstruction", "p5_04_dinosaur_features"),
    ("p5_05_synthesis_encoder_bridge", "Part05FinalSynthesisToEncoder", "p5_05_synthesis_encoder_bridge"),
]

# p4_04 is intentionally merged into Part04RGBReconstructionProblem visuals to keep
# the rebuilt video at 11 scenes while preserving the RGB limitation content.
MERGED_EXTRA = {
    "p4_03_rgb_reconstruction": "p4_04_rgb_distracts",
}

CUSTOM_NARRATION = {
    "p5_00_beyond_rgb_overview": (
        "Trước khi đi vào từng target cụ thể, hãy nhìn tổng quan bức tranh beyond RGB. "
        "Một reconstruction target không chỉ là thứ model cần dự đoán; nó còn định hình loại cấu trúc mà model có xu hướng học. "
        "RGB nhấn mạnh appearance. Optical flow nhấn mạnh motion. Depth và LiDAR nhấn mạnh geometry. "
        "Self-supervised features nhấn mạnh một representation có cấu trúc hơn raw pixels. "
        "Các target này không loại trừ nhau, nhưng mỗi target đặt trọng tâm học khác nhau. "
        "Điểm quan trọng là không target nào tự động giải quyết toàn bộ bài toán object-centric learning. "
        "Mỗi target chỉ cung cấp một training signal, hoặc một cue, để hướng model chú ý tới một phần cấu trúc của scene. "
        "Vì vậy, khi nói reconstruct beyond RGB, ta không nói RGB vô dụng. "
        "Ta chỉ nói rằng với real-world data, đôi khi model cần một tín hiệu phù hợp hơn với motion, geometry, hoặc feature-level structure."
    ),
}

APPEND_NARRATION = {
    "p5_05_synthesis_encoder_bridge": (
        "Nói cách khác, phần này trả lời câu hỏi target nên hướng model học cái gì. "
        "Phần tiếp theo sẽ trả lời câu hỏi encoder nên trích xuất bằng chứng thị giác như thế nào trước khi các slots và decoder làm việc phía sau."
    ),
}

PRONUNCIATION_MAP = {
    "synthetic-to-real gap": "sin-the-tic tu real gap",
    "self-supervised": "seo súp pơ vai",
    "object-centric": "óp-dzèct sen-tric",
    "Upgrading Encoder": "upgrading encoder",
    "Slot Attention": "slot attention",
    "optical flow": "óp-ti-cồ flow",
    "RGB frame": "a gi bi frame",
    "raw RGB": "raw a gi bi",
    "DINOSAUR": "đai nô so",
    "SAVi++": "sa vi plus plus",
    "LiDAR": "lai đa",
    "Waymo": "quây mô",
    "SAVi": "sa vi",
    "RGB": "a gi bi",
    "SSL": "ét ét eo",
    "Reconstruction": "ri con strúc sần",
}


def normalize_for_tts(text: str) -> str:
    normalized = text
    for term, pronunciation in sorted(PRONUNCIATION_MAP.items(), key=lambda item: len(item[0]), reverse=True):
        normalized = re.sub(re.escape(term), pronunciation, normalized, flags=re.IGNORECASE)
    return normalized


def extract_sections():
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^# ([a-z0-9_]+)\s*$", text))
    sections = {}
    for i, match in enumerate(matches):
        key = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n---\s*$", "", body).strip()
        sections[key] = body
    return sections


def narration_for_key(sections, key):
    if key in CUSTOM_NARRATION:
        return CUSTOM_NARRATION[key]
    body = sections[key].strip()
    extra_key = MERGED_EXTRA.get(key)
    if extra_key:
        body = body + "\n\n" + sections[extra_key].strip()
    if key in APPEND_NARRATION:
        body = body + "\n\n" + APPEND_NARRATION[key]
    return body


def split_text(text, limit=CHUNK_CHAR_LIMIT):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for paragraph in paragraphs:
        candidate = paragraph if not current else current + "\n\n" + paragraph
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = paragraph
    if current:
        chunks.append(current)
    return chunks


async def synthesize_chunk(text, path):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            communicate = edge_tts.Communicate(normalize_for_tts(text), VOICE, rate=RATE)
            await communicate.save(str(path))
            return
        except Exception:
            if attempt == MAX_RETRIES:
                raise
            await asyncio.sleep(1.5 * attempt)


def ffmpeg_exe():
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which("ffmpeg") or "ffmpeg"


def concat_chunks(chunks, output):
    if len(chunks) == 1:
        shutil.copyfile(chunks[0], output)
        return
    list_file = output.with_suffix(".txt")
    list_file.write_text("".join(f"file '{chunk.resolve().as_posix()}'\n" for chunk in chunks), encoding="utf-8")
    subprocess.run([ffmpeg_exe(), "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(output)], check=True)
    list_file.unlink(missing_ok=True)


async def main_async():
    if not SCRIPT_PATH.exists():
        raise FileNotFoundError(SCRIPT_PATH)
    OUTPUT_DIR.mkdir(exist_ok=True)
    sections = extract_sections()
    missing = [key for key, _, _ in SCENE_AUDIO if key not in sections and key not in CUSTOM_NARRATION]
    missing += [extra for extra in MERGED_EXTRA.values() if extra not in sections]
    if missing:
        raise RuntimeError(f"Missing narration sections: {missing}")

    for key, scene_name, output_key in SCENE_AUDIO:
        output = OUTPUT_DIR / f"{output_key}.mp3"
        chunks = split_text(narration_for_key(sections, key))
        chunk_paths = []
        print(f"{scene_name}: {len(chunks)} chunk(s) -> {output}")
        for i, chunk in enumerate(chunks, start=1):
            chunk_path = OUTPUT_DIR / f"{output_key}_chunk_{i:02d}.mp3"
            await synthesize_chunk(chunk, chunk_path)
            chunk_paths.append(chunk_path)
        concat_chunks(chunk_paths, output)
        for chunk_path in chunk_paths:
            if chunk_path != output:
                chunk_path.unlink(missing_ok=True)


def main():
    asyncio.run(main_async())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
