import os
import re
from pathlib import Path

fixes = [
    ("scene_003.py", r"(self\.play\(Flash\(formula, color=GOLD_A\), run_time=0\.5\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_004.py", r"(self\.play\(Write\(logic_text\), run_time=1\.0\)\s*\n\s*)self\.wait\(([\d.]+)\)", "q_mark, logic_text"),
    ("scene_009.py", r"(self\.play\(Write\(loss_label\), run_time=1\.0\)\s*\n\s*self\.play\(FadeIn\(loss_formula, shift=DOWN\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "loss_formula, loss_label"),
    ("scene_010.py", r"(self\.play\(Write\(formula\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_011.py", r"(self\.play\(Write\(formula\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_012.py", r"(self\.play\(Write\(formula\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_013.py", r"(self\.play\(Write\(formula\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_013.py", r"(self\.play\(Create\(arrow2\), Write\(label2\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "label1, label2"),
    ("scene_014.py", r"(self\.play\(Write\(formula\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_014.py", r"(self\.play\(Write\(question_mark\), run_time=1\.0\)\s*\n\s*)self\.wait\(([\d.]+)\)", "question_mark"),
    ("scene_015.py", r"(self\.play\(Flash\(formula, color=GOLD_A\), run_time=0\.5\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_016.py", r"(self\.play\(Write\(header\), run_time=0\.8\)\s*\n\s*)self\.wait\(([\d.]+)\)", "header"),
    ("scene_018.py", r"(self\.play\(Write\(formula\), run_time=1\.0\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_020.py", r"(self\.play\(Write\(formula\), run_time=1\.2\)\s*\n\s*)self\.wait\(([\d.]+)\)", "formula"),
    ("scene_024.py", r"(self\.play\(Create\(arrow1\), Write\(label_old\), run_time=1\.0\)\s*\n\s*)self\.wait\(([\d.]+)\)", "label_old"),
    ("scene_024.py", r"(self\.play\(Create\(arrow2\), Write\(label_new\), run_time=1\.0\)\s*\n\s*)self\.wait\(([\d.]+)\)", "label_new")
]

for filename, pattern, vars_to_fade in fixes:
    filepath = Path(f"manim_scenes/{filename}")
    if not filepath.exists():
        print(f"Skipping {filename}")
        continue
    content = filepath.read_text(encoding="utf-8")
    
    def repl(m):
        prefix = m.group(1)
        wait_time = float(m.group(2))
        new_wait_time = max(0, wait_time - 0.5)
        fadeout_str = ", ".join([f"FadeOut({v.strip()})" for v in vars_to_fade.split(",")])
        return f"{prefix}self.wait({new_wait_time:.1f})\n        self.play({fadeout_str}, run_time=0.5)"

    new_content, count = re.subn(pattern, repl, content)
    if count > 0:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"Patched {filename} for {vars_to_fade}")
    else:
        print(f"WARNING: Could not find match for {vars_to_fade} in {filename}")

# Wait, scene_009 has dot_product and loss_formula. Let me check scene_009 manually.
