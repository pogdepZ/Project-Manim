from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene017(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_017/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Mô hình nhân quả cấu trúc SCM")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("X_i = f_i(PA_i, U_i)")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 20.72s): Các phương trình, đầu vào
        # ---------------------------------------------------------
        pa = create_entity_box('math', 'Nguyên nhân (PA)', color=COLOR_USER).shift(UP * 1 + LEFT * 3)
        u = create_entity_box('noise', 'Nhiễu ẩn (U)', color=COLOR_WARNING).shift(DOWN * 1 + LEFT * 3)
        x = create_entity_box('results', 'Biến kết quả (X)', color=COLOR_RESULT).shift(RIGHT * 2)
        
        a1 = create_flow_arrow(pa, x)
        a2 = create_flow_arrow(u, x)
        
        self.play(FadeIn(pa, shift=RIGHT), FadeIn(u, shift=RIGHT), run_time=1.5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(x, shift=LEFT), run_time=1.5)
        
        sync_to(20.72)

        # ---------------------------------------------------------
        # SEGMENT 2 (20.72s - 29.12s): Mô hình vận hành tự nhiên
        # ---------------------------------------------------------
        graph = create_real_entity_box('world', 'Quy luật tự nhiên', scene_name="scene_017", color=COLOR_AI).shift(RIGHT * 4.15 + DOWN * 0.05)
        a3 = create_flow_arrow(x, graph)
        
        self.play(GrowArrow(a3), FadeIn(graph, shift=LEFT), run_time=1.5)
        self.play(Indicate(graph, color=COLOR_AI), run_time=1.5)
        
        sync_to(29.12)
        self.play(FadeOut(pa), FadeOut(u), FadeOut(x), FadeOut(graph), FadeOut(a1), FadeOut(a2), FadeOut(a3), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (29.12s - 36.40s): Kịch bản giả định
        # ---------------------------------------------------------
        scenario_a = create_entity_box('ball', 'Can thiệp: đổi X', color=COLOR_WARNING).shift(LEFT * 3.2 + DOWN * 0.15)
        scenario_b = create_entity_box('box', 'Kết quả mới', color=COLOR_RESULT).shift(RIGHT * 3.2 + DOWN * 0.15)
        hypo = create_text_box("Dự đoán kịch bản giả định", color=COLOR_MATH, width=4.0).shift(UP * 1.25)
        hypo_arrow = create_flow_arrow(scenario_a, scenario_b, color=COLOR_MATH)
        self.play(FadeIn(hypo, scale=0.8), FadeIn(scenario_a, shift=RIGHT), run_time=1.2)
        self.play(GrowArrow(hypo_arrow), FadeIn(scenario_b, shift=LEFT), run_time=1.2)
        self.play(Indicate(scenario_b, color=COLOR_RESULT), run_time=1.2)
        
        total_dur = 37.560
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
