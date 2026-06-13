from __future__ import annotations
from manim import *
import os
import sys
import numpy as np
import random

sys.path.append(os.path.dirname(__file__))
from visual_beats import *

class Batch1(Scene):
    def construct(self):
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        self.camera.background_color = BG_COLOR

        # --- START SCENE 001 ---

        # Audio
            
        # Total duration target: 41.784s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (0.0 - 6.0)
        # "Pích xơ dẫn tới đối tượng, dẫn tới mối quan hệ, dẫn tới nguyên nhân, dẫn tới mô hình thế giới."
        # ---------------------------------------------------------
        title = safe_text("A I có thật sự hiểu thế giới không?", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        pipeline = make_global_pipeline().scale(0.8).move_to(DOWN * 0.5)
        
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(pipeline, shift=UP*0.3), run_time=1.5)
        
        # Highlight each step in the pipeline in sync with narration
        # Pixels -> Objects -> Relations -> Causes -> World Model
        steps = [0, 1, 2, 3, 4]
        for i in steps:
            self.play(Indicate(pipeline[i], color=GOLD_A, scale_factor=1.2), run_time=0.6)
        
        self.wait(0.5) # Total: 6.0s

        # ---------------------------------------------------------
        # SEGMENT 2: Human Perception (6.5 - 13.0)
        # "Khi chúng ta nhìn vào một căn phòng, chúng ta không thấy một ma trận pích xơ."
        # ---------------------------------------------------------
        person = make_person().scale(1.5).to_edge(LEFT, buff=1.5)
        pixel_grid = make_pixel_grid(8, 8, 0.3).to_edge(RIGHT, buff=1.5)
        cross = Cross(pixel_grid, stroke_color=RED, stroke_width=10)
        
        self.play(FadeIn(person, shift=RIGHT), run_time=1.0)
        self.play(FadeIn(pixel_grid, shift=LEFT), run_time=1.0)
        self.wait(1.0)
        self.play(Create(cross), run_time=0.8)
        self.wait(2.2) # Total: 12.5s
        

        # ---------------------------------------------------------
        # SEGMENT 3: Seeing Objects (13.0 - 20.0)
        # "Chúng ta thấy cái bàn, cái ghế, cái ly, con người và sự chuyển động."
        # ---------------------------------------------------------
        table = make_table().scale(1.2).shift(DOWN * 0.5)
        chair = make_chair().scale(1.2).next_to(table, LEFT, buff=0.5)
        cup = make_cup().scale(0.8).next_to(table, UP, buff=0)
        person_standing = make_person().scale(1.2).next_to(table, RIGHT, buff=0.5)
        
        room_objects = VGroup(chair, table, cup, person_standing).center()
        
        self.play(LaggedStart(*[FadeIn(obj, shift=UP*0.5) for obj in room_objects], lag_ratio=0.3), run_time=2.0)
        self.play(person_standing.animate.shift(RIGHT * 1.5), run_time=1.5) # Movement
        self.wait(3.0) # Total: 19.5s
        
        self.play(FadeOut(room_objects), run_time=0.5) # Total: 20.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Dynamic Relations (20.0 - 28.0)
        # "Quan trọng hơn, chúng ta còn hiểu các mối liên hệ động học... người đẩy cửa thì cửa mở, xe dừng lại khi đèn đỏ."
        # ---------------------------------------------------------
        door_scene = VGroup(make_person().scale(1.2), make_door().scale(1.2)).arrange(RIGHT, buff=0.5).shift(LEFT * 3 + UP * 0.5)
        car_scene = VGroup(make_car().scale(1.2), make_traffic_light().scale(1.2)).arrange(RIGHT, buff=1.0).shift(RIGHT * 3 + UP * 0.5)
        
        self.play(FadeIn(door_scene, shift=RIGHT), FadeIn(car_scene, shift=LEFT), run_time=1.2)
        
        # Interaction
        self.play(
            door_scene[0].animate.shift(RIGHT * 0.3),
            door_scene[1][0].animate.stretch(0.1, 0, about_edge=LEFT), # Door open
            car_scene[0].animate.shift(RIGHT * 0.5), # Car moving
            run_time=1.5
        )
        self.play(Flash(car_scene[1][2][0], color=RED, line_length=0.3), run_time=0.5) # Traffic light Red
        self.play(car_scene[0].animate.shift(RIGHT * 0.1), run_time=0.5) # Car stop
        
        self.wait(3.8) # Total: 27.5s

        # ---------------------------------------------------------
        # SEGMENT 5: AI Perspective (28.0 - 34.0)
        # "Nhưng đối với A I, mọi thứ thường bắt đầu từ những điểm ảnh rời rạc. Một bức ảnh chỉ là một ma trận số thô sơ và vô hồn."
        # ---------------------------------------------------------
        matrix_grid = make_pixel_grid(6, 10, 0.4).move_to(ORIGIN)
        numbers = VGroup()
        for cell in matrix_grid:
            val = str(random.randint(0, 255))
            num = safe_text(val, 14, TEXT_COLOR).move_to(cell)
            numbers.add(num)
            
        ai_matrix = VGroup(matrix_grid, numbers)
        
        self.play(FadeIn(matrix_grid), run_time=1.0)
        self.play(LaggedStart(*[Write(n) for n in numbers], lag_ratio=0.01), run_time=1.5)
        self.play(ai_matrix.animate.set_color(GREY), run_time=1.0) # Soulless
        
        self.wait(2.0) # Total: 33.5s
        self.play(FadeOut(ai_matrix), run_time=0.5) # Total: 34.0s

        # ---------------------------------------------------------
        # SEGMENT 6: Journey from Pixel to Object (34.0 - 41.784)
        # "Làm thế nào để A I có thể hiểu thế giới giống như con người chúng ta? ... sự chuyển đổi từ không gian vật lý sang ma trận điểm ảnh..."
        # ---------------------------------------------------------
        pixel_to_obj = VGroup(
            make_pixel_grid(4, 4, 0.4).shift(LEFT * 4),
            Arrow(LEFT * 2, RIGHT * 2, color=GOLD_A),
            make_person().scale(1.5).shift(RIGHT * 4)
        )
        
        self.play(FadeIn(pixel_to_obj[0]), run_time=0.8)
        self.play(Create(pixel_to_obj[1]), run_time=1.0)
        self.play(FadeIn(pixel_to_obj[2], shift=LEFT), run_time=1.0)
        
        self.play(Flash(pixel_to_obj[2], color=GOLD_A), run_time=0.8)
        
        self.wait(3.684) # Total: 41.284s




        # --- END SCENE 001 ---


        # --- START SCENE 002 ---

        # Audio
            
        # Total duration target: 38.688s
        # The title "Pixel không phải là thế giới" is NOT in narration, 
        # so we must start visuals immediately or keep title as a quick overlay.
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction to Tensor (Start: 0.0s)
        # "Ảnh X thuộc không gian số thực chiều H x W x C..."
        # ---------------------------------------------------------
        # Title as a silent overlay at the top
        title = safe_text("Pixel không phải là thế giới", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title) # Add immediately without wait
        
        formula = MathTex("X \in \mathbb{R}^{H \\times W \\times C}", font_size=48, color=GOLD_A).move_to(UP * 0.5)
        tensor_stack = make_tensor_stack().scale(1.2).next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(formula), run_time=1.2)
        self.play(FadeIn(tensor_stack, shift=UP*0.3), run_time=1.2)
        self.wait(3.1) # Total: 5.5s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Dimensions H, W, C (5.5 - 12.0)
        # ---------------------------------------------------------
        h_brace = Brace(tensor_stack[0][0], LEFT, color=TEXT_COLOR)
        w_brace = Brace(tensor_stack[0][0], DOWN, color=TEXT_COLOR)
        c_brace = Brace(tensor_stack[0], RIGHT, color=TEXT_COLOR)
        
        h_label = safe_text("H", 24, TEXT_COLOR).next_to(h_brace, LEFT)
        w_label = safe_text("W", 24, TEXT_COLOR).next_to(w_brace, DOWN)
        c_label = safe_text("C = 3", 24, GOLD_A).next_to(c_brace, RIGHT)
        
        self.play(Create(h_brace), Write(h_label), run_time=0.6)
        self.play(Create(w_brace), Write(w_label), run_time=0.6)
        self.play(Create(c_brace), Write(c_label), run_time=0.6)
        self.play(Indicate(tensor_stack), run_time=1.0)
        self.wait(3.7) # Total: 12.0s
        
        self.play(FadeOut(VGroup(formula, tensor_stack, h_brace, w_brace, c_brace, h_label, w_label, c_label)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3: Standard Representation (12.0 - 18.0)
        # "Về mặt kỹ thuật, đây là cách biểu diễn rất chuẩn để máy tính xử lý."
        # ---------------------------------------------------------
        robot = make_robot().scale(1.3).shift(LEFT * 3)
        data_cloud = VGroup(*[Dot(color=ACCENT_COLOR, radius=0.05).move_to(RIGHT * 3 + np.random.randn(3) * 0.7) for _ in range(20)])
        connections = VGroup(*[Line(robot.get_right(), d.get_center(), stroke_opacity=0.2, color=BLUE) for d in data_cloud])
        
        self.play(FadeIn(robot, shift=RIGHT), run_time=0.8)
        self.play(FadeIn(data_cloud), Create(connections), run_time=1.2)
        self.wait(3.5) # Total: 17.5s
        
        self.play(FadeOut(VGroup(robot, data_cloud, connections)), run_time=0.5) # Total: 18.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Camera & Light (18.0 - 26.0)
        # "Tuy nhiên, pixel không đại diện trực tiếp cho thế giới thực vật chất..."
        # ---------------------------------------------------------
        cam_box = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.1, color=WHITE, fill_opacity=0.2).shift(LEFT * 4)
        lens = Circle(radius=0.2, color=WHITE, fill_opacity=0.5).move_to(cam_box)
        camera = VGroup(cam_box, lens)
        
        physical_world = VGroup(
            make_ball().scale(1.0).shift(RIGHT * 3 + UP * 0.8),
            make_box().scale(1.0).shift(RIGHT * 4 + DOWN * 0.8)
        )
        
        self.play(FadeIn(camera, shift=RIGHT), FadeIn(physical_world, shift=LEFT), run_time=1.0)
        
        rays = VGroup(*[Line(obj.get_center(), camera.get_center(), stroke_width=2, color=YELLOW, stroke_opacity=0.4) for obj in physical_world])
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.1), run_time=1.2)
        self.play(Flash(camera, color=YELLOW), run_time=0.5)
        
        self.wait(4.8) # Total: 25.5s
        self.play(FadeOut(VGroup(camera, physical_world, rays)), run_time=0.5) # Total: 26.0s

        # ---------------------------------------------------------
        # SEGMENT 5: Human Perception (26.0 - 34.0)
        # "Con người luôn tự động gom các pixel lại thành các vật thể độc lập..."
        # ---------------------------------------------------------
        person = make_person().scale(1.3).shift(LEFT * 4)
        pixel_field = make_pixel_grid(7, 7, 0.4).shift(RIGHT * 2)
        
        self.play(FadeIn(person, shift=RIGHT), FadeIn(pixel_field), run_time=1.0)
        self.wait(1.0)
        
        obj1_pixels = VGroup(*[pixel_field[i] for i in [10,11,17,18]])
        obj2_pixels = VGroup(*[pixel_field[i] for i in [30,31,32,38,39,40]])
        
        ball_outline = Circle(radius=0.6, color=ORANGE, stroke_width=5).move_to(obj1_pixels)
        box_outline = Square(side_length=1.0, color=TEAL, stroke_width=5).move_to(obj2_pixels)
        
        self.play(Create(ball_outline), obj1_pixels.animate.set_color(ORANGE), run_time=1.0)
        self.play(Create(box_outline), obj2_pixels.animate.set_color(TEAL), run_time=1.0)
        self.wait(3.5) # Total: 33.5s
        
        self.play(FadeOut(VGroup(person, pixel_field, ball_outline, box_outline)), run_time=0.5) # Total: 34.0s

        # ---------------------------------------------------------
        # SEGMENT 6: ML Reconstruction (34.0 - 38.688)
        # ---------------------------------------------------------
        recon_field = make_pixel_grid(6, 10, 0.45).move_to(ORIGIN)
        scan_line = Line(recon_field.get_left(), recon_field.get_left() + UP * 2.5 + DOWN * 2.5, color=WHITE, stroke_width=4)
        scan_line.move_to(recon_field.get_left())
        
        self.play(FadeIn(recon_field), run_time=0.8)
        self.play(scan_line.animate.move_to(recon_field.get_right()), run_time=2.2, rate_func=linear)
        self.wait(1.188) # Total: 38.188s



        

        # --- END SCENE 002 ---


        # --- START SCENE 003 ---

        # Audio
            
        # Total duration target: 30.264s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction to Representation (0.0 - 6.0)
        # "Véc tơ dê bằng hàm ép chỉ số theta của ảnh ích. Để A I hiểu ảnh, ta biến ten xơ ích thành một véc tơ biểu diễn dê."
        # ---------------------------------------------------------
        title = safe_text("Representation là gì?", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        formula = MathTex("z = f_\\theta(X)", font_size=64, color=GOLD_A).move_to(ORIGIN)
        
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(formula, shift=UP*0.3), run_time=1.2)
        self.play(Flash(formula, color=GOLD_A), run_time=0.5)
        
        self.wait(2.5)
        self.play(FadeOut(formula), run_time=0.5) # Total: 5.5s

        # ---------------------------------------------------------
        # SEGMENT 2: Compression & Encoder (6.0 - 13.0)
        # "Véc tơ biểu diễn này nén thông tin ảnh thành dạng dễ xử lý hơn... chiếc máy nén thông tin..."
        # ---------------------------------------------------------
        image_input = make_pixel_grid(6, 6, 0.35).shift(LEFT * 4)
        encoder_box = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2, color=ACCENT_COLOR, fill_opacity=0.3).shift(LEFT * 0.5)
        encoder_text = safe_text("ENCODER", 24, ACCENT_COLOR, weight=BOLD).move_to(encoder_box)
        
        vector_z = VGroup(*[
            Rectangle(width=0.15, height=0.8, color=GOLD_A, fill_opacity=0.8) 
            for _ in range(12)
        ]).arrange(RIGHT, buff=0.08).shift(RIGHT * 3.5)
        
        z_label = safe_text("z (latent vector)", 20, GOLD_A).next_to(vector_z, UP)
        
        self.play(FadeIn(image_input, shift=RIGHT), run_time=1.0)
        self.play(Create(encoder_box), Write(encoder_text), run_time=1.0)
        
        # Stream pixels into encoder
        stream = VGroup(*[
            Dot(color=WHITE, radius=0.05).move_to(image_input.get_right())
            for _ in range(5)
        ])
        self.play(
            LaggedStart(*[
                s.animate.move_to(encoder_box.get_left()).set_opacity(0)
                for s in stream
            ], lag_ratio=0.1),
            run_time=1.2
        )
        
        self.play(ReplacementTransform(encoder_box.copy(), vector_z), Write(z_label), run_time=1.2)
        self.wait(1.1) # Total: 12.5s
        

        # ---------------------------------------------------------
        # SEGMENT 3: Car Example (13.0 - 22.0)
        # "Chuỗi số này chứa đựng những đặc trưng quan trọng nhất... ví dụ chiếc xe..."
        # ---------------------------------------------------------
        car = make_car().scale(2.0).shift(LEFT * 2)
        features = VGroup(
            safe_text("Shape (Hình dáng)", 24, GOLD_A),
            safe_text("Color (Màu sắc)", 24, BLUE),
            safe_text("Position (Vị trí)", 24, TEAL),
            safe_text("Motion (Chuyển động)", 24, ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT * 3)
        
        self.play(FadeIn(car, shift=RIGHT), run_time=1.0)
        self.play(LaggedStart(*[Write(f) for f in features], lag_ratio=0.5), run_time=3.0)
        
        # Movement demo
        self.play(car.animate.shift(RIGHT * 0.5), features[3].animate.scale(1.2).set_color(WHITE), run_time=1.0)
        self.play(features[3].animate.scale(1/1.2).set_color(ORANGE), run_time=0.5)
        
        self.wait(3.0) # Total: 21.5s

        # ---------------------------------------------------------
        # SEGMENT 4: CNN & Efficiency (22.0 - 30.264)
        # "Quá trình nén thông qua các tầng nơ ron chập giúp trích xuất các đặc trưng bất biến, giảm thiểu đáng kể chi phí tính toán."
        # ---------------------------------------------------------
        cnn_stack = VGroup(*[
            Rectangle(width=0.4, height=1.8, color=GREY, fill_opacity=0.4).shift(RIGHT * i * 0.3)
            for i in range(5)
        ]).center()
        
        scan_line = Line(cnn_stack.get_top(), cnn_stack.get_bottom(), color=WHITE, stroke_width=4).move_to(cnn_stack.get_left())
        
        cost_label = safe_text("Computation Cost", 24, RED).shift(DOWN * 2)
        down_arrow = Arrow(cost_label.get_right() + UP*0.2, cost_label.get_right() + DOWN*0.2, color=RED)
        
        self.play(FadeIn(cnn_stack), run_time=1.0)
        self.play(scan_line.animate.move_to(cnn_stack.get_right()), run_time=2.0, rate_func=linear)
        
        self.play(Write(cost_label), Create(down_arrow), run_time=1.0)
        self.play(Indicate(cnn_stack, color=GOLD_A), run_time=1.0)
        
        self.wait(2.764) # Total: 29.764s




        # --- END SCENE 003 ---


        # --- START SCENE 004 ---

        # Audio
            
        # Total duration target: 31.752s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Entangled Information (0.0 - 7.5)
        # "Véc tơ dê chứa thông tin trộn lẫn của xe hơi, người đi bộ và đèn giao thông... trong các mô hình cũ..."
        # ---------------------------------------------------------
        title = safe_text("Biểu diễn trộn lẫn (Entanglement)", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        
        # Central mixed vector
        mixed_circle = Circle(radius=2.2, color=WHITE, stroke_opacity=0.5, fill_opacity=0.1)
        mixed_formula = MathTex("z = [\\text{car, person, light, ...}]", color=GOLD_A).next_to(mixed_circle, DOWN)
        
        # Overlapping icons
        car = make_car().scale(0.9).move_to(mixed_circle.get_center() + UP*0.4 + LEFT*0.3)
        person = make_person().scale(0.9).move_to(mixed_circle.get_center() + DOWN*0.2 + RIGHT*0.4)
        light = make_traffic_light().scale(0.8).move_to(mixed_circle.get_center() + LEFT*0.5 + DOWN*0.4)
        
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(mixed_circle), FadeIn(VGroup(car, person, light)), run_time=1.5)
        self.play(Write(mixed_formula), run_time=1.0)
        
        self.wait(3.7) # Total: 7.0s
        self.play(FadeOut(mixed_formula), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Logic Difficulty (7.5 - 15.5)
        # "Sự trộn lẫn này khiến việc suy luận logic trở nên vô cùng khó khăn..."
        # ---------------------------------------------------------
        q_mark = safe_text("?", 140, RED, weight=BOLD).move_to(mixed_circle)
        
        self.play(Write(q_mark), run_time=1.0)
        # Shake effect to show confusion
        self.play(
            VGroup(mixed_circle, car, person, light).animate.shift(LEFT*0.1),
            run_time=0.1, rate_func=wiggle
        )
        self.play(
            VGroup(mixed_circle, car, person, light).animate.shift(RIGHT*0.2),
            run_time=0.1, rate_func=wiggle
        )
        
        logic_text = safe_text("Logic Reasoning Error!", 24, RED).next_to(mixed_circle, DOWN)
        self.play(Write(logic_text), run_time=1.0)
        
        self.wait(4.8)
        self.play(FadeOut(q_mark), FadeOut(logic_text), run_time=0.5) # Total: 15.0s

        # ---------------------------------------------------------
        # SEGMENT 3: Structured Representation (15.5 - 24.5)
        # "Để A I suy luận tốt, chúng ta cần một biểu diễn có cấu trúc rõ ràng... tách biệt thông tin..."
        # ---------------------------------------------------------
        slots = VGroup(
            make_slot("z_car", BLUE),
            make_slot("z_person", TEAL),
            make_slot("z_light", ORANGE)
        ).arrange(RIGHT, buff=1.0).center()
        
        icons = VGroup(
            make_car().scale(0.7).next_to(slots[0], DOWN),
            make_person().scale(0.7).next_to(slots[1], DOWN),
            make_traffic_light().scale(0.6).next_to(slots[2], DOWN)
        )
        
        self.play(LaggedStart(*[FadeIn(s, shift=UP*0.3) for s in slots], lag_ratio=0.3), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN*0.3) for i in icons], lag_ratio=0.3), run_time=1.5)
        
        # Relation arrow
        rel_arrow = Arrow(slots[0].get_right(), slots[2].get_left(), color=GOLD_A, buff=0.2)
        rel_label = safe_text("Interaction", 18, GOLD_A).next_to(rel_arrow, UP)
        
        self.play(Create(rel_arrow), Write(rel_label), run_time=1.0)
        
        self.wait(4.5) # Total: 24.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Decision Boundaries (24.5 - 31.752)
        # "Không gian biểu diễn ẩn bị rối khiến các thuật toán phân lớp truyền thống không thể vạch ra ranh giới quyết định chính xác."
        # ---------------------------------------------------------
        # Entangled dots
        dots_blue = VGroup(*[Dot(color=BLUE).move_to(np.random.randn(3) * 0.8 + LEFT*0.5) for _ in range(15)])
        dots_orange = VGroup(*[Dot(color=ORANGE).move_to(np.random.randn(3) * 0.8 + RIGHT*0.5) for _ in range(15)])
        
        boundary = DashedLine(UP*2.5, DOWN*2.5, color=RED, stroke_width=6)
        
        fail_text = safe_text("Failed Decision Boundary", 28, RED).to_edge(UP)
        
        self.play(FadeIn(dots_blue), FadeIn(dots_orange), run_time=1.0)
        self.play(Create(boundary), Write(fail_text), run_time=1.2)
        
        # Shake boundary
        self.play(boundary.animate.rotate(0.2), run_time=1.0)
        self.play(boundary.animate.rotate(-0.4), run_time=1.0)
        
        self.wait(3.052) # Total: 31.252s




        # --- END SCENE 004 ---


        # --- START SCENE 005 ---

        # Audio
            
        # Total duration target: 30.6s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Object Detection (0.0 - 7.5)
        # "Cảnh gồm tập hợp đối tượng một, đối tượng hai, cho đến đối tượng thứ ca... Nhiều người sẽ nghĩ đến bài toán phát hiện đối tượng..."
        # ---------------------------------------------------------
        title = safe_text("Từ Object Detection đến Object-Centric", 30, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        formula = MathTex("\\text{Scene} = \\{O_1, O_2, \\dots, O_K\\}", color=GOLD_A).next_to(title, DOWN, buff=0.5)
        
        traffic_scene = VGroup(
            make_car().scale(0.8).shift(LEFT*2.5 + DOWN*0.5),
            make_person().scale(0.8).shift(LEFT*0.5 + DOWN*0.8),
            make_car().scale(0.8).shift(RIGHT*1.5 + DOWN*0.4),
            make_person().scale(0.8).shift(RIGHT*3.5 + DOWN*0.7)
        )
        
        bboxes = VGroup(*[
            SurroundingRectangle(obj, color=RED, buff=0.1, stroke_width=2)
            for obj in traffic_scene
        ])
        
        self.play(Write(title), run_time=0.8)
        self.play(Write(formula), run_time=1.0)
        self.play(FadeIn(traffic_scene), run_time=1.0)
        self.play(Create(bboxes), run_time=1.0)
        
        self.wait(2.7) # Total: 6.5s
        self.play(FadeOut(formula), run_time=0.5) # Total: 7.0s

        # ---------------------------------------------------------
        # SEGMENT 2: Beyond Bounding Boxes (7.5 - 15.5)
        # "Bài toán này tìm vật thể và vẽ các khung chữ nhật quanh chúng. Nhưng học theo trung tâm đối tượng tiến xa hơn..."
        # ---------------------------------------------------------
        # Bboxes disappear, objects glow and highlight themselves
        self.play(FadeOut(bboxes), run_time=1.0)
        
        # Self-highlighting (Segmentation effect)
        glows = VGroup(*[
            obj.copy().set_style(stroke_width=6, stroke_color=GOLD_A, fill_opacity=0.3)
            for obj in traffic_scene
        ])
        
        self.play(LaggedStart(*[FadeIn(g) for g in glows], lag_ratio=0.2), run_time=1.5)
        self.play(VGroup(traffic_scene, glows).animate.scale(0.8).shift(UP*1.0), run_time=1.2)
        
        self.wait(3.8) # Total: 15.0s
        self.play(FadeOut(glows), run_time=0.5) # Total: 15.5s

        # ---------------------------------------------------------
        # SEGMENT 3: Unsupervised Decomposition (15.5 - 24.5)
        # "Phương pháp này không cần con người gắn nhãn trước cho dữ liệu... tự động phân chia toàn bộ cảnh..."
        # ---------------------------------------------------------
        no_labels = safe_text("NO MANUAL LABELS", 32, RED, weight=BOLD).move_to(DOWN * 2.5)
        cross = Cross(no_labels, stroke_color=RED)
        
        self.play(Write(no_labels), run_time=0.8)
        self.play(Create(cross), run_time=0.8)
        
        # Objects separate into slots
        slots = VGroup(*[
            make_slot(f"Slot {i+1}", [BLUE, TEAL, ORANGE, GOLD_A][i])
            for i in range(4)
        ]).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.5)
        
        self.play(
            LaggedStart(*[
                traffic_scene[i].animate.scale(0.6).move_to(slots[i].get_center())
                for i in range(4)
            ], lag_ratio=0.2),
            FadeIn(slots),
            run_time=2.0
        )
        
        self.wait(4.4) # Total: 24.0s
        self.play(FadeOut(no_labels), FadeOut(cross), run_time=0.5) # Total: 24.5s

        # ---------------------------------------------------------
        # SEGMENT 4: New Era of AI Perception (24.5 - 30.6)
        # "A I sẽ học cách biểu diễn từng vật thể mà không cần giám sát... mở ra kỷ nguyên mới..."
        # ---------------------------------------------------------
        robot = make_robot().scale(1.5).move_to(UP * 0.5)
        
        sparkles = VGroup(*[
            Star(color=GOLD_A, outer_radius=0.1).move_to(robot.get_center() + np.random.randn(3)*1.0)
            for _ in range(8)
        ])
        
        self.play(FadeIn(robot, shift=UP), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in sparkles], lag_ratio=0.1), run_time=1.0)
        
        era_text = safe_text("UNSUPERVISED DISCOVERY", 24, GOLD_A).next_to(robot, UP)
        self.play(Write(era_text), run_time=0.8)
        
        self.play(Indicate(robot, color=GOLD_A), run_time=1.0)
        
        self.wait(1.8) # Total: 30.1s




        # --- END SCENE 005 ---


        # --- START SCENE 006 ---

        # Audio
            
        # Total duration target: 31.776s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction to Slots (0.0 - 7.5)
        # "Tập hợp dê bằng các phần tử dê một, dê hai, cho đến dê ca... khái niệm cốt lõi là các slot."
        # ---------------------------------------------------------
        title = safe_text("Object Slots", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        formula = MathTex("Z = \\{z_1, z_2, \\dots, z_K\\}", color=GOLD_A).next_to(title, DOWN, buff=0.5)
        
        slots_bg = VGroup(*[
            RoundedRectangle(width=1.5, height=1.0, corner_radius=0.15, color=GREY, stroke_opacity=0.3)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.5)
        
        self.play(Write(title), run_time=0.8)
        self.play(Write(formula), run_time=1.0)
        self.play(FadeIn(slots_bg, shift=UP), run_time=1.0)
        
        self.wait(4.2) # Total: 7.0s
        self.play(FadeOut(formula), run_time=0.5) # Total: 7.5s

        # ---------------------------------------------------------
        # SEGMENT 2: Trays Concept (7.5 - 15.5)
        # "Tưởng tượng mỗi slot là một chiếc khay chứa thông tin... bóng và hộp..."
        # ---------------------------------------------------------
        # Real slots (trays)
        slot1 = make_slot("Slot 1", BLUE).move_to(slots_bg[0])
        slot2 = make_slot("Slot 2", TEAL).move_to(slots_bg[1])
        
        ball = make_ball().scale(1.2).shift(UP * 2 + LEFT * 1)
        box = make_box().scale(1.2).shift(UP * 2 + RIGHT * 1)
        
        self.play(FadeIn(ball, shift=DOWN), FadeIn(box, shift=DOWN), run_time=1.2)
        
        self.play(
            ball.animate.move_to(slot1.get_center()).scale(0.5),
            FadeIn(slot1),
            run_time=1.5
        )
        self.play(
            box.animate.move_to(slot2.get_center()).scale(0.5),
            FadeIn(slot2),
            run_time=1.5
        )
        
        self.wait(1.8) # Total: 15.0s
        self.play(FadeOut(slots_bg[2:]), run_time=0.5) # Total: 15.5s

        # ---------------------------------------------------------
        # SEGMENT 3: Permutation Invariance Demo (15.5 - 24.5)
        # "Thứ tự của các slot không quan trọng... khay thứ nhất có thể là quả bóng hoặc chiếc hộp..."
        # ---------------------------------------------------------
        # Swap slots
        self.play(
            VGroup(slot1, ball).animate.move_to(slot2.get_center()),
            VGroup(slot2, box).animate.move_to(slot1.get_center()),
            run_time=2.5,
            path_arc=PI/2
        )
        
        # Glow the swapped state
        self.play(Flash(slot1, color=GOLD_A), Flash(slot2, color=GOLD_A), run_time=1.0)
        
        self.wait(5.5) # Total: 24.5s

        # ---------------------------------------------------------
        # SEGMENT 4: Permutation Invariance Concept (24.5 - 31.776)
        # "Đặc tính bất biến với hoán vị... kiến trúc mạng nơ ron không phụ thuộc vào thứ tự..."
        # ---------------------------------------------------------
        invariance_text = safe_text("PERMUTATION INVARIANCE", 28, GOLD_A, weight=BOLD).to_edge(UP)
        
        # Neural network abstract representation
        nn_nodes = VGroup(*[Circle(radius=0.15, color=WHITE) for _ in range(6)]).arrange(DOWN, buff=0.2).shift(RIGHT * 3)
        links = VGroup(*[
            Line(slot1.get_right(), node.get_left(), stroke_width=1, stroke_opacity=0.3)
            for node in nn_nodes
        ] + [
            Line(slot2.get_right(), node.get_left(), stroke_width=1, stroke_opacity=0.3)
            for node in nn_nodes
        ])
        
        self.play(Write(invariance_text), run_time=0.8)
        self.play(FadeIn(nn_nodes), Create(links), run_time=1.5)
        
        # Final highlight
        self.play(Indicate(invariance_text, color=GOLD_A, scale_factor=1.1), run_time=1.2)
        
        self.wait(3.776) # Total: 31.276s




        # --- END SCENE 006 ---


        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)