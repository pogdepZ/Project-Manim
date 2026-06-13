import os
import re
from pathlib import Path

scenes_dir = Path("manim_scenes")

for i in range(1, 32):
    filename = scenes_dir / f"scene_{i:03d}.py"
    if not filename.exists(): continue
    
    content = filename.read_text(encoding="utf-8")
    
    # Find variables created as text or math
    text_vars = re.findall(r"([a-zA-Z0-9_]+)\s*=\s*(?:safe_text|MathTex|Text)\(", content)
    
    # We ignore 'title' and 'causal_label', 'feat_label', 'vit_label' etc that might be attached to objects.
    # We mainly care about floating 'formula', 'question', 'text', 'desc' etc.
    floating_vars = [v for v in text_vars if v not in ['title'] and not v.endswith('_label') and not v.endswith('_text')]
    
    if not floating_vars:
        continue
        
    for var in floating_vars:
        # Check if it's written or faded in
        if re.search(fr"(?:Write|FadeIn)\({var}", content):
            # Check if it's faded out before the end
            # We look for FadeOut(..., var, ...) or FadeOut(var) or FadeOut(VGroup(..., var, ...))
            fade_out = re.search(fr"FadeOut\([^)]*{var}[^)]*\)", content)
            
            if not fade_out:
                print(f"[{filename.name}] {var} is written but NEVER Faded Out explicitly!")
