#!/usr/bin/env python3
"""
Generate Vietnamese narration using Microsoft Edge TTS.
Run: python generate_narration.py

Requires: pip install edge-tts pydub
"""

import asyncio
import subprocess
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts


narrations = {
    "scene1": (
        "Hãy nhìn vào một cảnh phức tạp với nhiều vật thể. "
        "Object-Centric Learning bắt đầu bằng một ý tưởng rất tự nhiên: thay vì xem cả bức ảnh như một khối, "
        "mô hình cố gắng nhận ra từng đối tượng riêng biệt."
    ),
    "scene2": (
        "Cách truyền thống là tách hình ảnh thành rất nhiều điểm ảnh nhỏ. "
        "Mỗi điểm chỉ là một con số màu sắc, nên mô hình phải tự tìm cấu trúc ẩn bên trong. "
        "Nó thấy pixel, nhưng chưa thấy vật thể."
    ),
    "scene3": (
        "Bây giờ ta chia ảnh thành các phần có nghĩa hơn. "
        "Các slot giống như những chiếc hộp trống, mỗi hộp chờ nhận một đối tượng. "
        "Từ đống pixel ban đầu, mô hình bắt đầu gom chúng lại thành các biểu diễn riêng."
    ),
    "scene4": (
        "Mỗi slot sẽ cạnh tranh để giải thích một vùng của ảnh. "
        "Slot nào khớp hơn sẽ nhận được nhiều chú ý hơn, và dần dần tập trung vào đúng đối tượng của mình. "
        "Đó là cách attention giúp phân chia scene một cách tự nhiên."
    ),
    "scene5": (
        "Khi đã có object vectors, mô hình làm việc tốt hơn trên các cảnh mới. "
        "Các vector này giữ được ý nghĩa của từng vật thể, nên mô hình dễ tổng quát hóa, dễ suy luận, "
        "và dễ hiểu điều gì sẽ đổi khi ta can thiệp vào một đối tượng."
    ),
    "scene6": (
        "Và đó là ý chính của video này: từ pixels đến objects, rồi từ objects đến reasoning. "
        "Khi mô hình hiểu được từng đối tượng, nó tiến gần hơn tới cách con người quan sát và suy nghĩ về thế giới."
    ),
}

VOICE = "vi-VN-HoaiMyNeural"
RATE = "+0%"


async def generate_narration(key, text, output_file):
    for attempt in range(1, 4):
        print(f"🎙️  Generating: {output_file}... attempt {attempt}/3")
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
            await communicate.save(output_file)
            if Path(output_file).stat().st_size == 0:
                raise RuntimeError("TTS returned an empty file")
            print(f"✓ {output_file} created ({len(text)} chars)")
            return
        except Exception as exc:
            if attempt == 3:
                raise
            print(f"  retrying after TTS error: {exc}")
            await asyncio.sleep(2)


async def main():
    print("=" * 60)
    print("Vietnamese Narration Generator (Edge TTS)")
    print("=" * 60)

    output_dir = Path("narration")
    output_dir.mkdir(exist_ok=True)

    print(f"\n📁 Output directory: {output_dir}")
    print(f"🎤 Voice: {VOICE}\n")

    for key, text in narrations.items():
        output_file = output_dir / f"{key}.mp3"
        await generate_narration(key, text, str(output_file))

    print("\n" + "=" * 60)
    print("✓ All narration files generated!")
    print("=" * 60)
    print("\nNext step: Run: python combine_video_audio.py")


if __name__ == "__main__":
    asyncio.run(main())
