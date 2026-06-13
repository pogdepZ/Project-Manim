from __future__ import annotations
from manim import *
from objectified_library import *

class Scene001(EduScene):
    def construct(self):
        duration = self.get_duration(34.0)
        
        title = self.create_title("A I có thật sự hiểu thế giới không?")
        formula = self.create_formula(r"\text{Pixels} \to \text{Objects} \to \text{Relations} \to \text{Causes} \to \text{World Model}")
        
        self.play(Write(title), run_time=duration * 0.1)

        room = create_room_scene().shift(DOWN*0.5)
        self.play(LaggedStartMap(FadeIn, room, shift=UP), run_time=duration * 0.2)
        
        # Object grouping & movement
        self.play(Indicate(room[2], color=TEAL), Indicate(room[3], color=ORANGE), run_time=duration * 0.15)
        self.play(room[3].animate.shift(LEFT*0.5), run_time=duration * 0.15)

        # To Pixels
        grid = create_feature_grid(8, 12).move_to(room)
        self.play(ReplacementTransform(room, grid), run_time=duration * 0.2)
        self.play(FadeIn(formula, shift=UP), run_time=duration * 0.1)
        
        self.auto_wait(grid)

class Scene002(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        
        title = self.create_title("Pixel không phải là thế giới")
        formula = self.create_formula(r"X \in \mathbb{R}^{H \times W \times C}")
        self.play(Write(title), run_time=duration * 0.1)

        camera = create_camera_sensor().shift(LEFT*3)
        car = create_car_icon(color=ORANGE).shift(RIGHT*3)
        self.play(FadeIn(camera), FadeIn(car), run_time=duration * 0.2)

        rays = VGroup(*[Line(car.get_left() + UP*i*0.2, camera[2].get_center(), color=GOLD_A, stroke_opacity=0.6) for i in range(-2, 3)])
        self.play(Create(rays), run_time=duration * 0.2)
        self.play(Flash(camera[2], color=WHITE), run_time=duration * 0.1)

        tensor = create_image_tensor().shift(RIGHT*3)
        self.play(FadeOut(car), FadeOut(rays), ReplacementTransform(camera[0].copy(), tensor), run_time=duration * 0.2)
        
        self.play(FadeIn(formula), run_time=duration * 0.1)
        self.auto_wait(tensor)

class Scene003(EduScene):
    def construct(self):
        duration = self.get_duration(28.0)
        
        title = self.create_title("Representation là gì?")
        formula = self.create_formula(r"z = f_{\theta}(X)")
        self.play(Write(title), run_time=duration * 0.1)

        img_frame = Square(1.5, color=GREY_OBJ).shift(LEFT*4)
        tunnel = create_neural_network_tunnel().shift(LEFT*1)
        
        self.play(FadeIn(img_frame), Create(tunnel), run_time=duration * 0.2)

        particles = VGroup(*[Dot(color=TEAL, radius=0.05).move_to(img_frame.get_center() + np.random.randn(3)*0.4) for _ in range(20)])
        self.play(FadeIn(particles), run_time=duration * 0.1)

        # Flow through tunnel
        self.play(LaggedStart(*[p.animate.move_to(tunnel.get_right() + RIGHT*1.5) for p in particles], lag_ratio=0.05), run_time=duration * 0.3)
        
        z_col = create_vector_column().shift(RIGHT*4)
        self.play(ReplacementTransform(particles, z_col), FadeIn(formula), run_time=duration * 0.2)
        
        self.auto_wait(z_col)

class Scene004(EduScene):
    def construct(self):
        duration = self.get_duration(28.0)
        
        title = self.create_title("Biểu diễn trộn lẫn")
        formula = self.create_formula(r"z = [z_{\text{car}}, z_{\text{pedestrian}}, z_{\text{light}}]")
        self.play(Write(title), run_time=duration * 0.1)

        icons = VGroup(create_car_icon(scale=0.5), create_person(scale=0.6), Circle(0.3, color=RED, fill_opacity=0.8)).arrange(RIGHT, buff=0.8).move_to(ORIGIN)
        soup = Circle(radius=2, color=GREY_OBJ, stroke_opacity=0.5)
        
        self.play(Create(soup), FadeIn(icons), run_time=duration * 0.2)
        self.play(icons.animate.scale(0.5).move_to(ORIGIN), run_time=duration * 0.2)
        
        question = Text("?", font_size=80, color=ORANGE).move_to(soup)
        self.play(Rotate(icons, angle=PI*2), FadeIn(question), run_time=duration * 0.2)

        slots = VGroup(*[create_object_slot_tray(color=BLUE).scale(0.8) for _ in range(3)]).arrange(RIGHT, buff=1).shift(DOWN*1)
        self.play(
            FadeOut(soup), FadeOut(question),
            ReplacementTransform(icons[0], icons[0].copy().scale(1.5).move_to(slots[0])),
            ReplacementTransform(icons[1], icons[1].copy().scale(1.5).move_to(slots[1])),
            ReplacementTransform(icons[2], icons[2].copy().scale(1.5).move_to(slots[2])),
            FadeIn(slots), FadeIn(formula),
            run_time=duration * 0.2
        )
        self.auto_wait(slots)

class Scene005(EduScene):
    def construct(self):
        duration = self.get_duration(30.0)
        
        title = self.create_title("Object-centric Learning")
        formula = self.create_formula(r"\text{Scene} = \{O_1, O_2, \dots, O_K\}")
        self.play(Write(title), run_time=duration * 0.1)

        car = create_car_icon(scale=1.5).shift(LEFT*2)
        person = create_person(scale=1.2).shift(RIGHT*2)
        
        box_car = SurroundingRectangle(car, color=RED)
        box_person = SurroundingRectangle(person, color=RED)

        self.play(FadeIn(car), FadeIn(person), run_time=duration * 0.2)
        self.play(Create(box_car), Create(box_person), run_time=duration * 0.2)

        glow_car = car.copy().set_stroke(TEAL, width=8, opacity=0.5).set_fill(TEAL, opacity=0.2)
        glow_person = person.copy().set_stroke(BLUE, width=8, opacity=0.5).set_fill(BLUE, opacity=0.2)

        self.play(
            FadeOut(box_car), FadeOut(box_person),
            Transform(car, glow_car), Transform(person, glow_person),
            run_time=duration * 0.3
        )
        
        self.play(car.animate.shift(UP*0.5), person.animate.shift(DOWN*0.5), FadeIn(formula), run_time=duration * 0.1)
        self.auto_wait(car)