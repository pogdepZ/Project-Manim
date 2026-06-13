#!/usr/bin/env python3
"""
Check if all dependencies are installed
Run: python check_dependencies.py
"""

import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

dependencies = {
    "manim": "Manim (animation library)",
    "edge_tts": "Microsoft Edge TTS",
    "pydub": "Audio processing",
    "av": "PyAV (media duration probing)",
    "ffmpeg": "FFmpeg (video/audio processing)"
}

print("=" * 60)
print("Dependency Checker")
print("=" * 60)

missing = []

# Check Python packages
for package, name in dependencies.items():
    if package == "ffmpeg":
        # Special check for FFmpeg
        try:
            local_ffmpeg = Path(__file__).parent / ".venv" / "bin" / "ffmpeg"
            ffmpeg_cmd = str(local_ffmpeg) if local_ffmpeg.exists() else "ffmpeg"
            subprocess.run([ffmpeg_cmd, "-version"], capture_output=True, check=True)
            print(f"✅ {name}")
        except Exception as e:
            print(f"❌ {name}")
            missing.append(package)
    else:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}")
            missing.append(package)

print("\n" + "=" * 60)

if not missing:
    print("✓ All dependencies installed!")
    sys.exit(0)
else:
    print(f"Missing: {', '.join(missing)}\n")
    
    # Suggest installation
    python_packages = [p for p in missing if p != "ffmpeg"]
    
    if python_packages:
        print("Install Python packages:")
        print(f"  pip install {' '.join(python_packages)}")
    
    if "ffmpeg" in missing:
        print("\nInstall FFmpeg:")
        print("  Windows: choco install ffmpeg")
        print("  Or download: https://ffmpeg.org/download.html")
    
    print("\nOr install all at once:")
    print("  pip install -r requirements.txt")
    
    sys.exit(1)
