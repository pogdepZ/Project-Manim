from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene022(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_022/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Sự tồn tại vĩnh viễn của đối tượng")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("z_t \\xrightarrow{\\text{Object Permanence}} z_{t+1}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 8.65s): Quả bóng lăn sau bìa
        # ---------------------------------------------------------
        ball = create_real_entity_box('objects', 'Quả bóng', scene_name="scene_022", color=COLOR_AI).shift(LEFT * 3.35)
        cover = create_real_entity_box('world', 'Tấm bìa che', scene_name="scene_022", color=COLOR_WARNING)
        
        self.play(FadeIn(ball, shift=RIGHT), FadeIn(cover, shift=UP), run_time=1.0)
        self.play(ball.animate.move_to(left_touch_position(ball, cover, gap=0.1)), run_time=1.4)
        self.play(FadeOut(ball, shift=RIGHT * 0.25), run_time=0.6)
        
        sync_to(8.65)

        # ---------------------------------------------------------
        # SEGMENT 2 (8.65s - 17.25s): Duy trì slot đối tượng
        # ---------------------------------------------------------
        ghost_ball = create_entity_box('results', 'Slot duy trì (z_t)', color=COLOR_RESULT)
        ghost_ball.next_to(cover, RIGHT, buff=0.5)
        self.play(FadeIn(ghost_ball), run_time=1.0)
        self.play(Indicate(ghost_ball, color=COLOR_RESULT), run_time=2.0)
        
        sync_to(17.25)

        # ---------------------------------------------------------
        # SEGMENT 3 (17.25s - 25.92s): Khớp lại với nhau
        # ---------------------------------------------------------
        ball.move_to(right_touch_position(ball, cover, gap=0.1))
        self.play(FadeIn(ball), Indicate(ball, color=COLOR_AI), run_time=1.0)
        self.play(Transform(ghost_ball, ball), run_time=1.0)
        
        sync_to(25.92)
        self.play(FadeOut(ball), FadeOut(cover), FadeOut(ghost_ball), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (25.92s - 37.31s): Bộ nhớ tuần tự tinh vi
        # ---------------------------------------------------------
        rnn_text = create_text_box("Transformer / RNN", color=COLOR_MATH).shift(DOWN * 0.5)
        self.play(FadeIn(rnn_text, scale=0.8), run_time=1.5)
        self.play(Indicate(rnn_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 38.496
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
