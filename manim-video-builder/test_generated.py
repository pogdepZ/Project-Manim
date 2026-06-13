from pathlib import Path

base_dir = Path('/home/pognova/SkillManim')
for i in range(1, 32):
    scene = f"scene_{i:03d}"
    vid1 = base_dir / f"videos/{scene}/720p30/GeneratedVideo.mp4"
    vid2 = base_dir / f"media/videos/{scene}/720p30/GeneratedVideo.mp4"
    out_vid = base_dir / f"manim-video-builder/output/scenes/{scene}/video_with_audio.mp4"
    
    status = []
    if vid1.exists(): status.append("vid1")
    if vid2.exists(): status.append("vid2")
    if out_vid.exists(): status.append("out")
    
    if not status:
        print(f"{scene}: ALL MISSING")
    else:
        print(f"{scene}: {', '.join(status)}")
