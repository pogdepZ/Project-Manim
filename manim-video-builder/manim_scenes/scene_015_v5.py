from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene015(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_015/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Nhân quả: câu hỏi về sự can thiệp")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("P(Y | do(X = x))")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 9.0s)
        # Voice: "Nhân quả đặt ra một câu hỏi sâu sắc hơn rất nhiều. Nếu chúng ta chủ động can thiệp vào ích, kết quả y sẽ thay đổi như thế nào?"
        # ---------------------------------------------------------
        x_block = create_entity_box('objects', 'Biến X', color=COLOR_WARNING).shift(LEFT * 3)
        y_block = create_entity_box('objects', 'Kết quả Y', color=COLOR_RESULT).shift(RIGHT * 3)
        arrow = create_flow_arrow(x_block, y_block)
        
        self.play(FadeIn(x_block, shift=RIGHT), FadeIn(y_block, shift=LEFT), GrowArrow(arrow), run_time=1.5)
        
        do_symbol = create_text_box("do(X)", color=COLOR_AI, width=1.9).move_to(x_block.get_top() + UP * 1.05)
        do_arrow = create_clean_arrow(do_symbol, x_block, color=COLOR_AI, direction=DOWN, buff=0.18)
        self.play(FadeIn(do_symbol, shift=DOWN*0.3), GrowArrow(do_arrow), run_time=1.0)
        
        sync_to(9.96)

        # ---------------------------------------------------------
        # SEGMENT 2 (9.0s - 18.0s)
        # Voice: "Trong lý thuyết nhân quả, chúng ta sử dụng ký hiệu toán học do. Nó biểu thị một hành động chủ động tác động vào hệ thống vật lý."
        # ---------------------------------------------------------
        self.play(Indicate(do_symbol, color=COLOR_AI), run_time=1.5)
        self.play(x_block.animate.set_color(COLOR_AI), run_time=1.0)
        
        sync_to(20.75)
        self.play(FadeOut(x_block), FadeOut(y_block), FadeOut(arrow), FadeOut(do_symbol), FadeOut(do_arrow), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (18.0s - 27.0s)
        # Voice: "Chúng ta muốn biết nếu ta thay đổi vận tốc bóng, chiếc hộp có trượt không. Sự can thiệp này giúp phân biệt tương quan và nguyên nhân thực sự."
        # ---------------------------------------------------------
        hand = create_entity_box('hand', 'Can thiệp do', color=COLOR_USER).shift(LEFT * 3.35 + UP * 1.45)
        ball = create_real_entity_box('ball', 'Bóng', scene_name="scene_015", color=COLOR_WARNING).shift(LEFT * 2)
        box = create_real_entity_box('box', 'Hộp', scene_name="scene_015", color=COLOR_RESULT).shift(RIGHT * 1)
        
        self.play(FadeIn(ball), FadeIn(box), run_time=1.0)
        self.play(FadeIn(hand, shift=DOWN*0.5), run_time=1.0)
        
        # Hand pushes ball
        hand_target = ball.get_center() + UP * 1.45
        self.play(hand.animate.move_to(hand_target), run_time=0.8)
        self.play(ball.animate.move_to(left_touch_position(ball, box, gap=0.1)), run_time=0.6)
        self.play(ball.animate.shift(RIGHT * 1.2), box.animate.shift(RIGHT * 1.2), hand.animate.shift(RIGHT * 1.2), run_time=0.8)
        
        sync_to(29.31)
        self.play(FadeOut(hand), FadeOut(ball), FadeOut(box), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (27.0s - 35.8s)
        # Voice: "Việc mô phỏng toán tử do cho phép chúng ta phá vỡ các liên kết nhân quả giả tạo, hướng tới sự hiểu biết cốt lõi về hệ thống."
        # ---------------------------------------------------------
        core_text = create_text_box("Hiểu biết cốt lõi (Causal Discovery)", color=COLOR_MATH).to_edge(UP, buff=1.2)
        self.play(FadeIn(core_text, scale=0.8), run_time=1.0)
        self.play(Indicate(core_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 37.776
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
