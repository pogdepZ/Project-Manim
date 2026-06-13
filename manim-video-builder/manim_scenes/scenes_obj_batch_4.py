from __future__ import annotations
from manim import *
from objectified_library import *

class Scene016(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Quan sát vs Can thiệp")
        formula = self.create_formula(r"\text{Observation vs Intervention}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        line = Line(UP*2, DOWN*2, color=GREY_OBJ)
        self.play(Create(line), run_time=duration * 0.1)

        telescope = Text("🔭", font_size=40).shift(LEFT*3 + UP*0.5)
        obs_label = Text("Quan sát", font_size=18).next_to(telescope, DOWN)
        car1 = create_car_icon(scale=0.4).shift(LEFT*5 + DOWN*1)
        self.play(FadeIn(telescope), Write(obs_label), FadeIn(car1), run_time=duration * 0.2)
        self.play(car1.animate.shift(RIGHT*1.5), run_time=duration * 0.2)

        stop_sign = Text("🛑", font_size=40).shift(RIGHT*3 + UP*0.5)
        int_label = Text("Can thiệp", font_size=18, color=ORANGE).next_to(stop_sign, DOWN)
        car2 = create_car_icon(scale=0.4).shift(RIGHT*1 + DOWN*1)
        self.play(FadeIn(stop_sign), Write(int_label), FadeIn(car2), run_time=duration * 0.2)
        self.play(car2.animate.set_color(RED).scale(1.1), run_time=duration * 0.1)
        self.auto_wait(stop_sign)

class Scene017(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Mô hình nhân quả cấu trúc S C M")
        formula = self.create_formula(r"X_i = f_i(PA_i, U_i)")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        u = Circle(radius=0.4, color=GREY_TEXT, fill_opacity=0.1).shift(UP*1.5 + LEFT*1)
        pa = Circle(radius=0.4, color=BLUE, fill_opacity=0.1).shift(UP*1.5 + RIGHT*1)
        xi = Circle(radius=0.6, color=TEAL, fill_opacity=0.2).shift(DOWN*1)
        
        lbl_u = MathTex("U_i", font_size=24).move_to(u)
        lbl_pa = MathTex("PA_i", font_size=24).move_to(pa)
        lbl_xi = MathTex("X_i", font_size=24).move_to(xi)

        self.play(FadeIn(u), FadeIn(lbl_u), FadeIn(pa), FadeIn(lbl_pa), run_time=duration * 0.3)
        arrow1 = Arrow(u.get_bottom(), xi.get_top(), color=GREY_OBJ)
        arrow2 = Arrow(pa.get_bottom(), xi.get_top(), color=BLUE)
        self.play(Create(arrow1), Create(arrow2), run_time=duration * 0.2)
        self.play(GrowFromCenter(xi), FadeIn(lbl_xi), run_time=duration * 0.2)
        self.auto_wait(xi)

class Scene018(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Cơ chế vật lý: Va chạm")
        formula = self.create_formula(r"\text{Ball} \to \text{Force} \to \text{Box}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        floor = Line(LEFT*6, RIGHT*6, color=GREY_OBJ).shift(DOWN*1.5)
        self.play(Create(floor), run_time=duration * 0.1)

        ball = Circle(radius=0.4, color=ORANGE, fill_opacity=0.8).shift(LEFT*5 + DOWN*1.1)
        box = Square(0.8, color=TEAL, fill_opacity=0.4).shift(RIGHT*1 + DOWN*1.1)
        self.play(FadeIn(ball), FadeIn(box), run_time=duration * 0.2)

        self.play(ball.animate.shift(RIGHT*5.3), run_time=duration * 0.2, rate_func=rate_functions.ease_in_sine)
        force_flash = Flash(ball.get_right(), color=RED)
        self.play(force_flash, box.animate.shift(RIGHT*2.5), ball.animate.shift(LEFT*0.2), run_time=duration * 0.2, rate_func=rate_functions.ease_out_sine)
        self.auto_wait(box)

class Scene019(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Phân tích động lượng")
        formula = self.create_formula(r"F = m \cdot a, \quad \Delta p = F \cdot \Delta t")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        m1 = Circle(radius=0.2, color=ORANGE, fill_opacity=0.5).shift(LEFT*3 + UP*1)
        m2 = Circle(radius=0.6, color=ORANGE, fill_opacity=0.8).shift(LEFT*3 + DOWN*1)
        
        arrow1 = Arrow(m1.get_right(), m1.get_right()+RIGHT*0.5, color=RED)
        arrow2 = Arrow(m2.get_right(), m2.get_right()+RIGHT*3, color=RED, stroke_width=10)

        self.play(FadeIn(m1), FadeIn(m2), run_time=duration * 0.3)
        self.play(Create(arrow1), Create(arrow2), run_time=duration * 0.4)
        self.auto_wait(arrow2)

class Scene020(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Tại sao Slots hỗ trợ Nhân quả?")
        formula = self.create_formula(r"\text{Slots} \to \text{Mechanism}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        s1 = create_object_slot_tray(color=BLUE).shift(LEFT*2.5).scale(0.8)
        s2 = create_object_slot_tray(color=TEAL).shift(RIGHT*2.5).scale(0.8)
        p1 = create_person(scale=0.5).move_to(s1)
        p2 = create_laptop(scale=0.4).move_to(s2)

        self.play(Create(s1), Create(s2), FadeIn(p1), FadeIn(p2), run_time=duration * 0.4)
        
        causal_link = Arrow(s1.get_right(), s2.get_left(), color=GOLD_A, stroke_width=8)
        self.play(Create(causal_link), run_time=duration * 0.3)
        self.auto_wait(causal_link)