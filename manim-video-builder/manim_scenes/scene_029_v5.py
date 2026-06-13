from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene029(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_029/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("AI đa phương thức: kết nối ngôn ngữ và hình ảnh")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Text Command} \\rightarrow \\text{Object Grounding} \\rightarrow \\text{Execution}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 12.13s): Lệnh văn bản và hình ảnh
        # ---------------------------------------------------------
        text_cmd = create_entity_box('math', '"Lấy chiếc cốc đỏ"', color=COLOR_MATH).shift(LEFT * 3.35 + UP * 1)
        camera_view = create_real_entity_box('camera', 'Tầm nhìn thực tế', scene_name="scene_029", color=COLOR_AI).shift(RIGHT * 3)
        
        self.play(FadeIn(text_cmd, shift=RIGHT), FadeIn(camera_view, shift=UP), run_time=1.5)
        
        sync_to(12.13)

        # ---------------------------------------------------------
        # SEGMENT 2 (12.13s - 20.94s): Liên kết slot và thuộc tính
        # ---------------------------------------------------------
        slot = create_entity_box('cup', 'Slot: Cốc', color=COLOR_USER).shift(LEFT * 1.75 + DOWN * 1.15)
        red_swatch = Circle(radius=0.34, color=RED, fill_color=RED, fill_opacity=0.9)
        attr = FlowchartBox(red_swatch, label_text='Thuộc tính: Đỏ', color=RED).shift(RIGHT * 1.0 + DOWN * 1.15)
        
        a1 = create_flow_arrow(text_cmd, slot)
        a2 = create_flow_arrow(text_cmd, attr)
        
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(slot), FadeIn(attr), run_time=1.5)
        
        sync_to(20.94)

        # ---------------------------------------------------------
        # SEGMENT 3 (20.94s - 30.08s): Không nhầm lẫn
        # ---------------------------------------------------------
        a3 = create_flow_arrow(slot, camera_view)
        self.play(GrowArrow(a3), run_time=1.0)
        self.play(Indicate(camera_view, color=COLOR_AI), run_time=1.5)
        
        sync_to(30.08)
        self.play(FadeOut(text_cmd), FadeOut(camera_view), FadeOut(slot), FadeOut(attr), FadeOut(a1), FadeOut(a2), FadeOut(a3), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (30.08s - 36.29s): Mô hình nền tảng mạnh mẽ
        # ---------------------------------------------------------
        foundation = create_text_box("Mô hình nền tảng đa phương thức", color=COLOR_RESULT).shift(UP * 0.5)
        self.play(FadeIn(foundation, scale=0.8), run_time=1.5)
        self.play(Indicate(foundation, color=COLOR_RESULT), run_time=1.5)
        
        total_dur = 37.464
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
