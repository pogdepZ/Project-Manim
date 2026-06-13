from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene005(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_005/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE (Top Safe Zone)
        title = create_title("Từ object detection đến học theo trung tâm đối tượng")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA (Bottom Safe Zone)
        formula = create_formula_panel("\\text{Scene} = \\{\\text{Object}_1, \\text{Object}_2, ..., \\text{Object}_K\\}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1: (0s - 8.72s)
        # Voice: "Cảnh gồm tập hợp đối tượng một, đối tượng hai, cho đến đối tượng thứ ca. Nhiều người sẽ nghĩ đến bài toán phát hiện đối tượng trong thị giác máy tính."
        # ---------------------------------------------------------
        scene_block = create_real_entity_box('camera', 'Cảnh thực tế', scene_name="scene_005", color=COLOR_WARNING).shift(LEFT * 3.35)
        detect_block = create_real_entity_box('ai', 'Phát hiện đối tượng\n(Object Detection)', scene_name="scene_005", color=COLOR_AI)
        
        arrow_1 = create_flow_arrow(scene_block, detect_block)

        self.play(FadeIn(scene_block, shift=UP*0.2), run_time=1.0)
        self.play(GrowArrow(arrow_1), FadeIn(detect_block, shift=UP*0.2), run_time=1.0)
        
        sync_to(8.72)

        # ---------------------------------------------------------
        # SEGMENT 2: (8.72s - 17.33s)
        # Voice: "Bài toán này tìm vật thể và vẽ các khung chữ nhật quanh chúng. Nhưng học theo trung tâm đối tượng tiến xa hơn phát hiện đối tượng thông thường."
        # ---------------------------------------------------------
        rect_boxes = VGroup(
            create_entity_box('objects', 'Khung chữ nhật 1', color=COLOR_USER),
            create_entity_box('objects', 'Khung chữ nhật 2', color=COLOR_USER)
        ).arrange(DOWN, buff=0.4).shift(RIGHT * 3.35)
        arrow_2 = create_flow_arrow(detect_block, rect_boxes)
        
        self.play(GrowArrow(arrow_2), FadeIn(rect_boxes, shift=LEFT), run_time=1.0)
        
        sync_to(17.33)
        self.play(FadeOut(scene_block), FadeOut(detect_block), FadeOut(rect_boxes), FadeOut(arrow_1), FadeOut(arrow_2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3: (17.33s - 25.38s)
        # Voice: "Phương pháp này không cần con người gắn nhãn trước cho dữ liệu. Mục tiêu là tự động phân chia toàn bộ cảnh thành các thực thể độc lập."
        # ---------------------------------------------------------
        human = create_real_entity_box('person', 'Con người gắn nhãn', scene_name="scene_005", color=COLOR_WARNING).shift(LEFT * 3)
        cross = Cross(human, stroke_color=RED, stroke_width=10)
        
        self.play(FadeIn(human, shift=UP*0.2), run_time=1.0)
        self.play(Create(cross), run_time=0.8)
        
        auto_split = create_text_box("Tự động phân chia", color=COLOR_RESULT).shift(RIGHT * 3)
        arrow_auto = create_flow_arrow(human, auto_split)
        
        self.play(GrowArrow(arrow_auto), FadeIn(auto_split, shift=LEFT), run_time=1.0)
        
        sync_to(25.38)
        self.play(FadeOut(human), FadeOut(cross), FadeOut(auto_split), FadeOut(arrow_auto), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4: (25.38s - 37.00s)
        # Voice: "A I sẽ học cách biểu diễn từng vật thể mà không cần giám sát. Phương pháp này hướng tới việc A I tự hình thành khái niệm về vật thể giống như não bộ trẻ sơ sinh."
        # ---------------------------------------------------------
        baby_brain = create_real_entity_box('robot', 'Học không giám sát', scene_name="scene_005", color=COLOR_AI).shift(UP * 1)
        concept = create_text_box("Tự khám phá cấu trúc tự nhiên", color=COLOR_MATH).shift(DOWN * 1.5)
        
        self.play(FadeIn(baby_brain, shift=DOWN*0.5), run_time=1.0)
        self.play(FadeIn(concept, shift=UP*0.5), run_time=1.0)
        self.play(Indicate(baby_brain, color=COLOR_AI), run_time=1.5)
        
        total_dur = 38.16
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
