from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene007(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_007/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE (Top Safe Zone)
        title = create_title("Cơ chế chú ý theo slot trực giác như thế nào?")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA (Bottom Safe Zone)
        formula = create_formula_panel("Attention(Q, K, V) = \\operatorname{softmax}(\\frac{Q K^T}{\\sqrt{d}}) V")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1: Input/Output of Slot Attention (0s - 9.0s)
        # Voice: "Cơ chế chú ý theo slot là một thuật toán vô cùng độc đáo. Đầu vào là các đặc trưng ảnh, đầu ra là thông tin trong các slot."
        # ---------------------------------------------------------
        features = create_entity_box('pixels', 'Đặc trưng ảnh', color=COLOR_WARNING).shift(LEFT * 3.35)
        algo = create_real_entity_box('ai', 'Slot Attention', scene_name="scene_007", color=COLOR_AI)
        slots = create_entity_box('objects', 'Thông tin Slots', color=COLOR_RESULT).shift(RIGHT * 3.35)
        
        arrow1 = create_flow_arrow(features, algo)
        arrow2 = create_flow_arrow(algo, slots)
        
        self.play(FadeIn(features, shift=RIGHT), run_time=1.0)
        self.play(GrowArrow(arrow1), FadeIn(algo, shift=UP), run_time=1.0)
        self.play(GrowArrow(arrow2), FadeIn(slots, shift=LEFT), run_time=1.0)
        
        sync_to(16.26)
        self.play(FadeOut(features), FadeOut(algo), FadeOut(slots), FadeOut(arrow1), FadeOut(arrow2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Initialization (9.0s - 18.0s)
        # Voice: "Cơ chế này khởi tạo các khay slot bằng các giá trị ngẫu nhiên ban đầu. Sau đó, các slot sẽ trải qua nhiều vòng cập nhật thông tin."
        # ---------------------------------------------------------
        init_slots = VGroup(
            create_entity_box('objects', 'Slot ngẫu nhiên', color=ARROW_GRAY),
            create_entity_box('objects', 'Slot ngẫu nhiên', color=ARROW_GRAY),
            create_entity_box('objects', 'Slot ngẫu nhiên', color=ARROW_GRAY)
        ).arrange(RIGHT, buff=0.8).center()
        
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN*0.2) for s in init_slots], lag_ratio=0.3), run_time=1.5)
        
        # Simulate blinking/updating
        self.play(LaggedStart(*[s.animate.set_color(COLOR_USER) for s in init_slots], lag_ratio=0.2), run_time=1.5)
        
        sync_to(24.25)

        # ---------------------------------------------------------
        # SEGMENT 3: Interaction (18.0s - 29.0s)
        # Voice: "Chúng sẽ tương tác với đặc trưng ảnh để tìm ra phần mình cần chịu trách nhiệm. Quá trình này giúp mô hình phân chia công việc cực kỳ thông minh."
        # ---------------------------------------------------------
        self.play(init_slots.animate.shift(DOWN * 1.5).scale(0.8), run_time=1.0)
        
        image_repr = create_real_entity_box('camera', 'Bức ảnh', scene_name="scene_007", color=COLOR_WARNING).shift(UP * 1.5)
        self.play(FadeIn(image_repr, shift=DOWN), run_time=1.0)
        
        interact_arrows = VGroup(*[
            create_clean_arrow(image_repr, s, color=ARROW_GRAY, direction=DOWN, buff=0.12)
            for s in init_slots
        ])
            
        self.play(LaggedStart(*[GrowArrow(a) for a in interact_arrows], lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[Indicate(s, color=COLOR_RESULT) for s in init_slots], lag_ratio=0.2), run_time=1.5)
        
        sync_to(32.80)

        # ---------------------------------------------------------
        # SEGMENT 4: Softmax competition (29.0s - 40.512s)
        # Voice: "Bằng việc sử dụng kỹ thuật Softmax có chuẩn hóa, mỗi điểm ảnh bị bắt buộc phải cạnh tranh để thuộc về một vùng chú ý duy nhất."
        # ---------------------------------------------------------
        softmax_text = create_text_box("Cạnh tranh\nSoftmax", font_size=20, color=COLOR_MATH, width=2.45).move_to(LEFT * 4.65 + UP * 1.15)
        self.play(FadeIn(softmax_text, scale=0.8), run_time=1.0)
        
        # Color the slots to show they took different parts
        c_colors = [COLOR_USER, COLOR_RESULT, COLOR_AI]
        self.play(LaggedStart(*[s.animate.set_color(c_colors[i]) for i, s in enumerate(init_slots)], lag_ratio=0.2), run_time=1.5)
        
        total_dur = 40.512
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
