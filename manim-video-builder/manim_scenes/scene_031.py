from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class GeneratedVideo(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_031/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Kết luận: hướng tới mô hình thế giới nhân quả")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Perception} + \\text{Causality} = \\text{Causal World Model}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 12.20s): Nhận thức và Nhân quả
        # ---------------------------------------------------------
        # Lowered slightly to avoid title overlap (from UP*1.5 to UP*1.25)
        percept_frame = RoundedRectangle(width=5.4, height=2.75, corner_radius=0.16, stroke_width=3, stroke_color=COLOR_USER, fill_color=COLOR_USER, fill_opacity=0.05).shift(LEFT * 3.1 + UP * 1.25)
        percept_label = Text("Nhận thức trung tâm đối tượng", font_size=20, color=COLOR_USER, weight=BOLD).next_to(percept_frame, UP, buff=0.12)
        slots = VGroup(
            create_entity_box('cup', 'cốc', color=COLOR_USER, width=1.35, height=1.05),
            create_entity_box('ball', 'bóng', color=COLOR_RESULT, width=1.35, height=1.05),
            create_entity_box('box', 'hộp', color=COLOR_MATH, width=1.35, height=1.05),
        ).arrange(RIGHT, buff=0.15).move_to(percept_frame)

        causal_frame = RoundedRectangle(width=5.4, height=2.75, corner_radius=0.16, stroke_width=3, stroke_color=COLOR_WARNING, fill_color=COLOR_WARNING, fill_opacity=0.05).shift(RIGHT * 3.1 + UP * 1.25)
        causal_label = Text("Nhân quả và quy luật SCM", font_size=20, color=COLOR_WARNING, weight=BOLD).next_to(causal_frame, UP, buff=0.12)
        cause = create_entity_box('ball', 'nguyên nhân', color=COLOR_WARNING, width=1.65, height=1.1).move_to(causal_frame.get_left() + RIGHT*1.3 + DOWN*0.15)
        effect = create_entity_box('box', 'kết quả', color=COLOR_RESULT, width=1.65, height=1.1).move_to(causal_frame.get_right() + LEFT*1.3 + DOWN*0.15)
        causal_arrow = create_flow_arrow(cause, effect, color=COLOR_WARNING)
        causal_graph = VGroup(cause, causal_arrow, effect)

        self.play(FadeIn(percept_frame), FadeIn(percept_label), LaggedStart(*[FadeIn(s, shift=UP*0.12) for s in slots], lag_ratio=0.15), run_time=1.5)
        self.play(FadeIn(causal_frame), FadeIn(causal_label), FadeIn(cause), GrowArrow(causal_arrow), FadeIn(effect), run_time=1.5)
        
        sync_to(12.20)

        # ---------------------------------------------------------
        # SEGMENT 2 (12.20s - 20.15s): Mô hình thế giới nhân quả
        # ---------------------------------------------------------
        # Lowered slightly to maintain gap (from DOWN*1.25 to DOWN*1.4)
        cwm = create_real_entity_box('mô hình thế giới', 'Mô hình thế giới\nnhân quả', scene_name="general", color=COLOR_AI).shift(DOWN * 1.4)
        a1 = create_clean_arrow(percept_frame, cwm, color=COLOR_USER, direction=DOWN, buff=0.14)
        a2 = create_clean_arrow(causal_frame, cwm, color=COLOR_WARNING, direction=DOWN, buff=0.14)

        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(cwm, shift=UP), run_time=1.2)
        
        # Add brain and future projections
        brain = ICON_MAP["brain"](color=COLOR_MATH).scale(0.8).next_to(cwm, RIGHT, buff=1.2)
        projections = VGroup(*[
            Arc(radius=0.3 + 0.2*i, start_angle=-PI/4, angle=PI/2, stroke_width=2, color=COLOR_MATH, stroke_opacity=0.6-0.1*i)
            for i in range(3)
        ]).next_to(brain, RIGHT, buff=0.1)
        
        self.play(FadeIn(brain, shift=LEFT), Create(projections), run_time=1.5)
        self.play(Indicate(cwm, color=COLOR_AI), brain.animate.scale(1.1).set_color(COLOR_RESULT), run_time=1.3)
        
        sync_to(20.15)
        self.play(
            FadeOut(percept_frame), FadeOut(percept_label), FadeOut(slots),
            FadeOut(causal_frame), FadeOut(causal_label), FadeOut(causal_graph),
            FadeOut(cwm), FadeOut(a1), FadeOut(a2), FadeOut(brain), FadeOut(projections), run_time=0.5
        )

        # ---------------------------------------------------------
        # SEGMENT 3 (20.15s - 30.77s): Cảm ơn mọi người
        # ---------------------------------------------------------
        journey = VGroup(
            create_entity_box('pixels', 'Pixels', color=COLOR_WARNING, width=1.35, height=1.05),
            create_entity_box('objects', 'Objects', color=COLOR_USER, width=1.35, height=1.05),
            create_entity_box('math', 'Causality', color=COLOR_MATH, width=1.35, height=1.05),
            create_entity_box('world_model', 'World Model', color=COLOR_RESULT, width=1.55, height=1.05),
        ).arrange(RIGHT, buff=0.38).shift(UP * 0.35)
        journey_arrows = VGroup(*[create_flow_arrow(journey[i], journey[i+1], color=ARROW_GRAY) for i in range(len(journey)-1)])
        thanks = create_text_box("Cảm ơn các bạn đã theo dõi!", color=COLOR_USER, width=4.4).shift(DOWN * 1.35)
        self.play(LaggedStart(*[FadeIn(j, shift=UP*0.15) for j in journey], lag_ratio=0.14), run_time=1.4)
        self.play(LaggedStart(*[GrowArrow(a) for a in journey_arrows], lag_ratio=0.12), FadeIn(thanks, scale=0.9), run_time=1.5)
        
        sync_to(30.77)

        # ---------------------------------------------------------
        # SEGMENT 4 (30.77s - 38.00s): Bình minh của AGI
        # ---------------------------------------------------------
        agi = create_text_box("Bình minh của\nTrí tuệ nhân tạo tổng quát", color=COLOR_MATH, width=4.6).shift(DOWN * 1.35)
        robot = ICON_MAP["robot"](color=COLOR_MATH).scale(1.25).move_to(UP * 1.25)
        halo = Circle(radius=0.9, color=COLOR_MATH, stroke_width=2, fill_opacity=0.06).move_to(robot)
        self.play(FadeOut(thanks), FadeOut(journey), FadeOut(journey_arrows), run_time=0.5)
        self.play(FadeIn(halo, scale=0.7), FadeIn(robot, shift=UP*0.2), FadeIn(agi, shift=UP), run_time=1.5)
        self.play(halo.animate.scale(1.08).set_stroke(opacity=0.45), agi.animate.set_color(COLOR_MATH), run_time=1.5)
        
        total_dur = 39.168
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
