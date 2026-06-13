from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene008(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_008/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE (Top Safe Zone)
        title = create_title("Quá trình cạnh tranh giữa các slot")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA (Bottom Safe Zone)
        formula = create_formula_panel("Competition \\rightarrow Disentanglement")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1: Puzzle pieces metaphor (0s - 9.0s)
        # Voice: "Hãy tưởng tượng một nhóm học sinh đang tranh nhau các mảnh ghép của bức tranh. Mỗi học sinh chỉ được chọn một nhóm mảnh ghép liên quan."
        # ---------------------------------------------------------
        students = VGroup(
            create_real_entity_box('person', 'Học sinh A', scene_name="scene_008", color=COLOR_USER),
            create_real_entity_box('person', 'Học sinh B', scene_name="scene_008", color=COLOR_USER)
        ).arrange(DOWN, buff=1.0).shift(LEFT * 3.35)
        
        puzzle = create_real_entity_box('objects', 'Mảnh ghép', scene_name="scene_008", color=COLOR_WARNING).shift(RIGHT * 3)
        
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT) for s in students], lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(puzzle, shift=LEFT), run_time=1.0)
        
        a1 = create_flow_arrow(students[0], puzzle)
        a2 = create_flow_arrow(students[1], puzzle)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        
        sync_to(11.83)

        # ---------------------------------------------------------
        # SEGMENT 2: Winning a piece (9.0s - 17.0s)
        # Voice: "Nếu một mảnh ghép đã được một học sinh giải thích tốt và giữ chặt. Các học sinh khác sẽ không tập trung vào mảnh ghép đó nữa."
        # ---------------------------------------------------------
        puzzle_won = create_real_entity_box('ball', 'Mảnh ghép (Quả bóng)', scene_name="scene_008", color=COLOR_RESULT).move_to(puzzle)
        self.play(Transform(puzzle, puzzle_won), run_time=1.0)
        self.play(a1.animate.set_color(COLOR_RESULT), FadeOut(a2), run_time=1.0)
        
        sync_to(19.72)
        self.play(FadeOut(students), FadeOut(puzzle), FadeOut(a1), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3: Slots separation (17.0s - 26.0s)
        # Voice: "Sự cạnh tranh này buộc các slot phải tự phân chia ranh giới vật thể. Nhờ vậy, mỗi slot chỉ tập trung biểu diễn một thực thể duy nhất."
        # ---------------------------------------------------------
        clean_slots = VGroup(
            create_real_entity_box('ball', 'Slot 1: Quả bóng', scene_name="scene_008", color=COLOR_RESULT),
            create_real_entity_box('table', 'Slot 2: Cái bàn', scene_name="scene_008", color=COLOR_RESULT),
            create_real_entity_box('chair', 'Slot 3: Cái ghế', scene_name="scene_008", color=COLOR_RESULT)
        ).arrange(RIGHT, buff=0.8).center()
        if clean_slots.width > 12.0: clean_slots.scale_to_fit_width(12.0)
        
        self.play(LaggedStart(*[FadeIn(s, shift=UP*0.3) for s in clean_slots], lag_ratio=0.4), run_time=2.0)
        
        sync_to(27.89)

        # ---------------------------------------------------------
        # SEGMENT 4: Information bottleneck (26.0s - 34.656s)
        # Voice: "Sự cạnh tranh này dựa trên nguyên lý thắt nút cổ chai thông tin, ép buộc mô hình phải loại bỏ sự dư thừa."
        # ---------------------------------------------------------
        bottleneck_text = create_text_box("Thắt nút cổ chai thông tin\n(Information Bottleneck)", color=COLOR_WARNING).to_edge(UP, buff=1.2)
        self.play(FadeIn(bottleneck_text, scale=0.8), run_time=1.0)
        self.play(Indicate(clean_slots, color=COLOR_RESULT), run_time=1.5)
        
        total_dur = 34.656
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
