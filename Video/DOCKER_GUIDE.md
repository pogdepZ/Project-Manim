# Chạy Manim với Docker

## Lệnh Chạy Docker (Windows PowerShell)

### 1️⃣ Render Một Scene

```powershell
docker run --rm -it `
  -v "${PWD}:/manim" `
  manimcommunity/manim `
  manim -ql scene.py SlotAttentionIntro
```

⚠️ **QUAN TRỌNG:** Không dùng flag `-p` (preview) vì Docker không có GUI!  
Chỉ dùng `-ql` hoặc `-qm` hoặc `-qh`

### 2️⃣ Render Tất Cả Scenes (Cách 1)

```powershell
# Scene 1
docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py SlotAttentionIntro

# Scene 2
docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py PixelsToObjects

# Scene 3
docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py SlotAttentionMechanism

# Scene 4
docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py AlphaChannelBlending

# Scene 5
docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py CausalIntervention

# Scene 6
docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py EndingScene
```

### 3️⃣ Render Tất Cả Scenes (Cách 2 - Recommended)

Tạo file `render_docker.sh` (hoặc `.ps1`):

```powershell
# render_docker.ps1

$scenes = @(
    "SlotAttentionIntro",
    "PixelsToObjects",
    "SlotAttentionMechanism",
    "AlphaChannelBlending",
    "CausalIntervention",
    "EndingScene"
)

