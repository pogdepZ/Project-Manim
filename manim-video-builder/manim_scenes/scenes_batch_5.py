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


# --- Scene 021 ---
class Scene021(EduScene):
    def construct(self):
        title = self.create_title("Dịch chuyển phân phối và tổng quát hóa")
        formula = self.create_formula(r"P_{\text{train}}(X, Y) \neq P_{\text{test}}(X, Y)")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Environment: Sunny
        sunny_bg = RoundedRectangle(width=8, height=4, color=GOLD_A, fill_opacity=0.1)
        sun = Circle(radius=0.3, color=GOLD_A, fill_opacity=0.9).move_to(sunny_bg.get_corner(UR) + DOWN * 0.5 + LEFT * 0.5)
        car = Text("🚗", font_size=40).shift(DOWN * 0.5)
        env_label = Text("Huấn luyện: Ban ngày", font_size=20, color=GOLD_A).next_to(sunny_bg, UP)

        self.play(Create(sunny_bg), FadeIn(sun), FadeIn(car), Write(env_label))
        self.wait(1)

        # 2. Transition: Night/Rain
        rain_bg = RoundedRectangle(width=8, height=4, color=BLUE, fill_opacity=0.2)
        rain_label = Text("Thực tế: Ban đêm / Mưa", font_size=20, color=BLUE).next_to(rain_bg, UP)
        
        rain_drops = VGroup(*[
            Line(UP * 0.1, DOWN * 0.1, color=BLUE, stroke_opacity=0.5).rotate(10 * DEGREES).move_to(np.random.randn(3) * 2)
            for _ in range(50)
        ]).shift(UP * 0.5)

        self.play(
            ReplacementTransform(sunny_bg, rain_bg),
            ReplacementTransform(env_label, rain_label),
            FadeOut(sun),
            FadeIn(rain_drops),
            car.animate.set_color(GREY),
            run_time=2
        )
        
        # Rule remains
        logic_box = SurroundingRectangle(car, color=GREEN, buff=0.3)
        logic_text = Text("Quy luật nhân quả (Dừng xe)", font_size=16, color=GREEN).next_to(logic_box, DOWN)
        
        self.play(Create(logic_box), Write(logic_text))
        self.play(Indicate(logic_box, color=GREEN))
        self.wait(2)


# --- Scene 022 ---
class Scene022(EduScene):
    def construct(self):
        title = self.create_title("Sự tồn tại vĩnh viễn của đối tượng")
        formula = self.create_formula(r"\text{Object Permanence: } z_t \to z_{t+1}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Objects
        ball = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).shift(LEFT * 5 + DOWN * 1)
        barrier = Rectangle(width=2, height=3, color=GREY, fill_opacity=0.5).shift(ORIGIN)
        
        self.play(FadeIn(ball), Create(barrier))
        
        # 2. Behind Barrier
        ghost_ball = DashedVMobject(Circle(radius=0.3, color=ORANGE, stroke_opacity=0.5), num_dashes=15)
        
        # Timeline
        self.play(ball.animate.shift(RIGHT * 4), run_time=1.5, rate_func=linear)
        
        # Visualizing the hidden state
        ghost_ball.move_to(ball.get_center())
        self.add(ghost_ball)
        self.play(ball.animate.shift(RIGHT * 2).set_opacity(0), ghost_ball.animate.shift(RIGHT * 2), run_time=1, rate_func=linear)
        
        # Emerging
        self.play(ball.animate.shift(RIGHT * 4).set_opacity(0.8), ghost_ball.animate.shift(RIGHT * 4), run_time=1.5, rate_func=linear)
        self.play(FadeOut(ghost_ball))
        self.play(Flash(ball, color=GOLD_A))
        
        self.wait(2)


