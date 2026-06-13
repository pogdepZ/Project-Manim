#!/usr/bin/env python3
"""
Generate Vietnamese-English narration using Split & Merge technique with Edge TTS.
Run: python generate_narration_split_merge.py

Requires: pip install edge-tts pydub
"""

import os
import re
import sys
import asyncio
import tempfile
import argparse
from pathlib import Path

try:
    import edge_tts
except ImportError:
    import subprocess
    print("❌ edge-tts chưa được cài đặt. Đang cài...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts

# Không còn dùng pydub để ghép nối, dùng binary append thay thế
# Import danh sách từ khóa tiếng Anh từ file hiện tại
try:
    from generate_narration_part6_7 import PHONETIC_MAP
except ImportError:
    print("❌ Lỗi: Không tìm thấy file generate_narration_part6_7.py để lấy danh sách từ tiếng Anh.")
    sys.exit(1)

# Thêm một số từ tiếng Anh phổ biến có trong script nhưng chưa có trong MAP
EXTRA_ENGLISH_TERMS = [
    "layer", "synthetic", "dataset", "mask", "signal", "texture", 
    "scratch", "frozen", "finetuned", "model", "features", "feature",
    "pixels", "pixel"
]

# Gộp danh sách từ tiếng Anh
ALL_ENGLISH_TERMS = list(PHONETIC_MAP.keys()) + EXTRA_ENGLISH_TERMS
# Sắp xếp theo chiều dài giảm dần để match chính xác (vd: "Slot Attention" trước "Slot")
ALL_ENGLISH_TERMS = sorted(list(set(ALL_ENGLISH_TERMS)), key=len, reverse=True)

# Regex tách từ tiếng Anh và tiếng Việt
ESCAPED_TERMS = [re.escape(t) for t in ALL_ENGLISH_TERMS]
SPLIT_PATTERN = re.compile(r"(?<![a-zA-ZÀ-ỹ0-9_-])(" + "|".join(ESCAPED_TERMS) + r")(?![a-zA-ZÀ-ỹ0-9_-])")

# Cấu hình giọng đọc
VOICE_VI = "vi-VN-HoaiMyNeural"
VOICE_EN = "en-US-AriaNeural"  # Giọng nữ Mỹ, phát âm cực chuẩn
RATE = "+0%"

SCRIPT_FILE = Path("merged_script_content.txt")

def load_narrations(script_file=SCRIPT_FILE):
    if not script_file.exists():
        raise FileNotFoundError(f"Missing narration script: {script_file}")

    content = script_file.read_text(encoding="utf-8")
    if "\\n" in content and "\n" not in content.replace("\\n", ""):
        content = content.replace("\\n", "\n")

    pattern = re.compile(
        r"^###\s+SCENE\s+(\d+):[^\n]*\n"
        r"\*\*Thời gian video:\s*TBD\*\*\n\n"
        r'"(.*?)"\n\n---',
        re.MULTILINE | re.DOTALL,
    )

    narrations = {}
    for match in pattern.finditer(content):
        scene_number = int(match.group(1))
        text = " ".join(match.group(2).split())
        narrations[f"scene{scene_number}"] = text

    return dict(sorted(narrations.items(), key=lambda item: int(item[0].replace("scene", ""))))

async def generate_chunk(text, voice, output_path):
    """Tạo audio cho 1 chunk text nhỏ."""
    communicate = edge_tts.Communicate(text, voice, rate=RATE)
    await communicate.save(output_path)

async def generate_split_merge(key, text, output_file, skip_existing=False):
    output_path = Path(output_file)
    if skip_existing and output_path.exists() and output_path.stat().st_size > 0:
        print(f"↷ Skipping existing: {output_file}")
        return "skipped"

    print(f"🎙️  Generating Split & Merge: {output_file}...")
    
    # Phân tách câu thành các đoạn Tiếng Việt và Tiếng Anh
    chunks = SPLIT_PATTERN.split(text)
    
    # Chuẩn hóa text trước khi chia chunk
    text = text.replace("(", ", ").replace(")", ", ")
    text = text.replace("—", "-")
    
    chunks = SPLIT_PATTERN.split(text)
    
    # Gom các chunk chỉ chứa dấu câu hoặc quá ngắn vào chunk trước đó
    merged_chunks = []
    for c in chunks:
        c = c.strip()
        if not c:
            continue
        # Nếu chunk không chứa chữ/số nào, gom nó vào chunk trước đó (nếu có)
        if not any(char.isalnum() for char in c) and merged_chunks:
            merged_chunks[-1] += " " + c
        else:
            merged_chunks.append(c)
            
    chunks = merged_chunks
    temp_files = []
    
    try:
        # Xóa file cũ nếu tồn tại
        if os.path.exists(output_file):
            os.remove(output_file)
            
        # Tạo thư mục tạm để chứa các file audio nhỏ
        with tempfile.TemporaryDirectory() as temp_dir:
            for idx, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                # Xác định ngôn ngữ dựa vào việc chunk có nằm trong danh sách từ tiếng Anh không
                is_english = chunk in ALL_ENGLISH_TERMS
                voice = VOICE_EN if is_english else VOICE_VI
                
                # Nếu là tiếng Anh, có thể thêm dấu phẩy nhỏ để ngắt nghỉ mượt hơn 
                # (tùy chọn, ở đây ta để nguyên gốc)
                
                chunk_file = os.path.join(temp_dir, f"chunk_{idx}.mp3")
                
                # Gọi edge-tts
                await generate_chunk(chunk, voice, chunk_file)
                
                # Ghép file mp3 bằng cơ chế nối nhị phân (binary append) thay vì dùng pydub
                with open(chunk_file, "rb") as f_in:
                    with open(output_file, "ab") as f_out:
                        f_out.write(f_in.read())
                
            print(f"✓ {output_file} created successfully! ({len(chunks)} chunks merged)")
            return "generated"
            
    except Exception as e:
        print(f"❌ Error generating {output_file}: {e}")
        raise

async def main():
    parser = argparse.ArgumentParser(
        description="Generate Bilingual Narration using Split & Merge (Edge TTS)."
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Do not regenerate mp3 files that already exist.",
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Chỉ test đoạn text ngắn. Ví dụ: --test 'Slot Attention ban đầu dùng CNN nhỏ'",
    )
    parser.add_argument(
        "--scene",
        type=str,
        help="Chỉ tạo mp3 cho 1 scene cụ thể. Ví dụ: --scene 1 hoặc --scene scene1",
    )
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("Split & Merge TTS Generator (Hoài My + Aria)")
    print("=" * 60)

    if args.test:
        print(f"🧪 Đang test phát âm cho: '{args.test}'")
        output_file = "test_split_merge.mp3"
        await generate_split_merge("test", args.test, output_file)
        print(f"\n✅ Đã tạo file test tại: {output_file}")
        print("Hãy mở file này để nghe sự mượt mà của 2 giọng đọc kết hợp nhé!")
        return

    output_dir = Path("narration_part6_7")
    output_dir.mkdir(exist_ok=True)
    narrations = load_narrations()
    if not narrations:
        raise RuntimeError(f"No narrations found in {SCRIPT_FILE}.")

    print(f"\n📁 Output directory: {output_dir}")
    print(f"🗣️  Voice VI: {VOICE_VI} | Voice EN: {VOICE_EN}\n")
    print(f"🧾 Loaded {len(narrations)} narration scenes")

    generated_count = 0
    skipped_count = 0
    for key, text in narrations.items():
        if args.scene:
            # Nếu người dùng nhập "1", nó sẽ kiểm tra số
            # Nếu người dùng nhập "scene1", nó sẽ match với key "scene1"
            import re
            
            # Kiểm tra xem args.scene có phải là số không
            if args.scene.isdigit():
                match = re.search(r'\d+', key)
                if match and int(match.group()) != int(args.scene):
                    continue
            else:
                # Nếu là chuỗi (ví dụ: S6_01_CNNFailure), thì so sánh thẳng hoặc một phần
                if args.scene.lower() not in key.lower():
                    continue
                
        output_file = output_dir / f"{key}.mp3"
        result = await generate_split_merge(key, text, str(output_file), skip_existing=args.skip_existing)
        if result == "generated":
            generated_count += 1
        elif result == "skipped":
            skipped_count += 1

    print("\n" + "=" * 60)
    print(f"✓ Done. Generated: {generated_count}, skipped existing: {skipped_count}")
    print("=" * 60)
    print("\nNext step: Run: python combine_part6_7.py")

if __name__ == "__main__":
    asyncio.run(main())
