from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene024(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_024/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Ứng dụng trong Robotics: lập kế hoạch hành động")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Perception} \\rightarrow \\text{Slots} \\rightarrow \\text{Causal Plan} \\rightarrow \\text{Action}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 13.51s): Cốc thủy tinh và bình nước nóng
        # ---------------------------------------------------------
        cup = create_real_entity_box('objects', 'Cốc thủy tinh', scene_name="scene_024", color=COLOR_AI).shift(LEFT * 2)
        bottle = create_real_entity_box('objects', 'Bình nước nóng', scene_name="scene_024", color=COLOR_WARNING).shift(RIGHT * 2)
        
        self.play(FadeIn(cup, shift=UP), FadeIn(bottle, shift=UP), run_time=1.5)
        
        sync_to(13.51)

        # ---------------------------------------------------------
        # SEGMENT 2 (13.51s - 22.10s): Lực ép bị vỡ
        # ---------------------------------------------------------
        warning = create_text_box("Lực ép cao -> Vỡ", color=RED).move_to(cup).shift(UP * 1.5)
        self.play(FadeIn(warning, shift=DOWN), run_time=1.0)
        self.play(Indicate(warning, color=RED), run_time=1.5)
        
        sync_to(22.10)

        # ---------------------------------------------------------
        # SEGMENT 3 (22.10s - 30.32s): Lên kế hoạch an toàn
        # ---------------------------------------------------------
        robot_arm = create_real_entity_box('robot', 'Cánh tay Robot', scene_name="scene_024", color=COLOR_USER).shift(UP * 1.45)
        self.play(FadeIn(robot_arm, shift=DOWN), run_time=1.0)
        
        a1 = create_flow_arrow(robot_arm, cup)
        self.play(GrowArrow(a1), run_time=1.0)
        
        safe_text = create_text_box("Lực an toàn", color=COLOR_RESULT).move_to(warning)
        self.play(Transform(warning, safe_text), run_time=1.0)
        
        sync_to(30.32)
        self.play(FadeOut(cup), FadeOut(bottle), FadeOut(robot_arm), FadeOut(warning), FadeOut(a1), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (30.32s - 36.95s): Học tăng cường
        # ---------------------------------------------------------
        rl_text = create_text_box("Học tăng cường hiệu quả", color=COLOR_MATH).shift(DOWN * 0.5)
        self.play(FadeIn(rl_text, scale=0.8), run_time=1.5)
        self.play(Indicate(rl_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 38.136
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
