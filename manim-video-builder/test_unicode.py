import asyncio
import unicodedata
import edge_tts

async def test_norm(text, norm_type):
    normalized_text = unicodedata.normalize(norm_type, text)
    print(f"Testing {norm_type} (length: {len(normalized_text)}): {repr(normalized_text)}")
    communicate = edge_tts.Communicate(normalized_text, "vi-VN-HoaiMyNeural")
    try:
        await communicate.save(f"test_{norm_type}.mp3")
        print(f"Success for {norm_type}!")
    except Exception as e:
        print(f"Failed for {norm_type}: {e}")

async def main():
    text = "cần hiểu"
    await test_norm(text, 'NFC')
    await test_norm(text, 'NFD')

if __name__ == "__main__":
    asyncio.run(main())
