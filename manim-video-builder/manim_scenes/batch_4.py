from __future__ import annotations
from manim import *
import os
import sys
import numpy as np
import random

sys.path.append(os.path.dirname(__file__))
from visual_beats import *

class Batch4(Scene):
    def construct(self):
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        self.camera.background_color = BG_COLOR

        # --- START SCENE 020 ---

        # Audio
            
        # Total duration target: 30.888s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Các slot dẫn tới đồ thị nhân quả, dẫn tới kết quả dự đoán hành vi."
        # ---------------------------------------------------------
        title = safe_text("Tại sao Slot hỗ trợ Nhân quả?", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = safe_text("Slots -> Causal Graph -> Prediction", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Natural Synergy (4.0 - 12.0)
        # "Học theo trung tâm đối tượng và nhân quả hỗ trợ nhau rất tự nhiên..."
        # ---------------------------------------------------------
        slot1 = make_slot("Slot 1 (Ball)", color=GOLD_A).shift(LEFT * 3 + DOWN * 0.5)
        slot2 = make_slot("Slot 2 (Box)", color=ACCENT_COLOR).shift(RIGHT * 3 + DOWN * 0.5)
        
        self.play(FadeIn(slot1, shift=RIGHT), FadeIn(slot2, shift=LEFT), run_time=1.0)
        
        ball = make_ball().scale(0.8).next_to(slot1, UP, buff=0.3)
        box = make_box().scale(0.8).next_to(slot2, UP, buff=0.3)
        
        self.play(GrowFromCenter(ball), GrowFromCenter(box), run_time=1.0)
        self.wait(6.0) # Total: 12.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Entities over Pixels (12.0 - 20.0)
        # "Chúng ta không nói pích xơ này gây ra sự thay đổi cho pích xơ kia. Chúng ta nói quả bóng va vào chiếc hộp..."
        # ---------------------------------------------------------
        pixel_grid = Square(side_length=1.5, color=GREY_E, fill_opacity=0.1).shift(DOWN * 2)
        pixel_label = safe_text("No pixel-level causality", 18, RED).next_to(pixel_grid, DOWN)
        
        cross = Cross(pixel_grid, stroke_color=RED, stroke_width=6)
        
        causal_arrow = Arrow(slot1.get_right(), slot2.get_left(), color=GOLD_A, stroke_width=8)
        causal_label = safe_text("CAUSAL LINK", 20, GOLD_A, weight=BOLD).next_to(causal_arrow, UP)
        
        self.play(FadeIn(pixel_grid), Write(pixel_label), run_time=0.8)
        self.play(Create(cross), run_time=0.6)
        self.play(Create(causal_arrow), Write(causal_label), run_time=1.2)
        self.wait(5.4) # Total: 20.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Structural Foundation (20.0 - 30.888)
        # "Tách được các slot đối tượng giúp ta xác định đúng chủ thể tác động..."
        # ---------------------------------------------------------
        self.play(FadeOut(VGroup(pixel_grid, pixel_label, cross)), run_time=0.5)
        
        graph = VGroup(
            make_node("z_ball", GOLD_A).scale(0.8),
            Arrow(LEFT, RIGHT, color=WHITE),
            make_node("z_box", ACCENT_COLOR).scale(0.8)
        ).arrange(RIGHT, buff=0.5).shift(DOWN * 1.5)
        
        self.play(ReplacementTransform(VGroup(slot1, slot2).copy(), graph), run_time=1.5)
        self.play(Indicate(graph, color=GOLD_A), run_time=1.0)
        
        self.wait(7.888) # Total: 29.888s




        # --- END SCENE 020 ---


        # --- START SCENE 021 ---

        # Audio
            
        # Total duration target: 30.936s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # Title
        title = safe_text("Dịch chuyển phân phối & Tổng quát hóa", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Distribution Shift Definition (0.0 - 7.5s)
        # "Phân phối dữ liệu huấn luyện khác với phân phối dữ liệu thử nghiệm thực tế..."
        # ---------------------------------------------------------
        formula = MathTex("P_{train}(X, Y) \\neq P_{test}(X, Y)", font_size=54, color=GOLD_A).move_to(UP * 0.5)
        
        glow = formula.copy().set_stroke(GOLD_A, 8).set_opacity(0.3)
        
        self.play(Write(formula), FadeIn(glow), run_time=1.5)
        self.wait(5.5)
        
        self.play(FadeOut(VGroup(formula, glow)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Day vs Night Environment (7.5 - 16.5s)
        # "Ví dụ, xe tự lái học đi đường vào ban ngày nắng ráo..."
        # ---------------------------------------------------------
        # Left side: Day
        day_rect = RoundedRectangle(width=5.5, height=3.5, corner_radius=0.2, color=GOLD_A, fill_opacity=0.1).shift(LEFT * 3)
        sun = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8).move_to(day_rect.get_corner(UR) + LEFT * 0.5 + DOWN * 0.5)
        sun_glow = sun.copy().scale(1.5).set_opacity(0.2)
        car_day = make_car().scale(0.8).move_to(day_rect.get_center() + DOWN * 0.5)
        
        # Right side: Night/Rain
        night_rect = RoundedRectangle(width=5.5, height=3.5, corner_radius=0.2, color=ACCENT_COLOR, fill_opacity=0.1).shift(RIGHT * 3)
        moon = Circle(radius=0.25, color=WHITE, fill_opacity=0.7).move_to(night_rect.get_corner(UR) + LEFT * 0.5 + DOWN * 0.5)
        rain = VGroup(*[Line(ORIGIN, DOWN * 0.2 + LEFT * 0.05, color=BLUE_C, stroke_width=1).shift(
            RIGHT * (3 + np.random.uniform(-2, 2)) + UP * np.random.uniform(-1, 1)
        ) for _ in range(20)])
        car_night = make_car().scale(0.8).move_to(night_rect.get_center() + DOWN * 0.5)
        car_night.set_color(GREY_B)
        
        self.play(FadeIn(day_rect), FadeIn(VGroup(sun, sun_glow)), FadeIn(car_day), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(night_rect), FadeIn(moon), FadeIn(rain), FadeIn(car_night), run_time=1.0)
        self.wait(4.5) # Total: 16.0s
        
        self.play(FadeOut(VGroup(day_rect, sun, sun_glow, car_day, night_rect, moon, rain, car_night)), run_time=0.5) # Total: 16.5s

        # ---------------------------------------------------------
        # SEGMENT 3: Feature Change & Error (16.5 - 23.5s)
        # "Khi đó các đặc trưng pích xơ bề mặt thay đổi hoàn toàn..."
        # ---------------------------------------------------------
        pixels_day = VGroup(*[Square(0.4, fill_color=GOLD_A, fill_opacity=0.8, stroke_width=1) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.1).shift(LEFT * 3)
        pixels_night = VGroup(*[Square(0.4, fill_color=BLUE_E, fill_opacity=0.8, stroke_width=1) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.1).shift(RIGHT * 3)
        
        not_equal = MathTex("\\neq", font_size=72, color=RED).move_to(ORIGIN)
        warning = safe_text("CORRELATION FAIL", 32, RED, weight=BOLD).next_to(not_equal, DOWN, buff=0.8)
        
        self.play(FadeIn(pixels_day), FadeIn(pixels_night), run_time=1.0)
        self.play(Write(not_equal), run_time=0.8)
        self.play(FadeIn(warning, shift=UP*0.3), Flash(warning, color=RED), run_time=0.8)
        self.wait(3.9) # Total: 23.0s
        
        self.play(FadeOut(VGroup(pixels_day, pixels_night, not_equal, warning)), run_time=0.5) # Total: 23.5s

        # ---------------------------------------------------------
        # SEGMENT 4: Causal Invariance (23.5 - 30.936s)
        # "Nhưng các quy luật nhân quả vật lý vẫn giữ nguyên giá trị của chúng..."
        # ---------------------------------------------------------
        law_box = RoundedRectangle(width=8, height=2, corner_radius=0.2, color=TEAL, fill_opacity=0.2).shift(UP * 0.5)
        law_text = safe_text("CAUSAL INVARIANCE", 42, TEAL, weight=BOLD).move_to(law_box)
        
        car_final = make_car().scale(1.2).shift(LEFT * 4 + DOWN * 1.5)
        obstacle = make_person().scale(1.0).shift(RIGHT * 4 + DOWN * 1.5)
        
        self.play(FadeIn(law_box), Write(law_text), run_time=1.0)
        self.play(FadeIn(car_final), FadeIn(obstacle), run_time=0.8)
        self.play(car_final.animate.next_to(obstacle, LEFT, buff=1.0), run_time=2.5)
        self.play(Indicate(law_text, color=GOLD_A), run_time=1.0)
        
        self.wait(1.636) # Total: 30.436s




        # --- END SCENE 021 ---


        # --- START SCENE 022 ---

        # Audio
            
        # Total duration target: 31.224s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # Title
        title = safe_text("Sự tồn tại vĩnh viễn (Object Permanence)", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Concept Introduction (0.0 - 7.5s)
        # "Trẻ em học được một quy luật quan trọng gọi là sự tồn tại vĩnh viễn..."
        # ---------------------------------------------------------
        formula = safe_text("Object Permanence: z_t -> z_{t+1}", 36, GOLD_A).move_to(UP * 0.5)
        glow = formula.copy().set_stroke(GOLD_A, 8).set_opacity(0.3)
        
        self.play(Write(formula), FadeIn(glow), run_time=1.5)
        self.wait(5.5)
        
        self.play(FadeOut(VGroup(formula, glow)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Occlusion Demo (7.5 - 15.5s)
        # "Chúng ta vẫn hiểu quả bóng đang nằm sau tấm bìa và sẽ lăn ra ngoài..."
        # ---------------------------------------------------------
        ball = make_ball().scale(1.5).move_to(LEFT * 5 + DOWN * 1)
        wall = Rectangle(width=2.5, height=4, fill_color=GREY_E, fill_opacity=0.9, stroke_color=WHITE).move_to(ORIGIN + DOWN * 1)
        wall_text = safe_text("Obstacle", 24, WHITE).move_to(wall).rotate(PI/2)
        
        self.play(FadeIn(wall), Write(wall_text), FadeIn(ball), run_time=1.0)
        self.play(ball.animate.move_to(ORIGIN + DOWN * 1), run_time=2.0, rate_func=linear)
        
        # Ghost ball (Latent state)
        ghost_ball = ball.copy().set_opacity(0.3).set_stroke(ACCENT_COLOR, 4, opacity=0.5)
        latent_label = safe_text("Latent state z", 20, ACCENT_COLOR).next_to(ghost_ball, UP, buff=0.3)
        
        self.play(FadeIn(ghost_ball), FadeIn(latent_label), run_time=0.8)
        self.play(
            ghost_ball.animate.move_to(RIGHT * 4 + DOWN * 1),
            latent_label.animate.move_to(RIGHT * 4 + UP * 0.5 - DOWN * 1),
            run_time=2.5, rate_func=linear
        )
        self.wait(0.7) # Total: 15.0s
        self.play(FadeOut(VGroup(wall, wall_text, ghost_ball, latent_label)), run_time=0.5) # Total: 15.5s

        # ---------------------------------------------------------
        # SEGMENT 3: System Stability (15.5 - 23.5s)
        # "Điều này giúp hệ thống không bị mất dấu vật thể khi gặp chướng ngại vật..."
        # ---------------------------------------------------------
        robot = make_robot().scale(1.2).shift(LEFT * 3)
        tracking_line = DashedLine(robot.get_right(), ball.get_center(), color=ACCENT_COLOR)
        tracking_label = safe_text("Persistent Tracking", 24, ACCENT_COLOR).next_to(tracking_line, UP)
        
        self.play(FadeIn(robot, shift=RIGHT), run_time=0.8)
        self.play(Create(tracking_line), Write(tracking_label), run_time=1.0)
        self.play(ball.animate.move_to(RIGHT * 4 + DOWN * 1), run_time=2.5)
        self.play(Indicate(ball), run_time=1.0)
        self.wait(2.2) # Total: 23.0s
        
        self.play(FadeOut(VGroup(robot, tracking_line, tracking_label, ball)), run_time=0.5) # Total: 23.5s

        # ---------------------------------------------------------
        # SEGMENT 4: Neural Memory (23.5 - 31.224s)
        # "Khả năng theo dõi đối tượng ẩn đòi hỏi bộ nhớ tuần tự tinh vi..."
        # ---------------------------------------------------------
        memory_cells = VGroup(*[
            RoundedRectangle(width=1.2, height=0.8, corner_radius=0.1, color=GOLD_A, fill_opacity=0.2)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.4).move_to(UP * 0.5)
        
        labels = VGroup(*[safe_text(f"t-{i}", 18, TEXT_COLOR).move_to(memory_cells[3-i]) for i in range(4)])
        arrows = VGroup(*[Arrow(memory_cells[i].get_right(), memory_cells[i+1].get_left(), buff=0.1, color=GOLD_A) for i in range(3)])
        
        rnn_text = safe_text("Transformer / RNN Memory", 32, GOLD_A).next_to(memory_cells, DOWN, buff=1.0)
        
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.2) for c in memory_cells], lag_ratio=0.1), run_time=1.0)
        self.play(Create(arrows), Write(labels), run_time=1.2)
        self.play(Write(rnn_text), run_time=1.0)
        self.play(ShowPassingFlash(Underline(rnn_text, color=GOLD_A), run_time=1.0))
        
        self.wait(2.524) # Total: 30.724s




        # --- END SCENE 022 ---


        # --- START SCENE 023 ---

        # Audio
            
        # Total duration target: 33.936s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # Title
        title = safe_text("Mô hình thế giới (World Models)", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Brain Simulation (0.0 - 8.0s)
        # "Mô hình thế giới là một bộ não giả lập bên trong hệ thống trí tuệ nhân tạo..."
        # ---------------------------------------------------------
        formula = MathTex("s_{t+1} = \text{WorldModel}(s_t, a_t)", font_size=48, color=GOLD_A).move_to(UP * 0.5)
        glow = formula.copy().set_stroke(GOLD_A, 8).set_opacity(0.3)
        
        brain_outline = Circle(radius=1.5, color=ACCENT_COLOR, fill_opacity=0.1).shift(DOWN * 1)
        brain_glow = brain_outline.copy().set_stroke(ACCENT_COLOR, 12).set_opacity(0.2)
        
        self.play(Write(formula), FadeIn(glow), run_time=1.5)
        self.play(FadeIn(brain_outline), FadeIn(brain_glow), run_time=1.0)
        self.wait(5.0)
        
        self.play(FadeOut(VGroup(formula, glow, brain_outline, brain_glow)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Slot Prediction vs Pixels (8.0 - 16.0s)
        # "Thay vì dự đoán toàn bộ bức ảnh tiếp theo gồm hàng triệu điểm ảnh..."
        # ---------------------------------------------------------
        pixel_grid = VGroup(*[Square(0.3, fill_color=GREY_E, fill_opacity=0.5, stroke_width=0.5) for _ in range(36)]).arrange_in_grid(6, 6, buff=0.05).shift(LEFT * 3)
        red_x = Cross(pixel_grid, color=RED, stroke_width=8)
        
        slots = VGroup(*[
            RoundedRectangle(width=1.2, height=0.6, corner_radius=0.1, color=TEAL, fill_opacity=0.3)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.3).shift(RIGHT * 3)
        slot_labels = VGroup(*[safe_text(f"Slot {i+1}", 18, TEXT_COLOR).move_to(slots[i]) for i in range(3)])
        
        arrow = Arrow(pixel_grid.get_right(), slots.get_left(), color=GOLD_A)
        
        self.play(FadeIn(pixel_grid), run_time=0.8)
        self.play(Create(red_x), run_time=0.6)
        self.play(Create(arrow), FadeIn(slots), Write(slot_labels), run_time=1.2)
        self.wait(4.9) # Total: 15.5s
        
        self.play(FadeOut(VGroup(pixel_grid, red_x, arrow, slots, slot_labels)), run_time=0.5) # Total: 16.0s

        # ---------------------------------------------------------
        # SEGMENT 3: Robot Interaction Simulation (16.0 - 25.0s)
        # "Nó tự hỏi nếu robot đẩy nhẹ quả bóng, quả bóng sẽ lăn đến tọa độ nào..."
        # ---------------------------------------------------------
        robot = make_robot().scale(0.8).move_to(LEFT * 4 + DOWN * 1)
        ball = make_ball().scale(1.2).move_to(LEFT * 1.5 + DOWN * 1)
        
        self.play(FadeIn(robot), FadeIn(ball), run_time=0.8)
        
        # Thinking bubble
        thought_cloud = Circle(radius=1.8, color=WHITE, fill_opacity=0.05).set_stroke(WHITE, 2, opacity=0.3).shift(RIGHT * 3 + UP * 1)
        ghost_ball = ball.copy().set_opacity(0.3).move_to(thought_cloud.get_center() + LEFT * 1)
        path = Line(ghost_ball.get_center(), thought_cloud.get_center() + RIGHT * 1, color=YELLOW).set_stroke(width=2, opacity=0.5)
        
        self.play(FadeIn(thought_cloud), run_time=0.6)
        self.play(FadeIn(ghost_ball), Create(path), run_time=1.0)
        self.play(ghost_ball.animate.move_to(thought_cloud.get_center() + RIGHT * 1), run_time=2.0)
        
        self.play(robot.animate.next_to(ball, LEFT, buff=0.1), run_time=1.0)
        self.play(ball.animate.shift(RIGHT * 3), run_time=1.5)
        
        self.wait(2.1) # Total: 25.0s
        self.play(FadeOut(VGroup(robot, ball, thought_cloud, ghost_ball, path)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 4: Latent Space Rollout (25.0 - 33.936s)
        # "Việc triển khai các chuỗi tự hồi quy bên trong không gian ẩn..."
        # ---------------------------------------------------------
        latent_nodes = VGroup(*[
            Circle(radius=0.4, color=GOLD_A, fill_opacity=0.2)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.8).shift(UP * 0.5)
        
        rollout_arrows = VGroup(*[
            Arrow(latent_nodes[i].get_right(), latent_nodes[i+1].get_left(), buff=0.1, color=GOLD_A)
            for i in range(4)
        ])
        
        rollout_text = safe_text("Long-term Latent Rollout", 32, GOLD_A).next_to(latent_nodes, DOWN, buff=1.0)
        
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in latent_nodes], lag_ratio=0.1), run_time=1.5)
        self.play(LaggedStart(*[Create(a) for a in rollout_arrows], lag_ratio=0.2), run_time=1.5)
        self.play(Write(rollout_text), run_time=1.0)
        self.play(Indicate(latent_nodes[-1], color=TEAL), run_time=1.0)
        
        self.wait(3.436) # Total: 33.436s




        # --- END SCENE 023 ---


        # --- START SCENE 024 ---

        # Audio
            
        # Total duration target: 31.488s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # Title
        title = safe_text("Robot & Kế hoạch nhân quả", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Robotic Perception (0.0 - 8.0s)
        # "Trong ngành robot, robot cần hiểu rõ cấu trúc của môi trường xung quanh..."
        # ---------------------------------------------------------
        formula = safe_text("Perception -> Slots -> Causal Plan -> Action", 32, GOLD_A).move_to(UP * 0.5)
        glow = formula.copy().set_stroke(GOLD_A, 8).set_opacity(0.3)
        
        self.play(Write(formula), FadeIn(glow), run_time=1.5)
        self.wait(6.0)
        
        self.play(FadeOut(VGroup(formula, glow)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Scene Decomposition (8.0 - 16.0s)
        # "Trên bàn có thể có chiếc cốc thủy tinh và bình nước nóng..."
        # ---------------------------------------------------------
        table = make_table().scale(2.5).shift(DOWN * 1.5)
        cup = make_cup().scale(1.5).next_to(table, UP, buff=0).shift(LEFT * 1.5)
        kettle = RoundedRectangle(width=1.2, height=1.8, corner_radius=0.2, color=ACCENT_COLOR, fill_opacity=0.3).next_to(table, UP, buff=0).shift(RIGHT * 1.5)
        kettle_label = safe_text("Bình nước", 20, TEXT_COLOR).move_to(kettle)
        
        slot_box_1 = RoundedRectangle(width=1.5, height=2, corner_radius=0.1, color=GOLD_A, stroke_width=2).move_to(cup)
        slot_box_2 = RoundedRectangle(width=1.8, height=2.5, corner_radius=0.1, color=TEAL, stroke_width=2).move_to(kettle)
        
        self.play(FadeIn(table), FadeIn(cup), FadeIn(kettle), FadeIn(kettle_label), run_time=1.0)
        self.play(Create(slot_box_1), Create(slot_box_2), run_time=1.2)
        self.play(Indicate(slot_box_1), Indicate(slot_box_2), run_time=1.0)
        self.wait(4.3) # Total: 15.5s
        
        self.play(FadeOut(VGroup(slot_box_2, kettle, kettle_label)), run_time=0.5) # Total: 16.0s

        # ---------------------------------------------------------
        # SEGMENT 3: Causal Planning & Action (16.0 - 24.0s)
        # "Robot lên kế hoạch hành động an toàn dựa trên quy luật nhân quả đã học..."
        # ---------------------------------------------------------
        robot = make_robot().scale(1.0).shift(LEFT * 4 + UP * 1)
        warning_tag = safe_text("Dễ vỡ (Fragile)", 22, RED, weight=BOLD).next_to(cup, UP, buff=0.4)
        force_vector = Arrow(robot.get_right(), cup.get_left(), color=GOLD_A, buff=0.1)
        force_text = safe_text("Lực tối ưu", 20, GOLD_A).next_to(force_vector, UP)
        
        self.play(FadeIn(robot, shift=RIGHT), run_time=0.8)
        self.play(FadeIn(warning_tag, shift=DOWN*0.2), Flash(warning_tag, color=RED), run_time=1.0)
        self.play(Create(force_vector), Write(force_text), run_time=1.0)
        
        self.play(robot.animate.next_to(cup, LEFT, buff=0.1), run_time=1.5)
        self.play(VGroup(robot, cup, slot_box_1).animate.shift(UP * 2), run_time=1.5)
        
        self.wait(1.7) # Total: 23.5s
        self.play(FadeOut(VGroup(robot, cup, slot_box_1, table, warning_tag, force_vector, force_text)), run_time=0.5) # Total: 24.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Sample Efficiency (24.0 - 31.488s)
        # "Khả năng học tăng cường dựa trên mô hình này giảm đáng kể..."
        # ---------------------------------------------------------
        efficiency_graph = VGroup(
            Line(LEFT * 3 + DOWN * 1.5, LEFT * 3 + UP * 1.5, color=WHITE), # Y
            Line(LEFT * 3 + DOWN * 1.5, RIGHT * 3 + DOWN * 1.5, color=WHITE) # X
        )
        y_label = safe_text("Samples", 18, TEXT_COLOR).next_to(efficiency_graph[0], LEFT).rotate(PI/2)
        x_label = safe_text("Skill Mastery", 18, TEXT_COLOR).next_to(efficiency_graph[1], DOWN)
        
        curve_old = FunctionGraph(lambda x: 0.1 * (x+3)**2 - 1.5, x_range=[-3, 3], color=GREY_C).set_stroke(opacity=0.4)
        curve_new = FunctionGraph(lambda x: 0.3 * np.log(x+3.1) - 1.5, x_range=[-3, 3], color=GOLD_A).set_stroke(width=5)
        
        label_old = safe_text("Traditional RL", 16, GREY_C).move_to(RIGHT * 1.5 + UP * 1.0)
        label_new = safe_text("Model-based / Causal", 16, GOLD_A).move_to(RIGHT * 1.5 + DOWN * 0.5)
        
        self.play(Create(efficiency_graph), Write(VGroup(x_label, y_label)), run_time=1.0)
        self.play(Create(curve_old), Write(label_old), run_time=1.2)
        self.play(Create(curve_new), Write(label_new), run_time=1.2)
        self.play(Flash(label_new, color=GOLD_A), run_time=0.5)
        
        self.wait(3.088) # Total: 30.988s




        # --- END SCENE 024 ---


        # --- START SCENE 025 ---

        # Audio
            
        # Total duration target: 30.072s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # Title
        title = safe_text("Xe tự lái & Đồ thị nhân quả", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Complex Environment (0.0 - 8.0s)
        # "Xe tự lái hoạt động trong một môi trường vô cùng phức tạp và nguy hiểm..."
        # ---------------------------------------------------------
        road = VGroup(
            Line(LEFT * 7 + DOWN * 2, RIGHT * 7 + DOWN * 2, color=GREY_E),
            Line(LEFT * 7 + DOWN * 0, RIGHT * 7 + DOWN * 0, color=WHITE, stroke_width=2),
            Line(LEFT * 7 + UP * 2, RIGHT * 7 + UP * 2, color=GREY_E),
        )
        lane_markers = VGroup(*[
            DashedLine(LEFT * 7 + DOWN * 1, RIGHT * 7 + DOWN * 1, color=WHITE, dash_length=0.5)
        ])
        
        self.play(Create(road), Create(lane_markers), run_time=1.2)
        
        car_self = make_car().scale(1.0).move_to(LEFT * 4 + DOWN * 1)
        car_front = make_car().scale(1.0).move_to(RIGHT * 1 + DOWN * 1).set_color(BLUE_D)
        pedestrian = make_person().scale(0.8).move_to(RIGHT * 5 + UP * 1)
        
        self.play(FadeIn(car_self), FadeIn(car_front), FadeIn(pedestrian), run_time=1.0)
        self.wait(5.8)
        
        # ---------------------------------------------------------
        # SEGMENT 2: Relation Updates (8.0 - 16.0s)
        # "Hệ thống phải liên tục cập nhật mối quan hệ giữa các thực thể này..."
        # ---------------------------------------------------------
        # Highlight front car braking
        brake_glow = car_front[0].copy().set_color(RED).set_opacity(0.4).set_stroke(RED, 8)
        warning_arrow = Arrow(car_front.get_left(), car_self.get_right(), color=RED, buff=0.2)
        warning_text = safe_text("GIẢM TỐC", 20, RED, weight=BOLD).next_to(warning_arrow, UP)
        
        self.play(FadeIn(brake_glow), run_time=0.4)
        self.play(Create(warning_arrow), Write(warning_text), run_time=0.8)
        self.play(car_self.animate.shift(LEFT * 1), run_time=1.2) # Self car slows down
        
        self.wait(5.6) # Total: 16.0s
        self.play(FadeOut(VGroup(warning_arrow, warning_text, brake_glow)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 3: Causal Decision (16.0 - 24.0s)
        # "Hiểu chuỗi nhân quả giúp xe tự lái đưa ra quyết định chính xác kịp thời..."
        # ---------------------------------------------------------
        # Obstacle detection
        scan_cone = Polygon(
            car_self.get_right(),
            car_self.get_right() + RIGHT * 8 + UP * 2,
            car_self.get_right() + RIGHT * 8 + DOWN * 2,
            fill_color=ACCENT_COLOR, fill_opacity=0.1, stroke_width=0
        )
        
        causal_link = Arrow(pedestrian.get_left(), car_self.get_top(), color=GOLD_A, buff=0.1, path_arc=0.5)
        causal_label = safe_text("QUY LUẬT NHÂN QUẢ", 22, GOLD_A, weight=BOLD).move_to(UP * 2)
        
        self.play(FadeIn(scan_cone), run_time=0.8)
        self.play(Create(causal_link), Write(causal_label), run_time=1.0)
        self.play(car_self.animate.next_to(pedestrian, LEFT, buff=2.0).shift(DOWN * 2), run_time=2.5)
        self.play(Flash(car_self, color=RED), run_time=0.5)
        
        self.wait(2.7) # Total: 23.5s
        self.play(FadeOut(VGroup(scan_cone, causal_link, causal_label)), run_time=0.5) # Total: 24.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Noise Filtering (24.0 - 30.072s)
        # "Hệ thống tránh va chạm tích cực sử dụng mô hình nhân quả để lọc bỏ nhiễu..."
        # ---------------------------------------------------------
        noise_car = make_car().scale(0.8).move_to(LEFT * 2 + UP * 1.5).set_opacity(0.3)
        noise_text = safe_text("Nhiễu (Noise)", 18, GREY_B).next_to(noise_car, UP)
        
        filter_box = RoundedRectangle(width=4, height=1.5, corner_radius=0.1, color=TEAL, fill_opacity=0.2).move_to(UP * 1.5 + RIGHT * 3)
        filter_text = safe_text("CAUSAL FILTER", 24, TEAL, weight=BOLD).move_to(filter_box)
        
        self.play(FadeIn(noise_car), Write(noise_text), run_time=0.8)
        self.play(FadeIn(filter_box), Write(filter_text), run_time=1.0)
        
        # Noise filtered out
        self.play(
            noise_car.animate.set_opacity(0),
            noise_text.animate.set_opacity(0),
            run_time=1.2
        )
        self.play(Indicate(filter_box, color=GOLD_A), run_time=1.0)
        
        self.wait(1.572) # Total: 29.572s




        # --- END SCENE 025 ---


        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)