import os
import subprocess
import glob

scene_dir = '/home/pognova/SkillManim/manim-video-builder/output/scenes'
for i in range(1, 32):
    scene_name = f'scene_{i:03d}'
    audio_path = os.path.join(scene_dir, scene_name, 'narration.mp3')
    if os.path.exists(audio_path):
        cmd = ['ffprobe', '-i', audio_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
        try:
            dur = float(subprocess.check_output(cmd).decode().strip())
            print(f'{scene_name}: audio={dur:.3f}')
        except Exception as e:
            pass
