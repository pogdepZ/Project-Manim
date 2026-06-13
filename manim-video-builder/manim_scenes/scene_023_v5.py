from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene023(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_023/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Mô hình thế giới trong trí tuệ nhân tạo")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("s_{t+1} = \\text{WorldModel}(s_t, a_t)")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 11.17s): Bộ não giả lập
        # ---------------------------------------------------------
        st = create_entity_box('math', 'Trạng thái s_t', color=COLOR_USER).shift(UP * 1 + LEFT * 3)
        at = create_entity_box('robot', 'Hành động a_t', color=COLOR_WARNING).shift(DOWN * 1 + LEFT * 3)
        wm = create_entity_box('ai', 'Mô hình thế giới', color=COLOR_AI).shift(RIGHT * 0)
        
        a1 = create_flow_arrow(st, wm)
        a2 = create_flow_arrow(at, wm)
        
        self.play(FadeIn(st, shift=RIGHT), FadeIn(at, shift=RIGHT), run_time=1.0)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(wm, shift=LEFT), run_time=1.5)
        
        sync_to(11.17)

        # ---------------------------------------------------------
        # SEGMENT 2 (11.17s - 23.68s): Dự đoán sự thay đổi của slot
        # ---------------------------------------------------------
        st1 = create_entity_box('results', 'Trạng thái s_{t+1}', color=COLOR_RESULT).shift(RIGHT * 3.35)
        a3 = create_flow_arrow(wm, st1)
        
        self.play(GrowArrow(a3), FadeIn(st1, shift=LEFT), run_time=1.5)
        
        slots_text = create_text_box("Cập nhật slot đối tượng", color=COLOR_RESULT, width=3.4).shift(DOWN * 1.88)
        self.play(FadeIn(slots_text, shift=UP), run_time=1.0)
        
        sync_to(23.68)
        self.play(FadeOut(slots_text), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (23.68s - 32.77s): Lên kế hoạch thông minh
        # ---------------------------------------------------------
        plan_text = create_text_box("Lên kế hoạch dự đoán", color=COLOR_AI, width=3.4).shift(DOWN * 1.88)
        self.play(FadeIn(plan_text, shift=UP), run_time=1.0)
        self.play(Indicate(wm, color=COLOR_AI), run_time=1.5)
        
        sync_to(32.77)
        self.play(FadeOut(st), FadeOut(at), FadeOut(wm), FadeOut(st1), FadeOut(a1), FadeOut(a2), FadeOut(a3), FadeOut(plan_text), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (32.77s - 40.14s): Chuỗi tự hồi quy
        # ---------------------------------------------------------
        autoreg = create_text_box("Mô phỏng tự hồi quy dài hạn", color=COLOR_MATH).shift(DOWN * 0.5)
        self.play(FadeIn(autoreg, scale=0.8), run_time=1.5)
        self.play(Indicate(autoreg, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 41.328
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
