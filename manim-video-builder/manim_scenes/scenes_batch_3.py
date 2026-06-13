from __future__ import annotations

from manim import *

# --- Style Constants ---
BG_COLOR = "#0F1117"
TITLE_YELLOW = "#F2C94C"
TEAL = "#4ECDC4"
ORANGE = "#FF6B4A"
BLUE = "#3A86FF"
RED = "#D76D77"
GREEN = "#6BCB77"
GREY = "#444444"

config.background_color = BG_COLOR


class EduScene(Scene):
    def create_title(self, text):
        title = Text(text, font_size=32, color=TITLE_YELLOW, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        underline = Line(LEFT, RIGHT, color=GREY, stroke_width=1).scale(6).next_to(title, DOWN, buff=0.2)
        return VGroup(title, underline)

    def create_formula(self, tex):
        formula = MathTex(tex, font_size=36, color=TITLE_YELLOW)
        formula.to_edge(DOWN, buff=0.5)
        return formula


# --- Scene 011 ---
class Scene011(EduScene):
    def construct(self):
        title = self.create_title("Vai trò của V I T và Đi nô")
        formula = self.create_formula(r"\text{Image} \to \text{ViT} \to \text{Semantic Features}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Input Image (Grid)
        img = Square(2, color=TEAL, fill_opacity=0.1).shift(LEFT * 4)
        label_img = Text("Ảnh gốc", font_size=18).next_to(img, UP)

        # 2. ViT Stack (Filter Layers)
        layers = VGroup(*[
            Rectangle(width=1, height=1.5, color=BLUE, fill_opacity=0.2).shift(LEFT * 1 + RIGHT * i * 0.3)
            for i in range(4)
        ])
        label_vit = Text("ViT Layers", font_size=18, color=BLUE).next_to(layers, UP)

        # 3. Semantic Heatmap
        heatmap = VGroup(*[
            Square(side_length=0.25, stroke_width=0, fill_opacity=np.random.rand()).set_fill(color=interpolate_color(BLUE, RED, np.random.rand()))
            for _ in range(64)
        ]).arrange_in_grid(8, 8, buff=0).shift(RIGHT * 4)
        label_heat = Text("Đặc trưng ngữ nghĩa", font_size=18, color=ORANGE).next_to(heatmap, UP)

        self.play(FadeIn(img), Write(label_img))
        self.play(Create(layers), Write(label_vit))
        
        # Propagation
        arrow = Arrow(img.get_right(), layers.get_left(), color=GREY)
        arrow2 = Arrow(layers.get_right(), heatmap.get_left(), color=GREY)
        
        self.play(Create(arrow), Create(arrow2))
        self.play(LaggedStartMap(FadeIn, heatmap, lag_ratio=0.01), Write(label_heat))
        self.wait(2)


# --- Scene 012 ---
class Scene012(EduScene):
    def construct(self):
        title = self.create_title("Đi nô sau và hướng tái tạo đặc trưng")
        formula = self.create_formula(r"\text{Loss} = ||F_{\text{ViT}} - F_{\text{decoded}}||^2")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Detail vs Structure
        detail_obj = VGroup(
            Circle(radius=1, color=TEAL, fill_opacity=0.1),
            *[Dot(radius=0.05, color=WHITE, fill_opacity=0.5).shift(np.random.randn(3) * 0.8) for _ in range(30)]
        ).shift(LEFT * 3)
        label_det = Text("Chi tiết thừa (Nhiễu)", font_size=18).next_to(detail_obj, UP)

        structure_obj = Circle(radius=1, color=TEAL, stroke_width=8, fill_opacity=0.4).shift(RIGHT * 3)
        label_str = Text("Cấu trúc ngữ nghĩa", font_size=18, color=TEAL).next_to(structure_obj, UP)

        self.play(FadeIn(detail_obj), Write(label_det))
        self.wait(1)
        
        # Focus/Filtering
        self.play(ReplacementTransform(detail_obj, structure_obj), Write(label_str), run_time=2)
        self.play(Indicate(structure_obj, color=GOLD_A))
        self.wait(2)


# --- Scene 013 ---
class Scene013(EduScene):
    def construct(self):
        title = self.create_title("Học quan hệ giữa các đối tượng")
        formula = self.create_formula(r"r_{ij} = g(z_i, z_j)")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Independent Objects
        obj1 = Circle(radius=0.5, color=ORANGE, fill_opacity=0.3).shift(UP * 1.5 + LEFT * 2)
        obj2 = Square(side_length=0.8, color=TEAL, fill_opacity=0.3).shift(DOWN * 1)
        obj3 = Triangle(color=BLUE, fill_opacity=0.3).scale(0.5).shift(UP * 1.5 + RIGHT * 2)

        self.play(FadeIn(obj1), FadeIn(obj2), FadeIn(obj3))
        self.wait(1)

        # 2. Semantic Relations (Graph)
        rel1 = Arrow(obj1.get_bottom(), obj2.get_top(), color=GREY, buff=0.1)
        rel1_label = Text("Đặt trên", font_size=16, color=WHITE).next_to(rel1, LEFT)
        
        rel2 = Arrow(obj3.get_bottom(), obj2.get_top(), color=GREY, buff=0.1)
        rel2_label = Text("Gần", font_size=16, color=WHITE).next_to(rel2, RIGHT)

        self.play(Create(rel1), Write(rel1_label))
        self.play(Create(rel2), Write(rel2_label))
        
        # Highlight relationship
        self.play(obj1.animate.set_color(GOLD_A), obj2.animate.set_color(GOLD_A), rel1.animate.set_color(GOLD_A))
        self.wait(2)


# --- Scene 014 ---
class Scene014(EduScene):
    def construct(self):
        title = self.create_title("Tương quan thống kê và hạn chế")
        formula = self.create_formula(r"P(Y | X)")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Correlation (Ghost Link)
        ball = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).shift(LEFT * 4)
        box = Square(side_length=0.6, color=TEAL, fill_opacity=0.8).shift(LEFT * 1)
        
        link = DashedLine(ball.get_right(), box.get_left(), color=GREY, stroke_opacity=0.5)
        label_corr = Text("Tương quan (Đi cùng nhau)", font_size=18).next_to(link, UP)

        self.play(FadeIn(ball), FadeIn(box), Create(link), Write(label_corr))
        
        # Movement together
        self.play(ball.animate.shift(RIGHT * 2), box.animate.shift(RIGHT * 2), run_time=2)
        self.wait(1)

        # 2. The Hidden Confounder (Robot Hand)
        hand = Text("🤖", font_size=40).next_to(box, DOWN, buff=1.5)
        mystery_line = DashedLine(hand.get_top(), box.get_bottom(), color=RED)
        
        self.play(FadeIn(hand, shift=UP))
        self.play(Create(mystery_line))
        self.play(Flash(hand, color=RED))
        
        label_hidden = Text("Yếu tố ẩn (Confounder)", font_size=18, color=RED).next_to(hand, DOWN)
        self.play(Write(label_hidden))
        self.wait(2)


# --- Scene 015 ---
class Scene015(EduScene):
    def construct(self):
        title = self.create_title("Nhân quả: câu hỏi về sự can thiệp")
        formula = self.create_formula(r"P(Y | \text{do}(X = x))")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. The 'do' Button
        button = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.2, color=ORANGE, fill_opacity=0.3)
        do_label = Text("do(X)", font_size=24, color=ORANGE).move_to(button)
        btn_group = VGroup(button, do_label).shift(LEFT * 3)

        # 2. System State
        state_x = Circle(radius=0.5, color=BLUE, fill_opacity=0.2).shift(RIGHT * 1)
        label_x = Text("X (Action)", font_size=18).next_to(state_x, UP)
        
        state_y = Circle(radius=0.5, color=TEAL, fill_opacity=0.2).shift(RIGHT * 4)
        label_y = Text("Y (Result)", font_size=18).next_to(state_y, UP)

        self.play(FadeIn(btn_group), FadeIn(state_x), Write(label_x), FadeIn(state_y), Write(label_y))
        
        # Interaction
        cursor = Text("👆", font_size=30).next_to(button, UR)
        self.play(FadeIn(cursor))
        self.play(button.animate.scale(0.9).set_color(WHITE), run_time=0.2)
        self.play(button.animate.scale(1.1).set_color(ORANGE), run_time=0.2)
        
        # Trigger Effect
        arrow = Arrow(state_x.get_right(), state_y.get_left(), color=GOLD_A)
        self.play(Create(arrow), state_x.animate.set_color(ORANGE), run_time=0.5)
        self.play(state_y.animate.set_color(GREEN).scale(1.2), Flash(state_y, color=GREEN))
        
        self.wait(2)
