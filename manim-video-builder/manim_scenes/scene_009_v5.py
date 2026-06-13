from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene009(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_009/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE (Top Safe Zone)
        title = create_title("Reconstruction và mask: kiểm tra việc học")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA (Bottom Safe Zone)
        formula = create_formula_panel("\\hat{x} = \\sum_{k} (m_k \\times \\hat{x}_k)")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction to reconstruction (0s - 9.0s)
        # Voice: "Làm thế nào để chúng ta biết các slot đã học đúng cấu trúc? Chúng ta bắt mô hình phải tái tạo lại bức ảnh ban đầu từ các slot."
        # ---------------------------------------------------------
        slots = create_entity_box('objects', 'Slots', color=COLOR_AI).shift(LEFT * 3.35)
        decoder = create_real_entity_box('ai', 'Decoder', scene_name="scene_009", color=COLOR_AI)
        reconstructed = create_real_entity_box('camera', 'Ảnh tái tạo', scene_name="scene_009", color=COLOR_RESULT).shift(RIGHT * 3.35)
        
        arrow1 = create_flow_arrow(slots, decoder)
        arrow2 = create_flow_arrow(decoder, reconstructed)

        self.play(FadeIn(slots, shift=RIGHT), run_time=0.8)
        self.play(GrowArrow(arrow1), FadeIn(decoder, shift=UP), run_time=1.0)
        self.play(GrowArrow(arrow2), FadeIn(reconstructed, shift=LEFT), run_time=1.0)
        
        sync_to(13.58)
        self.play(FadeOut(slots), FadeOut(decoder), FadeOut(reconstructed), FadeOut(arrow1), FadeOut(arrow2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Component images and masks (9.0s - 18.0s)
        # Voice: "Mỗi slot sẽ tạo ra một bức ảnh thành phần chứa vật thể nó phụ trách. Đồng thời, nó tạo ra một mặt nạ để chỉ rõ vùng hiển thị."
        # ---------------------------------------------------------
        img_part = create_real_entity_box('ball', 'Ảnh thành phần', scene_name="scene_009", color=COLOR_USER).shift(LEFT * 2)
        mask_part = create_entity_box('pixels', 'Mặt nạ (Mask)', color=COLOR_WARNING).shift(RIGHT * 2)
        plus = Text("+", font_size=36, color=TEXT_WHITE).move_to(ORIGIN)
        
        self.play(FadeIn(img_part, shift=RIGHT), run_time=1.0)
        self.play(FadeIn(plus), FadeIn(mask_part, shift=LEFT), run_time=1.0)
        
        sync_to(21.90)
        self.play(FadeOut(img_part), FadeOut(mask_part), FadeOut(plus), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3: Combining pieces (18.0s - 27.0s)
        # Voice: "Chúng ta nhân ảnh thành phần với mặt nạ rồi cộng tất cả lại với nhau. Kết quả thu được là bức ảnh tái tạo hoàn chỉnh."
        # ---------------------------------------------------------
        final_pieces = VGroup(
            create_real_entity_box('ball', 'Thành phần 1', scene_name="scene_009", color=COLOR_USER),
            create_real_entity_box('table', 'Thành phần 2', scene_name="scene_009", color=COLOR_USER)
        ).arrange(DOWN, buff=0.5).shift(LEFT * 3.35)
        
        combined_img = create_real_entity_box('city', 'Ảnh tái tạo hoàn chỉnh', scene_name="scene_009", color=COLOR_RESULT).shift(RIGHT * 3)
        
        a1 = create_flow_arrow(final_pieces[0], combined_img)
        a2 = create_flow_arrow(final_pieces[1], combined_img)
        
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT) for p in final_pieces], lag_ratio=0.3), run_time=1.5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(combined_img, shift=LEFT), run_time=1.5)
        
        sync_to(29.38)

        # ---------------------------------------------------------
        # SEGMENT 4: Reconstruction Loss (27.0s - 37.416s)
        # Voice: "Hàm suy hao tái tạo đóng vai trò như một tín hiệu giám sát mạnh mẽ, tối ưu hóa các trọng số của bộ mã hóa và giải mã."
        # ---------------------------------------------------------
        loss_text = create_text_box("Reconstruction Loss\n(Tín hiệu giám sát)", color=COLOR_WARNING).to_edge(UP, buff=1.2)
        self.play(FadeIn(loss_text, scale=0.8), run_time=1.0)
        self.play(Indicate(loss_text, color=COLOR_WARNING), run_time=1.5)
        
        total_dur = 37.416
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