# --- Scene 023 ---
class Scene023(EduScene):
    def construct(self):
        title = self.create_title("Mô hình thế giới trong trí tuệ nhân tạo")
        formula = self.create_formula(r"s_{t+1} = \text{WorldModel}(s_t, a_t)")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. State nodes
        st = Circle(radius=0.6, color=BLUE, fill_opacity=0.2).shift(LEFT * 3)
        label_st = MathTex("s_t", color=BLUE).move_to(st)
        
        at = Arrow(st.get_top(), st.get_top() + UP * 1.5, color=ORANGE)
        label_at = MathTex("a_t", color=ORANGE).next_to(at, RIGHT)

        self.play(GrowFromCenter(st), Write(label_st))
        self.play(Create(at), Write(label_at))

        # 2. Prediction (Ghost Rollout)
        wm_box = Rectangle(width=2, height=1.5, color=TEAL, fill_opacity=0.1).shift(ORIGIN)
        wm_label = Text("World Model", font_size=18).move_to(wm_box)
        
        self.play(Create(wm_box), Write(wm_label))
        
        st_plus_1 = Circle(radius=0.6, color=TEAL, fill_opacity=0.2).shift(RIGHT * 3)
        label_next = MathTex("s_{t+1}", color=TEAL).move_to(st_plus_1)
        
        ghost_state = st_plus_1.copy().set_stroke(opacity=0.3).set_fill(opacity=0.1)
        
        arrow_in = Arrow(st.get_right(), wm_box.get_left(), color=GREY)
        arrow_out = Arrow(wm_box.get_right(), st_plus_1.get_left(), color=GREY)
        
        self.play(Create(arrow_in))
        self.play(ReplacementTransform(st.copy(), ghost_state), Create(arrow_out), run_time=1.5)
        self.play(FadeIn(st_plus_1), Write(label_next))
        self.play(Indicate(st_plus_1, color=GOLD_A))
        
        self.wait(2)


# --- Scene 024 ---
class Scene024(EduScene):
    def construct(self):
        title = self.create_title("Ứng dụng trong Robotics: lập kế hoạch")
        formula = self.create_formula(r"\text{Perception} \to \text{Slots} \to \text{Causal Plan} \to \text{Action}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Robot Arm (Simplified)
        base = Square(0.8, color=GREY, fill_opacity=0.5).to_edge(LEFT, buff=1).shift(DOWN * 1)
        arm = VGroup(
            Line(base.get_top(), base.get_top() + UP * 2 + RIGHT * 1, color=GREY, stroke_width=8),
            Line(base.get_top() + UP * 2 + RIGHT * 1, base.get_top() + UP * 1 + RIGHT * 3, color=GREY, stroke_width=8)
        )
        self.play(Create(base), Create(arm))

        # 2. Fragile Object
        cup = RoundedRectangle(width=0.4, height=0.6, corner_radius=0.1, color=BLUE, fill_opacity=0.3).shift(RIGHT * 3 + DOWN * 0.7)
        label_cup = Text("Cốc thủy tinh", font_size=16).next_to(cup, DOWN)
        
        self.play(FadeIn(cup), Write(label_cup))

        # 3. HUD Planning
        hud_box = SurroundingRectangle(cup, color=RED, buff=0.2)
        hud_label = Text("DỰ ĐOÁN: DỄ VỠ", font_size=14, color=RED, weight=BOLD).next_to(hud_box, UP)
        force_label = Text("Lực < 5N", font_size=14, color=GREEN).next_to(hud_box, RIGHT)

        self.play(Create(hud_box), Write(hud_label))
        self.play(Write(force_label))
        
        # Action
        self.play(arm.animate.shift(RIGHT * 0.5), run_time=1)
        self.play(Indicate(force_label, color=GREEN))
        self.wait(2)


# --- Scene 025 ---
class Scene025(EduScene):
    def construct(self):
        title = self.create_title("Xe tự lái: hiểu mối quan hệ đường phố")
        formula = self.create_formula(r"\text{Entities + Relations} \to \text{Safe Driving}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Road & Cars
        road = VGroup(Line(LEFT * 6, RIGHT * 6), Line(LEFT * 6, RIGHT * 6).shift(UP * 2)).shift(DOWN * 1)
        self.play(Create(road))

        ego_car = VGroup(Rectangle(width=1, height=0.6, color=BLUE, fill_opacity=0.5), Text("Tôi", font_size=15)).shift(LEFT * 3 + DOWN * 0.5)
        lead_car = VGroup(Rectangle(width=1, height=0.6, color=GREY, fill_opacity=0.5), Text("Xe trước", font_size=15)).shift(RIGHT * 1 + DOWN * 0.5)

        self.play(FadeIn(ego_car), FadeIn(lead_car))

        # 2. Relational Safety HUD
        safety_bubble = Annulus(inner_radius=0.8, outer_radius=1.2, color=GREEN, stroke_opacity=0.3).move_to(ego_car)
        
        self.play(FadeIn(safety_bubble))
        
        # Brake event
        self.play(lead_car.animate.set_color(RED))
        brake_light = Flash(lead_car.get_left(), color=RED)
        
        arrow = Arrow(lead_car.get_left(), ego_car.get_right(), color=RED)
        label_rel = Text("Xe trước phanh -> Ta phanh", font_size=16, color=RED).next_to(arrow, UP)

        self.play(brake_light, Create(arrow), Write(label_rel))
        self.play(ego_car.animate.shift(LEFT * 0.5), run_time=0.5)
        
        self.wait(2)
