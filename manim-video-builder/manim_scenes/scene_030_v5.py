from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene030(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_030/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Các thách thức lớn trong tương lai")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Ambiguity} + \\text{Confounding} \\rightarrow \\text{Causal Discovery Limits}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 8.89s): Ranh giới đối tượng mơ hồ
        # ---------------------------------------------------------
        ambiguity = create_real_entity_box('objects', 'Ranh giới mơ hồ', scene_name="scene_030", color=COLOR_WARNING).shift(LEFT * 3 + UP * 1)
        self.play(FadeIn(ambiguity, shift=RIGHT), run_time=1.5)
        
        sync_to(8.89)

        # ---------------------------------------------------------
        # SEGMENT 2 (8.89s - 18.14s): Yếu tố gây nhiễu
        # ---------------------------------------------------------
        confound = create_entity_box('noise', 'Yếu tố gây nhiễu (U)', color=RED).shift(RIGHT * 3 + UP * 1)
        self.play(FadeIn(confound, shift=LEFT), run_time=1.5)
        
        cross = Cross(confound, stroke_color=RED, stroke_width=8)
        self.play(Create(cross), run_time=0.8)
        
        sync_to(18.14)

        # ---------------------------------------------------------
        # SEGMENT 3 (18.14s - 27.02s): Tốn kém năng lượng
        # ---------------------------------------------------------
        energy = create_text_box("Tiêu thụ năng lượng khổng lồ", color=COLOR_WARNING).shift(DOWN * 1.5)
        self.play(FadeIn(energy, shift=UP), run_time=1.0)
        self.play(Indicate(energy, color=COLOR_WARNING), run_time=1.5)
        
        sync_to(27.02)
        self.play(FadeOut(ambiguity), FadeOut(confound), FadeOut(cross), FadeOut(energy), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (27.02s - 37.56s): Rào cản tính toán
        # ---------------------------------------------------------
        limit = create_text_box("Rào cản tính toán bùng nổ", color=COLOR_MATH).shift(DOWN * 0.5)
        self.play(FadeIn(limit, scale=0.8), run_time=1.5)
        self.play(Indicate(limit, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 38.736
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
