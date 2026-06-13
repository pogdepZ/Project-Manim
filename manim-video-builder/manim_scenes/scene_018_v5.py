from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene018(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_018/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Ví dụ vật lý: quả bóng va chạm cái hộp")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Ball} \\xrightarrow{\\text{Force}} \\text{Box}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 11.57s): Quả bóng lăn đến hộp
        # ---------------------------------------------------------
        ground = Line(LEFT * 5.0, RIGHT * 5.0, stroke_width=3, color=ARROW_GRAY).shift(DOWN * 1.35)
        ball = create_entity_box('ball', 'Quả bóng', color=COLOR_AI).shift(LEFT * 3.35 + DOWN * 0.45)
        box = create_entity_box('box', 'Chiếc hộp', color=COLOR_WARNING).shift(RIGHT * 0.4 + DOWN * 0.45)
        
        self.play(Create(ground), FadeIn(ball, shift=RIGHT), FadeIn(box, shift=UP), run_time=1.0)
        self.play(ball.animate.move_to(left_touch_position(ball, box, gap=0.1)), run_time=2.0)
        
        sync_to(11.57)

        # ---------------------------------------------------------
        # SEGMENT 2 (11.57s - 24.63s): Lực va chạm và trượt
        # ---------------------------------------------------------
        force = create_text_box("Lực F", color=RED, width=1.7).next_to(VGroup(ball, box), UP, buff=0.28)
        force_arrow = create_clean_arrow(ball, box, color=RED, direction=RIGHT, buff=0.08)
        self.play(FadeIn(force, shift=DOWN), GrowArrow(force_arrow), run_time=0.8)
        
        push_delta = RIGHT * 1.5
        self.play(ball.animate.shift(push_delta), box.animate.shift(push_delta), force.animate.shift(push_delta), force_arrow.animate.shift(push_delta), run_time=1.5)
        
        sync_to(24.63)
        self.play(FadeOut(force), FadeOut(force_arrow), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (24.63s - 28.60s): Nếu không có quả bóng
        # ---------------------------------------------------------
        self.play(ball.animate.shift(LEFT * 3), box.animate.shift(LEFT * 2), run_time=1.0)
        cross = Cross(ball, stroke_color=RED, stroke_width=8)
        self.play(Create(cross), run_time=0.8)
        self.play(Indicate(box, color=COLOR_WARNING), run_time=1.0)
        
        sync_to(28.60)
        self.play(FadeOut(ball), FadeOut(box), FadeOut(cross), FadeOut(ground), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (28.60s - 35.08s): Nền tảng vật lý trực quan
        # ---------------------------------------------------------
        physics_text = create_text_box("Nền tảng vật lý trực quan", color=COLOR_MATH).shift(DOWN * 0.5)
        self.play(FadeIn(physics_text, scale=0.8), run_time=1.5)
        self.play(Indicate(physics_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 36.240
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
