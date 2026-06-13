from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene002(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_002/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE (Top Safe Zone)
        title = create_title("Pixel không phải là thế giới")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA (Bottom Safe Zone)
        formula = create_formula_panel("X \\in \\mathbb{R}^{H \\times W \\times C}")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 & 2: Tensor and RGB (0s - 18s)
        # Voice: "Trong thị giác máy tính, một bức ảnh được biểu diễn dưới dạng một ten xơ ích...
        # Đối với một bức ảnh màu R G B thông thường, giá trị sê sẽ bằng ba..."
        # ---------------------------------------------------------
        tensor_block = create_entity_box('pixels', 'Tensor X (H x W x C)', color=COLOR_AI).shift(LEFT * 2)
        rgb_block = create_text_box("C = 3\n(Red, Green, Blue)", color=COLOR_MATH).shift(RIGHT * 3)
        arrow_1 = create_flow_arrow(tensor_block, rgb_block)

        self.play(FadeIn(tensor_block, shift=UP*0.2), run_time=1.0)
        sync_to(9.0) # End of sentence 1
        
        self.play(GrowArrow(arrow_1), FadeIn(rgb_block, shift=UP*0.2), run_time=1.0)
        self.play(Indicate(rgb_block, color=COLOR_MATH), run_time=1.5)
        
        sync_to(22.55) # Tensor/RGB representation fully explained
        self.play(FadeOut(tensor_block), FadeOut(rgb_block), FadeOut(arrow_1), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3: Camera & Real World (19.0s - 29.0s)
        # Voice: "Tuy nhiên, pích xơ không đại diện trực tiếp cho thế giới thực vật chất. Chúng chỉ là những tín hiệu ánh sáng thô sơ được camera ghi nhận."
        # ---------------------------------------------------------
        camera_block = create_real_entity_box('camera', 'Camera', scene_name="scene_002", color=COLOR_USER).shift(RIGHT * 3)
        real_world_block = create_real_entity_box('ball', 'Vật thể thực', scene_name="scene_002", color=COLOR_RESULT).shift(LEFT * 3)
        arrow_2 = create_flow_arrow(real_world_block, camera_block)
        
        self.play(FadeIn(real_world_block, shift=RIGHT), run_time=1.0)
        self.play(GrowArrow(arrow_2), FadeIn(camera_block, shift=LEFT), run_time=1.0)
        
        sync_to(30.94) # Camera/light-signal idea fully explained
        self.play(FadeOut(camera_block), FadeOut(real_world_block), FadeOut(arrow_2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4: Human perception (29.0s - 39.0s)
        # Voice: "Con người luôn tự động gom các pích xơ lại thành các vật thể độc lập. Một vùng màu tròn là quả bóng, một khối vuông là chiếc hộp gỗ."
        # ---------------------------------------------------------
        objects_group = VGroup(
            create_real_entity_box("ball", "Quả bóng", scene_name="scene_002", color=COLOR_RESULT),
            create_real_entity_box("box", "Chiếc hộp gỗ", scene_name="scene_002", color=COLOR_RESULT)
        ).arrange(RIGHT, buff=1.5).center()
        
        self.play(FadeIn(objects_group[0], shift=UP*0.2), run_time=1.0)
        self.play(FadeIn(objects_group[1], shift=UP*0.2), run_time=1.0)
        
        sync_to(39.61) # Human grouping examples fully explained
        self.play(FadeOut(objects_group), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 5: Processing Independent Channels (39.0s - 48.2s)
        # Voice: "Bằng cách chia tách không gian màu RGB, hệ thống máy học có thể phân tích cường độ sáng một cách độc lập trước khi tái tạo lại vật thể."
        # ---------------------------------------------------------
        machine_block = create_real_entity_box("ai", "Hệ thống máy học", scene_name="scene_002", color=COLOR_AI).shift(LEFT*3)
        reconstruct_block = create_real_entity_box("objects", "Tái tạo vật thể", scene_name="scene_002", color=COLOR_RESULT).shift(RIGHT*3)
        arrow_3 = create_flow_arrow(machine_block, reconstruct_block)
        
        self.play(FadeIn(machine_block, shift=RIGHT), run_time=1.0)
        self.play(GrowArrow(arrow_3), FadeIn(reconstruct_block, shift=LEFT), run_time=1.0)
        self.play(Indicate(reconstruct_block, color=COLOR_RESULT), run_time=1.5)
        
        total_dur = 48.29
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
