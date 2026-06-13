from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene012(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_012/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("DINO sau và hướng tái tạo đặc trưng")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("\\text{Loss} = ||F_{\\text{ViT}} - F_{\\text{decoded}}||^2")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 9.0s)
        # Voice: "Mô hình Đi nô sau là một bước tiến vô cùng quan trọng gần đây. Thay vì tái tạo điểm ảnh gốc, mô hình này tái tạo lại các đặc trưng Đi nô."
        # ---------------------------------------------------------
        slots = create_entity_box('objects', 'Slots', color=COLOR_USER).shift(LEFT * 3.35 + UP * 0.45)
        decoder = create_real_entity_box('ai', 'Decoder', scene_name="scene_012", color=COLOR_AI).shift(UP * 0.45)
        feat_recon = create_entity_box('pixels', 'Đặc trưng DINO', color=COLOR_RESULT).shift(RIGHT * 3.35 + UP * 0.45)
        
        a1 = create_flow_arrow(slots, decoder)
        a2 = create_flow_arrow(decoder, feat_recon)
        
        self.play(FadeIn(slots, shift=RIGHT), run_time=1.0)
        self.play(GrowArrow(a1), FadeIn(decoder, shift=UP), run_time=1.0)
        self.play(GrowArrow(a2), FadeIn(feat_recon, shift=LEFT), run_time=1.0)
        
        sync_to(9.44)

        # ---------------------------------------------------------
        # SEGMENT 2 (9.0s - 18.0s)
        # Voice: "Việc này giúp mô hình tập trung vào cấu trúc ngữ nghĩa của bức ảnh. Nó bỏ qua các chi tiết thừa thãi như vân gỗ hay hạt bụi nhỏ."
        # ---------------------------------------------------------
        noise_text = create_text_box("Bỏ qua chi tiết thừa", color=COLOR_WARNING, width=3.2).shift(DOWN * 2.02)
        self.play(FadeIn(noise_text, shift=UP), run_time=1.0)
        self.play(Indicate(feat_recon, color=COLOR_RESULT), run_time=1.5)
        
        sync_to(22.79)
        self.play(FadeOut(noise_text), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3 (18.0s - 27.0s)
        # Voice: "Nhờ vậy, quá trình chia slot trở nên ổn định trên ảnh thế giới thực. A I có thể gom cụm các bộ phận thành vật thể lớn hoàn chỉnh."
        # ---------------------------------------------------------
        parts = VGroup(
            create_real_entity_box('car', 'Bánh xe', scene_name="scene_012", color=COLOR_USER),
            create_real_entity_box('car', 'Thân xe', scene_name="scene_012", color=COLOR_USER)
        ).arrange(RIGHT, buff=0.5).shift(DOWN * 1.55)
        
        self.play(FadeIn(parts), run_time=1.0)
        
        car_full = create_real_entity_box('car', 'Xe hoàn chỉnh', scene_name="scene_012", color=COLOR_RESULT).move_to(parts)
        self.play(Transform(parts, car_full), run_time=1.5)
        
        sync_to(31.47)
        self.play(FadeOut(parts), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4 (27.0s - 36.5s)
        # Voice: "Sự tinh cất tri thức từ Đi nô giúp duy trì tính nhất quán về mặt hình học, đảm bảo quá trình chia slot hội tụ nhanh hơn."
        # ---------------------------------------------------------
        converge_text = create_text_box("Hội tụ nhanh & Ổn định", color=COLOR_MATH).to_edge(UP, buff=1.2)
        self.play(FadeIn(converge_text, scale=0.8), run_time=1.0)
        self.play(Indicate(converge_text, color=COLOR_MATH), run_time=1.5)
        
        total_dur = 39.528
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
