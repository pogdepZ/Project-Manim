from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene026(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_026/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("AI hiện thân và agent trong môi trường game")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Embodied Agent}: \\text{Action} \\rightarrow \\text{Environment} \\rightarrow \\text{Reward}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 12.21s): AI hiện thân trong không gian
        # ---------------------------------------------------------
        agent = create_real_entity_box('robot', 'Agent (Tác nhân)', scene_name="scene_026", color=COLOR_USER).shift(LEFT * 3.35)
        env = create_real_entity_box('world', 'Môi trường', scene_name="scene_026", color=COLOR_AI)
        
        self.play(FadeIn(agent, shift=RIGHT), FadeIn(env, shift=UP), run_time=1.5)
        
        sync_to(12.21)

        # ---------------------------------------------------------
        # SEGMENT 2 (12.21s - 17.46s): Chìa khóa và cửa
        # ---------------------------------------------------------
        key = create_entity_box('objects', 'Chìa khóa', color=COLOR_WARNING).shift(UP * 1.4 + RIGHT * 2.8)
        door = create_entity_box('objects', 'Cánh cửa', color=COLOR_RESULT).shift(DOWN * 0.7 + RIGHT * 2.8)
        
        self.play(FadeIn(key, shift=DOWN * 0.25), run_time=0.7)
        self.play(FadeIn(door, shift=UP * 0.25), run_time=0.7)
        
        a1 = create_clean_arrow(key, door, direction=DOWN, buff=0.28)
        self.play(GrowArrow(a1), run_time=0.8)
        
        sync_to(17.46)

        # ---------------------------------------------------------
        # SEGMENT 3 (17.46s - 29.47s): Thử nghiệm trong đầu
        # ---------------------------------------------------------
        self.play(FadeOut(key), FadeOut(door), FadeOut(a1), run_time=0.5)

        brain = create_text_box("Mô hình thế giới (Trong đầu)", color=COLOR_AI).shift(RIGHT * 3.35)
        a2 = create_flow_arrow(agent, brain)
        
        self.play(GrowArrow(a2), FadeIn(brain, shift=LEFT), run_time=1.5)
        self.play(Indicate(brain, color=COLOR_AI), run_time=1.5)
        
        sync_to(29.47)
        self.play(FadeOut(agent), FadeOut(env), FadeOut(a2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (29.47s - 37.48s): Đạt phần thưởng tối đa
        # ---------------------------------------------------------
        reward = create_text_box("Phần thưởng tối đa\nChi phí thấp", color=COLOR_RESULT).move_to(brain)
        self.play(Transform(brain, reward), run_time=1.5)
        self.play(brain.animate.set_color(COLOR_RESULT), run_time=1.5)
        
        total_dur = 38.640
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
