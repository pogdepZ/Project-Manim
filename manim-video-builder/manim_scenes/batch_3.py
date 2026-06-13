from __future__ import annotations
from manim import *
import os
import sys
import numpy as np
import random

sys.path.append(os.path.dirname(__file__))
from visual_beats import *

class Batch3(Scene):
    def construct(self):
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        self.camera.background_color = BG_COLOR

        # --- START SCENE 013 ---

        # Audio
            
        # Total duration target: 29.592s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Mối quan hệ chỉ số i j bằng hàm rê của véc tơ dê i và véc tơ dê j."
        # ---------------------------------------------------------
        title = safe_text("Học quan hệ giữa các đối tượng", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = MathTex(r"r_{ij} = g(z_i, z_j)", font_size=48, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Objects in space (4.0 - 12.0)
        # "Sau khi tách được các đối tượng đơn lẻ, chúng ta cần học mối quan hệ..."
        # ---------------------------------------------------------
        ball = make_ball().scale(1.2).shift(LEFT * 4 + UP * 1.5)
        box = make_box().scale(1.2).shift(ORIGIN + UP * 0.5)
        table = make_table().scale(1.5).shift(RIGHT * 4 + DOWN * 0.5)
        
        self.play(FadeIn(ball, shift=DOWN), run_time=0.8)
        self.play(FadeIn(box, shift=UP), run_time=0.8)
        self.play(FadeIn(table, shift=LEFT), run_time=1.0)
        self.wait(5.4) # Total: 12.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Relation learning (12.0 - 20.0)
        # "Thế giới không phải là những vật thể nằm tách biệt vô nghĩa. Chúng ta học hàm rê..."
        # ---------------------------------------------------------
        rel1 = Line(ball.get_center(), box.get_center(), color=GOLD_A, stroke_width=4)
        rel2 = Line(box.get_center(), table.get_top(), color=ACCENT_COLOR, stroke_width=4)
        
        label1 = safe_text("On top of?", 20, GOLD_A).next_to(rel1.get_center(), UP, buff=0.2)
        label2 = safe_text("Placed on?", 20, ACCENT_COLOR).next_to(rel2.get_center(), RIGHT, buff=0.2)
        
        self.play(Create(rel1), Write(label1), run_time=1.0)
        self.play(Create(rel2), Write(label2), run_time=1.0)
        self.wait(5.5)
        self.play(FadeOut(label1), FadeOut(label2), run_time=0.5) # Total: 20.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Structural context (20.0 - 29.592)
        # "Các mối quan hệ này tạo nên cấu trúc ngữ nghĩa cho toàn cảnh... GNN..."
        # ---------------------------------------------------------
        graph_nodes = VGroup(
            make_node("z_1", GOLD_A).scale(0.6).shift(DOWN * 2 + LEFT * 3),
            make_node("z_2", ACCENT_COLOR).scale(0.6).shift(DOWN * 2),
            make_node("z_3", TEAL).scale(0.6).shift(DOWN * 2 + RIGHT * 3)
        )
        graph_edges = VGroup(
            Arrow(graph_nodes[0].get_right(), graph_nodes[1].get_left(), color=WHITE, buff=0.1),
            Arrow(graph_nodes[1].get_right(), graph_nodes[2].get_left(), color=WHITE, buff=0.1)
        )
        
        self.play(FadeIn(graph_nodes), run_time=1.2)
        self.play(Create(graph_edges), run_time=1.0)
        self.play(Indicate(graph_nodes, color=GOLD_A), run_time=1.0)
        
        self.wait(5.392) # Total: 28.592s




        # --- END SCENE 013 ---


        # --- START SCENE 014 ---

        # Audio
            
        # Total duration target: 29.496s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Xác suất của biến cố y khi biết biến cố ích."
        # ---------------------------------------------------------
        title = safe_text("Tương quan thống kê và hạn chế", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = MathTex(r"P(Y | X)", font_size=54, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Observation (4.0 - 12.0)
        # "Hầu hết các mô hình trí tuệ nhân tạo hiện nay chỉ học tương quan thống kê..."
        # ---------------------------------------------------------
        ball = make_ball().scale(1.2).shift(LEFT * 4 + DOWN * 0.5)
        box = make_box().scale(1.2).shift(LEFT * 1 + DOWN * 0.5)
        
        observation_label = safe_text("Observation", 24, TEXT_COLOR).next_to(box, UP, buff=1.0)
        
        self.play(FadeIn(ball), FadeIn(box), Write(observation_label), run_time=1.0)
        
        # Move ball to box, then box moves
        self.play(ball.animate.next_to(box, LEFT, buff=0.1), run_time=1.5)
        self.play(box.animate.shift(RIGHT * 2), run_time=1.0)
        self.wait(3.5) # Total: 12.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Correlation Memory (12.0 - 20.0)
        # "Mô hình sẽ ghi nhớ mối tương quan bóng gần hộp thì hộp chuyển động..."
        # ---------------------------------------------------------
        memory_box = RoundedRectangle(width=3, height=2, corner_radius=0.2, color=ACCENT_COLOR, fill_opacity=0.2).shift(RIGHT * 3 + UP * 1.5)
        memory_text = safe_text("If Ball near Box\nThen Box moves", 20, TEXT_COLOR).move_to(memory_box)
        
        arrow = Arrow(box.get_top(), memory_box.get_bottom(), color=GOLD_A)
        
        self.play(Create(arrow), FadeIn(memory_box), Write(memory_text), run_time=1.2)
        self.play(Indicate(memory_box, color=GOLD_A), run_time=1.0)
        self.wait(5.8) # Total: 20.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Spurious Correlation (20.0 - 29.496)
        # "Nhưng tương quan này có thể bị sai... robot ẩn đẩy..."
        # ---------------------------------------------------------
        hidden_robot = make_robot().scale(0.8).set_opacity(0.3).move_to(box.get_center() + RIGHT * 1.5)
        
        question_mark = safe_text("?", 60, RED, weight=BOLD).next_to(memory_box, DOWN)
        
        self.play(FadeIn(hidden_robot), run_time=1.0)
        self.play(hidden_robot.animate.next_to(box, RIGHT, buff=0.1), run_time=1.0)
        self.play(box.animate.shift(LEFT * 1), run_time=0.8) # Robot "pushes" box
        self.play(Write(question_mark), run_time=0.5)
        
        self.wait(5.196) # Total: 28.496s




        # --- END SCENE 014 ---


        # --- START SCENE 015 ---

        # Audio
            
        # Total duration target: 30.48s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Xác suất của biến cố y khi thực hiện can thiệp ích nhận giá trị ích nhỏ."
        # ---------------------------------------------------------
        title = safe_text("Nhân quả: Sự can thiệp", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = MathTex(r"P(Y | do(X = x))", font_size=54, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Deep Question (4.0 - 12.0)
        # "Nhân quả đặt ra một câu hỏi sâu sắc hơn rất nhiều. Nếu chúng ta chủ động can thiệp vào ích..."
        # ---------------------------------------------------------
        question = safe_text("What if we INTERVENE?", 28, TEXT_COLOR).next_to(formula, DOWN, buff=0.5)
        
        do_op = safe_text("do(X)", 48, ORANGE, weight=BOLD).move_to(ORIGIN)
        glow_circle = Circle(radius=1.2, color=ORANGE, stroke_width=8).move_to(do_op)
        
        self.play(Write(question), run_time=1.0)
        self.play(FadeIn(glow_circle, scale=0.5), FadeIn(do_op, scale=0.5), run_time=1.2)
        self.wait(5.8) # Total: 12.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Active Interaction (12.0 - 22.0)
        # "Trong lý thuyết nhân quả, chúng ta sử dụng ký hiệu toán học do. Nó biểu thị một hành động..."
        # ---------------------------------------------------------
        self.play(FadeOut(VGroup(question, do_op, glow_circle)), run_time=0.5)
        
        ball = make_ball().scale(1.2).shift(LEFT * 4 + DOWN * 1.0)
        box = make_box().scale(1.2).shift(RIGHT * 1 + DOWN * 1.0)
        
        hand = make_person().scale(0.8).next_to(ball, LEFT, buff=0.5).set_color(GOLD_A)
        
        self.play(FadeIn(ball), FadeIn(box), run_time=0.8)
        self.play(FadeIn(hand, shift=RIGHT), run_time=1.0)
        
        # Intervention: hand pushes ball
        self.play(hand.animate.next_to(ball, LEFT, buff=0.0), run_time=0.5)
        self.play(
            hand.animate.shift(RIGHT * 4),
            ball.animate.shift(RIGHT * 4),
            run_time=1.5,
            rate_func=rate_functions.ease_in_sine
        )
        
        # Impact
        collision_flash = Flash(box.get_left(), color=ORANGE, line_length=0.4)
        self.play(
            box.animate.shift(RIGHT * 2),
            ball.animate.shift(LEFT * 0.5),
            collision_flash,
            run_time=0.8,
            rate_func=rate_functions.ease_out_sine
        )
        self.wait(4.9) # Total: 22.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Understanding System (22.0 - 30.48)
        # "Sự can thiệp này giúp phân biệt tương quan và nguyên nhân thực sự..."
        # ---------------------------------------------------------
        causal_link = Arrow(ball.get_center(), box.get_center(), color=GOLD_A, buff=0.2)
        causal_label = safe_text("TRUE CAUSE", 24, GOLD_A, weight=BOLD).next_to(causal_link, UP)
        
        self.play(Create(causal_link), Write(causal_label), run_time=1.2)
        self.play(Indicate(causal_label, color=GOLD_A), run_time=1.0)
        
        self.wait(5.28) # Total: 29.48s




        # --- END SCENE 015 ---


        # --- START SCENE 016 ---

        # Audio
            
        # Total duration target: 30.168s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Sự khác biệt giữa việc quan sát thụ động và can thiệp chủ động."
        # ---------------------------------------------------------
        title = safe_text("Sức mạnh của hành động can thiệp", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        header = safe_text("Observation vs Intervention", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(header), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(header), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Passive Observation (4.0 - 12.0)
        # "Quan sát thụ động giống như việc chúng ta ngồi nhìn dòng xe cộ chạy..."
        # ---------------------------------------------------------
        obs_bg = Rectangle(width=5.5, height=3.5, color=GREY_E, fill_opacity=0.1).shift(LEFT * 3.2 + DOWN * 1.0)
        obs_label = safe_text("Passive Observation", 22, TEXT_COLOR).next_to(obs_bg, UP)
        
        person_watching = make_person().scale(1.0).move_to(obs_bg.get_left() + RIGHT * 0.8 + DOWN * 0.5)
        cars = VGroup(*[make_car().scale(0.6).shift(LEFT * 2.5 + RIGHT * i * 1.5 + DOWN * 1.2) for i in range(3)])
        
        self.play(FadeIn(obs_bg), Write(obs_label), run_time=0.8)
        self.play(FadeIn(person_watching), run_time=0.8)
        self.play(LaggedStart(*[c.animate.shift(RIGHT * 6) for c in cars], lag_ratio=0.5), run_time=4.0, rate_func=linear)
        self.wait(2.4) # Total: 12.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Active Intervention (12.0 - 20.0)
        # "Can thiệp chủ động giống như ta đặt thêm một biển báo dừng xe..."
        # ---------------------------------------------------------
        int_bg = Rectangle(width=5.5, height=3.5, color=ACCENT_COLOR, fill_opacity=0.1).shift(RIGHT * 3.2 + DOWN * 1.0)
        int_label = safe_text("Active Intervention", 22, ACCENT_COLOR).next_to(int_bg, UP)
        
        person_acting = make_person().scale(1.0).move_to(int_bg.get_left() + RIGHT * 0.8 + DOWN * 0.5).set_color(GOLD_A)
        stop_sign = make_traffic_light().scale(0.8).move_to(int_bg.get_center() + RIGHT * 1.0 + DOWN * 0.5)
        
        self.play(FadeIn(int_bg), Write(int_label), run_time=0.8)
        self.play(FadeIn(person_acting), run_time=0.8)
        self.play(person_acting.animate.next_to(stop_sign, LEFT, buff=0.2), FadeIn(stop_sign, shift=UP), run_time=1.5)
        
        intervened_car = make_car().scale(0.6).move_to(int_bg.get_left() + RIGHT * 0.5 + DOWN * 1.2)
        self.play(intervened_car.animate.next_to(stop_sign, LEFT, buff=0.2), run_time=2.0)
        self.play(Flash(stop_sign, color=RED), run_time=0.5)
        self.wait(2.4) # Total: 20.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Breaking Spurious Correlations (20.0 - 30.168)
        # "Can thiệp giúp ta phá vỡ các mối tương quan giả tạo... chìa khóa trí thông minh thực sự..."
        # ---------------------------------------------------------
        self.play(FadeOut(VGroup(obs_bg, obs_label, person_watching, cars)), run_time=0.5)
        self.play(int_bg.animate.center().scale(1.2), int_label.animate.center().shift(UP * 2.5), run_time=1.0)
        
        causal_graph = VGroup(
            make_robot().scale(0.8).shift(LEFT * 2),
            Arrow(LEFT * 1.5, RIGHT * 1.5, color=GOLD_A),
            safe_text("Decisions", 24, GOLD_A).shift(RIGHT * 2.5)
        ).shift(DOWN * 1.0)
        
        self.play(FadeIn(causal_graph), run_time=1.2)
        self.play(Indicate(causal_graph, color=GOLD_A), run_time=1.0)
        
        self.wait(5.968) # Total: 29.168s




        # --- END SCENE 016 ---


        # --- START SCENE 017 ---

        # Audio
            
        # Total duration target: 30.288s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Biến ích chỉ số i bằng hàm ép chỉ số i của các biến cha chỉ số i và nhiễu u chỉ số i."
        # ---------------------------------------------------------
        title = safe_text("Mô hình nhân quả cấu trúc (SCM)", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = MathTex(r"X_i = f_i(PA_i, U_i)", font_size=54, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(3.8) # Total: 5.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Components (5.0 - 13.0)
        # "Mô hình nhân quả cấu trúc S C M mô tả thế giới qua các phương trình..."
        # ---------------------------------------------------------
        pa_label = safe_text("PA_i: Direct Causes (Parents)", 22, ACCENT_COLOR).shift(LEFT * 3 + DOWN * 1.5)
        u_label = safe_text("U_i: Exogenous Noise", 22, MAROON_B).shift(RIGHT * 3 + DOWN * 1.5)
        
        pa_arrow = Arrow(pa_label.get_top(), formula[0][5:8], color=ACCENT_COLOR) # points to PA_i
        u_arrow = Arrow(u_label.get_top(), formula[0][9:11], color=MAROON_B) # points to U_i
        
        self.play(FadeIn(pa_label, shift=UP), Create(pa_arrow), run_time=1.0)
        self.play(FadeIn(u_label, shift=UP), Create(u_arrow), run_time=1.0)
        self.wait(6.0) # Total: 13.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Graph Structure (13.0 - 22.0)
        # "Mô hình này giúp ta biểu diễn chính xác cơ chế vận hành của tự nhiên..."
        # ---------------------------------------------------------
        self.play(FadeOut(VGroup(pa_label, u_label, pa_arrow, u_arrow, formula)), run_time=0.5)
        
        nodes = VGroup(
            make_node("X_1", BLUE_C).shift(LEFT * 2 + UP * 1),
            make_node("X_2", BLUE_C).shift(RIGHT * 2 + UP * 1),
            make_node("X_3", GOLD_A).shift(DOWN * 1.5)
        )
        
        u_nodes = VGroup(
            make_node("U_1", MAROON_B).scale(0.5).next_to(nodes[0], LEFT, buff=0.5),
            make_node("U_2", MAROON_B).scale(0.5).next_to(nodes[1], RIGHT, buff=0.5),
            make_node("U_3", MAROON_B).scale(0.5).next_to(nodes[2], DOWN, buff=0.5)
        )
        
        edges = VGroup(
            Arrow(nodes[0].get_bottom(), nodes[2].get_top(), color=WHITE, buff=0.1),
            Arrow(nodes[1].get_bottom(), nodes[2].get_top(), color=WHITE, buff=0.1),
            DashedLine(u_nodes[0].get_right(), nodes[0].get_left(), color=MAROON_B),
            DashedLine(u_nodes[1].get_left(), nodes[1].get_right(), color=MAROON_B),
            DashedLine(u_nodes[2].get_top(), nodes[2].get_bottom(), color=MAROON_B)
        )
        
        self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.2), run_time=1.2)
        self.play(Create(edges), FadeIn(u_nodes), run_time=1.5)
        self.wait(5.8) # Total: 22.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Predictions (22.0 - 30.288)
        # "Khi xác định được đồ thị nhân quả cấu trúc, chúng ta có thể phân tích sự can thiệp..."
        # ---------------------------------------------------------
        self.play(Indicate(nodes[2], color=GOLD_A), run_time=1.0)
        prediction_text = safe_text("Predicting Interventions", 24, GOLD_A).next_to(nodes[2], RIGHT, buff=1.0)
        self.play(Write(prediction_text), run_time=1.0)
        
        self.wait(5.288) # Total: 29.288s




        # --- END SCENE 017 ---


        # --- START SCENE 018 ---

        # Audio
            
        # Total duration target: 29.784s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Đồ thị va chạm gồm bóng tác động lực dẫn tới hộp chuyển động."
        # ---------------------------------------------------------
        title = safe_text("Ví dụ vật lý: Va chạm", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = safe_text("Ball -> Force -> Box", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Setup (4.0 - 10.0)
        # "Chúng ta hãy phân tích một ví dụ vật lý vô cùng trực quan..."
        # ---------------------------------------------------------
        ground = Line(LEFT * 5, RIGHT * 5, color=GREY_E).shift(DOWN * 1.5)
        ball = make_ball().scale(1.2).next_to(ground, UP, buff=0).shift(LEFT * 4)
        box = make_box().scale(1.2).next_to(ground, UP, buff=0).shift(RIGHT * 1)
        
        self.play(Create(ground), run_time=0.8)
        self.play(FadeIn(ball, shift=RIGHT), FadeIn(box, shift=LEFT), run_time=1.2)
        self.wait(4.0) # Total: 10.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Collision (10.0 - 20.0)
        # "Vận tốc của quả bóng chính là nguyên nhân trực tiếp tạo ra lực va chạm..."
        # ---------------------------------------------------------
        vel_arrow = Arrow(ball.get_left(), ball.get_right(), color=GOLD_A).next_to(ball, UP)
        vel_label = safe_text("Velocity", 18, GOLD_A).next_to(vel_arrow, UP)
        
        self.play(Create(vel_arrow), Write(vel_label), run_time=0.8)
        
        # Animation: ball moves to box
        self.play(
            ball.animate.next_to(box, LEFT, buff=0),
            vel_arrow.animate.next_to(box, LEFT, buff=0).shift(UP * 0.8),
            run_time=1.5,
            rate_func=linear
        )
        
        # Impact
        force_arrow = Arrow(ball.get_center(), box.get_center() + RIGHT * 1.0, color=ORANGE, stroke_width=8)
        force_label = safe_text("FORCE", 24, ORANGE, weight=BOLD).next_to(force_arrow, UP)
        
        self.play(
            Create(force_arrow), 
            Write(force_label), 
            Flash(box.get_left(), color=ORANGE),
            run_time=0.8
        )
        
        self.play(
            box.animate.shift(RIGHT * 2.5),
            ball.animate.shift(LEFT * 0.2),
            force_arrow.animate.shift(RIGHT * 1.0).set_opacity(0),
            run_time=1.2,
            rate_func=rate_functions.ease_out_sine
        )
        self.wait(2.7) # Total: 20.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Causal Chain (20.0 - 29.784)
        # "Chuỗi nhân quả ở đây rất rõ ràng... robot tương tác an toàn..."
        # ---------------------------------------------------------
        chain = VGroup(
            make_node("Ball", BLUE_C).scale(0.7),
            Arrow(LEFT, RIGHT, color=GOLD_A),
            make_node("Force", ORANGE).scale(0.7),
            Arrow(LEFT, RIGHT, color=GOLD_A),
            make_node("Box", TEAL_D).scale(0.7)
        ).arrange(RIGHT, buff=0.3).shift(UP * 1.5)
        
        self.play(FadeIn(chain, shift=DOWN), run_time=1.5)
        self.play(Indicate(chain, color=GOLD_A), run_time=1.0)
        
        self.wait(6.284) # Total: 28.784s




        # --- END SCENE 018 ---


        # --- START SCENE 019 ---

        # Audio
            
        # Total duration target: 30.216s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Lực bằng khối lượng nhân gia tốc, độ biến thiên động lượng bằng lực nhân khoảng thời gian."
        # ---------------------------------------------------------
        title = safe_text("Lực và Động lượng nhân quả", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formulas = VGroup(
            MathTex(r"F = m \cdot a", font_size=48, color=GOLD_A),
            MathTex(r"\Delta p = F \cdot \Delta t", font_size=48, color=ACCENT_COLOR)
        ).arrange(DOWN, buff=0.5).shift(UP * 0.5)
        
        self.play(Write(formulas[0]), run_time=1.0)
        self.play(Write(formulas[1]), run_time=1.0)
        self.wait(2.0) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Intervention - Mass Increase (4.0 - 12.0)
        # "Nếu ta can thiệp làm tăng khối lượng quả bóng, lực va chạm sẽ lớn hơn..."
        # ---------------------------------------------------------
        ball = make_ball().scale(1.2).shift(LEFT * 4 + DOWN * 1.0)
        box = make_box().scale(1.2).shift(RIGHT * 1 + DOWN * 1.0)
        
        mass_label = safe_text("Mass (m)", 20, GOLD_A).next_to(ball, UP)
        
        self.play(FadeIn(ball), FadeIn(box), Write(mass_label), run_time=1.0)
        self.wait(1.0)
        
        # Increase mass
        self.play(
            ball.animate.scale(1.5).set_color(GOLD_A),
            mass_label.animate.scale(1.2).set_color(GOLD_A),
            run_time=1.2
        )
        self.play(Indicate(ball, color=GOLD_A), run_time=0.8)
        self.wait(4.0) # Total: 12.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Larger Impact (12.0 - 22.0)
        # "Chiếc hộp sẽ nhận động lượng lớn hơn và trượt đi xa hơn..."
        # ---------------------------------------------------------
        # Movement
        self.play(ball.animate.next_to(box, LEFT, buff=0), run_time=1.2, rate_func=linear)
        
        # Impact
        large_force = Arrow(ball.get_center(), box.get_center() + RIGHT * 2.0, color=ORANGE, stroke_width=12)
        force_label = safe_text("LARGE FORCE", 24, ORANGE, weight=BOLD).next_to(large_force, UP)
        
        self.play(Create(large_force), Write(force_label), Flash(box.get_left(), color=ORANGE, flash_radius=0.8), run_time=0.8)
        
        self.play(
            box.animate.shift(RIGHT * 4.5), # Slides further
            ball.animate.shift(LEFT * 0.3),
            large_force.animate.shift(RIGHT * 1.5).set_opacity(0),
            run_time=1.5,
            rate_func=rate_functions.ease_out_sine
        )
        self.wait(5.7) # Total: 22.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Stable Mechanism (22.0 - 30.216)
        # "Mối quan hệ vật lý này chính là một cơ chế nhân quả ổn định... Robot..."
        # ---------------------------------------------------------
        mechanism_box = RoundedRectangle(width=6, height=1.5, corner_radius=0.2, color=GOLD_A, fill_opacity=0.1).shift(UP * 1.5)
        mechanism_text = safe_text("Stable Causal Mechanism", 28, GOLD_A).move_to(mechanism_box)
        
        self.play(FadeIn(mechanism_box, shift=DOWN), Write(mechanism_text), run_time=1.5)
        self.play(Indicate(mechanism_text, color=GOLD_A), run_time=1.0)
        
        self.wait(4.716) # Total: 29.216s




        # --- END SCENE 019 ---


        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)