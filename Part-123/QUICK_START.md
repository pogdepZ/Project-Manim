# QUICK START - 5 Phút Bắt Đầu Ngay

## ⚡ 3 Bước Chính

### Step 1️⃣: Render Video (30-45 phút)

**Option A: Docker (Khuyên Dùng)**
```bash
.\auto_all.ps1
```

**Option B: Local Manim**
```bash
python render_all.py
```

### Step 2️⃣: Tạo Lồng Tiếng (2-3 phút)
```bash
python generate_narration.py
```
✅ Tạo 13 file MP3 tiếng Việt tự động

### Step 3️⃣: Ghép Video + Audio (5-10 phút)
```bash
python combine_video_audio.py
```
✅ Output: `final_video_with_narration.mp4`

---

## 🎯 Kết Quả Cuối Cùng

```
final_video_with_narration.mp4  (150-200 MB)
├── 13 scenes
├── Công thức toán học (animated)
├── Lồng tiếng tiếng Việt
└── Sẵn sàng upload YouTube/TikTok
```

---

## 📋 Những Gì Sẽ Học Được (5 phút)

1. **Pixels → Objects** - Cách Machine Learning hiểu ảnh  
2. **Slot Attention** - Công thức cốt lõi (với animation)  
3. **Alpha Channel** - Cách objects blending  
4. **Causality** - Tại sao model phải "hiểu" causal reasoning  
5. **Real-World Apps** - Ứng dụng thực tế

---

## 🛠️ Yêu Cầu Hệ Thống

✅ **Cần:**
- Python 3.9+
- FFmpeg

✅ **Sẽ tự cài:**
- Manim
- edge-tts (TTS)

**Kiểm tra sẵn có:**
```bash
python --version        # Phải >= 3.9
ffmpeg -version        # Phải cài
```

---

## ⏱️ Tổng Thời Gian

| Bước | Thời Gian |
|------|----------|
| Render video | 30-45 phút |
| Tạo lồng tiếng | 2-3 phút |
| Ghép video + audio | 5-10 phút |
| **TỔNG** | **40-60 phút** |

---

## 📂 File Quan Trọng

- `scene.py` - Manim code (13 scenes)
- `NARRATION_SCRIPT.md` - Script lồng tiếng
- `README.md` - Hướng dẫn chi tiết
- `render_all.py` - Auto render
- `generate_narration.py` - Auto TTS
- `combine_video_audio.py` - Auto merge

---

## ⚠️ Lưu Ý Quan Trọng

1. **Render lâu?** Normal đó, chạy background
2. **Âm thanh lỗi?** Check `narration/` folder có .mp3 không
3. **Output kém chất lượng?** Thay đổi `-pqh` thành `-pql` ở render

---

## ❓ Nếu Có Lỗi

**→ Đọc:** `README.md` (phần Troubleshooting)

---

**Bắt đầu ngay:** `python render_all.py` ☕
