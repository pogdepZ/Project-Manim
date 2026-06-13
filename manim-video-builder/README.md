# manim-video-builder

`manim-video-builder` biến một kịch bản dài thành video giải thích bằng Manim theo phong cách visual math animation. Pipeline hiện tại dành cho video dài 20-30 phút: tách script thành nhiều scene nhỏ, tạo narration và subtitle riêng cho từng scene, render từng file Manim riêng, ghép audio/video từng scene, rồi concat thành video cuối.

## Cấu trúc

```text
manim-video-builder/
├── input/
│   └── script.txt
├── output/
│   ├── scenes/
│   │   └── scene_001/
│   │       ├── voice_text.txt
│   │       ├── chunks/
│   │       ├── audio_chunks/
│   │       ├── narration.mp3
│   │       ├── subtitles.srt
│   │       ├── video_no_audio.mp4
│   │       └── video_with_audio.mp4
│   └── final/
│       ├── final_video.mp4
│       ├── narration.mp3
│       ├── subtitles.srt
│       └── manifest.json
├── src/
│   ├── main.py
│   ├── text_cleaner.py
│   ├── splitter.py
│   ├── tts.py
│   ├── timing.py
│   ├── manim_generator.py
│   ├── render.py
│   ├── merger.py
│   ├── subtitle.py
│   └── utils.py
├── manim_scenes/
│   ├── scene_001.py
│   ├── scene_002.py
│   └── ...
├── requirements.txt
└── README.md
```

## Cài đặt

Tạo virtual environment nếu cần:

```bash
python -m venv .venv
source .venv/bin/activate
```

Cài Python packages:

```bash
pip install -r requirements.txt
```

Cài `ffmpeg`:

```bash
sudo apt update
sudo apt install ffmpeg
```

Cài Manim dependencies theo hệ điều hành của bạn nếu Manim báo thiếu Cairo, Pango hoặc LaTeX. Với Ubuntu thường cần:

```bash
sudo apt install libcairo2-dev libpango1.0-dev texlive texlive-latex-extra
```

Kiểm tra công cụ:

```bash
manim --version
ffmpeg -version
ffprobe -version
python -m edge_tts --list-voices | grep vi-VN
```

## Cách chạy

Từ thư mục `manim-video-builder/`:

```bash
python src/main.py --input input/script.txt --voice vi-VN-HoaiMyNeural --quality medium --scene-duration 60 --max-chars 800 --resume
```

Chạy sạch output cũ:

```bash
python src/main.py --clean
```

Resume mặc định không xoá output cũ. Khi dùng `--resume`, scene nào đã có `video_with_audio.mp4` và narration hợp lệ sẽ được bỏ qua:

```bash
python src/main.py --resume
```

Render lại các scene được chọn:

```bash
python src/main.py --force
```

Chỉ chạy một scene hoặc một đoạn scene:

```bash
python src/main.py --only-scene 5 --resume
python src/main.py --from-scene 10 --to-scene 20 --resume
```

Chỉ sinh manifest và code Manim, chưa render (hữu ích cho chế độ manual mode):

```bash
python src/main.py --no-render
```

Giữ lại code Manim tự chỉnh sửa thủ công ở thư mục `manim_scenes/` (không ghi đè/tạo lại từ template):

```bash
python src/main.py --keep-code
```

Quy trình Manual Mode để có animation đẹp (giống 3Blue1Brown):
1. Chạy với `--no-render` để tạo ra code template và file manifest.
2. Mở file code trong `manim_scenes/` và tùy chỉnh các hiệu ứng, công thức, đồ thị theo ý muốn.
3. Chạy lại tool với `--keep-code` để render video và ghép audio mà không làm mất các thay đổi code đã thực hiện.

Chỉ tạo animation, bỏ TTS:

```bash
python src/main.py --no-tts
```

Các mức render:

```bash
python src/main.py --quality low
python src/main.py --quality medium
python src/main.py --quality high
```

## Đổi voice tiếng Việt

Mặc định là:

```text
vi-VN-HoaiMyNeural
```

Giọng nam tiếng Việt:

```bash
python src/main.py --voice vi-VN-NamMinhNeural
```

Có thể chỉnh tốc độ và âm lượng:

```bash
python src/main.py --rate "+8%" --volume "+0%"
```

## Output

Pipeline tạo:

- `output/scenes/scene_001/voice_text.txt`: nội dung voice của scene.
- `output/scenes/scene_001/chunks/scene_001_chunk_001.txt`: chunk text cho edge-tts.
- `output/scenes/scene_001/audio_chunks/scene_001_chunk_001.mp3`: audio từng chunk.
- `output/scenes/scene_001/narration.mp3`: narration riêng của scene.
- `output/scenes/scene_001/subtitles.srt`: subtitle timing riêng của scene.
- `output/scenes/scene_001/video_no_audio.mp4`: render Manim chưa có audio.
- `output/scenes/scene_001/video_with_audio.mp4`: video scene đã ghép narration.
- `output/final/narration.mp3`: narration đầy đủ.
- `output/final/manifest.json`: metadata từng scene.
- `output/final/subtitles.srt`: subtitle.
- `manim_scenes/scene_001.py`: code Manim riêng từng scene.
- `output/final/final_video.mp4`: video cuối có animation và voice.

Manifest tổng ghi `scene_index`, `scene_title`, `voice_text`, `duration`, `audio_file`, `manim_file`, `video_no_audio`, `video_with_audio`, `formulas`, `animation_type`, `status`, `start` và `end`.

## Debug

Nếu Manim lỗi, tool sẽ in command gây lỗi, stdout và stderr. Chạy lại command đó trực tiếp để xem log đầy đủ, ví dụ:

```bash
manim -qm manim_scenes/scene_001.py GeneratedVideo
```

Nếu lỗi `MathTex`, kiểm tra LaTeX đã cài đủ chưa. Nếu muốn chỉnh animation thủ công, sửa `manim_scenes/generated_scene.py`, rồi render lại bằng command Manim ở trên và ghép audio:

```bash
ffmpeg -y -i output/scenes/scene_001/video_no_audio.mp4 -i output/scenes/scene_001/narration.mp3 -c:v copy -c:a aac -shortest output/scenes/scene_001/video_with_audio.mp4
```

Nếu TTS lỗi mạng hoặc voice không tồn tại, kiểm tra:

```bash
python -m edge_tts --list-voices
```

Giảm `--max-chars` xuống 500-700 nếu edge-tts không ổn định với đoạn dài.
