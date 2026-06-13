import json
import re
from pathlib import Path

manifest_path = Path("manim-video-builder/output/final/manifest.json")
manifest = json.loads(manifest_path.read_text())

for i in range(1, 7):
    # Scene 1 is scene_001_v3.py, others are scene_002.py etc.
    if i == 1:
        file_path = Path(f"manim-video-builder/manim_scenes/scene_001_v3.py")
    else:
        file_path = Path(f"manim-video-builder/manim_scenes/scene_{i:03d}.py")
        
    if not file_path.exists():
        print(f"File not found: {file_path}")
        continue
        
    duration = manifest[i-1]["duration"]
    content = file_path.read_text()
    
    # Remove any existing trailing wait or sync_wait if we want to be clean, 
    # but for now I'll just append it before the end of the construct method.
    
    # Find the last line of construct (usually it ends with a FadeOut or hold_visual)
    # I'll just append sync_wait(self, duration) at the very end of construct.
    
    if "sync_wait(self," in content:
        # Already added or exists
        content = re.sub(r"sync_wait\(self, [\d.]+\)", f"sync_wait(self, {duration})", content)
    else:
        # Append before the last line if it's a wait or just at the end
        # Assuming the construct method is the last thing or we can find its end.
        lines = content.splitlines()
        # Find the last indented line
        last_indented_idx = -1
        for idx, line in enumerate(lines):
            if line.startswith("        "): # double indent
                last_indented_idx = idx
        
        if last_indented_idx != -1:
            lines.insert(last_indented_idx + 1, f"        sync_wait(self, {duration})")
            content = "\n".join(lines)
            
    file_path.write_text(content)
    print(f"Updated {file_path} with duration {duration}")
