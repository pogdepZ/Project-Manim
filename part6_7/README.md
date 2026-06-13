# Object-Centric Learning Visualization - Video Production Guide

**Video Duration:** ~5 phút  
**Language:** Tiếng Việt (Vietnamese)  
**Quality:** 1080p60

---

## 📋 Tổng Quan Quy Trình

```
1. Render Manim scenes
       ↓
2. Generate Vietnamese narration (TTS)
       ↓
3. Combine video + audio
       ↓
4. Final video: final_video_with_narration.mp4
```

---

## 🚀 Hướng Dẫn Chi Tiết

### BƯỚC 1: Chuẩn Bị Môi Trường

```bash
# Cài đặt dependencies
pip install manim pydub edge-tts

# Cài đặt FFmpeg (Windows)
choco install ffmpeg
# Hoặc download từ: https://ffmpeg.org/download.html
```

### BƯỚC 2: Render Video Scenes

```bash
# Option A: Render tất cả scenes tự động
python render_all.py

# Option B: Render từng scene thủ công
manim -pqh scene.py SlotAttentionIntro
manim -pqh scene.py PixelsToObjects
manim -pqh scene.py SlotAttentionMechanism
manim -pqh scene.py AlphaChannelBlending
manim -pqh scene.py CausalIntervention
manim -pqh scene.py EndingScene
```

**Lưu ý:**
- `-p` = preview (mở video sau khi render)
- `-q` = quality: `l`=low, `m`=medium, `h`=high
- `-k` = để lại file (không xóa)
- `-s` = save last frame

**Thời gian render (tùy máy tính):**
- High quality 1080p60: ~30-45 phút
- Medium quality 720p30: ~10-15 phút

### BƯỚC 3: Tạo Lồng Tiếng (Narration)

```bash
# Tự động tạo từ text-to-speech
python generate_narration.py
```

**Kết quả:** 6 file MP3 trong folder `narration/`
- `narration/scene1.mp3` (15s)
- `narration/scene2.mp3` (45s)
- `narration/scene3.mp3` (75s)
- `narration/scene4.mp3` (60s)
- `narration/scene5.mp3` (75s)
- `narration/scene6.mp3` (30s)

**Thay thế bằng giọng của bạn:**

Nếu bạn muốn ghi âm giọng nói riêng của mình:
1. Tải script: `NARRATION_SCRIPT.md`
2. Dùng Audacity (free) hoặc điện thoại ghi âm
3. Lưu 6 file MP3 trong folder `narration/`

### BƯỚC 4: Ghép Video + Audio

```bash
# Tự động ghép video + lồng tiếng
python combine_video_audio.py
```

**Quá trình tự động:**
1. Tạo file concat list
2. Ghép 6 video scenes thành 1
3. Ghép 6 audio files thành 1
4. Merge video + audio
5. Tạo `final_video_with_narration.mp4`

**Thời gian chờ:** ~5-10 phút (tùy hiệu năng máy)

### BƯỚC 5: Kiểm Tra Output

```bash
# Xem thông tin video
ffprobe final_video_with_narration.mp4

# Phát để kiểm tra
# Windows
start final_video_with_narration.mp4

# Mac
open final_video_with_narration.mp4

# Linux
vlc final_video_with_narration.mp4
```

---

## 📁 Cấu Trúc Thư Mục

```
d:\manim-object-video\
├── scene.py                      # Manim scenes (6 classes)
├── render_all.py                 # Script render tất cả
├── generate_narration.py          # Tạo lồng tiếng từ TTS
├── combine_video_audio.py         # Ghép video + audio
├── NARRATION_SCRIPT.md           # Script lồng tiếng (tiếng Việt)
├── README.md                     # File này
├── narration/                    # Folder chứa audio files
│   ├── scene1.mp3
│   ├── scene2.mp3
│   ├── scene3.mp3
│   ├── scene4.mp3
│   ├── scene5.mp3
│   └── scene6.mp3
├── media/                        # Manim output (tự tạo)
│   └── videos/
│       └── 1080p60/
│           └── ObjectCentricLearning/
│               ├── SlotAttentionIntro.mp4
│               ├── PixelsToObjects.mp4
│               ├── SlotAttentionMechanism.mp4
│               ├── AlphaChannelBlending.mp4
│               ├── CausalIntervention.mp4
│               └── EndingScene.mp4
├── final_video_with_narration.mp4  # OUTPUT CUỐI CÙNG
└── (temp files: concat.txt, combined_video.mp4, etc.)
```

