from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene016(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_016/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Sức mạnh của hành động can thiệp")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Observation vs Intervention}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 7.52s): Quan sát thụ động vs Can thiệp chủ động
        # ---------------------------------------------------------
        obs_panel = RoundedRectangle(width=5.4, height=3.05, corner_radius=0.16, stroke_width=3, stroke_color=COLOR_WARNING, fill_color=COLOR_WARNING, fill_opacity=0.05).shift(LEFT * 3.05 + UP * 0.35)
        int_panel = RoundedRectangle(width=5.4, height=3.05, corner_radius=0.16, stroke_width=3, stroke_color=COLOR_RESULT, fill_color=COLOR_RESULT, fill_opacity=0.05).shift(RIGHT * 3.05 + UP * 0.35)
        obs_label = Text("Quan sát thụ động", font_size=22, color=COLOR_WARNING, weight=BOLD).next_to(obs_panel, UP, buff=0.12)
        int_label = Text("Can thiệp chủ động", font_size=22, color=COLOR_RESULT, weight=BOLD).next_to(int_panel, UP, buff=0.12)

        cam = ICON_MAP["camera"](color=COLOR_WARNING).move_to(obs_panel.get_left() + RIGHT*0.9 + UP*0.35)
        obs_ball = ICON_MAP["ball"](color=COLOR_USER).move_to(obs_panel.get_center() + RIGHT*0.25 + DOWN*0.35)
        obs_box = ICON_MAP["box"](color=COLOR_MATH).move_to(obs_panel.get_right() + LEFT*1.05 + DOWN*0.35)
        sight = VGroup(
            DashedLine(cam.get_right(), obs_ball.get_left(), dash_length=0.08, color=COLOR_WARNING),
            DashedLine(cam.get_right(), obs_box.get_left(), dash_length=0.08, color=COLOR_WARNING),
        )
        passive_note = Text("chỉ nhìn, không chạm", font_size=17, color=TEXT_MUTED).next_to(obs_panel, DOWN, buff=0.08)

        robot = ICON_MAP["robot"](color=COLOR_RESULT).move_to(int_panel.get_left() + RIGHT*0.9 + UP*0.2)
        int_ball = ICON_MAP["ball"](color=COLOR_USER).move_to(int_panel.get_center() + LEFT*0.15 + DOWN*0.35)
        int_box = ICON_MAP["box"](color=COLOR_MATH).move_to(int_panel.get_right() + LEFT*1.05 + DOWN*0.35)
        push_arrow = Arrow(robot.get_right(), int_ball.get_left(), color=COLOR_RESULT, stroke_width=5, tip_length=0.22, buff=0.12)
        active_note = Text("tác động để kiểm tra nguyên nhân", font_size=17, color=TEXT_MUTED).next_to(int_panel, DOWN, buff=0.08)

        self.play(FadeIn(obs_panel), FadeIn(obs_label), FadeIn(cam), FadeIn(obs_ball), FadeIn(obs_box), run_time=1.1)
        self.play(Create(sight), FadeIn(passive_note), run_time=0.9)
        self.play(FadeIn(int_panel), FadeIn(int_label), FadeIn(robot), FadeIn(int_ball), FadeIn(int_box), run_time=1.1)
        self.play(GrowArrow(push_arrow), int_ball.animate.shift(RIGHT*0.55), int_box.animate.shift(RIGHT*0.42), FadeIn(active_note), run_time=1.1)
        
        sync_to(7.52)

        # ---------------------------------------------------------
        # SEGMENT 2 (7.52s - 16.20s): Phá vỡ tương quan giả
        # ---------------------------------------------------------
        self.play(FadeOut(passive_note), FadeOut(active_note), run_time=0.3)
        break_text = create_text_box("Phá vỡ tương quan giả", color=COLOR_AI, width=3.5).shift(DOWN * 1.95)
        self.play(FadeIn(break_text, shift=UP), run_time=1.0)
        self.play(Indicate(break_text, color=COLOR_AI), run_time=1.5)
        
        sync_to(16.20)
        self.play(
            FadeOut(obs_panel), FadeOut(int_panel), FadeOut(obs_label), FadeOut(int_label),
            FadeOut(cam), FadeOut(obs_ball), FadeOut(obs_box), FadeOut(sight),
            FadeOut(robot), FadeOut(int_ball), FadeOut(int_box), FadeOut(push_arrow),
            FadeOut(break_text), run_time=0.5
        )

        # ---------------------------------------------------------
        # SEGMENT 3 (16.20s - 25.06s): AI tự suy luận can thiệp
        # ---------------------------------------------------------
        ai_brain = create_entity_box('ai', 'Hệ thống AI', color=COLOR_AI).shift(LEFT * 2)
        decide_box = create_entity_box('hand', 'Quyết định can thiệp', color=COLOR_USER).shift(RIGHT * 2)
        arrow2 = create_flow_arrow(ai_brain, decide_box)
        
        self.play(FadeIn(ai_brain, shift=UP), run_time=1.0)
        self.play(GrowArrow(arrow2), FadeIn(decide_box, shift=UP), run_time=1.0)
        
        sync_to(25.06)
        self.play(FadeOut(ai_brain), FadeOut(decide_box), FadeOut(arrow2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (25.06s - 36.19s): Suy luận phi nghịch đảo
        # ---------------------------------------------------------
        final_text = create_text_box("Suy luận phản thực tế:\nNếu ta không đẩy thì sao?", color=COLOR_MATH, width=4.8).shift(DOWN * 0.25)
        self.play(FadeIn(final_text, scale=0.8), run_time=1.5)
        self.play(Indicate(final_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 37.368
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
