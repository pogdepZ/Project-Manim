from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene019(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_019/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Phân tích lực và động lượng dưới góc nhìn nhân quả")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("F = m \\cdot a,\\quad \\Delta p = F \\cdot \\Delta t")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 11.93s): Công thức vật lý
        # ---------------------------------------------------------
        eq_box = create_entity_box('math', 'Phương trình chuyển động', color=COLOR_MATH).shift(UP * 1.5)
        self.play(FadeIn(eq_box, shift=DOWN), run_time=1.5)
        
        sync_to(11.93)

        # ---------------------------------------------------------
        # SEGMENT 2 (11.93s - 20.53s): Can thiệp khối lượng
        # ---------------------------------------------------------
        ball = create_real_entity_box('objects', 'Quả bóng to (m lớn)', scene_name="scene_019", color=COLOR_AI).shift(LEFT * 3.35 + DOWN * 1)
        box = create_real_entity_box('objects', 'Chiếc hộp', scene_name="scene_019", color=COLOR_WARNING).shift(LEFT * 1 + DOWN * 1)
        
        self.play(FadeIn(ball, shift=RIGHT), FadeIn(box, shift=UP), run_time=1.0)
        self.play(ball.animate.move_to(left_touch_position(ball, box, gap=0.1)), run_time=1.0)
        self.play(ball.animate.shift(RIGHT * 1.6), box.animate.shift(RIGHT * 1.6), run_time=1.5)
        
        sync_to(20.53)
        self.play(FadeOut(ball), FadeOut(box), FadeOut(eq_box), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (20.53s - 29.07s): Cơ chế nhân quả ổn định
        # ---------------------------------------------------------
        stable = create_text_box("Cơ chế nhân quả ổn định", color=COLOR_RESULT).shift(UP * 0.5)
        self.play(FadeIn(stable, scale=0.8), run_time=1.5)
        self.play(Indicate(stable, color=COLOR_RESULT), run_time=1.5)
        
        sync_to(29.07)

        # ---------------------------------------------------------
        # SEGMENT 4 (29.07s - 35.23s): Bảo toàn đại lượng vật lý
        # ---------------------------------------------------------
        conserve = create_text_box("Bảo toàn đại lượng vật lý", color=COLOR_USER).shift(DOWN * 1.5)
        self.play(FadeIn(conserve, shift=UP), run_time=1.0)
        
        total_dur = 36.384
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
