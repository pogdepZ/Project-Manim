from __future__ import annotations
from manim import *
import os
import sys
import numpy as np
import random

sys.path.append(os.path.dirname(__file__))
from visual_beats import *

class Batch2(Scene):
    def construct(self):
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        self.camera.background_color = BG_COLOR

        # --- START SCENE 007 ---

        # Audio
            
        # Total duration target: 32.472s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Attention Formula (0.0 - 8.5)
        # "Hàm chú ý của truy vấn quy, khóa ca, giá trị vê bằng softmax của quy nhân ca chuyển vị chia căn bậc hai của đê... cơ chế chú ý theo slot..."
        # ---------------------------------------------------------
        title = safe_text("Cơ chế Slot Attention", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        formula = MathTex(
            "\\text{Attn}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d}}\\right)V",
            font_size=48, color=GOLD_A
        ).move_to(ORIGIN)
        
        self.play(Write(title), run_time=0.8)
        self.play(Write(formula), run_time=1.5)
        self.play(Indicate(formula, color=GOLD_A), run_time=1.0)
        
        self.wait(4.7) # Total: 8.0s
        self.play(FadeOut(formula), run_time=0.5) # Total: 8.5s

        # ---------------------------------------------------------
        # SEGMENT 2: Flow and Initialization (8.5 - 16.5)
        # "Đầu vào là các đặc trưng ảnh, đầu ra là thông tin trong các slot... khởi tạo ngẫu nhiên..."
        # ---------------------------------------------------------
        features = make_pixel_grid(6, 6, 0.3).shift(LEFT * 4)
        f_label = safe_text("Image Features", 18, TEXT_COLOR).next_to(features, UP)
        
        slots = VGroup(*[
            make_slot(f"Slot {i+1}", [BLUE, TEAL, ORANGE][i])
            for i in range(3)
        ]).arrange(DOWN, buff=0.4).shift(RIGHT * 4)
        
        self.play(FadeIn(features), Write(f_label), run_time=1.0)
        self.play(FadeIn(slots, shift=LEFT), run_time=1.2)
        
        # Random initialization effect
        self.play(
            LaggedStart(*[
                Flash(s, color=WHITE, line_length=0.2)
                for s in slots
            ], lag_ratio=0.2),
            run_time=1.0
        )
        
        self.wait(4.3) # Total: 16.0s
        self.play(FadeOut(f_label), run_time=0.5) # Total: 16.5s

        # ---------------------------------------------------------
        # SEGMENT 3: Update Loop (16.5 - 25.5)
        # "Trải qua nhiều vòng cập nhật thông tin... tương tác với đặc trưng ảnh..."
        # ---------------------------------------------------------
        # Iterative update arrows
        update_arrows = VGroup(*[
            CurvedArrow(slots[i].get_bottom() + LEFT*0.2, slots[i].get_top() + LEFT*0.2, angle=PI, color=ACCENT_COLOR).scale(0.5)
            for i in range(3)
        ])
        
        # Interaction lines
        lines = VGroup(*[
            Line(features[np.random.randint(0, 36)].get_center(), slots[i].get_left(), stroke_width=1, stroke_opacity=0.3, color=WHITE)
            for i in range(3) for _ in range(5)
        ])
        
        self.play(Create(update_arrows), Create(lines), run_time=1.5)
        
        # Loop animation
        for _ in range(2):
            self.play(
                *[s.animate.set_style(fill_opacity=0.5) for s in slots],
                run_time=0.5
            )
            self.play(
                *[s.animate.set_style(fill_opacity=0.16) for s in slots],
                run_time=0.5
            )
            
        self.wait(4.0) # Total: 25.0s
        self.play(FadeOut(update_arrows), FadeOut(lines), FadeOut(title), run_time=0.5) # Total: 25.5s

        # ---------------------------------------------------------
        # SEGMENT 4: Softmax Competition (25.5 - 32.472)
        # "Sử dụng kỹ thuật Softmax... mỗi điểm ảnh bị bắt buộc phải cạnh tranh..."
        # ---------------------------------------------------------
        softmax_text = safe_text("Softmax (Competition)", 28, GOLD_A, weight=BOLD).to_edge(UP)
        
        # Competition visual
        target_pixel = features[15]
        comp_arrows = VGroup(*[
            Arrow(target_pixel.get_center(), slots[i].get_left(), buff=0.1, color=[BLUE, TEAL, ORANGE][i])
            for i in range(3)
        ])
        
        self.play(Write(softmax_text), Indicate(target_pixel, color=GOLD_A), run_time=1.0)
        self.play(Create(comp_arrows), run_time=1.2)
        
        # Winner takes all
        self.play(
            comp_arrows[0].animate.set_stroke(width=8).set_color(GOLD_A),
            comp_arrows[1:].animate.set_opacity(0.1),
            target_pixel.animate.set_color(GOLD_A),
            run_time=1.5
        )
        
        self.wait(2.772) # Total: 31.972s




        # --- END SCENE 007 ---


        # --- START SCENE 008 ---

        # Audio
            
        # Total duration target: 27.792s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Competition & Puzzle Analogy (0.0 - 7.5)
        # "Quá trình cạnh tranh dẫn tới sự phân rã biểu diễn không trộn lẫn... tưởng tượng nhóm học sinh tranh nhau mảnh ghép..."
        # ---------------------------------------------------------
        title = safe_text("Quá trình cạnh tranh giữa các Slot", 30, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        
        puzzle_grid = VGroup(*[
            Square(side_length=0.4, stroke_width=1, stroke_color=WHITE, fill_opacity=0.1)
            for _ in range(25)
        ]).arrange_in_grid(5, 5, buff=0.05).move_to(ORIGIN)
        
        students = VGroup(*[
            make_person().scale(0.8)
            for _ in range(3)
        ]).arrange(RIGHT, buff=3.0).shift(DOWN * 2)
        
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(puzzle_grid, shift=UP), run_time=1.0)
        self.play(FadeIn(students, shift=UP), run_time=1.2)
        
        self.wait(4.5) # Total: 7.5s

        # ---------------------------------------------------------
        # SEGMENT 2: Competition for Pieces (7.5 - 15.0)
        # "Mỗi học sinh chỉ được chọn một nhóm mảnh ghép... một mảnh ghép được giữ chặt..."
        # ---------------------------------------------------------
        # Arrows from students to pieces
        arrows = VGroup(*[
            Arrow(students[i].get_top(), puzzle_grid[np.random.randint(0, 25)].get_center(), buff=0.1, color=[BLUE, TEAL, ORANGE][i])
            for i in range(3) for _ in range(4)
        ])
        
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.05), run_time=1.5)
        
        # Winner claiming a region
        claimed_indices = [6, 7, 8, 11, 12, 13, 16, 17, 18]
        claimed_pieces = VGroup(*[puzzle_grid[i] for i in claimed_indices])
        
        self.play(
            claimed_pieces.animate.set_fill(BLUE, opacity=0.6).set_stroke(GOLD_A, width=4),
            students[0].animate.set_color(BLUE).scale(1.2),
            run_time=1.5
        )
        
        # Other students' arrows to this region disappear
        dead_arrows = VGroup(*[
            a for a in arrows 
            if any(np.allclose(a.get_end(), puzzle_grid[i].get_center()) for i in claimed_indices)
            and not np.allclose(a.get_start(), students[0].get_top())
        ])
        
        self.play(FadeOut(dead_arrows), run_time=1.0)
        self.wait(3.5) # Total: 15.0s

        # ---------------------------------------------------------
        # SEGMENT 3: Disentangled Slots (15.0 - 22.0)
        # "Buộc các slot phải tự phân chia ranh giới vật thể... mỗi slot chỉ tập trung biểu diễn một thực thể duy nhất."
        # ---------------------------------------------------------
        
        final_slots = VGroup(
            make_slot("Ball", BLUE),
            make_slot("Box", TEAL),
            make_slot("Robot", ORANGE)
        ).arrange(RIGHT, buff=1.0).center()
        
        objects = VGroup(
            make_ball().scale(0.8).move_to(final_slots[0]),
            make_box().scale(0.8).move_to(final_slots[1]),
            make_robot().scale(0.6).move_to(final_slots[2])
        )
        
        self.play(LaggedStart(*[FadeIn(s, shift=UP*0.3) for s in final_slots], lag_ratio=0.2), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(o, scale=0.5) for o in objects], lag_ratio=0.2), run_time=1.2)
        
        # Boundary glow
        self.play(*[Indicate(s, color=GOLD_A) for s in final_slots], run_time=1.5)
        
        self.wait(2.6) # Total: 21.5s
        self.play(FadeOut(objects), run_time=0.5) # Total: 22.0s

        # ---------------------------------------------------------
        # SEGMENT 4: Information Bottleneck (22.0 - 27.792)
        # "Nguyên lý thắt nút cổ chai thông tin... loại bỏ sự dư thừa."
        # ---------------------------------------------------------
        bottleneck = Polygon(
            LEFT*2 + UP*1, RIGHT*2 + UP*1, 
            RIGHT*0.5 + DOWN*1, LEFT*0.5 + DOWN*1,
            color=GOLD_A, fill_opacity=0.2, stroke_width=4
        ).shift(DOWN * 0.5)
        
        bn_label = safe_text("Information Bottleneck", 24, GOLD_A, weight=BOLD).next_to(bottleneck, UP)
        
        input_data = VGroup(*[Dot(color=WHITE, radius=0.04).move_to(UP*1 + LEFT*1.5 + RIGHT*i*0.2) for i in range(15)])
        output_data = VGroup(*[Dot(color=GOLD_A, radius=0.06).move_to(DOWN*1.2 + LEFT*0.3 + RIGHT*i*0.2) for i in range(4)])
        
        self.play(FadeIn(bottleneck), Write(bn_label), run_time=1.0)
        self.play(FadeIn(input_data), run_time=0.8)
        
        # Compression animation
        self.play(
            LaggedStart(*[
                d.animate.move_to(bottleneck.get_center()).set_opacity(0)
                for d in input_data
            ], lag_ratio=0.05),
            FadeIn(output_data, shift=DOWN),
            run_time=2.0
        )
        
        self.wait(1.992) # Total: 27.292s




        # --- END SCENE 008 ---


        # --- START SCENE 009 ---

        # Audio
            
        # Total duration target: 30.072s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Reconstruction Formula (0.0 - 7.5)
        # "Ảnh ích mũ bằng tổng các tích của mặt nạ em ca nhân ảnh thành phần ích mũ ca... làm thế nào để biết slot đã học đúng?"
        # ---------------------------------------------------------
        title = safe_text("Reconstruction & Masking", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        formula = MathTex("\\hat{x} = \\sum_{k=1}^K m_k \\cdot \\hat{x}_k", font_size=54, color=GOLD_A).move_to(ORIGIN)
        
        self.play(Write(title), run_time=0.8)
        self.play(Write(formula), run_time=1.2)
        self.play(Flash(formula, color=GOLD_A), run_time=0.5)
        
        self.wait(4.5) # Total: 7.0s
        self.play(FadeOut(formula), run_time=0.5) # Total: 7.5s

        # ---------------------------------------------------------
        # SEGMENT 2: Components and Masks (7.5 - 15.5)
        # "Tái tạo lại bức ảnh ban đầu từ các slot... mỗi slot tạo ra ảnh thành phần và mặt nạ..."
        # ---------------------------------------------------------
        slot = make_slot("Slot k", BLUE).shift(LEFT * 5)
        
        # Component and Mask for a ball
        comp_x = VGroup(
            Rectangle(width=2, height=2, color=GREY, fill_opacity=0.1),
            make_ball().scale(2.0)
        ).shift(LEFT * 1.5 + UP * 0.5)
        comp_label = safe_text("Component x_k", 18, TEXT_COLOR).next_to(comp_x, DOWN)
        
        mask_m = VGroup(
            Rectangle(width=2, height=2, color=GREY, fill_opacity=0.1),
            Circle(radius=0.7, color=WHITE, fill_opacity=1.0)
        ).shift(RIGHT * 2 + UP * 0.5)
        mask_label = safe_text("Mask m_k", 18, TEXT_COLOR).next_to(mask_m, DOWN)
        
        arrow1 = Arrow(slot.get_right(), comp_x.get_left(), color=WHITE)
        arrow2 = Arrow(slot.get_right(), mask_m.get_left(), color=WHITE)
        
        self.play(FadeIn(slot), run_time=0.8)
        self.play(Create(arrow1), Create(arrow2), FadeIn(comp_x), FadeIn(mask_m), Write(comp_label), Write(mask_label), run_time=1.5)
        
        self.wait(5.2) # Total: 15.0s
        self.play(FadeOut(slot), FadeOut(arrow1), FadeOut(arrow2), run_time=0.5) # Total: 15.5s

        # ---------------------------------------------------------
        # SEGMENT 3: Summation (15.5 - 24.5)
        # "Nhân ảnh thành phần với mặt nạ rồi cộng tất cả lại... kết quả là bức ảnh tái tạo hoàn chỉnh."
        # ---------------------------------------------------------
        # Multiply effect
        dot_product = MathTex("\\times", font_size=48, color=GOLD_A).move_to(VGroup(comp_x, mask_m).get_center() + UP*0.5)
        self.play(Write(dot_product), run_time=0.8)
        
        reconstructed_img = VGroup(
            make_pixel_grid(6, 6, 0.4),
            make_ball().scale(2.5).set_opacity(0.9)
        ).shift(DOWN * 1.5)
        recon_label = safe_text("Reconstructed Image (x_hat)", 24, GOLD_A).next_to(reconstructed_img, DOWN)
        
        self.play(
            ReplacementTransform(VGroup(comp_x, mask_m, dot_product), reconstructed_img),
            Write(recon_label),
            FadeOut(comp_label), FadeOut(mask_label),
            run_time=2.0
        )
        
        self.wait(5.7) # Total: 24.0s
        self.play(FadeOut(reconstructed_img), FadeOut(recon_label), run_time=0.5) # Total: 24.5s

        # ---------------------------------------------------------
        # SEGMENT 4: Loss and Optimization (24.5 - 30.072)
        # "Hàm suy hao tái tạo... tín hiệu giám sát mạnh mẽ... tối ưu hóa bộ mã hóa và giải mã."
        # ---------------------------------------------------------
        loss_formula = MathTex(
            "\\mathcal{L} = \\|x - \\hat{x}\\|^2",
            font_size=64, color=RED
        ).move_to(ORIGIN)
        loss_label = safe_text("RECONSTRUCTION LOSS", 32, RED, weight=BOLD).next_to(loss_formula, UP, buff=0.5)
        
        self.play(Write(loss_label), run_time=1.0)
        self.play(FadeIn(loss_formula, shift=DOWN), run_time=1.2)
        
        # Optimization arrows
        opt_arrows = VGroup(
            Arrow(loss_formula.get_bottom(), DOWN*2.5 + LEFT*2, color=GOLD_A),
            Arrow(loss_formula.get_bottom(), DOWN*2.5 + RIGHT*2, color=GOLD_A)
        )
        opt_labels = VGroup(
            safe_text("Update Encoder", 18, GOLD_A).next_to(opt_arrows[0], DOWN),
            safe_text("Update Decoder", 18, GOLD_A).next_to(opt_arrows[1], DOWN)
        )
        
        self.play(Create(opt_arrows), Write(opt_labels), run_time=1.5)
        
        self.wait(1.872) # Total: 29.572s




        # --- END SCENE 009 ---


        # --- START SCENE 010 ---

        # Audio
            
        # Total duration target: 29.928s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Synthetic vs Real (Start: 0.0s)
        # "Thế giới mô phỏng đơn giản dẫn tới thế giới thực phức tạp."
        # ---------------------------------------------------------
        title = safe_text("Bài toán dữ liệu mô phỏng và thế giới thực", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = safe_text("Synthetic (Simple) -> Real World (Complex)", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: Simple Simulation (4.0 - 10.0)
        # "Các nghiên cứu ban đầu thường chỉ chạy trên dữ liệu mô phỏng đơn giản..."
        # ---------------------------------------------------------
        sim_bg = Rectangle(width=4, height=3, color=GREY_E, fill_opacity=0.2).shift(LEFT * 3 + DOWN * 0.5)
        sim_label = safe_text("Simulation", 24, TEXT_COLOR).next_to(sim_bg, UP)
        
        ball = make_ball().scale(1.2).move_to(sim_bg.get_center() + LEFT * 0.8 + UP * 0.4)
        box = make_box().scale(1.2).move_to(sim_bg.get_center() + RIGHT * 0.8 + DOWN * 0.4)
        
        self.play(FadeIn(sim_bg), Write(sim_label), run_time=0.8)
        self.play(GrowFromCenter(ball), GrowFromCenter(box), run_time=1.0)
        self.wait(4.2) # Total: 10.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Real World Complexity (10.0 - 18.0)
        # "Nhưng thế giới thực phức tạp hơn rất nhiều... texture, bóng đổ..."
        # ---------------------------------------------------------
        real_bg = Rectangle(width=4, height=3, color=ACCENT_COLOR, fill_opacity=0.1).shift(RIGHT * 3 + DOWN * 0.5)
        real_label = safe_text("Real World", 24, ACCENT_COLOR).next_to(real_bg, UP)
        
        # Complex textures/details representation
        complex_dots = VGroup(*[
            Dot(radius=0.03, color=interpolate_color(BLUE, WHITE, np.random.rand()))
            .move_to(real_bg.get_center() + np.random.randn(3) * 0.8)
            for _ in range(50)
        ])
        
        self.play(FadeIn(real_bg), Write(real_label), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d) for d in complex_dots], lag_ratio=0.01), run_time=1.5)
        self.wait(5.7) # Total: 18.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: The Barrier / Gap (18.0 - 24.0)
        # "Nếu chỉ học trên môi trường mô phỏng, mô hình sẽ thất bại khi ra thực tế."
        # ---------------------------------------------------------
        barrier = Line(UP * 2, DOWN * 3, color=MAROON, stroke_width=6).move_to(ORIGIN)
        cross = Cross(sim_bg, stroke_color=RED, stroke_width=8).scale(0.8)
        
        self.play(Create(barrier), run_time=1.0)
        self.play(Create(cross), run_time=0.8)
        self.wait(4.2) # Total: 24.0s
        
        # ---------------------------------------------------------
        # SEGMENT 5: AI Engineers solving the gap (24.0 - 29.928)
        # ---------------------------------------------------------
        engineer = make_robot().scale(1.0).move_to(UP * 2.5 + RIGHT * 5)
        bridge = Arrow(sim_bg.get_right(), real_bg.get_left(), color=GOLD_A, buff=0.1)
        
        self.play(FadeIn(engineer, shift=LEFT), Create(bridge), run_time=1.2)
        self.play(Indicate(bridge, color=GOLD_A), run_time=1.0)
        
        self.wait(2.728) # Total: 28.928s




        # --- END SCENE 010 ---


        # --- START SCENE 011 ---

        # Audio
            
        # Total duration target: 30.504s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Ảnh gốc đi qua mạng biến đổi thị giác để tạo ra các đặc trưng ngữ nghĩa."
        # ---------------------------------------------------------
        title = safe_text("Vai trò của ViT và DINO", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = safe_text("Image -> ViT -> Semantic Features", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(2.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 4.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: ViT Processing (4.0 - 12.0)
        # "Để giải quyết khoảng cách này, chúng ta không dùng điểm ảnh thô trực tiếp..."
        # ---------------------------------------------------------
        raw_img = make_pixel_grid(6, 6, 0.3).shift(LEFT * 4 + DOWN * 0.5)
        vit_block = RoundedRectangle(width=2.5, height=2.0, corner_radius=0.2, color=ACCENT_COLOR, fill_opacity=0.3).shift(DOWN * 0.5)
        vit_label = safe_text("ViT (Transformer)", 20, TEXT_COLOR).move_to(vit_block)
        
        arrow1 = Arrow(raw_img.get_right(), vit_block.get_left(), color=GOLD_A)
        
        self.play(FadeIn(raw_img, shift=RIGHT), run_time=1.0)
        self.play(Create(arrow1), FadeIn(vit_block), Write(vit_label), run_time=1.2)
        self.wait(3.8) # Total: 10.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: DINO Features (10.0 - 20.0)
        # "Thay vào đó, ta sử dụng mạng biến đổi thị giác làm nền tảng. Các mô hình tự giám sát như Đi nô..."
        # ---------------------------------------------------------
        features = VGroup(*[
            Circle(radius=0.15, color=GOLD_A, fill_opacity=0.8)
            
            .shift(RIGHT * 4 + UP * (1.2 - i * 0.6) + DOWN * 0.5)
            for i in range(5)
        ])
        feat_label = safe_text("Semantic Features (DINO)", 18, GOLD_A).next_to(features, UP)
        
        arrow2 = Arrow(vit_block.get_right(), features.get_left(), color=GOLD_A)
        
        self.play(Create(arrow2), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(f, scale=1.5) for f in features], lag_ratio=0.1), Write(feat_label), run_time=1.5)
        self.wait(5.5) # Total: 18.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Slot Attention (18.0 - 26.0)
        # "Khi slot attention hoạt động trên các đặc trưng cao cấp này, nó chạy tốt hơn..."
        # ---------------------------------------------------------
        slots = VGroup(*[make_slot(f"Slot {i+1}").scale(0.8).shift(RIGHT * 6 + UP * (0.8 - i * 1.0) + DOWN * 0.5) for i in range(2)])
        
        lines = VGroup(*[Line(features[i].get_right(), slots[i//3].get_left(), stroke_opacity=0.3, color=WHITE) for i in range(5)])
        
        self.play(FadeIn(slots, shift=LEFT), Create(lines), run_time=1.2)
        self.play(Indicate(slots, color=GOLD_A), run_time=1.0)
        self.wait(5.8) # Total: 26.0s
        
        # ---------------------------------------------------------
        # SEGMENT 5: Global Attention (26.0 - 30.504)
        # "Kiến trúc Transformer với cơ chế tự chú ý toàn cục..."
        # ---------------------------------------------------------
        global_lines = VGroup(*[
            Line(raw_img[i].get_center(), vit_block.get_center(), stroke_opacity=0.1, color=ACCENT_COLOR)
            for i in range(0, 36, 4)
        ])
        
        self.play(Create(global_lines), vit_block.animate.set_fill(opacity=0.6), run_time=1.5)
        self.wait(2.004) # Total: 29.504s



        

        # --- END SCENE 011 ---


        # --- START SCENE 012 ---

        # Audio
            
        # Total duration target: 32.616s
        
        # Constants
        BG_COLOR = "#0D1117"
        TITLE_COLOR = "#FFD700"  
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        self.camera.background_color = BG_COLOR
        
        # ---------------------------------------------------------
        # SEGMENT 1: Introduction (Start: 0.0s)
        # "Sai số tái tạo đặc trưng bằng bình phương độ chuẩn hiệu véc tơ đặc trưng V I T và đặc trưng giải mã."
        # ---------------------------------------------------------
        title = safe_text("DINOSAUR: Tái tạo đặc trưng", 32, TITLE_COLOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(title)
        
        formula = MathTex(r"L = \|F_{ViT} - F_{decoded}\|^2", font_size=42, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.2)
        self.wait(3.3)
        self.play(FadeOut(formula), run_time=0.5) # Total: 5.0s
        
        # ---------------------------------------------------------
        # SEGMENT 2: DINO vs Pixels (5.0 - 13.0)
        # "Mô hình Đi nô sau là một bước tiến vô cùng quan trọng gần đây..."
        # ---------------------------------------------------------
        pixel_grid = Square(side_length=1.5, color=GREY_D, fill_opacity=0.2).shift(LEFT * 4 + DOWN * 0.5)
        pixel_label = safe_text("Raw Pixels", 18, TEXT_COLOR).next_to(pixel_grid, UP)
        
        cross = Cross(pixel_grid, stroke_color=RED, stroke_width=6)
        
        dino_feat = Circle(radius=0.75, color=GOLD_A, fill_opacity=0.4).shift(LEFT * 1 + DOWN * 0.5)
        dino_label = safe_text("DINO Features", 18, GOLD_A).next_to(dino_feat, UP)
        
        self.play(FadeIn(pixel_grid), Write(pixel_label), run_time=0.8)
        self.play(Create(cross), run_time=0.6)
        self.play(FadeIn(dino_feat, shift=RIGHT), Write(dino_label), run_time=1.0)
        self.wait(5.6) # Total: 13.0s
        
        # ---------------------------------------------------------
        # SEGMENT 3: Semantic Focus (13.0 - 22.0)
        # "Việc này giúp mô hình tập trung vào cấu trúc ngữ nghĩa... bỏ qua chi tiết thừa thãi..."
        # ---------------------------------------------------------
        tree_trunk = Rectangle(width=0.4, height=2.0, color="#8B4513", fill_opacity=0.8).shift(RIGHT * 3 + DOWN * 1.0)
        leaves = Circle(radius=0.8, color=GREEN, fill_opacity=0.6).next_to(tree_trunk, UP, buff=0)
        tree = VGroup(tree_trunk, leaves)
        
        blur_tree = tree.copy().set_opacity(0.2).shift(LEFT * 0.5)
        semantic_outline = tree.copy().set_fill(opacity=0).set_stroke(color=GOLD_A, width=4)
        
        self.play(FadeIn(tree, shift=UP), run_time=1.0)
        self.play(tree.animate.set_opacity(0.2), FadeIn(semantic_outline), run_time=1.5)
        self.wait(6.5) # Total: 22.0s
        
        # ---------------------------------------------------------
        # SEGMENT 4: Object Grouping (22.0 - 32.616)
        # "Nhờ vậy, quá trình chia slot trở nên ổn định... gom cụm các bộ phận thành vật thể lớn..."
        # ---------------------------------------------------------
        car_parts = VGroup(
            RoundedRectangle(width=1.0, height=0.4).shift(LEFT * 0.5),
            RoundedRectangle(width=1.0, height=0.4).shift(RIGHT * 0.5),
            Circle(radius=0.2).shift(DOWN * 0.4 + LEFT * 0.4),
            Circle(radius=0.2).shift(DOWN * 0.4 + RIGHT * 0.4)
        ).scale(0.8).move_to(DOWN * 1.5 + RIGHT * 3)
        
        car_full = make_car().scale(0.8).move_to(car_parts)
        
        slot_box = make_slot("Slot: Car", color=ACCENT_COLOR).scale(1.2).move_to(RIGHT * 5 + DOWN * 0.5)
        
        self.play(FadeIn(car_parts), run_time=1.0)
        self.play(ReplacementTransform(car_parts, car_full), run_time=1.2)
        self.play(Create(Arrow(car_full.get_right(), slot_box.get_left(), color=GOLD_A)), FadeIn(slot_box), run_time=1.0)
        
        self.wait(6.416) # Total: 31.616s




        # --- END SCENE 012 ---


        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)