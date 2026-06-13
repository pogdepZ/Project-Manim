from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene025(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_025/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Xe tự lái: hiểu các mối quan hệ trên đường phố")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Entities} + \\text{Relations} \\rightarrow \\text{Safe Driving}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 10.46s): Thực thể giao thông
        # ---------------------------------------------------------
        self_car = create_real_entity_box('car', 'Xe tự lái', scene_name="scene_025", color=COLOR_AI).shift(LEFT * 3.35)
        other_car = create_real_entity_box('car', 'Xe phía trước', scene_name="scene_025", color=COLOR_WARNING)
        
        self.play(FadeIn(self_car, shift=RIGHT), FadeIn(other_car, shift=RIGHT), run_time=1.5)
        
        sync_to(10.46)

        # ---------------------------------------------------------
        # SEGMENT 2 (10.46s - 20.47s): Phanh
        # ---------------------------------------------------------
        brake_light = create_text_box("Sáng đèn phanh", color=RED).move_to(other_car).shift(UP * 1.5)
        self.play(FadeIn(brake_light, shift=DOWN), run_time=1.0)
        
        a1 = create_clean_arrow(other_car, self_car, direction=LEFT, buff=0.32)
        a1.set_color(RED)
        
        action = create_text_box("Chuẩn bị phanh", color=COLOR_WARNING).move_to(self_car).shift(DOWN * 1.5)
        
        self.play(GrowArrow(a1), run_time=1.0)
        self.play(FadeIn(action, shift=UP), run_time=1.0)
        
        sync_to(20.47)

        # ---------------------------------------------------------
        # SEGMENT 3 (20.47s - 28.88s): Chuỗi nhân quả, tránh tương quan giả
        # ---------------------------------------------------------
        self.play(Indicate(a1, color=RED), run_time=1.5)
        
        sync_to(28.88)
        self.play(FadeOut(self_car), FadeOut(other_car), FadeOut(brake_light), FadeOut(action), FadeOut(a1), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (28.88s - 35.88s): Hệ thống tránh va chạm
        # ---------------------------------------------------------
        safe_text = create_text_box("Hệ thống tránh va chạm tích cực", color=COLOR_RESULT).shift(DOWN * 0.5)
        self.play(FadeIn(safe_text, scale=0.8), run_time=1.5)
        self.play(Indicate(safe_text, color=COLOR_RESULT), run_time=1.5)
        
        total_dur = 37.080
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
