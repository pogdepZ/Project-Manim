from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene004(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_004/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        title = create_title("Biểu diễn trộn lẫn và bài toán suy luận")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        formula_panel = create_formula_panel("z = [z_car, z_pedestrian, z_light]")
        self.play(FadeIn(formula_panel, shift=UP*0.2), run_time=1.0)

        car = create_entity_box('car', 'Xe hơi', color=COLOR_USER)
        person = create_entity_box('person', 'Người đi bộ', color=COLOR_RESULT)
        light = create_entity_box('traffic_light', 'Đèn giao thông', color=COLOR_MATH)
        objects = VGroup(car, person, light).arrange(RIGHT, buff=0.45).shift(UP * 1.14)
        mixed = create_entity_box('vector', 'Vector z trộn lẫn', color=COLOR_WARNING).shift(DOWN * 0.9)
        to_mixed = VGroup(*[create_clean_arrow(obj, mixed, color=obj.box.get_color(), direction=DOWN, buff=0.12) for obj in objects])

        self.play(LaggedStart(*[FadeIn(obj, shift=UP*0.2) for obj in objects], lag_ratio=0.18), run_time=1.4)
        sync_to(8.0)
        self.play(FadeIn(mixed, shift=UP*0.2), LaggedStart(*[GrowArrow(a) for a in to_mixed], lag_ratio=0.12), run_time=1.5)
        self.play(Indicate(mixed, color=COLOR_WARNING), run_time=1.0)
        sync_to(18.41)

        tangled = VGroup(*[
            Line(
                mixed.get_center() + np.array([np.cos(i)*0.75, np.sin(i*1.7)*0.45, 0]),
                mixed.get_center() + np.array([np.cos(i+1.9)*0.75, np.sin(i*1.3+1)*0.45, 0]),
                stroke_width=3,
                color=[COLOR_USER, COLOR_RESULT, COLOR_MATH, COLOR_WARNING][i % 4],
            )
            for i in range(18)
        ])
        question = Text("?", font_size=76, color=COLOR_WARNING, weight=BOLD).move_to(mixed)
        reasoning = create_text_box("Suy luận logic bị rối", font_size=20, color=COLOR_WARNING, width=3.4).move_to(LEFT * 3.35 + DOWN * 1.45)
        self.play(Create(tangled), FadeIn(question, scale=0.7), FadeIn(reasoning, shift=UP*0.2), run_time=1.4)
        sync_to(23.70)

        who_affects = create_text_box("Ai tác động lên ai?", font_size=20, color=COLOR_MATH, width=3.2).move_to(LEFT * 3.35 + UP * 0.05)
        question_arrow = create_clean_arrow(mixed, who_affects, color=COLOR_MATH, direction=LEFT, buff=0.28)
        blocked = Cross(who_affects, stroke_color=COLOR_WARNING, stroke_width=6)
        self.play(GrowArrow(question_arrow), FadeIn(who_affects, shift=LEFT*0.2), Create(blocked), run_time=1.2)
        sync_to(28.45)

        separated = VGroup(
            create_entity_box('car', 'z_car', color=COLOR_USER),
            create_entity_box('person', 'z_person', color=COLOR_RESULT),
            create_entity_box('traffic_light', 'z_light', color=COLOR_MATH),
        ).arrange(RIGHT, buff=0.55).shift(DOWN * 0.9)
        self.play(
            FadeOut(tangled), FadeOut(question), FadeOut(reasoning), FadeOut(who_affects), FadeOut(blocked), FadeOut(question_arrow),
            ReplacementTransform(mixed, separated),
            FadeOut(to_mixed),
            run_time=1.5
        )
        sync_to(32.63)
        boundary = create_text_box("Cần biểu diễn có cấu trúc rõ ràng", font_size=20, color=COLOR_RESULT, width=4.4).shift(DOWN * 2.15)
        self.play(FadeIn(boundary, shift=UP*0.2), Indicate(separated, color=COLOR_RESULT), run_time=1.6)

        sync_to(39.60)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
