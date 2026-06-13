from __future__ import annotations
from manim import *
import os
import sys
import numpy as np
import random

sys.path.append(os.path.dirname(__file__))
from visual_beats import *

class Batch5(Scene):
    def construct(self):
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        self.camera.background_color = BG_COLOR

        # --- START SCENE 026 ---

        # Audio
            
        # Total duration target: 30.624s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # Title
        title = safe_text("AI Hiện Thân & Agent Trong Game", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Embodied AI (0.0 - 8.0s)
        # "A I hiện thân là những tác nhân thông minh hoạt động trong thế giới vật lý hoặc giả lập..."
        # ---------------------------------------------------------
        formula = safe_text("Action -> Environment -> Reward", 32, GOLD_A).move_to(UP * 0.5)
        glow = formula.copy().set_stroke(GOLD_A, 8).set_opacity(0.3)
        
        agent = make_robot().scale(0.8).shift(DOWN * 1)
        
        self.play(Write(formula), FadeIn(glow), run_time=1.5)
        self.play(FadeIn(agent, shift=UP*0.2), run_time=1.0)
        self.wait(5.0)
        
        self.play(FadeOut(VGroup(formula, glow, agent)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Key-Door Causal Logic (8.0 - 16.0s)
        # "Ví dụ, trong trò chơi, tác nhân muốn mở cửa thì phải tìm được chìa khóa vàng..."
        # ---------------------------------------------------------
        door = make_door().scale(2.5).shift(RIGHT * 4 + DOWN * 1)
        key = Star(color=GOLD_A, fill_opacity=1, stroke_width=2).scale(0.4).move_to(LEFT * 4 + DOWN * 1)
        key_glow = key.copy().scale(1.5).set_opacity(0.3)
        
        agent = make_robot().scale(0.7).move_to(LEFT * 6 + DOWN * 1)
        
        causal_rule = safe_text("Causal: [Key] -> [Open Door]", 26, GOLD_A, weight=BOLD).move_to(UP * 1.5)
        
        self.play(FadeIn(door), FadeIn(key), FadeIn(key_glow), FadeIn(agent), run_time=1.0)
        self.play(Write(causal_rule), run_time=0.8)
        
        self.play(agent.animate.move_to(key.get_center()), run_time=1.5)
        self.play(FadeOut(key), FadeOut(key_glow), agent.animate.shift(UP * 0.3), run_time=0.5)
        self.play(agent.animate.move_to(door.get_left() + LEFT * 0.5), run_time=1.5)
        
        self.wait(1.2) # Total: 15.5s
        self.play(FadeOut(VGroup(door, agent, causal_rule)), run_time=0.5) # Total: 16.0s

        # ---------------------------------------------------------
        # SEGMENT 3: Simulated Planning (16.0 - 24.0s)
        # "Tác nhân sử dụng mô hình thế giới để thử nghiệm các chuỗi hành động trong đầu..."
        # ---------------------------------------------------------
        agent_thinking = make_robot().scale(1.2).shift(LEFT * 4 + DOWN * 1)
        thought_bubble = Circle(radius=2.0, color=WHITE, fill_opacity=0.05).shift(RIGHT * 2 + UP * 1)
        
        planning_tree = VGroup(
            Dot(thought_bubble.get_center() + UP * 1),
            Line(thought_bubble.get_center() + UP * 1, thought_bubble.get_center() + LEFT * 0.8),
            Line(thought_bubble.get_center() + UP * 1, thought_bubble.get_center() + RIGHT * 0.8),
            Dot(thought_bubble.get_center() + LEFT * 0.8),
            Dot(thought_bubble.get_center() + RIGHT * 0.8),
            Line(thought_bubble.get_center() + LEFT * 0.8, thought_bubble.get_center() + LEFT * 1.2 + DOWN * 0.8),
            Line(thought_bubble.get_center() + RIGHT * 0.8, thought_bubble.get_center() + RIGHT * 1.2 + DOWN * 0.8),
            Dot(thought_bubble.get_center() + LEFT * 1.2 + DOWN * 0.8, color=GREEN),
            Dot(thought_bubble.get_center() + RIGHT * 1.2 + DOWN * 0.8, color=RED)
        ).set_color(ACCENT_COLOR)
        
        plan_text = safe_text("World Model Simulation", 24, ACCENT_COLOR, weight=BOLD).next_to(thought_bubble, UP)
        
        self.play(FadeIn(agent_thinking), run_time=0.8)
        self.play(FadeIn(thought_bubble), Write(plan_text), run_time=0.8)
        self.play(LaggedStart(*[Create(m) for m in planning_tree], lag_ratio=0.1), run_time=2.0)
        self.play(Indicate(planning_tree[-2], color=GREEN), run_time=1.0)
        
        self.wait(2.9) # Total: 23.5s
        self.play(FadeOut(VGroup(agent_thinking, thought_bubble, planning_tree, plan_text)), run_time=0.5) # Total: 24.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Reward Maximization (24.0 - 30.624s)
        # "Bằng cách mô phỏng các chính sách khác nhau bên trong mô hình thế giới..."
        # ---------------------------------------------------------
        reward_icon = Star(color=YELLOW, fill_opacity=0.8).scale(1.5).move_to(UP * 0.5)
        reward_glow = reward_icon.copy().scale(1.4).set_stroke(YELLOW, 10).set_opacity(0.2)
        reward_text = safe_text("MAXIMUM REWARD", 36, YELLOW, weight=BOLD).next_to(reward_icon, DOWN, buff=0.8)
        
        risk_text = safe_text("Zero Physical Risk", 24, GREEN).next_to(reward_text, DOWN, buff=0.4)
        
        self.play(FadeIn(reward_icon), FadeIn(reward_glow), Write(reward_text), run_time=1.2)
        self.play(Write(risk_text), run_time=1.0)
        self.play(ShowPassingFlash(Underline(reward_text, color=YELLOW), run_time=1.0))
        
        self.wait(2.924) # Total: 30.124s




        # --- END SCENE 026 ---


        # --- START SCENE 027 ---

        # Audio
            
        # Total duration target: 27.984s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # Title
        title = safe_text("Y khoa & Giải thích được (XAI)", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Complex Medical Data (0.0 - 7.5s)
        # "Dữ liệu ảnh y khoa như chụp cắt lớp hay cộng hưởng từ thường vô cùng phức tạp..."
        # ---------------------------------------------------------
        formula = safe_text("Medical Image -> Segments -> Diagnosis", 32, GOLD_A).move_to(UP * 0.5)
        glow = formula.copy().set_stroke(GOLD_A, 8).set_opacity(0.3)
        
        self.play(Write(formula), FadeIn(glow), run_time=1.5)
        
        xray_frame = Rectangle(width=4, height=5, color=GREY_A, stroke_width=2).shift(DOWN * 1)
        scan_lines = VGroup(*[Line(xray_frame.get_left() + UP * i * 0.5, xray_frame.get_right() + UP * i * 0.5, color=WHITE, stroke_opacity=0.1) for i in range(-4, 5)])
        
        self.play(FadeIn(xray_frame), FadeIn(scan_lines), run_time=1.0)
        self.wait(4.5)
        
        self.play(FadeOut(VGroup(formula, glow, scan_lines)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Object-centric Partitioning (7.5 - 15.0s)
        # "Học theo trung tâm đối tượng giúp phân tách ảnh thành các vùng mô bệnh học riêng biệt..."
        # ---------------------------------------------------------
        lung_l = Ellipse(width=1.2, height=3.5, color=BLUE_C, fill_opacity=0.15).move_to(xray_frame.get_center() + LEFT * 0.8)
        lung_r = Ellipse(width=1.2, height=3.5, color=BLUE_C, fill_opacity=0.15).move_to(xray_frame.get_center() + RIGHT * 0.8)
        
        self.play(FadeIn(lung_l), FadeIn(lung_r), run_time=1.0)
        
        lesion = Circle(radius=0.25, color=RED, fill_opacity=0.6).move_to(lung_l.get_center() + UP * 0.8)
        lesion_glow = lesion.copy().set_stroke(RED, 10).set_opacity(0.3)
        
        label_box = SurroundingRectangle(lesion, color=RED, buff=0.15)
        label_text = safe_text("TỔN THƯƠNG", 22, RED, weight=BOLD).next_to(label_box, LEFT, buff=0.3)
        
        self.play(FadeIn(lesion), FadeIn(lesion_glow), Create(label_box), run_time=1.2)
        self.play(Write(label_text), Flash(lesion, color=RED), run_time=1.0)
        
        self.wait(3.8) # Total: 14.5s
        self.play(FadeOut(label_text), run_time=0.5) # Total: 15.0s

        # ---------------------------------------------------------
        # SEGMENT 3: Explainability (15.0 - 22.0s)
        # "Khả năng giải thích này giúp bác sĩ hiểu rõ cơ sở đưa ra chẩn đoán của A I..."
        # ---------------------------------------------------------
        info_panel = RoundedRectangle(width=5.5, height=3.5, corner_radius=0.2, color=TEAL, fill_opacity=0.15).shift(RIGHT * 3.5 + DOWN * 1)
        panel_header = safe_text("Giải thích AI (XAI)", 24, TEAL, weight=BOLD).next_to(info_panel, UP, buff=0.2)
        
        bullet_points = VGroup(
            safe_text("• Slot #4: Phát hiện khối u", 18, TEXT_COLOR),
            safe_text("• Đặc trưng: Độ cản quang cao", 18, TEXT_COLOR),
            safe_text("• Tương quan: Bất thường mạch máu", 18, TEXT_COLOR),
            safe_text("• Độ tin cậy: 97.4%", 18, GOLD_A, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(info_panel)
        
        connector = Arrow(label_box.get_right(), info_panel.get_left(), color=TEAL)
        
        self.play(FadeIn(info_panel), Write(panel_header), Create(connector), run_time=1.2)
        self.play(LaggedStart(*[Write(p) for p in bullet_points], lag_ratio=0.5), run_time=2.5)
        
        self.wait(2.8) # Total: 21.5s
        self.play(FadeOut(VGroup(connector, info_panel, panel_header, bullet_points)), run_time=0.5) # Total: 22.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Ethical & Legal Standards (22.0 - 27.984s)
        # "Kỹ thuật giải thích mô hình A I như thế này đặc biệt cấp thiết..."
        # ---------------------------------------------------------
        law_icon = VGroup(
            Rectangle(width=0.8, height=1.2, color=GOLD_A, fill_opacity=0.3), # Law book
            Line(UP * 0.4, UP * 0.4 + RIGHT * 0.4, color=GOLD_A).shift(LEFT * 0.2),
            Line(ORIGIN, RIGHT * 0.4, color=GOLD_A).shift(LEFT * 0.2),
            Line(DOWN * 0.4, DOWN * 0.4 + RIGHT * 0.4, color=GOLD_A).shift(LEFT * 0.2),
        ).shift(UP * 0.5)
        
        ethic_text = safe_text("Tiêu chuẩn Đạo đức & Pháp lý", 32, GOLD_A, weight=BOLD).next_to(law_icon, DOWN, buff=0.5)
        
        self.play(FadeIn(law_icon, shift=UP*0.3), run_time=1.0)
        self.play(Write(ethic_text), run_time=1.0)
        self.play(Indicate(ethic_text, color=GOLD_A), run_time=1.0)
        
        self.wait(2.484) # Total: 27.484s




        # --- END SCENE 027 ---


        # --- START SCENE 028 ---

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
        title = safe_text("Thành Phố Thông Minh & Bản Sao Số", 36, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)

        # ---------------------------------------------------------
        # SEGMENT 1: Digital Twin Concept (0.0 - 8.0s)
        # "Trong quản lý đô thị hiện đại, chúng ta xây dựng bản sao số của thành phố..."
        # ---------------------------------------------------------
        formula = safe_text("Physical City -> Digital Twin (Entities)", 32, GOLD_A).move_to(UP * 0.5)
        glow = formula.copy().set_stroke(GOLD_A, 8).set_opacity(0.3)
        
        city_base = Rectangle(width=10, height=6, color=BLUE_E, fill_opacity=0.05).shift(DOWN * 1)
        grid = NumberPlane(x_range=[-5, 5, 1], y_range=[-3, 3, 1], background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.2}).move_to(city_base)
        
        self.play(Write(formula), FadeIn(glow), run_time=1.5)
        self.play(FadeIn(city_base), Create(grid), run_time=1.0)
        self.wait(5.0)
        
        self.play(FadeOut(VGroup(formula, glow)), run_time=0.5)

        # ---------------------------------------------------------
        # SEGMENT 2: Data Compression (8.0 - 16.0s)
        # "Thay vì xử lý video thô từ hàng ngàn camera an ninh quá tải..."
        # ---------------------------------------------------------
        cam_icon = VGroup(
            RoundedRectangle(width=0.6, height=0.4, corner_radius=0.1, color=WHITE, fill_opacity=0.2),
            Circle(radius=0.1, color=WHITE, fill_opacity=0.5)
        ).shift(LEFT * 4 + UP * 1)
        
        video_noise = VGroup(*[
            Square(0.1, fill_opacity=np.random.rand(), color=GREY)
            for _ in range(25)
        ]).arrange_in_grid(5, 5, buff=0.02).next_to(cam_icon, DOWN)
        
        entity_cars = VGroup(*[
            Dot(color=GOLD_A).move_to(grid.c2p(x, y))
            for x, y in [(-3, 0.5), (-1, 0.5), (1, 0.5), (3, 0.5), (-2, -1.5), (0, -1.5)]
        ])
        car_labels = VGroup(*[safe_text(f"ID:{i}", 12, TEXT_COLOR).next_to(entity_cars[i], UP, buff=0.05) for i in range(len(entity_cars))])
        
        compress_arrow = Arrow(video_noise.get_right(), entity_cars[0].get_left(), color=GOLD_A)
        compress_text = safe_text("NÉN THỰC THỂ", 20, GOLD_A, weight=BOLD).next_to(compress_arrow, UP)
        
        self.play(FadeIn(cam_icon), FadeIn(video_noise), run_time=0.8)
        self.play(Create(compress_arrow), Write(compress_text), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in entity_cars], lag_ratio=0.1), Write(car_labels), run_time=1.2)
        
        self.play(VGroup(entity_cars, car_labels).animate.shift(RIGHT * 1), run_time=1.5)
        self.wait(2.4) # Total: 15.5s
        self.play(FadeOut(VGroup(cam_icon, video_noise, compress_arrow, compress_text)), run_time=0.5) # Total: 16.0s

        # ---------------------------------------------------------
        # SEGMENT 3: Causal Rerouting (16.0 - 24.0s)
        # "Hệ thống sử dụng mô hình nhân quả để dự báo ùn tắc khi đóng một làn đường..."
        # ---------------------------------------------------------
        road_block = Cross(Square(side_length=0.8), stroke_color=RED, stroke_width=6).move_to(grid.c2p(3, 0.5))
        block_text = safe_text("ĐÓNG ĐƯỜNG", 20, RED, weight=BOLD).next_to(road_block, UP)
        
        prediction_bubble = Circle(radius=1.5, color=TEAL, fill_opacity=0.1).shift(UP * 1.5 + RIGHT * 2)
        predict_text = safe_text("Dự báo nhân quả", 22, TEAL).next_to(prediction_bubble, UP)
        
        self.play(Create(road_block), Write(block_text), run_time=1.0)
        self.play(FadeIn(prediction_bubble), Write(predict_text), run_time=0.8)
        
        # Reroute one car in simulation
        sim_car = Dot(color=GOLD_A).move_to(grid.c2p(1, 0.5))
        sim_path = Line(grid.c2p(1, 0.5), grid.c2p(1, -0.5), color=GOLD_A).set_stroke(opacity=0.5)
        
        self.play(FadeIn(sim_car), Create(sim_path), run_time=0.8)
        self.play(sim_car.animate.move_to(grid.c2p(1, -0.5)), run_time=1.2)
        
        self.play(VGroup(entity_cars[3], car_labels[3]).animate.move_to(grid.c2p(2, -0.5)), run_time=1.5) # Real car moves
        
        self.wait(1.2) # Total: 23.5s
        self.play(FadeOut(VGroup(road_block, block_text, prediction_bubble, predict_text, sim_car, sim_path)), run_time=0.5) # Total: 24.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Real-time Optimization (24.0 - 30.936s)
        # "Hệ thống ra quyết định phân tán dựa trên bản sao số có thể tối ưu hóa lưu lượng..."
        # ---------------------------------------------------------
        opt_glow = city_base.copy().set_stroke(TEAL, 8).set_opacity(0.3)
        opt_text = safe_text("TỐI ƯU HÓA THỜI GIAN THỰC", 32, TEAL, weight=BOLD).move_to(UP * 0.5)
        
        # All cars moving smoothly
        self.play(FadeIn(opt_glow), Write(opt_text), run_time=1.0)
        self.play(
            VGroup(entity_cars, car_labels).animate.shift(RIGHT * 2),
            run_time=3.0, rate_func=linear
        )
        self.play(Flash(opt_text, color=TEAL), run_time=1.0)
        
        self.wait(1.436) # Total: 30.436s




        # --- END SCENE 028 ---


        # --- START SCENE 029 ---

        # 1. Perfect Sync & Audio
        target_duration = 31.224
            
        self.camera.background_color = BG_COLOR
        
        # 2. High Fidelity Title
        title = self.create_title("AI ĐA PHƯƠNG THỨC: NGÔN NGỮ & HÌNH ẢNH")
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)
        
        # --- Segment 1: Command & Object Grounding ---
        # "Lệnh văn bản được liên kết với đối tượng thực tế..."
        
        command_rect = RoundedRectangle(width=9, height=1.2, corner_radius=0.2, color=BLUE, fill_opacity=0.1).shift(UP * 1.5)
        command_text = Text('Lấy "chiếc cốc màu đỏ" trên bàn', font_size=32, color=WHITE, t2c={"chiếc cốc": GOLD_A, "màu đỏ": RED}).move_to(command_rect)

        
        self.play(FadeIn(command_rect), Write(command_text), run_time=2)
        self.wait(1)
        
        # Literal Mapping: Table and Cups
        table = Line(LEFT*4, RIGHT*4, color=GREY_TEXT).shift(DOWN*2)
        cup_red = VGroup(
            RoundedRectangle(width=0.6, height=0.8, corner_radius=0.1, color=RED, fill_opacity=0.8),
            Rectangle(width=0.2, height=0.4, color=RED).shift(RIGHT*0.35)
        ).scale(0.8).next_to(table, UP, buff=0).shift(LEFT*1.5)
        
        cup_blue = VGroup(
            RoundedRectangle(width=0.6, height=0.8, corner_radius=0.1, color=BLUE, fill_opacity=0.8),
            Rectangle(width=0.2, height=0.4, color=BLUE).shift(RIGHT*0.35)
        ).scale(0.8).next_to(table, UP, buff=0).shift(RIGHT*1.5)
        
        self.play(Create(table), FadeIn(cup_red, shift=UP), FadeIn(cup_blue, shift=UP), run_time=1.5)
        self.wait(2)
        
        # 3. Object Grounding Animation
        slot_red = create_object_slot_tray(color=GOLD_A).scale(0.8).move_to(cup_red)
        vector_col = create_vector_column().scale(0.5).next_to(slot_red, LEFT, buff=0.5)
        
        self.play(Create(slot_red), FadeIn(vector_col), run_time=1)
        
        # Connectors (High fidelity)
        arrow_cup = CurvedArrow(command_text.get_bottom() + LEFT*0.5, slot_red.get_top(), color=GOLD_A, angle=-TAU/8)
        arrow_red = CurvedArrow(command_text.get_bottom() + RIGHT*0.5, vector_col[1].get_right(), color=RED, angle=TAU/8)
        
        self.play(Create(arrow_cup), Create(arrow_red), run_time=1.5)
        self.wait(3)
        
        # 4. Segment Clearing
        self.play(FadeOut(command_rect, command_text, arrow_cup, arrow_red, cup_blue), run_time=1)
        
        # --- Segment 2: Execution ---
        # "Sự liên kết có cấu trúc này giúp AI tương tác chính xác..."
        
        robot_arm = create_robot_arm().scale(1.2).to_edge(LEFT, buff=1).shift(DOWN*1)
        self.play(FadeIn(robot_arm, shift=RIGHT), run_time=1.5)
        
        # Robot movement to red cup
        self.play(
            robot_arm.animate.next_to(cup_red, LEFT, buff=0.2).shift(UP*0.5),
            run_time=2,
            rate_func=bezier([0, 0, 1, 1])
        )
        
        # Grip and Lift
        self.play(
            VGroup(robot_arm, cup_red, slot_red, vector_col).animate.shift(UP*1.5),
            run_time=2
        )
        
        # Glow / Flash success
        glow = SurroundingRectangle(cup_red, color=GOLD_A, stroke_width=4, buff=0.2)
        self.play(Create(glow), Flash(cup_red, color=GOLD_A), run_time=1)
        self.wait(2)
        
        # 5. Final Wait to match duration
        current_time = self.renderer.time
        if target_duration > current_time:
            self.wait(target_duration - current_time)
        else:
            self.wait(0.1)

        # --- END SCENE 029 ---


        # --- START SCENE 030 ---

        # 1. Perfect Sync & Audio
        target_duration = 31.8
            
        self.camera.background_color = BG_COLOR
        
        # 2. High Fidelity Title
        title = self.create_title("CÁC THÁCH THỨC LỚN TRONG TƯƠNG LAI")
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)
        
        # --- Segment 1: Ambiguity ---
        # "Đầu tiên là ranh giới của đối tượng thế giới thực rất mơ hồ."
        
        # Literal Mapping: Tree with blurry boundaries
        tree_trunk = RoundedRectangle(width=0.4, height=2.5, corner_radius=0.1, color=DARK_BROWN, fill_opacity=0.8).shift(DOWN*1)
        leaves = VGroup(*[
            Circle(radius=0.4, color=GREEN, fill_opacity=0.3).shift(UP * (0.5 + random.uniform(-0.5, 0.8)) + RIGHT * random.uniform(-1, 1))
            for _ in range(25)
        ]).next_to(tree_trunk, UP, buff=-0.5)
        tree = VGroup(tree_trunk, leaves).shift(LEFT*3)
        
        # Blurry effect: Multiple overlapping outlines
        blurry_outlines = VGroup(*[
            tree.copy().set_stroke(color=TEAL, width=1, opacity=0.2).scale(1 + i*0.05)
            for i in range(1, 5)
        ])
        
        self.play(FadeIn(tree, shift=UP), run_time=1.5)
        self.play(FadeIn(blurry_outlines), run_time=1)
        
        label_ambiguity = Text("Ranh giới mơ hồ", font_size=24, color=WHITE).next_to(tree, DOWN)
        self.play(Write(label_ambiguity), run_time=1)
        self.wait(2)
        
        # --- Segment 2: Confounding ---
        # "Thứ hai, các yếu tố gây nhiễu ẩn giấu..."
        
        # SCM with Hidden U
        x_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.2).move_to(ORIGIN + RIGHT*1 + DOWN*0.5)
        y_node = Circle(radius=0.5, color=TEAL, fill_opacity=0.2).move_to(ORIGIN + RIGHT*4 + DOWN*0.5)
        u_node = Circle(radius=0.4, color=RED, fill_opacity=0.1).move_to(ORIGIN + RIGHT*2.5 + UP*1.5)
        u_node.set_stroke(color=RED, width=2, opacity=0.5) # Hidden/Dashed
        
        x_label = MathTex("X", color=WHITE).move_to(x_node)
        y_label = MathTex("Y", color=WHITE).move_to(y_node)
        u_label = Text("U (Nhiễu ẩn)", font_size=20, color=RED).next_to(u_node, UP)
        
        arrow_ux = Arrow(u_node.get_bottom(), x_node.get_top(), color=RED, buff=0.1)
        arrow_uy = Arrow(u_node.get_bottom(), y_node.get_top(), color=RED, buff=0.1)
        arrow_xy = DashedLine(x_node.get_right(), y_node.get_left(), color=GREY_TEXT)
        
        scm_group = VGroup(x_node, y_node, u_node, x_label, y_label, u_label, arrow_ux, arrow_uy, arrow_xy)
        
        self.play(FadeIn(scm_group), run_time=2)
        self.play(Indicate(u_node, color=RED), run_time=1)
        self.wait(3)
        
        # --- Segment 3: Scaling & Energy ---
        # "Cuối cùng, việc mở rộng mô hình... tốn kém năng lượng."
        
        # Segment Clearing
        self.play(FadeOut(tree, blurry_outlines, label_ambiguity, scm_group), run_time=1)
        
        energy_db = create_database_cylinder(color=ORANGE).scale(1.5).shift(LEFT*3)
        energy_bar = Rectangle(width=1, height=0.1, color=GREEN, fill_opacity=0.8).next_to(energy_db, UP, buff=0.1)
        
        self.play(FadeIn(energy_db), run_time=1)
        
        # Energy growth animation
        self.play(
            energy_bar.animate.stretch_to_fit_height(3, about_edge=DOWN).set_color(RED),
            run_time=4,
            rate_func=linear
        )
        
        explosion_text = Text("Bùng nổ tổ hợp!", font_size=40, color=RED, weight=BOLD).shift(RIGHT*2 + UP*0.5)
        grid = create_feature_grid(rows=10, cols=10).scale(0.8).next_to(explosion_text, DOWN)
        
        self.play(Write(explosion_text), FadeIn(grid), run_time=1.5)
        self.play(Flash(explosion_text, color=RED), run_time=0.5)
        
        # 5. Final Wait
        current_time = self.renderer.time
        if target_duration > current_time:
            self.wait(target_duration - current_time)
        else:
            self.wait(0.1)

        # --- END SCENE 030 ---


        # --- START SCENE 031 ---

        # 1. Perfect Sync & Audio
        target_duration = 31.92
            
        self.camera.background_color = BG_COLOR
        
        # 2. High Fidelity Title
        title = self.create_title("KẾT LUẬN: MÔ HÌNH THẾ GIỚI NHÂN QUẢ")
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)
        
        # --- Segment 1: Synthesis ---
        # "Tóm lại, học theo trung tâm đối tượng cung cấp các biến số biểu diễn độc lập..."
        
        slots = VGroup(*[create_object_slot_tray(color=c).scale(0.6) for c in [TEAL, ORANGE, BLUE]]).arrange(RIGHT, buff=1).shift(UP*0.5)
        icons = VGroup(
            Circle(radius=0.3, color=TEAL, fill_opacity=0.6),
            Square(side_length=0.6, color=ORANGE, fill_opacity=0.6),
            Triangle().scale(0.4).set_color(BLUE).set_fill(BLUE, opacity=0.6)
        )
        for i, icon in enumerate(icons):
            icon.move_to(slots[i])
            
        self.play(FadeIn(slots, shift=UP), FadeIn(icons, shift=UP), run_time=2)
        self.wait(2)
        
        # "Học biểu diễn nhân quả kết nối chúng bằng quy luật tự nhiên."
        arrows = VGroup(
            Arrow(slots[0].get_right(), slots[1].get_left(), color=GOLD_A),
            Arrow(slots[1].get_right(), slots[2].get_left(), color=GOLD_A)
        )
        self.play(Create(arrows), run_time=1.5)
        self.wait(3)
        
        # --- Segment 2: Causal World Model ---
        # "Sự kết hợp này mở ra cánh cửa tiến tới mô hình thế giới nhân quả thực thụ."
        
        # Segment Clearing
        self.play(FadeOut(slots, icons, arrows), run_time=1)
        
        brain_glow = Circle(radius=2.5, color=GOLD_A, fill_opacity=0.05).set_stroke(opacity=0.2)
        brain_center = create_neural_network_tunnel().scale(1.5).rotate(90*DEGREES).move_to(ORIGIN)
        
        self.play(FadeIn(brain_glow), FadeIn(brain_center, shift=IN), run_time=2)
        
        model_text = Text("MÔ HÌNH THẾ GIỚI NHÂN QUẢ", font_size=36, color=TITLE_YELLOW, weight=BOLD).shift(UP*2)
        self.play(Write(model_text), run_time=1.5)
        
        # Literal Mapping: AI Robot Agent
        robot = create_robot_arm().scale(1.2).shift(DOWN*1.5 + LEFT*4)
        environment = RoundedRectangle(width=4, height=2.5, color=TEAL, fill_opacity=0.1).shift(DOWN*1.5 + RIGHT*2)
        env_label = Text("Môi trường", font_size=24, color=TEAL).next_to(environment, UP)
        
        self.play(FadeIn(robot, shift=RIGHT), FadeIn(environment, shift=LEFT), Write(env_label), run_time=1.5)
        self.wait(4)
        
        # --- Segment 3: Outro ---
        # "Cảm ơn mọi người... bình minh của AGI"
        
        self.play(FadeOut(robot, environment, env_label, brain_center, brain_glow, model_text), run_time=1)
        
        thanks_text = Text("CẢM ƠN CÁC BẠN ĐÃ THEO DÕI!", font_size=42, color=GOLD_A, weight=BOLD)
        agi_text = Text("Bình minh của Trí tuệ nhân tạo tổng quát (AGI)", font_size=28, color=GREY_TEXT).next_to(thanks_text, DOWN, buff=0.5)
        
        self.play(Write(thanks_text), run_time=2)
        self.play(FadeIn(agi_text, shift=UP), run_time=1.5)
        self.play(Flash(thanks_text, color=GOLD_A, line_length=1), run_time=1)
        
        # 5. Final Wait
        current_time = self.renderer.time
        if target_duration > current_time:
            self.wait(target_duration - current_time)
        else:
            self.wait(0.1)

        # --- END SCENE 031 ---


        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)