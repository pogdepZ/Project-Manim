import json
import os
from pathlib import Path

# Path configuration
BUILDER_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = BUILDER_ROOT / "output" / "final" / "manifest.json"
SCENE_DIR = BUILDER_ROOT / "manim_scenes"

SCENE_SPECS = {
    1: [], # Handled manually inside the script
    2: [("Real object", "output", "ball"), ("Camera", "entity", "camera"), ("RGB Tensor", "module", "pixels"), ("Pixel matrix", "module", "pixels")],
    3: [("Image X", "module", "pixels"), ("Encoder f_theta", "model", "ai"), ("Vector z", "output", "objects")],
    4: [("Car", "entity", "car"), ("Pedestrian", "entity", "person"), ("Traffic light", "entity", "traffic_light"), ("Mixed vector", "warning", "causes")],
    5: [("Street scene", "output", "car"), ("Detection boxes", "warning", "objects"), ("Object slots", "model", "objects"), ("Unsupervised learning", "output", "world")],
    6: [("Ball", "entity", "ball"), ("Slot z1", "model", "objects"), ("Box", "entity", "box"), ("Slot z2", "model", "objects")],
    7: [("Image features", "module", "pixels"), ("Slot Attention", "model", "ai"), ("Clean slots", "output", "objects")],
    8: [("Puzzle pieces", "entity", "table"), ("Competition", "warning", "causes"), ("Disentangled slots", "output", "objects")],
    9: [("Slots", "model", "objects"), ("Decoder", "model", "ai"), ("Masks", "module", "pixels"), ("Reconstruction", "output", "world")],
    10: [("Synthetic world", "module", "world"), ("Reality gap", "warning", "causes"), ("Real world", "output", "world")],
    11: [("Image", "module", "pixels"), ("ViT", "model", "ai"), ("DINO features", "model", "ai"), ("Semantic slots", "output", "objects")],
    12: [("Slots", "model", "objects"), ("Feature decoder", "model", "ai"), ("DINO target", "module", "ai"), ("Feature loss", "warning", "causes")],
    13: [("Object zi", "output", "ball"), ("Relation g", "model", "relations"), ("Object zj", "output", "box")],
    14: [("Observed X", "module", "pixels"), ("Correlation P(Y|X)", "warning", "causes"), ("Result Y", "output", "box")],
    15: [("Intervention do(X)", "warning", "person"), ("Physical system", "entity", "ball"), ("Outcome Y", "output", "box")],
    16: [("Passive observer", "user", "person"), ("Hidden confounder", "warning", "causes"), ("Active intervention", "output", "traffic_light")],
    17: [("Parents PA_i", "module", "relations"), ("SCM function f_i", "model", "ai"), ("Variable X_i", "output", "objects"), ("Noise U_i", "warning", "causes")],
    18: [("Ball velocity", "entity", "ball"), ("Impact force", "warning", "causes"), ("Box motion", "output", "box")],
    19: [("Mass and accel", "module", "math"), ("Force F=m a", "model", "math"), ("Momentum change", "warning", "causes"), ("Slide distance", "output", "box")],
    20: [("Object slots", "model", "objects"), ("Causal graph", "model", "relations"), ("Behavior prediction", "output", "world")],
    21: [("Sunny training", "entity", "sun"), ("Distribution shift", "warning", "cloud"), ("Rainy testing", "output", "rain"), ("Stable rules", "model", "ai")],
    22: [("Visible ball", "entity", "ball"), ("Occluder", "entity", "box"), ("Persistent slot", "model", "ai"), ("Reappears", "output", "ball")],
    23: [("State s_t", "module", "world"), ("Action a_t", "entity", "robot_arm"), ("World Model", "model", "world_model"), ("Future s_t+1", "output", "world")],
    24: [("Robot arm", "entity", "robot_arm"), ("Cup + bottle", "entity", "cup"), ("Causal plan", "model", "ai"), ("Safe grasp", "output", "robot_arm")],
    25: [("Road entities", "entity", "car"), ("Relations", "model", "relations"), ("Brake decision", "warning", "traffic_light"), ("Safe driving", "output", "car")],
    26: [("Embodied agent", "entity", "game_agent"), ("Key", "entity", "key"), ("Door rule", "model", "ai"), ("Reward", "output", "world")],
    27: [("Medical image", "entity", "xray"), ("Segments", "model", "objects"), ("Lesion region", "warning", "causes"), ("Diagnosis", "output", "ai")],
    28: [("Physical city", "entity", "city"), ("Camera streams", "entity", "camera"), ("Digital twin", "model", "world_model"), ("Traffic control", "output", "traffic_light")],
    29: [("Text command", "module", "pixels"), ("Object grounding", "model", "ai"), ("Red cup slot", "output", "cup"), ("Robot action", "entity", "robot_arm")],
    30: [("Ambiguous objects", "warning", "tree"), ("Hidden U", "warning", "causes"), ("No intervention", "warning", "causes"), ("Scale cost", "warning", "causes")],
    31: [("Perception", "model", "ai"), ("Causality", "model", "relations"), ("Causal World Model", "output", "brain"), ("Safe action", "entity", "robot")],
}

