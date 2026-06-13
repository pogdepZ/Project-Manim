from __future__ import annotations
from manim import *
from objectified_library import *

class Scene006(EduScene):
    def construct(self):
        duration = self.get_duration(28.0)
        
        title = self.create_title("Object slots là gì?")
        formula = self.create_formula(r"Z = \{z_1, z_2, \dots, z_K\}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        trays = VGroup(*[create_object_slot_tray(color=BLUE) for _ in range(3)]).arrange(RIGHT, buff=1)
        car = create_car_icon(scale=0.5).move_to(trays[0])
        person = create_person(scale=0.6).move_to(trays[1])
        doc = create_document_card(scale=0.5).move_to(trays[2])

        self.play(LaggedStartMap(Create, trays, lag_ratio=0.2), run_time=duration * 0.2)
        self.play(FadeIn(car), FadeIn(person), FadeIn(doc), run_time=duration * 0.2)
        
        self.play(
            car.animate.move_to(trays[2]),
            doc.animate.move_to(trays[0]),
            trays[0].animate.set_color(WHITE),
            trays[2].animate.set_color(ORANGE),
            run_time=duration * 0.3
        )
        self.auto_wait(trays)

class Scene007(EduScene):
    def construct(self):
        duration = self.get_duration(34.0)
        
        title = self.create_title("Cơ chế chú ý theo slot")
        formula = self.create_formula(r"\text{Attention}(Q, K, V)")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        grid = create_feature_grid(6, 6).shift(LEFT * 3)
        slots = VGroup(*[Circle(radius=0.4, color=BLUE, fill_opacity=0.1).shift(RIGHT * 3 + UP * i - UP * 1) for i in range(3)])

        self.play(FadeIn(grid), Create(slots), run_time=duration * 0.2)

        rays = VGroup()
        for slot in slots:
            light = Triangle(color=BLUE, fill_opacity=0.15).scale(1.5).rotate(-90*DEGREES).move_to(slot.get_left() + LEFT*1.5)
            rays.add(light)

        self.play(LaggedStartMap(FadeIn, rays, lag_ratio=0.3), run_time=duration * 0.2)
        
        # Iterative update visualization
        self.play(rays[0].animate.set_color(ORANGE).set_opacity(0.4), grid[7:14].animate.set_fill(ORANGE, opacity=0.8), run_time=duration * 0.2)
        self.play(rays[1].animate.set_color(RED).set_opacity(0.4), grid[20:25].animate.set_fill(RED, opacity=0.8), run_time=duration * 0.2)
        self.auto_wait(slots)

class Scene008(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        
        title = self.create_title("Cạnh tranh giữa các slot")
        formula = self.create_formula(r"\text{Competition} \to \text{Disentanglement}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        s1 = create_student_character(color=ORANGE).shift(RIGHT*3 + UP*1.5)
        s2 = create_student_character(color=TEAL).shift(RIGHT*3 + DOWN*1.5)
        pieces = VGroup(*[Square(0.4, color=GREY_OBJ, fill_opacity=0.3) for _ in range(12)]).arrange_in_grid(3, 4).shift(LEFT*3)

        self.play(FadeIn(s1), FadeIn(s2), FadeIn(pieces), run_time=duration * 0.2)

        piece = pieces[5]
        arm1 = Line(s1.get_left(), piece.get_center(), color=ORANGE)
        arm2 = Line(s2.get_left(), piece.get_center(), color=TEAL)

        self.play(Create(arm1), Create(arm2), run_time=duration * 0.2)
        self.play(piece.animate.scale(1.2).set_color(WHITE), run_time=duration * 0.1)
        
        self.play(FadeOut(arm2), arm1.animate.set_stroke(width=6), piece.animate.move_to(s1).set_color(ORANGE), run_time=duration * 0.2)
        self.auto_wait(s1)

class Scene009(EduScene):
    def construct(self):
        duration = self.get_duration(32.0)
        
        title = self.create_title("Reconstruction và mask")
        formula = self.create_formula(r"\hat{x} = \sum_{k} (m_k \cdot \hat{x}_k)")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        g1 = VGroup(Rectangle(width=2, height=2, color=GREY_OBJ, fill_opacity=0.05), create_car_icon(scale=0.5)).shift(LEFT*4)
        g2 = VGroup(Rectangle(width=2, height=2, color=GREY_OBJ, fill_opacity=0.05), create_person(scale=0.5)).shift(LEFT*1)
        g3 = VGroup(Rectangle(width=2, height=2, color=GREY_OBJ, fill_opacity=0.05), create_camera_sensor(scale=0.4)).shift(RIGHT*2)

        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), run_time=duration * 0.3)
        
        final = VGroup(create_car_icon(scale=0.5).shift(DOWN*0.3), create_person(scale=0.5).shift(UP*0.2), create_camera_sensor(scale=0.4).shift(RIGHT*0.5)).shift(RIGHT*5)
        
        self.play(
            ReplacementTransform(g1.copy(), final),
            ReplacementTransform(g2.copy(), final),
            ReplacementTransform(g3.copy(), final),
            run_time=duration * 0.4
        )
        self.auto_wait(final)

class Scene010(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        
        title = self.create_title("Mô phỏng và thực tế")
        formula = self.create_formula(r"\text{Synthetic} \to \text{Real World}")
        self.play(Write(title), FadeIn(formula, shift=UP), run_time=duration * 0.1)

        syn = VGroup(Circle(0.5, color=RED, fill_opacity=0.8), Square(0.8, color=BLUE, fill_opacity=0.8)).arrange(RIGHT).shift(LEFT*3)
        label_syn = Text("Mô phỏng (Dễ)", font_size=20, color=TEAL).next_to(syn, UP)

        real = create_room_scene().shift(RIGHT*3)
        label_real = Text("Thế giới thực (Khó)", font_size=20, color=ORANGE).next_to(real, UP)

        self.play(FadeIn(syn), Write(label_syn), run_time=duration * 0.3)
        
        barrier = Line(UP*2, DOWN*2, color=RED, stroke_width=6)
        self.play(Create(barrier), FadeIn(real), Write(label_real), run_time=duration * 0.3)
        self.play(Flash(barrier, color=RED), run_time=duration * 0.1)
        self.auto_wait(barrier)