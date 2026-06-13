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


# --- Scene 006 ---
class Scene006(EduScene):
    def construct(self):
        title = self.create_title("Object slots là gì?")
        formula = self.create_formula(r"Z = \{z_1, z_2, \dots, z_K\}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Trays (Slots)
        trays = VGroup(*[
            RoundedRectangle(width=1.5, height=1, corner_radius=0.2, color=BLUE, fill_opacity=0.1)
            for _ in range(3)
        ]).arrange(RIGHT, buff=1)

        self.play(LaggedStartMap(Create, trays, lag_ratio=0.2))
        self.wait(1)

        # 2. Fill with Objects
        ball = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).move_to(trays[0])
        box = Square(side_length=0.5, color=TEAL, fill_opacity=0.8).move_to(trays[1])
        
        self.play(GrowFromCenter(ball), GrowFromCenter(box))
        self.wait(1)

        # 3. Permutation Invariance (Swap)
        self.play(
            ball.animate.move_to(trays[1]),
            box.animate.move_to(trays[0]),
            trays[0].animate.set_color(TEAL),
            trays[1].animate.set_color(ORANGE),
            run_time=2
        )
        self.play(Indicate(trays[0]), Indicate(trays[1]))
        self.wait(2)


# --- Scene 007 ---
class Scene007(EduScene):
    def construct(self):
        title = self.create_title("Cơ chế chú ý theo slot trực giác")
        formula = self.create_formula(r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Input Features (Dots)
        features = VGroup(*[
            Dot(radius=0.08, color=TEAL, fill_opacity=0.5).shift(LEFT * 3 + np.random.randn(3) * 1.5)
            for _ in range(40)
        ]).shift(UP * 0.5)

        # 2. Slots (Circles)
        slots = VGroup(*[
            Circle(radius=0.5, color=BLUE, fill_opacity=0.2).shift(RIGHT * 3 + UP * i - UP * 1)
            for i in range(3)
        ])

        self.play(FadeIn(features), Create(slots))
        self.wait(1)

        # 3. Searchlights (Attention)
        rays = VGroup()
        for slot in slots:
            for _ in range(5):
                target = features[np.random.randint(len(features))]
                ray = Line(slot.get_left(), target.get_center(), color=BLUE, stroke_width=1, stroke_opacity=0.4)
                rays.add(ray)

        self.play(LaggedStartMap(Create, rays, lag_ratio=0.02), run_time=2)
        
        # Iterative update (Flash)
        for _ in range(2):
            self.play(
                slots.animate.set_stroke(ORANGE, width=6),
                rays.animate.set_stroke(ORANGE, opacity=0.8),
                run_time=0.5
            )
            self.play(
                slots.animate.set_stroke(BLUE, width=2),
                rays.animate.set_stroke(BLUE, opacity=0.4),
                run_time=0.5
            )
        
        self.wait(2)


# --- Scene 008 ---
class Scene008(EduScene):
    def construct(self):
        title = self.create_title("Quá trình cạnh tranh giữa các slot")
        formula = self.create_formula(r"\text{Competition} \to \text{Disentanglement}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Jigsaw Pieces
        pieces = VGroup(*[
            Square(side_length=0.4, color=GREY, fill_opacity=0.3)
            for _ in range(20)
        ]).arrange_in_grid(4, 5, buff=0.1).shift(LEFT * 2)

        # 2. Slot Agents
        agents = VGroup(
            Text("Slot A", font_size=20, color=ORANGE).shift(RIGHT * 3 + UP * 1),
            Text("Slot B", font_size=20, color=TEAL).shift(RIGHT * 3 + DOWN * 1)
        )

        self.play(FadeIn(pieces), Write(agents))
        self.wait(1)

        # 3. Tug of war (Lines)
        piece = pieces[7]
        line_a = Line(agents[0].get_left(), piece.get_center(), color=ORANGE)
        line_b = Line(agents[1].get_left(), piece.get_center(), color=TEAL)

        self.play(Create(line_a), Create(line_b))
        self.play(piece.animate.scale(1.2).set_color(WHITE))
        
        # Win-Loss
        self.play(
            line_b.animate.set_stroke(opacity=0),
            line_a.animate.set_stroke(width=5),
            piece.animate.set_color(ORANGE).move_to(agents[0].get_bottom() + DOWN * 0.5),
            run_time=1.5
        )
        self.play(Flash(piece, color=ORANGE))
        self.wait(2)


# --- Scene 009 ---
class Scene009(EduScene):
    def construct(self):
        title = self.create_title("Reconstruction và mask: kiểm tra việc học")
        formula = self.create_formula(r"\hat{x} = \sum_{k} (m_k \cdot \hat{x}_k)")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Components (Slot outputs)
        comp1 = VGroup(Circle(radius=0.5, color=ORANGE, fill_opacity=0.8), Text("Mask 1", font_size=15).next_to(ORIGIN, DOWN)).shift(LEFT * 3)
        comp2 = VGroup(Square(side_length=0.8, color=TEAL, fill_opacity=0.8), Text("Mask 2", font_size=15).next_to(ORIGIN, DOWN)).shift(LEFT * 1)
        comp3 = VGroup(Triangle(color=BLUE, fill_opacity=0.8).scale(0.6), Text("Mask 3", font_size=15).next_to(ORIGIN, DOWN)).shift(RIGHT * 1)

        self.play(FadeIn(comp1), FadeIn(comp2), FadeIn(comp3))
        self.wait(1)

        # 2. Summation (Reconstruction)
        plus = Text("+", font_size=30).move_to(LEFT * 2)
        plus2 = Text("+", font_size=30).move_to(ORIGIN)
        equal = Text("=", font_size=30).move_to(RIGHT * 2)

        final_img = VGroup(
            Circle(radius=0.5, color=ORANGE, fill_opacity=0.8).shift(UP * 0.2),
            Square(side_length=0.8, color=TEAL, fill_opacity=0.8).shift(DOWN * 0.2 + LEFT * 0.2),
            Triangle(color=BLUE, fill_opacity=0.8).scale(0.6).shift(RIGHT * 0.3)
        ).shift(RIGHT * 4)

        self.play(Write(plus), Write(plus2), Write(equal))
        self.play(
            ReplacementTransform(comp1[0].copy(), final_img[0]),
            ReplacementTransform(comp2[0].copy(), final_img[1]),
            ReplacementTransform(comp3[0].copy(), final_img[2]),
            run_time=2
        )
        self.play(final_img.animate.set_stroke(WHITE, width=2))
        self.wait(2)


# --- Scene 010 ---
class Scene010(EduScene):
    def construct(self):
        title = self.create_title("Dữ liệu mô phỏng và thế giới thực")
        formula = self.create_formula(r"\text{Synthetic} \to \text{Real World}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Synthetic World (Simple)
        left_side = RoundedRectangle(width=5, height=4, color=GREY, fill_opacity=0.05).shift(LEFT * 3)
        label_syn = Text("Mô phỏng (Dễ)", font_size=20, color=TEAL).next_to(left_side, UP)
        
        shapes = VGroup(
            Circle(radius=0.3, color=RED, fill_opacity=0.8).move_to(left_side.get_center() + UP),
            Square(side_length=0.5, color=BLUE, fill_opacity=0.8).move_to(left_side.get_center() + DOWN + LEFT),
            Triangle(color=GREEN, fill_opacity=0.8).scale(0.4).move_to(left_side.get_center() + RIGHT)
        )

        self.play(Create(left_side), Write(label_syn), FadeIn(shapes))
        self.wait(1)

        # 2. Real World (Complex/Noisy)
        right_side = RoundedRectangle(width=5, height=4, color=GREY, fill_opacity=0.05).shift(RIGHT * 3)
        label_real = Text("Thế giới thực (Khó)", font_size=20, color=ORANGE).next_to(right_side, UP)

        # Simulated "Complexity"
        noise = VGroup(*[
            Dot(radius=0.02, color=WHITE, fill_opacity=0.2).move_to(right_side.get_center() + np.random.randn(3) * 1.8)
            for _ in range(100)
        ])
        complex_shapes = VGroup(*[
            Polygon(*[np.random.randn(3) * 0.4 for _ in range(5)], color=GREY, fill_opacity=0.3).move_to(right_side.get_center() + np.random.randn(3) * 1.2)
            for _ in range(8)
        ])

        self.play(Create(right_side), Write(label_real))
        self.play(FadeIn(noise), FadeIn(complex_shapes))
        
        # Barrier
        barrier = Line(UP * 2, DOWN * 2, color=RED, stroke_width=8).move_to(ORIGIN)
        self.play(Create(barrier))
        self.play(Flash(barrier, color=RED))
        self.wait(2)