def generate_scene_001_code():
    return """from manim import *
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene001(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_001/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        title = create_title("Mở đầu: AI có thật sự hiểu thế giới không?")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)
        
        # 1. Pipeline
        pipeline = VGroup(
            create_entity_box("pixels", "Pixels", color=COLOR_USER),
            create_entity_box("objects", "Objects", color=COLOR_RESULT),
            create_entity_box("relations", "Relations", color=COLOR_AI),
            create_entity_box("causes", "Causes", color=COLOR_WARNING),
            create_entity_box("world_model", "World Model", color=COLOR_MATH)
        ).arrange(RIGHT, buff=0.6).scale(0.6).shift(DOWN*0.1)
        if pipeline.width > 12: pipeline.scale_to_fit_width(12)
        arrows = VGroup(*[create_flow_arrow(pipeline[i], pipeline[i+1]) for i in range(4)])
        
        for i in range(5):
            self.play(FadeIn(pipeline[i], shift=UP*0.2), run_time=0.6)
            if i < 4: self.play(GrowArrow(arrows[i]), run_time=0.4)
            
        sync_to(7.0)
        self.play(FadeOut(pipeline), FadeOut(arrows), run_time=0.5)

        # 2. Human vs Pixels
        room_bg = RoundedRectangle(width=9, height=4, corner_radius=0.2, stroke_color=BLUE, fill_opacity=0.05).shift(DOWN*0.3)
        room_label = Text("Căn phòng thực tế", font_size=24, color=BLUE).next_to(room_bg, UP)
        self.play(Create(room_bg), Write(room_label), run_time=1.0)
        
        pixel_grid = VGroup(*[
            Square(side_length=0.3, stroke_width=1, color=COLOR_WARNING, fill_opacity=0.1)
            for _ in range(50)
        ]).arrange_in_grid(5, 10, buff=0.05).move_to(room_bg)
        self.play(FadeIn(pixel_grid), run_time=1.5)
        cross = Cross(pixel_grid, stroke_color=RED, stroke_width=15)
        self.play(Create(cross), run_time=1.0)
        
        sync_to(14.5)
        self.play(FadeOut(room_bg), FadeOut(room_label), FadeOut(pixel_grid), FadeOut(cross), run_time=0.5)

        # 3. Objects
        objects = VGroup(
            create_entity_box("table", "Cái bàn", color=COLOR_RESULT),
            create_entity_box("chair", "Cái ghế", color=COLOR_RESULT),
            create_entity_box("cup", "Cái ly", color=COLOR_RESULT),
            create_entity_box("person", "Con người", color=COLOR_USER)
        ).arrange(RIGHT, buff=0.6).scale(0.8).shift(DOWN*0.2)
        if objects.width > 12: objects.scale_to_fit_width(12)
        
        self.play(LaggedStart(*[FadeIn(obj, shift=UP*0.3) for obj in objects], lag_ratio=0.4), run_time=2.5)
        self.play(objects[3].animate.shift(RIGHT*1.0), run_time=0.8)
        self.play(objects[3].animate.shift(LEFT*1.0), run_time=0.8)
        
        sync_to(21.5)
        self.play(FadeOut(objects), run_time=0.5)

        # 4. Relations
        rel1 = VGroup(
            create_entity_box("person", "Người đẩy", color=COLOR_USER),
            create_entity_box("door", "Cửa mở", color=COLOR_RESULT)
        ).arrange(RIGHT, buff=1.5).shift(UP*0.5).scale(0.8)
        arrow1 = create_flow_arrow(rel1[0], rel1[1])
        
        rel2 = VGroup(
            create_entity_box("traffic_light", "Đèn đỏ", color=COLOR_WARNING),
            create_entity_box("car", "Xe dừng", color=COLOR_USER)
        ).arrange(RIGHT, buff=1.5).shift(DOWN*1.8).scale(0.8)
        arrow2 = create_flow_arrow(rel2[0], rel2[1])
        
        self.play(FadeIn(rel1[0]), run_time=0.6)
        self.play(GrowArrow(arrow1), FadeIn(rel1[1]), run_time=0.8)
        self.play(FadeIn(rel2[0]), run_time=0.6)
        self.play(GrowArrow(arrow2), FadeIn(rel2[1]), run_time=0.8)
        
        sync_to(29.5)
        self.play(FadeOut(rel1), FadeOut(arrow1), FadeOut(rel2), FadeOut(arrow2), run_time=0.5)

        # 5. AI Starting Point
        ai_brain = create_entity_box("robot", "AI System", color=COLOR_AI).shift(LEFT*3.5)
        numbers = VGroup(*[
            Text(str(np.random.randint(0, 255)), font_size=18, color=TEXT_WHITE)
            for _ in range(16)
        ]).arrange_in_grid(4, 4, buff=0.4)
        matrix = FlowchartBox(numbers, label_text="Ma trận số", color=COLOR_WARNING, pad_x=0.6, pad_y=0.6).shift(RIGHT*3)
        arrow_ai = create_flow_arrow(ai_brain, matrix)
        
        self.play(FadeIn(ai_brain), run_time=0.8)
        self.play(GrowArrow(arrow_ai), FadeIn(matrix), run_time=1.0)
        self.play(Indicate(matrix, color=COLOR_WARNING), run_time=1.2)
        
        sync_to(39.5)
        self.play(FadeOut(ai_brain), FadeOut(matrix), FadeOut(arrow_ai), run_time=0.5)

        # 6. Conclusion
        question = Text("Làm thế nào để AI hiểu thế giới như con người?", font_size=32, color=COLOR_MATH, weight=BOLD)
        self.play(Write(question), run_time=2.0)
        self.play(question.animate.to_edge(UP, buff=1.5).scale(0.8), run_time=1.0)
        
        final_flow = VGroup(
            create_entity_box("pixels", "Pixels", color=COLOR_WARNING),
            create_text_box("AI Cognitive Process", color=COLOR_AI, width=4.0),
            create_entity_box("objects", "Objects", color=COLOR_RESULT)
        ).arrange(RIGHT, buff=1.0).scale(0.8).shift(DOWN*0.5)
        if final_flow.width > 12: final_flow.scale_to_fit_width(12)
        f_arrows = VGroup(
            create_flow_arrow(final_flow[0], final_flow[1]),
            create_flow_arrow(final_flow[1], final_flow[2])
        )
        
        self.play(FadeIn(final_flow[0]), run_time=1.0)
        self.play(GrowArrow(f_arrows[0]), FadeIn(final_flow[1]), run_time=1.0)
        self.play(GrowArrow(f_arrows[1]), FadeIn(final_flow[2]), run_time=1.0)
        
        sync_to(51.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
"""

