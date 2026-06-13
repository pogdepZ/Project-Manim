from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene021(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_021/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Dịch chuyển phân phối và khả năng tổng quát hóa")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("P_{\\text{train}}(X, Y) \\neq P_{\\text{test}}(X, Y)")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 8.23s): Dịch chuyển phân phối
        # ---------------------------------------------------------
        car_day = create_real_entity_box('car', 'Xe ban ngày', scene_name="scene_021", color=COLOR_AI).shift(LEFT * 3 + UP * 0.45)
        sun = VGroup(
            Circle(radius=0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=0.9),
            *[
                Line(0.32 * np.array([np.cos(a), np.sin(a), 0]), 0.55 * np.array([np.cos(a), np.sin(a), 0]), color=YELLOW, stroke_width=3)
                for a in np.linspace(0, TAU, 8, endpoint=False)
            ],
        ).move_to(car_day.get_top() + UP * 0.55)
        self.play(FadeIn(car_day, shift=UP), run_time=1.5)
        self.play(FadeIn(sun, scale=0.7), run_time=0.6)
        
        sync_to(8.23)

        # ---------------------------------------------------------
        # SEGMENT 2 (8.23s - 17.17s): Thực tế trời mưa
        # ---------------------------------------------------------
        car_night = create_real_entity_box('car', 'Xe ban đêm/mưa', scene_name="scene_021", color=COLOR_WARNING).shift(RIGHT * 3 + UP * 0.45)
        cloud = VGroup(
            Circle(radius=0.22, color=BLUE_B, fill_color=BLUE_E, fill_opacity=0.5),
            Circle(radius=0.28, color=BLUE_B, fill_color=BLUE_E, fill_opacity=0.5).shift(RIGHT * 0.24),
            Circle(radius=0.2, color=BLUE_B, fill_color=BLUE_E, fill_opacity=0.5).shift(LEFT * 0.24),
        ).move_to(car_night.get_top() + UP * 0.55)
        rain = VGroup(*[
            Line(UP * 0.08, DOWN * 0.22, color=BLUE_C, stroke_width=3).shift(RIGHT * x)
            for x in [-0.3, 0, 0.3]
        ]).next_to(cloud, DOWN, buff=0.05)
        weather = VGroup(cloud, rain)
        self.play(FadeIn(car_night, shift=UP), FadeIn(weather, shift=DOWN * 0.15), run_time=1.5)
        
        arrow = create_flow_arrow(car_day, car_night)
        self.play(GrowArrow(arrow), run_time=1.0)
        
        sync_to(17.17)

        # ---------------------------------------------------------
        # SEGMENT 3 (17.17s - 25.53s): Quy luật nhân quả giữ nguyên
        # ---------------------------------------------------------
        causal_rule = create_text_box("Quy luật nhân quả bền vững", color=COLOR_RESULT).shift(DOWN * 1.35)
        self.play(FadeIn(causal_rule, shift=UP), run_time=1.5)
        self.play(Indicate(causal_rule, color=COLOR_RESULT), run_time=1.5)
        
        sync_to(25.53)
        self.play(FadeOut(car_day), FadeOut(car_night), FadeOut(sun), FadeOut(weather), FadeOut(arrow), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (25.53s - 36.53s): Tổng quát hóa
        # ---------------------------------------------------------
        gen_text = create_text_box("Học cơ chế nền tảng", color=COLOR_MATH).shift(UP * 0.5)
        self.play(FadeIn(gen_text, scale=0.8), run_time=1.5)
        self.play(Indicate(gen_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 37.704
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
