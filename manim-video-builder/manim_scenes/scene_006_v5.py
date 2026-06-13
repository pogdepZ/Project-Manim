from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene006(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_006/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE (Top Safe Zone)
        title = create_title("Object slots là gì?")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA (Bottom Safe Zone)
        formula = create_formula_panel("Z = \\{z_1, z_2, ..., z_K\\}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1: Intro slots as empty trays (0s - 10.0s)
        # Voice: "Một khái niệm cốt lõi trong học theo trung tâm đối tượng là các slot. Chúng ta hãy tưởng tượng mỗi slot là một chiếc khay chứa thông tin."
        # ---------------------------------------------------------
        def make_slot(label):
            tray = RoundedRectangle(width=2.05, height=1.55, corner_radius=0.16, stroke_width=3, stroke_color=COLOR_AI, fill_color=COLOR_AI, fill_opacity=0.08)
            txt = Text(label, font_size=18, color=TEXT_WHITE, weight=BOLD).next_to(tray, DOWN, buff=0.16)
            slot = VGroup(tray, txt)
            slot.box = tray
            slot.rect = tray
            return slot

        slots_group = VGroup(
            make_slot('Khay 1 (Slot)'),
            make_slot('Khay 2 (Slot)'),
            make_slot('Khay 3 (Slot)')
        ).arrange(RIGHT, buff=0.72).center().shift(DOWN * 0.05)
        
        self.play(LaggedStart(*[FadeIn(slot, shift=UP*0.2) for slot in slots_group], lag_ratio=0.3), run_time=2.0)
        
        sync_to(12.30)

        # ---------------------------------------------------------
        # SEGMENT 2: Objects filling the trays (10.0s - 19.0s)
        # Voice: "Nếu cảnh có quả bóng và chiếc hộp, mô hình sẽ tạo ra hai véc tơ biểu diễn. Véc tơ dê một cho quả bóng, véc tơ dê hai cho chiếc hộp."
        # ---------------------------------------------------------
        ball_icon = ICON_MAP["ball"](color=COLOR_RESULT).scale(0.75)
        ball_label = Text("z1: bóng", font_size=16, color=COLOR_RESULT, weight=BOLD).next_to(ball_icon, DOWN, buff=0.12)
        ball = VGroup(ball_icon, ball_label).move_to(slots_group[0].box)
        box_icon = ICON_MAP["box"](color=COLOR_RESULT).scale(0.72)
        box_label = Text("z2: hộp", font_size=16, color=COLOR_RESULT, weight=BOLD).next_to(box_icon, DOWN, buff=0.12)
        box = VGroup(box_icon, box_label).move_to(slots_group[1].box)
        
        # Start them from outside
        ball.shift(UP * 1.45)
        box.shift(UP * 1.45)
        
        self.play(FadeIn(ball, shift=DOWN), run_time=0.8)
        self.play(FadeIn(box, shift=DOWN), run_time=0.8)
        self.play(ball.animate.move_to(slots_group[0].box), box.animate.move_to(slots_group[1].box), run_time=1.0)
        
        sync_to(21.58)

        # ---------------------------------------------------------
        # SEGMENT 3: Permutation Invariance (19.0s - 29.0s)
        # Voice: "Thứ tự của các slot trong tập hợp này không hề quan trọng đối với mô hình. Khay thứ nhất có thể là quả bóng trong cảnh này, nhưng là chiếc hộp ở cảnh khác."
        # ---------------------------------------------------------
        self.play(Indicate(slots_group[0]), Indicate(slots_group[1]), run_time=1.5)
        
        # Swap animation
        pos1 = slots_group[0].box.get_center()
        pos2 = slots_group[1].box.get_center()
        
        self.play(
            ball.animate.move_to(pos2),
            box.animate.move_to(pos1),
            path_arc=PI/2, run_time=1.5
        )
        sync_to(31.10)

        # ---------------------------------------------------------
        # SEGMENT 4: Conclusion of invariance (29.0s - 39.648s)
        # Voice: "Đặc tính bất biến với hoán vị của các slot đảm bảo rằng kiến trúc mạng nơ ron không bị phụ thuộc vào thứ tự ngẫu nhiên của các đối tượng."
        # ---------------------------------------------------------
        invariance_text = create_text_box("Bất biến với hoán vị\n(Permutation Invariance)", color=COLOR_WARNING).to_edge(UP, buff=1.2)
        self.play(FadeIn(invariance_text, scale=0.8), run_time=1.0)
        
        total_dur = 39.648
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
