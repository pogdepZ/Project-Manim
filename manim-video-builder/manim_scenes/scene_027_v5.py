from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene027(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_027/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Hỗ trợ chẩn đoán y tế dựa trên vùng có ý nghĩa")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Medical Image} \\rightarrow \\text{Segments} \\rightarrow \\text{Diagnosis}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 11.26s): Phát hiện tự động khối u
        # ---------------------------------------------------------
        lungs = create_real_entity_box('objects', 'Phổi', scene_name="scene_027", color=COLOR_USER).shift(LEFT * 3.35)
        tumor = create_real_entity_box('objects', 'Khối u', scene_name="scene_027", color=RED).shift(LEFT * 1)
        
        self.play(FadeIn(lungs, shift=UP), FadeIn(tumor, shift=UP), run_time=1.5)
        
        sync_to(11.26)

        # ---------------------------------------------------------
        # SEGMENT 2 (11.26s - 19.19s): Phân tích nhân quả
        # ---------------------------------------------------------
        risk = create_entity_box('results', 'Nguy cơ di căn', color=COLOR_WARNING).shift(RIGHT * 3)
        a1 = create_flow_arrow(tumor, risk)
        a1.set_color(RED)
        
        self.play(GrowArrow(a1), FadeIn(risk, shift=LEFT), run_time=1.5)
        
        sync_to(19.19)

        # ---------------------------------------------------------
        # SEGMENT 3 (19.19s - 26.81s): Kịch bản can thiệp
        # ---------------------------------------------------------
        cut_tumor = Cross(tumor, stroke_color=WHITE, stroke_width=8)
        self.play(Create(cut_tumor), run_time=0.8)
        
        effect = create_text_box("Mạch máu tái cấu trúc?", color=COLOR_MATH).shift(DOWN * 1.55)
        self.play(FadeIn(effect, shift=UP), run_time=1.0)
        
        sync_to(26.81)
        self.play(FadeOut(lungs), FadeOut(tumor), FadeOut(cut_tumor), FadeOut(risk), FadeOut(a1), FadeOut(effect), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (26.81s - 33.96s): Đáng tin cậy
        # ---------------------------------------------------------
        trust_text = create_text_box("AI Y Tế Đáng Tin Cậy", color=COLOR_RESULT).shift(UP * 0.5)
        self.play(FadeIn(trust_text, scale=0.8), run_time=1.5)
        self.play(Indicate(trust_text, color=COLOR_RESULT), run_time=1.5)
        
        total_dur = 35.136
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
