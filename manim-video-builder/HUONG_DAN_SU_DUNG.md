# Huong dan su dung skill manim-video-builder

File nay huong dan cach dung `manim-video-builder` de tao video Manim dai tu mot docs/script dai. Pipeline hien tai khong render ca video bang mot file Manim duy nhat. Moi scene duoc tach, tao voice rieng, render rieng, roi concat thanh video cuoi.

## 1. Chuan bi moi truong

Chay tu thu muc goc cua project:

```bash
cd /home/pognova/SkillManim/manim-video-builder
```

Kich hoat virtual environment neu dang dung `venv` co san:

```bash
source venv/bin/activate
```

Kiem tra cac cong cu can thiet:

```bash
python --version
manim --version
ffmpeg -version
ffprobe -version
python -m edge_tts --list-voices | grep vi-VN
```

Neu `python` khong ton tai tren may, dung `python3`.

## 2. Chuan bi script dau vao

Dat noi dung script vao:

```text
input/script.txt
```

Script nen co cac heading ro rang de tool tach scene tot hon. Vi du:

```text
Tieu de: Object-Centric Learning va Causal World Models

1. Pixel khong phai la the gioi

Noi dung voice cho phan 1...

2. Object slots

Noi dung voice cho phan 2...
```

Khuyen nghi:

- Moi section nen la mot y tuong ro rang.
- Dung doan ngan, cau ro, it ky hieu kho doc.
- Cong thuc co the de trong script, tool se co gang lam cho TTS de doc hon.
- Voi video 20-30 phut, hay chia script thanh nhieu section lon, tool se tach tiep thanh scene 45-90 giay.

## 3. Command chay mac dinh

```bash
python src/main.py \
  --input input/script.txt \
  --voice vi-VN-HoaiMyNeural \
  --quality medium \
  --scene-duration 60 \
  --max-chars 800 \
  --resume
```

Y nghia:

- `--scene-duration 60`: moi scene nham khoang 60 giay voice.
- `--max-chars 800`: moi chunk gui cho `edge-tts` toi da 800 ky tu.
- `--quality medium`: render Manim chat luong trung binh.
- `--resume`: scene da xong thi bo qua, khong render lai.

## 4. Output duoc tao

Moi scene co folder rieng:

```text
output/scenes/scene_001/
|-- voice_text.txt
|-- chunks/
|-- audio_chunks/
|-- narration.mp3
|-- subtitles.srt
|-- video_no_audio.mp4
`-- video_with_audio.mp4
```

File Manim rieng cho moi scene:

```text
manim_scenes/scene_001.py
manim_scenes/scene_002.py
...
```

Output cuoi:

```text
output/final/final_video.mp4
output/final/narration.mp3
output/final/subtitles.srt
output/final/manifest.json
```

`manifest.json` ghi metadata cho tung scene, gom:

- `scene_index`
- `scene_title`
- `voice_text`
- `duration`
- `audio_file`
- `manim_file`
- `video_no_audio`
- `video_with_audio`
- `formulas`
- `animation_type`
- `status`
- `start`
- `end`

## 5. Resume va render lai

Tiep tuc job dang chay do dang:

```bash
python src/main.py --input input/script.txt --resume
```

Neu scene nao da co `video_with_audio.mp4` va narration hop le, tool se bo qua scene do.

Render lai tat ca scene:

```bash
python src/main.py --input input/script.txt --force
```

Render lai mot scene:

```bash
python src/main.py --input input/script.txt --only-scene 5 --force
```

Render tiep tu scene 10 den scene 20:

```bash
python src/main.py --input input/script.txt --from-scene 10 --to-scene 20 --resume
```

## 6. Chay dry-run de kiem tra split va code

Chi tao manifest, subtitle, voice text va code Manim; khong render:

```bash
python src/main.py --input input/script.txt --no-render --resume
```

Bo qua TTS, dung duration uoc luong tu text:

```bash
python src/main.py --input input/script.txt --no-tts --no-render
```

Day la cach nhanh de kiem tra script co tach scene dung khong.

## 7. Dieu chinh tham so

Scene ngan hon, phu hop nhieu cut:

```bash
python src/main.py --scene-duration 45 --max-chars 700 --resume
```

Scene dai hon, it cut hon:

```bash
python src/main.py --scene-duration 90 --max-chars 800 --resume
```

Chat luong render:

```bash
python src/main.py --quality low
python src/main.py --quality medium
python src/main.py --quality high
```

Voice tieng Viet:

```bash
python src/main.py --voice vi-VN-HoaiMyNeural
python src/main.py --voice vi-VN-NamMinhNeural
```

Chinh toc do va am luong:

```bash
python src/main.py --rate "+8%" --volume "+0%" --resume
```

## 8. Workflow sua Manim thu cong

Tool se sinh file:

```text
manim_scenes/scene_001.py
```

Neu muon sua animation thu cong:

1. Chay dry-run de sinh code:

```bash
python src/main.py --input input/script.txt --no-render
```

2. Sua file scene can chinh, vi du:

```text
manim_scenes/scene_005.py
```

3. Render thu cong scene do:

```bash
manim -qm manim_scenes/scene_005.py GeneratedVideo
```

4. Copy video render ra folder scene va ghep audio:

```bash
cp media/videos/scene_005/720p30/GeneratedVideo.mp4 output/scenes/scene_005/video_no_audio.mp4
ffmpeg -y \
  -i output/scenes/scene_005/video_no_audio.mp4 \
  -i output/scenes/scene_005/narration.mp3 \
  -c:v copy \
  -c:a aac \
  -shortest \
  output/scenes/scene_005/video_with_audio.mp4
```

Luu y: neu chay lai `python src/main.py` cho scene do, tool co the sinh lai file `manim_scenes/scene_005.py`. Hay giu ban backup neu da sua thu cong.

## 9. Debug loi thuong gap

TTS loi:

- Kiem tra internet.
- Kiem tra voice co ton tai:

```bash
python -m edge_tts --list-voices | grep vi-VN
```

- Giam `--max-chars` xuong 500-700.

Manim loi:

- Chay lai command render scene de xem log:

```bash
manim -qm manim_scenes/scene_001.py GeneratedVideo
```

- Neu loi `MathTex`, kiem tra LaTeX da cai du.

ffmpeg loi:

- Kiem tra `ffmpeg` va `ffprobe` co trong PATH.
- Kiem tra file audio/video cua scene co ton tai.

Job dung giua chung:

- Xem `output/final/manifest.json`.
- Scene loi se co `status: error`.
- Chay lai voi `--resume` de tiep tuc sau khi sua loi.

## 10. Lenh khuyen dung cho video dai 20-30 phut

```bash
python src/main.py \
  --input input/script.txt \
  --voice vi-VN-HoaiMyNeural \
  --quality medium \
  --scene-duration 60 \
  --max-chars 800 \
  --resume
```
