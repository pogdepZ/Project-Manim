from __future__ import annotations
from manim import *
from objectified_library import *

class Scene021(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Dịch chuyển phân phối")
        formula = self.create_formula(r"P_{\text{train}}(X, Y) \neq P_{\text{test}}(X, Y)")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        bg_sun = RoundedRectangle(width=5, height=3, color=GOLD_A, fill_opacity=0.1).shift(LEFT*3)
        sun = Circle(radius=0.3, color=GOLD_A, fill_opacity=0.8).move_to(bg_sun.get_corner(UR) + DOWN*0.5 + LEFT*0.5)
        car1 = create_car_icon(scale=0.6).move_to(bg_sun.get_center() + DOWN*0.5)
        label_train = Text("Huấn luyện (Nắng)", font_size=16, color=GOLD_A).next_to(bg_sun, UP)

        self.play(Create(bg_sun), FadeIn(sun), FadeIn(car1), Write(label_train), run_time=duration * 0.3)

        bg_rain = RoundedRectangle(width=5, height=3, color=BLUE, fill_opacity=0.2).shift(RIGHT*3)
        rain = VGroup(*[Line(UP*0.1, DOWN*0.1, color=BLUE).rotate(20*DEGREES).move_to(bg_rain.get_center() + np.random.randn(3)*1.2) for _ in range(30)])
        car2 = create_car_icon(scale=0.6).move_to(bg_rain.get_center() + DOWN*0.5)
        label_test = Text("Thực tế (Mưa)", font_size=16, color=BLUE).next_to(bg_rain, UP)

        self.play(Create(bg_rain), FadeIn(rain), FadeIn(car2), Write(label_test), run_time=duration * 0.3)

        rule = Arrow(bg_sun.get_right(), bg_rain.get_left(), color=GREEN, stroke_width=6)
        self.play(Create(rule), run_time=duration * 0.1)
        self.auto_wait(rule)

class Scene022(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Sự tồn tại vĩnh viễn")
        formula = self.create_formula(r"z_t \to z_{t+1}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        ball = Circle(radius=0.4, color=ORANGE, fill_opacity=0.8).shift(LEFT*5 + DOWN*0.5)
        board = Rectangle(width=3, height=2, color=GREY_OBJ, fill_opacity=0.9).shift(ORIGIN + DOWN*0.5)
        
        self.play(FadeIn(ball), Create(board), run_time=duration * 0.2)

        ghost = DashedVMobject(Circle(radius=0.4, color=ORANGE, stroke_opacity=0.5), num_dashes=15)
        self.play(ball.animate.shift(RIGHT*3), run_time=duration * 0.2, rate_func=linear)
        ghost.move_to(ball.get_center())
        self.add(ghost)
        
        self.play(ball.animate.shift(RIGHT*2).set_opacity(0), ghost.animate.shift(RIGHT*2), run_time=duration * 0.2, rate_func=linear)
        self.play(ball.animate.shift(RIGHT*2).set_opacity(0.8), ghost.animate.shift(RIGHT*2), run_time=duration * 0.2, rate_func=linear)
        
        self.play(FadeOut(ghost), run_time=duration * 0.05)
        self.auto_wait(ball)

class Scene023(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Mô hình thế giới")
        formula = self.create_formula(r"s_{t+1} = \text{WorldModel}(s_t, a_t)")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        car = create_car_icon(scale=0.8).shift(LEFT*4)
        label_s = MathTex("s_t", font_size=24, color=BLUE).next_to(car, UP)
        
        wm = RoundedRectangle(width=3, height=2, corner_radius=0.2, color=TEAL, fill_opacity=0.1).shift(RIGHT*2)
        label_wm = Text("World Model", font_size=20, color=TEAL).next_to(wm, UP)

        self.play(FadeIn(car), Write(label_s), Create(wm), Write(label_wm), run_time=duration * 0.3)

        ghost_car1 = create_car_icon(scale=0.6).set_stroke(opacity=0.5).set_fill(opacity=0.2).move_to(wm.get_center() + LEFT*0.5)
        ghost_car2 = create_car_icon(scale=0.6).set_stroke(opacity=0.5).set_fill(opacity=0.2).move_to(wm.get_center() + RIGHT*0.5 + UP*0.5)
        
        arrow = Arrow(car.get_right(), wm.get_left(), color=GREY_TEXT)
        sim_path = Arrow(ghost_car1.get_right(), ghost_car2.get_bottom(), color=ORANGE, path_arc=-0.5)

        self.play(Create(arrow), FadeIn(ghost_car1), run_time=duration * 0.2)
        self.play(Create(sim_path), FadeIn(ghost_car2), run_time=duration * 0.2)
        self.auto_wait(ghost_car2)

class Scene024(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Ứng dụng Robotics")
        formula = self.create_formula(r"\text{Perception} \to \text{Plan} \to \text{Action}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        arm = create_robot_arm().shift(LEFT*3 + DOWN*1)
        cup = create_document_card(color=BLUE, scale=0.5).shift(RIGHT*2 + DOWN*1)
        
        self.play(Create(arm), FadeIn(cup), run_time=duration * 0.3)

        hud = SurroundingRectangle(cup, color=RED)
        label_hud = Text("DỰ ĐOÁN: DỄ VỠ", font_size=14, color=RED).next_to(hud, UP)
        
        self.play(Create(hud), Write(label_hud), run_time=duration * 0.2)
        self.play(arm[1].animate.set_angle(PI/4), arm[2].animate.set_angle(-PI/4), run_time=duration * 0.3)
        self.auto_wait(hud)

class Scene025(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Xe tự lái")
        formula = self.create_formula(r"\text{Entities + Relations} \to \text{Safe Driving}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        road = Line(LEFT*6, RIGHT*6, color=GREY_OBJ, stroke_width=20).shift(DOWN*0.5)
        my_car = create_car_icon(color=BLUE, scale=0.8).shift(LEFT*3 + DOWN*0.2)
        lead_car = create_car_icon(color=GREY_OBJ, scale=0.8).shift(RIGHT*2 + DOWN*0.2)

        self.play(Create(road), FadeIn(my_car), FadeIn(lead_car), run_time=duration * 0.2)

        bubble = Annulus(inner_radius=1.0, outer_radius=1.2, color=GREEN, fill_opacity=0.2).move_to(my_car)
        self.play(FadeIn(bubble), run_time=duration * 0.2)

        self.play(lead_car.animate.set_color(RED), run_time=duration * 0.1)
        rel_arrow = Arrow(lead_car.get_left(), my_car.get_right(), color=RED)
        label_rel = Text("Phanh", font_size=16, color=RED).next_to(rel_arrow, UP)

        self.play(Create(rel_arrow), Write(label_rel), run_time=duration * 0.2)
        self.play(my_car.animate.shift(LEFT*0.5), bubble.animate.shift(LEFT*0.5), run_time=duration * 0.1)
        self.auto_wait(my_car)