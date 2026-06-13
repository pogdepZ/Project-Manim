from pathlib import Path

builder_dir = Path('/home/pognova/SkillManim/manim-video-builder')
missing = []
for i in range(1, 32):
    scene_name = f"scene_{i:03d}"
    vid = builder_dir / f"output/scenes/{scene_name}/video_with_audio.mp4"
    if not vid.exists():
        missing.append(scene_name)

print("Missing:", missing)
