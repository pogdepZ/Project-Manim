from __future__ import annotations
from manim import *
from objectified_library import *

class Scene011(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Vai trò của V I T và Đi nô")
        formula = self.create_formula(r"\text{Image} \to \text{ViT} \to \text{Semantic Features}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        img = create_car_icon(scale=0.8).shift(LEFT*5)
        self.play(FadeIn(img), run_time=duration * 0.2)

        stack = VGroup(*[Rectangle(width=0.8, height=1.2, color=BLUE, fill_opacity=0.15).shift(LEFT*1 + RIGHT*i*0.4) for i in range(4)])
        self.play(Create(stack), run_time=duration * 0.2)

        heatmap = create_feature_grid(7, 7).shift(RIGHT*4)
        for sq in heatmap:
            sq.set_fill(color=interpolate_color(ManimColor(BLUE), ManimColor(ORANGE), np.random.rand()))
            
        self.play(img.copy().animate.move_to(stack.get_left()), run_time=duration * 0.1)
        self.play(ReplacementTransform(stack.copy(), heatmap), run_time=duration * 0.2)
        self.auto_wait(heatmap)

class Scene012(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Đi nô sau và tái tạo đặc trưng")
        formula = self.create_formula(r"\text{Feature Reconstruction Loss}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        messy = VGroup(create_person(scale=1.2, color=GREY_OBJ), *[Dot(radius=0.03, color=WHITE, fill_opacity=0.3).shift(np.random.randn(3)*0.7) for _ in range(40)]).shift(LEFT*3)
        label_messy = Text("Chi tiết thừa", font_size=18, color=GREY_TEXT).next_to(messy, UP)

        clean = create_person(scale=1.2, color=TEAL).set_stroke(width=8, opacity=0.5).shift(RIGHT*3)
        label_clean = Text("Cấu trúc ngữ nghĩa", font_size=18, color=TEAL).next_to(clean, UP)

        self.play(FadeIn(messy), Write(label_messy), run_time=duration * 0.3)
        self.play(ReplacementTransform(messy, clean), Write(label_clean), run_time=duration * 0.4)
        self.auto_wait(clean)

class Scene013(EduScene):
    def construct(self):
        duration = self.get_duration(28.0)
        title = self.create_title("Học quan hệ đối tượng")
        formula = self.create_formula(r"r_{ij} = g(z_i, z_j)")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        p = create_person(scale=0.8).shift(LEFT*3 + UP*1)
        lt = create_laptop(scale=0.5).shift(ORIGIN + DOWN*1)
        desk = Line(LEFT*2, RIGHT*2, color=GREY_OBJ).next_to(lt, DOWN, buff=0)

        self.play(FadeIn(p), FadeIn(lt), Create(desk), run_time=duration * 0.3)

        arrow1 = Arrow(p.get_bottom(), lt.get_top(), color=GOLD_A, buff=0.1)
        label1 = Text("Làm việc với", font_size=16).next_to(arrow1, RIGHT)

        self.play(Create(arrow1), Write(label1), run_time=duration * 0.3)
        self.auto_wait(arrow1)

class Scene014(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Tương quan thống kê")
        formula = self.create_formula(r"P(Y | X)")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        ball = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).shift(LEFT*4)
        box = Square(0.6, color=TEAL, fill_opacity=0.4).shift(LEFT*1)
        ghost_link = DashedLine(ball.get_right(), box.get_left(), color=GREY_OBJ, stroke_opacity=0.5)

        self.play(FadeIn(ball), FadeIn(box), Create(ghost_link), run_time=duration * 0.2)
        
        # Loop movement
        self.play(ball.animate.shift(RIGHT*1.5), box.animate.shift(RIGHT*1.5), run_time=duration * 0.2)
        self.play(ball.animate.shift(LEFT*1.5), box.animate.shift(LEFT*1.5), run_time=duration * 0.2)
        self.play(ball.animate.shift(RIGHT*1.5), box.animate.shift(RIGHT*1.5), run_time=duration * 0.2)

        robot = Text("🤖", font_size=40).next_to(box, DOWN, buff=1)
        self.play(FadeIn(robot, shift=UP), run_time=duration * 0.1)
        self.auto_wait(robot)

class Scene015(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Nhân quả: sự can thiệp (do)")
        formula = self.create_formula(r"P(Y | \text{do}(X = x))")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        panel = RoundedRectangle(width=2, height=1, color=ORANGE, fill_opacity=0.2).shift(LEFT*4)
        btn = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).move_to(panel)
        label_do = Text("DO", font_size=20, weight=BOLD).move_to(btn)
        hand = create_intervention_hand().next_to(btn, DR)
        
        self.play(Create(panel), FadeIn(btn), Write(label_do), FadeIn(hand), run_time=duration * 0.2)

        ball = Circle(radius=0.3, color=BLUE, fill_opacity=0.8).shift(RIGHT*1)
        box = Square(0.6, color=TEAL, fill_opacity=0.4).shift(RIGHT*4)
        self.play(FadeIn(ball), FadeIn(box), run_time=duration * 0.2)

        self.play(hand.animate.move_to(btn), btn.animate.scale(0.8), run_time=duration * 0.1)
        self.play(btn.animate.scale(1.25), run_time=duration * 0.1)
        
        self.play(ball.animate.move_to(box.get_left()), run_time=duration * 0.1, rate_func=rate_functions.ease_in_sine)
        self.play(box.animate.shift(RIGHT*1.5), Flash(box, color=GREEN), run_time=duration * 0.1)
        self.auto_wait(box)