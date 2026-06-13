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


# --- Scene 016 ---
class Scene016(EduScene):
    def construct(self):
        title = self.create_title("Sức mạnh của hành động can thiệp")
        formula = self.create_formula(r"\text{Observation vs Intervention}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # Split screen
        line = Line(UP * 2, DOWN * 2, color=GREY)
        self.play(Create(line))

        # Left: Observation
        obs_icon = Text("🔭", font_size=40).shift(LEFT * 3 + UP * 0.5)
        obs_label = Text("Quan sát thụ động", font_size=18).next_to(obs_icon, DOWN)
        
        cars = VGroup(*[Text("🚗", font_size=20).shift(LEFT * 5 + RIGHT * i * 0.8) for i in range(3)]).shift(DOWN * 1)
        
        self.play(FadeIn(obs_icon), Write(obs_label))
        self.play(cars.animate.shift(RIGHT * 2), run_time=2, rate_func=linear)

        # Right: Intervention
        int_icon = Text("🛑", font_size=40).shift(RIGHT * 3 + UP * 0.5)
        int_label = Text("Can thiệp chủ động", font_size=18, color=ORANGE).next_to(int_icon, DOWN)
        
        stop_cars = VGroup(*[Text("🚗", font_size=20).shift(RIGHT * 1 + RIGHT * i * 0.8) for i in range(3)]).shift(DOWN * 1)
        
        self.play(FadeIn(int_icon), Write(int_label))
        self.play(stop_cars.animate.shift(RIGHT * 1), run_time=1, rate_func=linear)
        self.play(Flash(int_icon, color=ORANGE))
        self.play(stop_cars.animate.scale(1.1).set_color(RED))
        
        self.wait(2)


# --- Scene 017 ---
class Scene017(EduScene):
    def construct(self):
        title = self.create_title("Mô hình nhân quả cấu trúc S C M")
        formula = self.create_formula(r"X_i = f_i(PA_i, U_i)")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Blueprint Nodes
        node_u = Circle(radius=0.4, color=GREY, fill_opacity=0.1).shift(UP * 1.5 + LEFT * 1)
        label_u = MathTex("U_i", color=GREY).move_to(node_u)
        
        node_pa = Circle(radius=0.4, color=BLUE, fill_opacity=0.1).shift(UP * 1.5 + RIGHT * 1)
        label_pa = MathTex("PA_i", color=BLUE).move_to(node_pa)
        
        node_xi = Circle(radius=0.6, color=TEAL, fill_opacity=0.2).shift(DOWN * 1)
        label_xi = MathTex("X_i", color=TEAL).move_to(node_xi)

        # 2. Mechanism (Gears/Lines)
        arrow1 = Arrow(node_u.get_bottom(), node_xi.get_top(), color=GREY)
        arrow2 = Arrow(node_pa.get_bottom(), node_xi.get_top(), color=BLUE)

        self.play(FadeIn(node_u), Write(label_u), FadeIn(node_pa), Write(label_pa))
        self.play(Create(arrow1), Create(arrow2))
        self.play(GrowFromCenter(node_xi), Write(label_xi))
        
        # Flash the mechanism
        self.play(Indicate(node_xi, color=GOLD_A))
        self.wait(2)


# --- Scene 018 ---
class Scene018(EduScene):
    def construct(self):
        title = self.create_title("Ví dụ vật lý: quả bóng va chạm cái hộp")
        formula = self.create_formula(r"\text{Collision Graph: Ball} \to \text{Force} \to \text{Box}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Objects
        ball = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).shift(LEFT * 5 + DOWN * 1)
        box = Square(side_length=0.7, color=TEAL, fill_opacity=0.4).shift(RIGHT * 1 + DOWN * 1)
        floor = Line(LEFT * 6, RIGHT * 6, color=GREY).next_to(box, DOWN, buff=0)

        self.play(Create(floor), FadeIn(ball), FadeIn(box))
        
        # 2. Rolling
        self.play(ball.animate.shift(RIGHT * 5.3), run_time=1.5, rate_func=slow_into)
        
        # 3. Impact
        force_vec = Arrow(ball.get_center(), ball.get_center() + RIGHT * 1.5, color=RED, buff=0)
        self.play(Create(force_vec), run_time=0.2)
        self.play(Flash(ball.get_right(), color=RED, line_length=0.4))
        
        # 4. Reaction
        self.play(
            box.animate.shift(RIGHT * 2.5),
            ball.animate.shift(LEFT * 0.2),
            FadeOut(force_vec),
            run_time=1,
            rate_func=decelerate
        )
        self.wait(2)


# --- Scene 019 ---
class Scene019(EduScene):
    def construct(self):
        title = self.create_title("Phân tích lực và động lượng")
        formula = self.create_formula(r"F = m \cdot a, \quad \Delta p = F \cdot \Delta t")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Scale Comparison
        small_ball = Circle(radius=0.2, color=ORANGE, fill_opacity=0.5).shift(LEFT * 3 + UP * 1)
        large_ball = Circle(radius=0.5, color=ORANGE, fill_opacity=0.8).shift(LEFT * 3 + DOWN * 1)
        
        label_small = Text("m nhỏ", font_size=18).next_to(small_ball, LEFT)
        label_large = Text("m lớn", font_size=18, color=ORANGE, weight=BOLD).next_to(large_ball, LEFT)

        self.play(FadeIn(small_ball), Write(label_small), FadeIn(large_ball), Write(label_large))
        
        # 2. Resulting Force
        f_small = Arrow(small_ball.get_right(), small_ball.get_right() + RIGHT * 0.5, color=RED)
        f_large = Arrow(large_ball.get_right(), large_ball.get_right() + RIGHT * 2.5, color=RED, stroke_width=8)
        
        self.play(Create(f_small), Create(f_large))
        self.play(Indicate(f_large, color=GOLD_A))
        self.wait(2)


# --- Scene 020 ---
class Scene020(EduScene):
    def construct(self):
        title = self.create_title("Tại sao trung tâm đối tượng hỗ trợ nhân quả?")
        formula = self.create_formula(r"\text{Slots} \to \text{Causal Graph} \to \text{Prediction}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. The Bridge
        slots = VGroup(
            Circle(radius=0.6, color=BLUE, fill_opacity=0.2),
            Circle(radius=0.6, color=TEAL, fill_opacity=0.2)
        ).arrange(RIGHT, buff=3)
        
        label_s1 = Text("Slot 1 (Ball)", font_size=18).next_to(slots[0], UP)
        label_s2 = Text("Slot 2 (Box)", font_size=18).next_to(slots[1], UP)

        self.play(Create(slots), Write(label_s1), Write(label_s2))
        self.wait(1)

        # 2. Causal Arrow
        causal_arrow = Arrow(slots[0].get_right(), slots[1].get_left(), color=GOLD_A)
        causal_label = Text("Quy luật vật lý", font_size=18, color=GOLD_A).next_to(causal_arrow, UP)

        self.play(Create(causal_arrow), Write(causal_label))
        
        # Pulse
        self.play(slots[0].animate.set_fill(ORANGE, opacity=0.5), run_time=0.5)
        self.play(causal_arrow.animate.set_stroke(width=10), run_time=0.5)
        self.play(slots[1].animate.set_fill(GREEN, opacity=0.5), Flash(slots[1], color=GREEN), run_time=0.5)
        
        self.wait(2)
