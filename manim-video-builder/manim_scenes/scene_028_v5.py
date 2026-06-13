from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene028(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_028/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Thành phố thông minh và bản sao số")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Physical City} \\rightarrow \\text{Digital Twin (Entities)}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 6.50s): Bản sao số của thành phố
        # ---------------------------------------------------------
        city = create_real_entity_box('world', 'Thành phố vật lý', scene_name="scene_028", color=COLOR_WARNING).shift(LEFT * 3 + UP * 0.45)
        twin = create_real_entity_box('math', 'Bản sao số 3D', scene_name="scene_028", color=COLOR_AI).shift(RIGHT * 3 + UP * 0.45)
        
        a1 = create_flow_arrow(city, twin)
        self.play(FadeIn(city, shift=RIGHT), run_time=1.0)
        self.play(GrowArrow(a1), FadeIn(twin, shift=LEFT), run_time=1.5)
        
        sync_to(6.50)

        # ---------------------------------------------------------
        # SEGMENT 2 (6.50s - 17.55s): Thay vì video thô
        # ---------------------------------------------------------
        camera_feed = create_text_box("Video camera (Quá tải)", color=RED).shift(DOWN * 1.25 + LEFT * 3)
        entities = create_text_box("Thực thể độc lập", color=COLOR_RESULT).shift(DOWN * 1.25 + RIGHT * 3)
        
        self.play(FadeIn(camera_feed, shift=UP), run_time=1.0)
        cross = Cross(camera_feed, stroke_color=RED, stroke_width=8)
        self.play(Create(cross), run_time=0.8)
        
        a2 = create_clean_arrow(camera_feed, entities, direction=RIGHT, buff=0.3)
        self.play(GrowArrow(a2), FadeIn(entities, shift=LEFT), run_time=1.0)
        
        sync_to(17.55)
        self.play(FadeOut(city), FadeOut(camera_feed), FadeOut(cross), FadeOut(a1), FadeOut(a2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (17.55s - 26.01s): Dự báo ùn tắc
        # ---------------------------------------------------------
        plan = create_entity_box('results', 'Phân luồng tự động', color=COLOR_USER).shift(LEFT * 3 + UP * 0.15)
        a3 = create_clean_arrow(twin, plan, direction=LEFT, buff=0.34)
        
        self.play(GrowArrow(a3), FadeIn(plan, shift=RIGHT), run_time=1.5)
        self.play(Indicate(plan, color=COLOR_USER), run_time=1.5)
        
        sync_to(26.01)
        self.play(FadeOut(twin), FadeOut(plan), FadeOut(entities), FadeOut(a3), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (26.01s - 36.44s): Tối ưu hóa thời gian thực
        # ---------------------------------------------------------
        opt_text = create_text_box("Tối ưu lưu lượng giao thông toàn thành phố", color=COLOR_MATH).shift(DOWN * 0.5)
        self.play(FadeIn(opt_text, scale=0.8), run_time=1.5)
        self.play(Indicate(opt_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 37.632
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
