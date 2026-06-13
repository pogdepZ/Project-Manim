import os
import re
import subprocess

scene_dir = '/home/pognova/SkillManim/manim-video-builder/output/scenes'
manim_scenes_dir = '/home/pognova/SkillManim/manim-video-builder/manim_scenes'

for i in range(1, 32):
    scene_name = f'scene_{i:03d}'
    audio_path = os.path.join(scene_dir, scene_name, 'narration.mp3')
    py_path = os.path.join(manim_scenes_dir, f'{scene_name}.py')
    
    if os.path.exists(audio_path) and os.path.exists(py_path):
        cmd = ['ffprobe', '-i', audio_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
        try:
            dur = float(subprocess.check_output(cmd).decode().strip())
        except Exception:
            continue
            
        with open(py_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract target duration
        target_match = re.search(r'# Total duration target:\s*([0-9\.]+)s', content)
        if target_match:
            target_dur = float(target_match.group(1))
            diff = dur - target_dur
            
            if diff > 0.5: # Only pad if difference is more than half a second
                print(f"Padding {scene_name} by {diff:.3f}s")
                # find the last FadeOut line
                fadeout_matches = list(re.finditer(r'(\s*self\.play\(FadeOut\([^)]+\)\)(?:.*?))(\n|$)', content))
                if fadeout_matches:
                    last_fadeout = fadeout_matches[-1]
                    insert_idx = last_fadeout.start()
                    pad_code = f"\n        self.wait({diff:.3f}) # Pad for audio\n"
                    new_content = content[:insert_idx] + pad_code + content[insert_idx:]
                    with open(py_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                else:
                    # Just append at the end of construct method
                    new_content = content + f"\n        self.wait({diff:.3f}) # Pad for audio\n"
                    with open(py_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
