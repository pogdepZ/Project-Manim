from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene010(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_010/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE (Top Safe Zone)
        title = create_title("Bài toán dữ liệu mô phỏng và thế giới thực")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA (Bottom Safe Zone)
        formula = create_formula_panel("\\text{Synthetic (Simple)} \\rightarrow \\text{Real World (Complex)}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1: Sim-to-Real intro (0s - 8.0s)
        # Voice: "Các nghiên cứu ban đầu thường chỉ chạy trên dữ liệu mô phỏng đơn giản. Dữ liệu này có nền trơn, ánh sáng hoàn hảo và vật thể đơn sắc."
        # ---------------------------------------------------------
        synthetic = create_real_entity_box('objects', 'Thế giới mô phỏng\n(Đơn giản)', scene_name="scene_010", color=COLOR_AI).shift(LEFT * 3)
        self.play(FadeIn(synthetic, shift=RIGHT), run_time=1.5)
        
        sync_to(12.38)

        # ---------------------------------------------------------
        # SEGMENT 2: Real world complexity (8.0s - 17.0s)
        # Voice: "Nhưng thế giới thực phức tạp hơn rất nhiều so với môi trường mô phỏng. Nó chứa hàng ngàn texture khác nhau, bóng đổ và sự che khuất phức tạp."
        # ---------------------------------------------------------
        real_world = create_real_entity_box('world', 'Thế giới thực\n(Phức tạp)', scene_name="scene_010", color=COLOR_RESULT).shift(RIGHT * 3)
        self.play(FadeIn(real_world, shift=LEFT), run_time=1.5)
        
        sync_to(21.01)

        # ---------------------------------------------------------
        # SEGMENT 3: Reality gap (17.0s - 26.0s)
        # Voice: "Nếu chỉ học trên môi trường mô phỏng, mô hình sẽ thất bại khi ra thực tế. Đây là khoảng cách lớn cần phải vượt qua."
        # ---------------------------------------------------------
        gap_line = Line(UP*2, DOWN*2, stroke_width=8, color=COLOR_WARNING).shift(ORIGIN)
        gap_text = create_text_box("Reality Gap", color=COLOR_WARNING, width=2.8).move_to(UP * 1.15)
        
        self.play(Create(gap_line), FadeIn(gap_text, shift=DOWN), run_time=1.5)
        
        sync_to(28.49)

        # ---------------------------------------------------------
        # SEGMENT 4: Machine Learning challenge (26.0s - 36.552s)
        # Voice: "Sự chênh lệch miền dữ liệu này chính là bài toán chuyển giao học máy cốt lõi mà các kỹ sư AI đang nỗ lực giải quyết."
        # ---------------------------------------------------------
        arrow_cross = create_flow_arrow(synthetic, real_world, color=COLOR_MATH)
        self.play(GrowArrow(arrow_cross), run_time=1.5)
        self.play(Indicate(arrow_cross, color=COLOR_MATH), run_time=1.0)
        
        total_dur = 36.552
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
