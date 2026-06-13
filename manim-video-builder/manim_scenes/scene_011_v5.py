from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene011(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_011/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Vai trò của ViT và DINO trong biểu diễn ngữ nghĩa")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Image} \\rightarrow \\text{ViT} \\rightarrow \\text{Semantic Features}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 10.0s)
        # Voice: "Để giải quyết khoảng cách này, chúng ta không dùng điểm ảnh thô trực tiếp. Thay vào đó, ta sử dụng mạng biến đổi thị giác làm nền tảng."
        # ---------------------------------------------------------
        image_input = create_real_entity_box('camera', 'Ảnh đầu vào', scene_name="scene_011", color=COLOR_WARNING).shift(LEFT * 3.35)
        vit_block = create_real_entity_box('ai', 'Mạng ViT', scene_name="scene_011", color=COLOR_AI)
        arrow1 = create_flow_arrow(image_input, vit_block)
        
        self.play(FadeIn(image_input, shift=UP*0.2), run_time=1.0)
        self.play(GrowArrow(arrow1), FadeIn(vit_block, shift=UP*0.2), run_time=1.0)
        
        sync_to(8.08)

        # ---------------------------------------------------------
        # SEGMENT 2 (10.0s - 20.0s)
        # Voice: "Các mô hình tự giám sát như Đi nô giúp trích xuất đặc trưng ngữ nghĩa. Các đặc trưng này chứa thông tin về ranh giới vật thể rất tốt."
        # ---------------------------------------------------------
        features = VGroup(
            create_entity_box('pixels', 'Đặc trưng ngữ nghĩa 1', color=COLOR_RESULT),
            create_entity_box('pixels', 'Đặc trưng ngữ nghĩa 2', color=COLOR_RESULT)
        ).arrange(DOWN, buff=0.42).shift(RIGHT * 2.9 + DOWN * 0.15)
        arrow2 = create_flow_arrow(vit_block, features)
        
        self.play(GrowArrow(arrow2), FadeIn(features, shift=UP*0.2), run_time=1.5)
        
        sync_to(20.46)

        # ---------------------------------------------------------
        # SEGMENT 3 (20.0s - 30.0s)
        # Voice: "Khi slot attention hoạt động trên các đặc trưng cao cấp này, nó chạy tốt hơn. Nó không bị lừa bởi màu sắc bề mặt hay nhiễu ánh sáng."
        # ---------------------------------------------------------
        self.play(FadeOut(image_input), FadeOut(vit_block), FadeOut(arrow1), FadeOut(arrow2), run_time=0.45)
        slots = VGroup(
            create_entity_box('objects', 'Slot Attention', color=COLOR_USER).move_to(LEFT * 2.85 + UP * 0.25)
        )
        arrow_slot = create_clean_arrow(slots[0], features, color=COLOR_USER, direction=RIGHT, buff=0.32)
        
        self.play(GrowArrow(arrow_slot), FadeIn(slots[0]), run_time=1.0)
        self.play(Indicate(slots[0], color=COLOR_USER), run_time=1.5)
        
        sync_to(29.31)

        # ---------------------------------------------------------
        # SEGMENT 4 (30.0s - 40.5s)
        # Voice: "Kiến trúc Transformer với cơ chế tự chú ý toàn cục cho phép mô hình nhìn bao quát toàn bộ bức ảnh ngay từ những tầng xử lý đầu tiên."
        # ---------------------------------------------------------
        self.play(FadeOut(slots), FadeOut(arrow_slot), FadeOut(features), run_time=0.45)
        global_attention = create_text_box("Tự chú ý toàn cục\n(Global Attention)", color=COLOR_AI, width=3.6).move_to(ORIGIN + DOWN * 0.05)
        self.play(FadeIn(global_attention, shift=DOWN*0.2), run_time=1.0)
        self.play(Indicate(global_attention, color=COLOR_AI), run_time=1.5)
        
        total_dur = 37.752
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
