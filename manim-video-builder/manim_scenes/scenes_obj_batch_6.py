from __future__ import annotations
from manim import *
from objectified_library import *

class Scene026(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("A I hiện thân")
        formula = self.create_formula(r"\text{Action} \to \text{Environment} \to \text{Reward}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        maze = VGroup(*[Line(UP*0.5, DOWN*0.5, color=GREY_OBJ, stroke_width=8) for _ in range(4)]).arrange(RIGHT, buff=2).shift(DOWN*1)
        agent = create_person(color=BLUE, scale=0.6).move_to(maze[0].get_center() + LEFT*1)
        
        self.play(Create(maze), FadeIn(agent), run_time=duration * 0.2)

        key = Circle(radius=0.2, color=GOLD_A, fill_opacity=0.8).shift(LEFT*1 + DOWN*1)
        door = Rectangle(width=0.4, height=1, color=ORANGE, fill_opacity=0.8).shift(RIGHT*4 + DOWN*1)

        self.play(FadeIn(key), FadeIn(door), run_time=duration * 0.2)
        
        self.play(agent.animate.move_to(key), run_time=duration * 0.2)
        self.play(FadeOut(key), agent.animate.set_color(GOLD_A), run_time=duration * 0.1)
        self.play(agent.animate.move_to(door.get_left()), run_time=duration * 0.1)
        self.play(Flash(door, color=GOLD_A), door.animate.set_color(GREEN), run_time=duration * 0.05)
        self.auto_wait(door)

class Scene027(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Y tế")
        formula = self.create_formula(r"\text{Medical Image} \to \text{Segments}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        chest = create_person(color=GREY_TEXT, scale=2.5).center().shift(DOWN*0.5)
        chest.set_fill(opacity=0.05).set_stroke(opacity=0.5)
        
        ribs = VGroup(*[Line(LEFT*0.8, RIGHT*0.8, color=GREY_OBJ, stroke_opacity=0.3).shift(UP*(1-i*0.4)) for i in range(5)]).shift(DOWN*0.2)
        
        self.play(FadeIn(chest), Create(ribs), run_time=duration * 0.3)

        lesion_site = Dot(color=RED, radius=0.1).shift(UP*0.5 + RIGHT*0.5)
        spotlight = Annulus(inner_radius=0, outer_radius=0.6, color=RED, fill_opacity=0.2).move_to(lesion_site)
        label = Text("Tổn thương", font_size=16, color=RED).next_to(spotlight, UR)

        self.play(FadeIn(spotlight, scale=0.1), Create(lesion_site), run_time=duration * 0.2)
        self.play(spotlight.animate.scale(2).set_opacity(0.1), run_time=duration * 0.2)
        self.play(Write(label), Indicate(lesion_site, color=RED), run_time=duration * 0.1)
        self.auto_wait(lesion_site)

class Scene028(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Bản sao số")
        formula = self.create_formula(r"\text{Physical City} \to \text{Digital Twin}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        road = Line(LEFT*6, RIGHT*6, color=GREY_OBJ, stroke_width=20).shift(DOWN*1)
        cars = VGroup(*[create_car_icon(scale=0.5).shift(LEFT*(4-i*2) + DOWN*0.7) for i in range(4)])
        
        self.play(Create(road), FadeIn(cars), run_time=duration * 0.3)

        grid = NumberPlane(x_range=[-6, 6], y_range=[-3, 3], background_line_style={"stroke_opacity": 0.2})
        dots = VGroup(*[Dot(radius=0.1, color=TEAL).move_to(c.get_center()) for c in cars])
        
        self.play(ReplacementTransform(road, grid), ReplacementTransform(cars, dots), run_time=duration * 0.3)
        
        barrier = Line(DOWN*1.5, DOWN*0.5, color=RED, stroke_width=6).shift(RIGHT*1)
        self.play(Create(barrier), Flash(barrier, color=RED), run_time=duration * 0.1)
        
        self.play(dots[2].animate.shift(UP*1 + RIGHT*1), dots[3].animate.shift(UP*1 + RIGHT*1), run_time=duration * 0.1)
        self.auto_wait(barrier)

class Scene029(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("AI đa phương thức")
        formula = self.create_formula(r"\text{Text} \to \text{Object Grounding}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        cmd = create_document_card(scale=1.2).shift(LEFT*3)
        text_line = Text("Lấy tài liệu màu vàng", font_size=16, color=TITLE_YELLOW).move_to(cmd).shift(UP*0.3)
        
        self.play(FadeIn(cmd), Write(text_line), run_time=duration * 0.3)

        doc1 = create_document_card(scale=0.8).shift(RIGHT*3 + UP*1)
        doc1.set_color(TITLE_YELLOW)
        doc2 = create_document_card(scale=0.8).shift(RIGHT*3 + DOWN*1)
        doc2.set_color(BLUE)

        self.play(FadeIn(doc1), FadeIn(doc2), run_time=duration * 0.2)

        arrow = Arrow(cmd.get_right(), doc1.get_left(), color=GOLD_A, stroke_width=6)
        self.play(Create(arrow), run_time=duration * 0.2)
        self.play(Indicate(doc1, color=TITLE_YELLOW), run_time=duration * 0.1)
        self.auto_wait(doc1)

class Scene030(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        title = self.create_title("Thách thức tương lai")
        formula = self.create_formula(r"\text{Ambiguity + Confounding} \to \text{Limits}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        tree = VGroup(Line(ORIGIN, UP*1, color=GREY_OBJ), Circle(radius=0.6, color=GREEN, fill_opacity=0.2).shift(UP*1)).shift(LEFT*3)
        fog = VGroup(*[Dot(radius=0.15, color=WHITE, fill_opacity=0.1).shift(tree.get_center() + np.random.randn(3)*0.5) for _ in range(30)])
        label_amb = Text("Mơ hồ ranh giới", font_size=16).next_to(tree, DOWN)

        self.play(Create(tree), FadeIn(fog), Write(label_amb), run_time=duration * 0.3)

        u = Circle(radius=0.4, color=RED, fill_opacity=0.1).shift(RIGHT*3 + UP*1)
        label_u = Text("Yếu tố ẩn", font_size=16, color=RED).next_to(u, UP)
        a = Circle(radius=0.3, color=GREY_OBJ).shift(RIGHT*2 + DOWN*1)
        b = Circle(radius=0.3, color=GREY_OBJ).shift(RIGHT*4 + DOWN*1)
        
        self.play(FadeIn(u), Write(label_u), FadeIn(a), FadeIn(b), run_time=duration * 0.3)
        self.play(Create(Arrow(u.get_bottom(), a.get_top(), color=RED)), Create(Arrow(u.get_bottom(), b.get_top(), color=RED)), run_time=duration * 0.2)
        self.auto_wait(u)

class Scene031(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        title = self.create_title("Causal World Model")
        formula = self.create_formula(r"\text{Perception + Causality = Causal World Model}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        eye = create_camera_sensor(scale=0.8).shift(LEFT*2)
        label_p = Text("Nhận thức", font_size=18).next_to(eye, DOWN)
        
        gears = VGroup(*[Circle(radius=0.3, color=TEAL, stroke_width=4).shift(RIGHT*2 + np.random.randn(3)*0.2) for _ in range(3)])
        label_c = Text("Nhân quả", font_size=18).next_to(gears, DOWN)

        self.play(FadeIn(eye), Write(label_p), run_time=duration * 0.2)
        self.play(Create(gears), Write(label_c), run_time=duration * 0.2)

        brain = VGroup(
            Ellipse(width=2.5, height=1.8, color=GOLD_A, fill_opacity=0.2),
            *[CubicBezier(ORIGIN, UP*0.5, RIGHT*0.5, [0.3,0.3,0], color=GOLD_A, stroke_width=2).shift(np.random.randn(3)*0.4) for _ in range(8)]
        ).shift(UP*0.5)
        
        self.play(
            ReplacementTransform(eye, brain),
            ReplacementTransform(gears, brain),
            FadeOut(label_p), FadeOut(label_c),
            run_time=duration * 0.3
        )
        self.play(Indicate(brain, color=GOLD_A), run_time=duration * 0.1)
        self.auto_wait(brain)