---

## ⚙️ Tùy Chỉnh Chi Tiết

### Thay Đổi Độ Phân Giải

**Trong `render_all.py`:**
```python
RESOLUTION = "1080p60"  # Options: 
                        # 480p15 (nhanh, chất lượng thấp)
                        # 720p30 (trung bình)
                        # 1080p60 (cao, chậm)
```

### Thay Đổi Giọng Đọc

**Trong `generate_narration.py`:**
```python
VOICE = "vi-VN-HoaiMyNeural"  # Options:
                               # vi-VN-HoaiMyNeural (nữ)
                               # vi-VN-NamMinhNeural (nam)
```

### Điều Chỉnh Tốc Độ Giọng

**Trong `generate_narration.py`:**
```python
RATE = "+0%"     # -50% (chậm), 0% (bình thường), +50% (nhanh)
```

---

## 🐛 Khắc Phục Sự Cố

### Lỗi: `ModuleNotFoundError: No module named 'manim'`
```bash
pip install manim
# Hoặc (nếu trên Mac):
pip install manim[jupyter]
```

### Lỗi: `ffmpeg not found`
```bash
# Windows
choco install ffmpeg

# Hoặc download thủ công: https://ffmpeg.org/download.html
# Thêm vào PATH hoặc copy vào project folder
```

### Lỗi: `edge-tts not found`
```bash
pip install edge-tts
```

### Video không có âm thanh
- Kiểm tra: Các file MP3 trong `narration/` folder có tồn tại không?
- Chạy lại: `python generate_narration.py`
- Hoặc ghi âm thủ công bằng Audacity

### Chất lượng video kém
- Tăng resolution: từ `720p30` lên `1080p60`
- Tăng quality: `-pqh` thay vì `-pql`
- Render lại: `python render_all.py`

### Video quá lâu hoặc quá ngắn
- Kiểm tra timing trong `scene.py` (các `self.wait()`)
- Chỉnh lại số giây wait để kéo dài/rút ngắn

---

## 💡 Gợi Ý Nâng Cao

### Thêm Background Music
```bash
# Tải nhạc lofi từ YouTube (có sẵn free license)
# Lưu vào: background_music.mp3

# Trong combine_video_audio.py, uncomment dòng:
add_background_music()
```

### Export Cho Social Media

**YouTube:**
```bash
# Format: MP4, H.264, 1080p60
# Đã tối ưu sẵn
```

**TikTok/Instagram Reels:**
```bash
# Crop thành 9:16 (dọc)
ffmpeg -i final_video_with_narration.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  output_vertical.mp4
```

**Facebook:**
```bash
# Tự động tối ưu, cứ upload file gốc là được
```

### Tạo Subtitles

```bash
# Từ narration script, tạo .srt file
# Sử dụng: ffmpeg-python hoặc web tool
```

---

## 📊 Thống Kê Video

| Metric | Giá Trị |
|--------|--------|
| Duration | ~5 phút (300s) |
| Resolution | 1080p |
| FPS | 60 fps |
| File Size | ~150-200 MB |
| Audio | 128 kbps MP3 |
| Scenes | 6 |
| Voice | Vietnamese (TTS) |

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra NARRATION_SCRIPT.md (hướng dẫn chi tiết)
2. Xem FFmpeg docs: https://ffmpeg.org/
3. Xem Manim docs: https://docs.manim.community/
4. Xem Edge TTS: https://github.com/rany2/edge-tts

---

## ✅ Checklist Hoàn Thành

- [ ] Cài Python 3.9+
- [ ] Cài Manim: `pip install manim`
- [ ] Cài edge-tts: `pip install edge-tts`
- [ ] Cài FFmpeg
- [ ] Chạy: `python render_all.py`
- [ ] Chạy: `python generate_narration.py`
- [ ] Chạy: `python combine_video_audio.py`
- [ ] Kiểm tra: `final_video_with_narration.mp4`
- [ ] Upload lên YouTube/TikTok

---

**Tạo bởi:** AI Assistant  
**Ngày:** May 19, 2026  
**License:** MIT
