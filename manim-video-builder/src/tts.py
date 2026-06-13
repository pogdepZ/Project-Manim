from __future__ import annotations

import asyncio
import logging
from pathlib import Path


async def synthesize_text(
    text: str,
    output_file: Path,
    voice: str,
    rate: str = "+0%",
    volume: str = "+0%",
    retries: int = 3,
    retry_delay: float = 2.0,
    timeout: float = 60.0,
) -> bool:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            import edge_tts

            await asyncio.sleep(1.5)
            logging.info("TTS %s (attempt %s/%s)", output_file.name, attempt, retries)
            communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
            await asyncio.wait_for(communicate.save(str(output_file)), timeout=timeout)
            if output_file.exists() and output_file.stat().st_size > 0:
                return True
            raise RuntimeError(f"edge-tts created an empty file: {output_file}")
        except TimeoutError as exc:
            output_file.unlink(missing_ok=True)
            last_error = exc
            logging.warning("TTS timed out for %s after %.0f seconds", output_file.name, timeout)
            if attempt < retries:
                await asyncio.sleep(retry_delay * attempt)
        except Exception as exc:
            output_file.unlink(missing_ok=True)
            last_error = exc
            logging.warning("TTS failed for %s: %s", output_file.name, exc)
            if attempt < retries:
                await asyncio.sleep(retry_delay * attempt)
    logging.error("TTS permanently failed for %s: %s", output_file.name, last_error)
    return False


def synthesize_text_sync(
    text: str,
    output_file: Path,
    voice: str,
    rate: str = "+0%",
    volume: str = "+0%",
    retries: int = 3,
) -> bool:
    return asyncio.run(
        synthesize_text(
            text=text,
            output_file=output_file,
            voice=voice,
            rate=rate,
            volume=volume,
            retries=retries,
        )
    )
