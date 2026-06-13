from __future__ import annotations

from pathlib import Path


def build_srt(manifest: list[dict], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    blocks: list[str] = []
    for index, entry in enumerate(manifest, start=1):
        start = _format_srt_time(float(entry.get("start", 0.0)))
        end = _format_srt_time(float(entry.get("end", 0.0)))
        text = " ".join(str(entry.get("voice_text", "")).split())
        blocks.append(f"{index}\n{start} --> {end}\n{text[:500]}")
    output_file.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def _format_srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, rem = divmod(millis, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"
