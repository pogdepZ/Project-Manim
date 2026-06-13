from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene020(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_020/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Tại sao học theo trung tâm đối tượng hỗ trợ nhân quả?")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Slots} \\rightarrow \\text{Causal Graph} \\rightarrow \\text{Prediction}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 8.43s): Slots và thực thể
        # ---------------------------------------------------------
        slots = create_entity_box('objects', 'Slots (Thực thể)', color=COLOR_AI).shift(LEFT * 3.35 + UP * 0.42)
        graph = create_entity_box('math', 'Đồ thị Nhân quả', color=COLOR_MATH).shift(UP * 0.42)
        a1 = create_flow_arrow(slots, graph)
        
        self.play(FadeIn(slots, shift=RIGHT), run_time=1.0)
        self.play(GrowArrow(a1), FadeIn(graph, shift=RIGHT), run_time=1.5)
        
        sync_to(8.43)

        # ---------------------------------------------------------
        # SEGMENT 2 (8.43s - 17.13s): Pixel vs Object level
        # ---------------------------------------------------------
        pixel_cross = create_text_box("Pixel -> Pixel", color=COLOR_WARNING).shift(DOWN * 1.5 + LEFT * 2)
        cross = Cross(pixel_cross, stroke_color=RED, stroke_width=8)
        
        obj_flow = create_text_box("Bóng -> Hộp", color=COLOR_RESULT).shift(DOWN * 1.5 + RIGHT * 2)
        
        self.play(FadeIn(pixel_cross), run_time=1.0)
        self.play(Create(cross), run_time=0.8)
        self.play(FadeIn(obj_flow, shift=LEFT), run_time=1.0)
        
        sync_to(17.13)
        self.play(FadeOut(pixel_cross), FadeOut(cross), FadeOut(obj_flow), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (17.13s - 25.29s): Tách slots
        # ---------------------------------------------------------
        pred = create_entity_box('results', 'Dự đoán chuẩn xác', color=COLOR_USER).shift(RIGHT * 3.35)
        a2 = create_flow_arrow(graph, pred)
        
        self.play(GrowArrow(a2), FadeIn(pred, shift=LEFT), run_time=1.5)
        self.play(Indicate(pred, color=COLOR_USER), run_time=1.5)
        
        sync_to(25.29)
        self.play(FadeOut(slots), FadeOut(graph), FadeOut(pred), FadeOut(a1), FadeOut(a2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (25.29s - 36.88s): Giải quyết khám phá nhân quả
        # ---------------------------------------------------------
        final_text = create_text_box("Giải quyết khám phá nhân quả", color=COLOR_MATH).shift(DOWN * 0.5)
        self.play(FadeIn(final_text, scale=0.8), run_time=1.5)
        self.play(Indicate(final_text, color=COLOR_AI), run_time=1.5)
        
        total_dur = 38.064
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
