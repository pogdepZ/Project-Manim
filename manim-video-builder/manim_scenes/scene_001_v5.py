from manim import *
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene001(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_001/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        title = create_title("Mở đầu: AI có thật sự hiểu thế giới không?")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction Pipeline (0s - 7.0s)
        # Voice: "Pích xơ dẫn tới đối tượng, dẫn tới mối quan hệ, dẫn tới nguyên nhân, dẫn tới mô hình thế giới."
        # ---------------------------------------------------------
        pipeline = VGroup(
            create_entity_box("pixels", "Pixels", color=COLOR_AI),
            create_entity_box("objects", "Objects", color=COLOR_RESULT),
            create_entity_box("relations", "Relations", color=COLOR_USER),
            create_entity_box("causes", "Causes", color=COLOR_WARNING),
            create_entity_box("world_model", "World Model", color=COLOR_MATH)
        ).arrange(RIGHT, buff=0.6).scale(0.6).shift(DOWN*0.1)
        if pipeline.width > 12: pipeline.scale_to_fit_width(12)
        arrows = VGroup(*[create_flow_arrow(pipeline[i], pipeline[i+1]) for i in range(4)])
        
        for i in range(5):
            self.play(FadeIn(pipeline[i], shift=UP*0.2), run_time=0.6)
            if i < 4: self.play(GrowArrow(arrows[i]), run_time=0.4)
            
        sync_to(6.0)
        self.play(FadeOut(pipeline), FadeOut(arrows), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Human Vision vs Pixels (7.0s - 14.5s)
        # Voice: "Khi chúng ta nhìn vào một căn phòng, chúng ta không thấy một ma trận pích xơ."
        # ---------------------------------------------------------
        human_block = create_real_entity_box("person", "Con người", scene_name="scene_001", color=COLOR_USER).shift(LEFT * 3)
        pixel_block = create_entity_box("pixels", "Ma trận Pixels", color=COLOR_WARNING).shift(RIGHT * 3)
        cross_mark = Cross(pixel_block, stroke_color=COLOR_WARNING, stroke_width=15)
        
        self.play(FadeIn(human_block, shift=RIGHT), run_time=1.0)
        self.play(FadeIn(pixel_block, shift=LEFT), run_time=1.0)
        self.play(Create(cross_mark), run_time=0.8)
        
        sync_to(11.07)
        self.play(FadeOut(human_block), FadeOut(pixel_block), FadeOut(cross_mark), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3: Seeing Real Objects (14.5s - 21.5s)
        # Voice: "Chúng ta thấy cái bàn, cái ghế, cái ly, con người và sự chuyển động."
        # ---------------------------------------------------------
        objects = VGroup(
            create_real_entity_box("table", "Cái bàn", scene_name="scene_001", color=COLOR_RESULT),
            create_real_entity_box("chair", "Cái ghế", scene_name="scene_001", color=COLOR_RESULT),
            create_real_entity_box("cup", "Cái ly", scene_name="scene_001", color=COLOR_RESULT),
            create_real_entity_box("person", "Con người", scene_name="scene_001", color=COLOR_USER)
        ).arrange(RIGHT, buff=0.6).scale(0.8).shift(DOWN*0.2)
        if objects.width > 12: objects.scale_to_fit_width(12)
        
        self.play(LaggedStart(*[FadeIn(obj, shift=UP*0.3) for obj in objects], lag_ratio=0.4), run_time=2.5)
        
        # Motion
        self.play(objects[3].animate.shift(RIGHT*1.0), run_time=0.8)
        self.play(objects[3].animate.shift(LEFT*1.0), run_time=0.8)
        
        sync_to(16.1)
        self.play(FadeOut(objects), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4: Dynamic Relations (21.5s - 29.5s)
        # Voice: "Quan trọng hơn, chúng ta còn hiểu các mối liên hệ động học... người đẩy cửa thì cửa mở, xe dừng lại khi đèn đỏ."
        # ---------------------------------------------------------
        rel1 = VGroup(
            create_real_entity_box("person", "Người đẩy", scene_name="scene_001", color=COLOR_USER),
            create_real_entity_box("door", "Cửa mở", scene_name="scene_001", color=COLOR_RESULT)
        ).arrange(RIGHT, buff=1.5).shift(UP*0.5).scale(0.8)
        arrow1 = create_flow_arrow(rel1[0], rel1[1])
        
        rel2 = VGroup(
            create_real_entity_box("traffic_light", "Đèn đỏ", scene_name="scene_001", color=COLOR_WARNING),
            create_real_entity_box("car", "Xe dừng", scene_name="scene_001", color=COLOR_USER)
        ).arrange(RIGHT, buff=1.5).shift(DOWN*1.8).scale(0.8)
        arrow2 = create_flow_arrow(rel2[0], rel2[1])
        
        self.play(FadeIn(rel1[0]), run_time=0.6)
        self.play(GrowArrow(arrow1), FadeIn(rel1[1]), run_time=0.8)
        self.play(FadeIn(rel2[0]), run_time=0.6)
        self.play(GrowArrow(arrow2), FadeIn(rel2[1]), run_time=0.8)
        
        sync_to(25.06)
        self.play(FadeOut(rel1), FadeOut(arrow1), FadeOut(rel2), FadeOut(arrow2), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 5: AI Starting Point (29.5s - 39.5s)
        # Voice: "Nhưng đối với AI, mọi thứ thường bắt đầu từ những điểm ảnh rời rạc... Sự chuyển đổi..."
        # ---------------------------------------------------------
        ai_brain = create_real_entity_box("robot", "AI System", scene_name="scene_001", color=COLOR_AI).shift(LEFT*3.5)
        numbers = VGroup(*[
            Text(str(np.random.randint(0, 255)), font_size=18, color=TEXT_WHITE)
            for _ in range(16)
        ]).arrange_in_grid(4, 4, buff=0.4)
        matrix = FlowchartBox(numbers, label_text="Ma trận số", color=COLOR_WARNING, pad_x=0.6, pad_y=0.6).shift(RIGHT*3)
        arrow_ai = create_flow_arrow(ai_brain, matrix)
        
        self.play(FadeIn(ai_brain), run_time=0.8)
        self.play(GrowArrow(arrow_ai), FadeIn(matrix), run_time=1.0)
        self.play(Indicate(matrix, color=COLOR_WARNING), run_time=1.2)
        
        sync_to(33.80)
        self.play(FadeOut(ai_brain), FadeOut(matrix), FadeOut(arrow_ai), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 6: Conclusion (39.5s - 52.1s)
        # Voice: "Làm thế nào để AI hiểu thế giới giống như con người? Cái nhìn của AI là một màn hình nhiễu loạn..."
        # ---------------------------------------------------------
        question = Text("Làm thế nào để AI hiểu thế giới như con người?", font_size=32, color=COLOR_MATH, weight=BOLD)
        self.play(Write(question), run_time=2.0)
        self.play(question.animate.to_edge(UP, buff=1.5).scale(0.8), run_time=1.0)
        
        final_flow = VGroup(
            create_real_entity_box("camera", "Camera (Pixels)", scene_name="scene_001", color=COLOR_WARNING),
            create_text_box("Thuật toán trích xuất biểu diễn", color=COLOR_AI, width=4.0),
            create_real_entity_box("world", "Không gian vật lý", scene_name="scene_001", color=COLOR_RESULT)
        ).arrange(RIGHT, buff=1.0).scale(0.8).shift(DOWN*0.5)
        if final_flow.width > 12: final_flow.scale_to_fit_width(12)
        f_arrows = VGroup(
            create_flow_arrow(final_flow[0], final_flow[1]),
            create_flow_arrow(final_flow[1], final_flow[2])
        )
        
        self.play(FadeIn(final_flow[0]), run_time=1.0)
        self.play(GrowArrow(f_arrows[0]), FadeIn(final_flow[1]), run_time=1.0)
        self.play(GrowArrow(f_arrows[1]), FadeIn(final_flow[2]), run_time=1.0)
        
        self.play(Indicate(final_flow[1], color=COLOR_AI), run_time=1.5)
        
        sync_to(52.152)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