foreach ($scene in $scenes) {
    Write-Host "======================================="
    Write-Host "Rendering: $scene"
    Write-Host "======================================="
    
    docker run --rm -it `
      -v "${PWD}:/manim" `
      manimcommunity/manim `
      manim -pql scene.py $scene
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error rendering $scene"
        exit 1
    }
}

Write-Host "`n✓ All scenes rendered!"
```

Chạy:
```powershell
.\render_docker.ps1
```

---

## Giải Thích Lệnh Docker

```powershell
docker run --rm -it `
  -v "${PWD}:/manim" `
  manimcommunity/manim `
  manim -pql scene.py SlotAttentionIntro
```

| Phần | Ý Nghĩa |
|------|--------|
| `docker run` | Chạy container |
| `--rm` | Xóa container sau khi chạy xong (dọn dẹp) |
| `-it` | Interactive terminal (hiện output) |
| `-v "${PWD}:/manim"` | Mount thư mục hiện tại vào `/manim` trong container |
| `manimcommunity/manim` | Docker image (tự động tải nếu chưa có) |
| `manim -pql scene.py` | Lệnh manim (p=preview, q=quiet, l=low quality) |

---

## 📁 Cấu Trúc File Trong Docker

```
Container (/manim)
├── scene.py
├── media/              (output)
│   └── videos/
│       └── 480p15/     (do -l option)
│           └── ObjectCentricLearning/
│               ├── SlotAttentionIntro.mp4
│               ├── PixelsToObjects.mp4
│               └── ...

Host (Windows)
├── scene.py
├── media/              (mount từ container)
│   └── videos/
│       └── ...
```

---

## Quality Options

```powershell
# Low quality (nhanh, file nhỏ)
manim -ql scene.py SlotAttentionIntro    # 480p @ 15fps

# Medium quality (trung bình)
manim -qm scene.py SlotAttentionIntro    # 720p @ 30fps

# High quality (chậm, file to)
manim -qh scene.py SlotAttentionIntro    # 1080p @ 60fps
```

---

## Preview Options

```powershell
# ✅ Docker: Không preview (không có GUI)
docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py SlotAttentionIntro

# ⚠️ LỖI: Docker không hỗ trợ -p (preview)
# docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -pql scene.py SlotAttentionIntro
# → Error: FileNotFoundError: [Errno 2] No such file or directory: 'xdg-open'
```

**Lý do:** Docker container là Linux environment không có GUI. Nếu cần preview, render video trước rồi xem bằng máy tính cá nhân.

---

## 🐛 Troubleshooting Docker

### ⚠️ Lỗi: `FileNotFoundError: [Errno 2] No such file or directory: 'xdg-open'`

**Nguyên nhân:** Đang dùng flag `-p` (preview) trong Docker  
**Giải pháp:** Loại bỏ `-p`, chỉ dùng `-q` flags

```powershell
# ❌ Sai
manim -pql scene.py SlotAttentionIntro

# ✅ Đúng
manim -ql scene.py SlotAttentionIntro
```

### Lỗi: `docker: command not found`
```powershell
# Cài Docker Desktop
# Windows: https://www.docker.com/products/docker-desktop
# Hoặc chạy:
choco install docker-desktop
```

### Lỗi: `Cannot connect to Docker daemon`
```powershell
# Khởi động Docker Desktop hoặc Docker Service
# Hoặc chạy PowerShell as Administrator
```

### Lỗi: `Cannot find image manimcommunity/manim`
```powershell
# Tự động tải, hoặc pull trước:
docker pull manimcommunity/manim
```

### Muốn xóa Docker image (giải phóng dung lượng)
```powershell
docker rmi manimcommunity/manim
```

---

## 📊 So Sánh: Docker vs Local

| Tiêu Chí | Docker | Local |
|---------|--------|-------|
| Cài đặt | Docker Desktop | Manim + dependencies |
| Tốc độ | Nhanh (sau lần đầu) | Phụ thuộc máy |
| Dung lượng | ~3-4 GB | ~500 MB |
| Compatibility | 100% (containerized) | Tùy OS |
| Setup time | 5 phút | 15-30 phút |

---

## 🚀 One-Liner (Tất Cả 6 Scenes)

**Windows PowerShell:**
```powershell
@("SlotAttentionIntro","PixelsToObjects","SlotAttentionMechanism","AlphaChannelBlending","CausalIntervention","EndingScene") | ForEach-Object { docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -ql scene.py $_ }
```

**Bash/Linux:**
```bash
for scene in SlotAttentionIntro PixelsToObjects SlotAttentionMechanism AlphaChannelBlending CausalIntervention EndingScene; do
  docker run --rm -it -v "${PWD}:/manim" manimcommunity/manim manim -pql scene.py $scene
done
```

---

## ✅ Recommended Workflow

```powershell
# 1. Pull image (một lần)
docker pull manimcommunity/manim

# 2. Render một scene để test (không preview trong Docker)
docker run --rm -it `
  -v "${PWD}:/manim" `
  manimcommunity/manim `
  manim -ql scene.py SlotAttentionIntro

# 3. Nếu OK, render tất cả
.\render_docker.ps1

# 4. Ghép video + audio (local, không cần Docker)
python generate_narration.py
python combine_video_audio.py

# 5. Output: final_video_with_narration.mp4
```

---

## 🎯 Nếu Muốn Dùng Docker Cho Toàn Bộ Pipeline

Tạo `Dockerfile`:
```dockerfile
FROM manimcommunity/manim:latest

WORKDIR /manim

RUN pip install edge-tts pydub

COPY . .

CMD ["bash", "-c", "manim -pql scene.py SlotAttentionIntro && python generate_narration.py && python combine_video_audio.py"]
```

Build & Run:
```powershell
docker build -t manim-video .
docker run --rm -it -v "${PWD}:/manim" manim-video
```

---

## 📞 Nếu Gặp Vấn Đề

1. **Video quá chậm khi chạy Docker?**
   → Tăng Docker memory limit (Docker Desktop → Settings → Resources)

2. **Output file khác với local?**
   → Cùng image version, kết quả giống nhau

3. **Muốn preview video sau render?**
   → `docker run` với `-p` flag sẽ tự mở media player

---

**Khuyến nghị:** Dùng Docker cho render (clean, portable), dùng local cho audio/combine (nhanh hơn).