def generate_generic_scene_code(entry):
    idx = entry["scene_index"]
    title = entry.get("title", f"Scene {idx}")
    duration = entry.get("duration", 30.0)
    audio_file = entry.get("audio_file", f"output/scenes/scene_{idx:03d}/narration.mp3")
    formulas = entry.get("screen_formulas", [])
    hints = entry.get("visual_hints", [])
    spec = SCENE_SPECS.get(idx, [("Input", "module", None), ("Model", "model", None), ("Output", "output", None)])
    
    code = f"""from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene{idx:03d}(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/{audio_file}"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # 0. Title & Formula Base
        title = create_title("{title}")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)
"""
    if formulas:
        code += f"""
        formula_panel = create_formula_panel("{formulas[0]}")
        self.play(FadeIn(formula_panel, shift=UP*0.2), run_time=1.0)
"""

    code += """
        # 1. Main Visual Sequence
        blocks = VGroup(
"""
    for label, role, entity in spec:
        color_var = "COLOR_USER" if role == "user" or role == "entity" else "COLOR_AI" if role == "module" or role == "model" else "COLOR_RESULT" if role == "output" else "COLOR_WARNING"
        entity_val = entity if entity else label
        code += f"            create_entity_box('{entity_val}', '{label}', color={color_var}),\n"
    
    code += "        ).arrange(RIGHT, buff=0.7).center().shift(UP*0.1)\n"
    code += "        if blocks.width > 12.0: blocks.scale_to_fit_width(12.0)\n"
    code += "        arrows = VGroup(*[create_flow_arrow(blocks[i], blocks[i+1]) for i in range(len(blocks)-1)])\n"

    # Split duration for blocks reveal
    reveal_end = duration * 0.45
    step = reveal_end / max(1, len(spec))
    
    code += f"""
        for i in range(len(blocks)):
            self.play(FadeIn(blocks[i], shift=UP*0.2), run_time=0.7)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.4)
            sync_to(1.5 + (i+1)*{step:.2f})
"""

    # 2. Detail Phase: Add "Indicate" or "Sub-animations" based on hints
    detail_start = reveal_end + 2.0
    detail_end = duration * 0.85
    
    code += f"""
        # 2. Detail Phase (Audio continues)
        sync_to({detail_start:.2f})
"""
    
    # Cycle through blocks to highlight them while audio talks
    for i in range(len(spec)):
        t_highlight = detail_start + (i * (detail_end - detail_start) / len(spec))
        code += f"""
        sync_to({t_highlight:.2f})
        self.play(Indicate(blocks[{i}], color=blocks[{i}].box.get_color()), run_time=1.5)
"""

    # Final hold and cleanup
    code += f"""
        # Final Hold
        sync_to({duration:.2f} - 0.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
"""
    return code


def main():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    
    for entry in manifest:
        idx = entry["scene_index"]
        if idx > 31: continue
            
        print(f"Generating perfect v4 code for scene_{idx:03d}...")
        
        if idx == 1:
            code = generate_scene_001_code()
        else:
            code = generate_generic_scene_code(entry)
            
        out_path = SCENE_DIR / f"scene_{idx:03d}_v4.py"
        with open(out_path, "w") as f:
            f.write(code)
            
        # Update pointer
        main_scene_path = SCENE_DIR / f"scene_{idx:03d}.py"
        with open(main_scene_path, "w") as f:
            f.write(f"import sys, os\nsys.path.append(os.path.dirname(__file__))\nfrom scene_{idx:03d}_v4 import Scene{idx:03d} as GeneratedVideo")

if __name__ == "__main__":
    main()
