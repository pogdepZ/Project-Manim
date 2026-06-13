from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene014(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_014/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Tương quan thống kê và hạn chế của mô hình truyền thống")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("P(Y | X)")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 9.0s)
        # Voice: "Hầu hết các mô hình trí tuệ nhân tạo hiện nay chỉ học tương quan thống kê. Chúng học xác suất của kết quả y khi quan sát thấy điều kiện ích."
        # ---------------------------------------------------------
        x_block = create_entity_box('objects', 'Điều kiện X', color=COLOR_WARNING).shift(LEFT * 3)
        y_block = create_entity_box('objects', 'Kết quả Y', color=COLOR_RESULT).shift(RIGHT * 3)
        arrow = create_flow_arrow(x_block, y_block, color=COLOR_USER)
        
        self.play(FadeIn(x_block, shift=UP*0.2), run_time=1.0)
        self.play(GrowArrow(arrow), FadeIn(y_block, shift=UP*0.2), run_time=1.0)
        
        sync_to(11.00)

        # ---------------------------------------------------------
        # SEGMENT 2 (9.0s - 18.5s)
        # Voice: "Ví dụ, cứ khi thấy quả bóng ở gần hộp, ta thấy hộp di chuyển. Mô hình sẽ ghi nhớ mối tương quan bóng gần hộp thì hộp chuyển động."
        # ---------------------------------------------------------
        self.play(FadeOut(x_block), FadeOut(y_block), FadeOut(arrow), run_time=0.5)
        
        ball = create_real_entity_box('ball', 'Bóng (X)', scene_name="scene_014", color=COLOR_WARNING).shift(LEFT * 3.35 + DOWN * 0.42)
        box = create_real_entity_box('box', 'Hộp (Y)', scene_name="scene_014", color=COLOR_RESULT).shift(LEFT * 1 + DOWN * 0.56)
        
        self.play(FadeIn(ball), FadeIn(box), run_time=1.0)
        self.play(ball.animate.move_to(left_touch_position(ball, box, gap=0.1)), run_time=1.0)
        self.play(ball.animate.shift(RIGHT * 1.2), box.animate.shift(RIGHT * 1.2), run_time=1.0)
        
        sync_to(19.90)

        # ---------------------------------------------------------
        # SEGMENT 3 (18.5s - 28.0s)
        # Voice: "Nhưng tương quan này có thể bị sai nếu môi trường thay đổi đột ngột. Nó không trả lời được câu hỏi liệu bóng có trực tiếp tác động hay không."
        # ---------------------------------------------------------
        # Reset position
        self.play(ball.animate.move_to(LEFT * 3.0 + DOWN * 0.42), box.animate.move_to(LEFT * 0.7 + DOWN * 0.56), run_time=1.0)
        
        robot = create_real_entity_box('robot', 'Robot ẩn', scene_name="scene_014", color=COLOR_AI).shift(UP * 1.55 + RIGHT * 2.25)
        arrow_robot = create_clean_arrow(robot, box, color=COLOR_AI, direction=LEFT, buff=0.34)
        arrow_robot.add_updater(
            lambda m: m.become(create_clean_arrow(robot, box, color=COLOR_AI, direction=LEFT, buff=0.34))
        )
        
        self.play(FadeIn(robot, shift=DOWN*0.5), run_time=1.0)
        self.play(GrowArrow(arrow_robot), box.animate.shift(RIGHT * 2.0), run_time=1.0)
        arrow_robot.clear_updaters()
        
        sync_to(28.31)
        self.play(FadeOut(ball), FadeOut(box), FadeOut(robot), FadeOut(arrow_robot), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (28.0s - 37.5s)
        # Voice: "Những tương quan rác này là nguyên nhân chính khiến các mô hình học sâu hiện đại sụp đổ khi được triển khai trong thực tế."
        # ---------------------------------------------------------
        collapse_text = create_text_box("Tương quan rác\n(Spurious Correlations)", color=COLOR_WARNING).to_edge(UP, buff=1.2)
        self.play(FadeIn(collapse_text, scale=0.8), run_time=1.0)
        self.play(Indicate(collapse_text, color=COLOR_WARNING), run_time=1.5)
        
        total_dur = 35.664
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
