from __future__ import annotations

from manim import *

# --- Global Style Constants ---
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
    """Base class for consistent styling."""

    def create_title(self, text):
        title = Text(text, font_size=32, color=TITLE_YELLOW, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        underline = Line(LEFT, RIGHT, color=GREY, stroke_width=1).scale(6).next_to(title, DOWN, buff=0.2)
        return VGroup(title, underline)

    def create_formula(self, tex):
        formula = MathTex(tex, font_size=36, color=TITLE_YELLOW)
        formula.to_edge(DOWN, buff=0.5)
        return formula


# --- Helpers ---
def make_room_objects():
    # Table
    table_top = Rectangle(width=2, height=0.2, color=TEAL, fill_opacity=0.3).shift(DOWN * 1)
    table_legs = VGroup(
        Line(table_top.get_left() + RIGHT * 0.2, table_top.get_left() + RIGHT * 0.2 + DOWN * 0.8, color=TEAL),
        Line(table_top.get_right() + LEFT * 0.2, table_top.get_right() + LEFT * 0.2 + DOWN * 0.8, color=TEAL),
    )
    table = VGroup(table_top, table_legs)

    # Chair
    chair_seat = Rectangle(width=0.8, height=0.15, color=BLUE, fill_opacity=0.3).next_to(table, LEFT, buff=0.2)
    chair_back = Rectangle(width=0.15, height=1, color=BLUE, fill_opacity=0.2).next_to(chair_seat, LEFT, buff=0)
    chair_legs = VGroup(Line(chair_seat.get_bottom(), chair_seat.get_bottom() + DOWN * 0.5, color=BLUE))
    chair = VGroup(chair_seat, chair_back, chair_legs)

    # Cup
    cup = RoundedRectangle(width=0.3, height=0.4, corner_radius=0.05, color=WHITE, fill_opacity=0.1).next_to(table_top, UP, buff=0)

    return VGroup(table, chair, cup).center().shift(DOWN * 0.5)


# --- Scene 001 ---
class Scene001(EduScene):
    def construct(self):
        title = self.create_title("A I có thật sự hiểu thế giới không?")
        formula = self.create_formula(r"\text{Pixels} \to \text{Objects} \to \text{Relations} \to \text{Causes} \to \text{World Model}")

        self.play(Write(title))
        self.play(FadeIn(formula, shift=UP))
        self.wait(1)

        # 1. Human view: Room
        room = make_room_objects()
        room_label = Text("Nhận thức con người", font_size=20, color=WHITE).next_to(room, UP)

        self.play(LaggedStartMap(FadeIn, room, shift=UP), Write(room_label), run_time=2)
        self.wait(2)

        # 2. AI view: Matrix
        grid = VGroup(*[
            Square(side_length=0.4, stroke_width=1, color=GREY).add(
                Text(str(np.random.randint(0, 255)), font_size=10, color=GREY)
            )
            for _ in range(35)
        ]).arrange_in_grid(5, 7, buff=0).move_to(room)

        ai_label = Text("Ma trận điểm ảnh (AI)", font_size=20, color=ORANGE).next_to(grid, UP)

        self.play(
            ReplacementTransform(room, grid),
            ReplacementTransform(room_label, ai_label),
            run_time=2
        )
        self.wait(2)

        # 3. Highlight groups (Objects discovery)
        group1 = SurroundingRectangle(VGroup(*grid[7:11], *grid[14:18]), color=TEAL, buff=0.05)
        group2 = SurroundingRectangle(VGroup(*grid[21:23]), color=BLUE, buff=0.05)

        self.play(Create(group1), Create(group2))
        self.play(group1.animate.set_fill(TEAL, opacity=0.3), group2.animate.set_fill(BLUE, opacity=0.3))
        self.wait(2)


# --- Scene 002 ---
class Scene002(EduScene):
    def construct(self):
        title = self.create_title("Pixel không phải là thế giới")
        formula = self.create_formula(r"X \in \mathbb{R}^{H \times W \times C}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # Tensor visualization
        grid_base = VGroup(*[Square(0.4, stroke_width=1, color=TEAL) for _ in range(16)]).arrange_in_grid(4, 4, buff=0)
        tensor = VGroup(*[grid_base.copy().set_stroke(opacity=0.5 - i * 0.1).shift(IN * i * 0.5) for i in range(3)])
        tensor.rotate(30 * DEGREES, axis=OUT).rotate(60 * DEGREES, axis=RIGHT)

        h_brace = Brace(tensor, LEFT, color=GREY).scale(0.8)
        w_brace = Brace(tensor, DOWN, color=GREY).scale(0.8)
        c_label = Text("C = 3 (RGB)", font_size=20, color=RED).next_to(tensor, RIGHT)

        self.play(FadeIn(tensor))
        self.play(Write(h_brace), Write(w_brace), Write(c_label))
        self.wait(2)

        # Split into RGB
        self.play(FadeOut(h_brace), FadeOut(w_brace), FadeOut(c_label))
        layers = tensor.copy().arrange(RIGHT, buff=1).rotate(-60 * DEGREES, axis=RIGHT).rotate(-30 * DEGREES, axis=OUT)
        layers[0].set_color(RED)
        layers[1].set_color(GREEN)
        layers[2].set_color(BLUE)

        self.play(ReplacementTransform(tensor, layers))
        self.wait(2)

        # Camera Metaphor
        cam_body = Rectangle(width=1, height=0.6, color=GREY, fill_opacity=0.5)
        cam_lens = Circle(radius=0.2, color=GREY, fill_opacity=0.8).next_to(cam_body, RIGHT, buff=0)
        camera = VGroup(cam_body, cam_lens).to_edge(LEFT).shift(UP * 0.5)

        obj = Circle(radius=0.5, color=ORANGE, fill_opacity=0.3).to_edge(RIGHT).shift(UP * 0.5)
        light_ray = Line(obj.get_left(), camera.get_right(), color=GOLD_A, stroke_width=2)

        self.play(FadeOut(layers), FadeIn(camera), FadeIn(obj))
        self.play(Create(light_ray))
        self.play(Flash(camera, color=GOLD_A))
        self.wait(2)


# --- Scene 003 ---
class Scene003(EduScene):
    def construct(self):
        title = self.create_title("Representation là gì?")
        formula = self.create_formula(r"z = f_{\theta}(X)")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # Image X
        img_x = Square(2, color=TEAL, fill_opacity=0.2)
        label_x = Text("X (Pixels)", font_size=20).next_to(img_x, UP)

        # Funnel (Neural Network)
        funnel = Polygon(
            [-1, 1, 0], [1, 1, 0], [0.2, -1, 0], [-0.2, -1, 0],
            color=BLUE, fill_opacity=0.2
        ).shift(RIGHT * 3)
        label_f = MathTex(r"f_{\theta}", color=BLUE).move_to(funnel)

        # Vector z
        vec_z = VGroup(*[Rectangle(width=0.4, height=0.2, color=ORANGE, fill_opacity=0.5) for _ in range(8)]).arrange(DOWN, buff=0.05).shift(RIGHT * 6)
        label_z = MathTex("z", color=ORANGE).next_to(vec_z, RIGHT)

        self.play(FadeIn(img_x), Write(label_x))
        self.wait(1)
        self.play(Create(funnel), Write(label_f))

        # Compression Animation
        dots = VGroup(*[Dot(color=TEAL, radius=0.05).move_to(img_x.get_center() + np.random.randn(3) * 0.5) for _ in range(20)])
        self.play(FadeIn(dots))
        self.play(
            LaggedStart(*[d.animate.move_to(funnel.get_top()) for d in dots], lag_ratio=0.05),
            run_time=1
        )
        self.play(
            LaggedStart(*[d.animate.move_to(funnel.get_bottom()).scale(0.1) for d in dots], lag_ratio=0.05),
            run_time=1
        )
        self.play(FadeOut(dots), FadeIn(vec_z), Write(label_z))
        self.wait(2)


# --- Scene 004 ---
class Scene004(EduScene):
    def construct(self):
        title = self.create_title("Biểu diễn trộn lẫn và bài toán suy luận")
        formula = self.create_formula(r"z = [z_{\text{car}}, z_{\text{pedestrian}}, z_{\text{light}}]")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # Entangled Soup
        soup_circle = Circle(radius=1.5, color=GREY, fill_opacity=0.1)
        icons = VGroup(
            Text("🚗", font_size=30), Text("🚶", font_size=30), Text("🚦", font_size=30),
            Text("🚗", font_size=20), Text("🚶", font_size=20)
        )
        for icon in icons:
            icon.move_to(soup_circle.get_center() + np.random.randn(3) * 0.7)

        self.play(Create(soup_circle), FadeIn(icons))
        self.play(icons.animate.rotate(PI / 2), run_time=2, rate_func=linear)
        self.wait(1)

        # Disentanglement
        slots = VGroup(
            Circle(radius=0.6, color=BLUE, fill_opacity=0.2),
            Circle(radius=0.6, color=TEAL, fill_opacity=0.2),
            Circle(radius=0.6, color=RED, fill_opacity=0.2)
        ).arrange(RIGHT, buff=1).shift(DOWN * 0.5)

        labels = VGroup(
            Text("Xe", font_size=18).next_to(slots[0], UP),
            Text("Người", font_size=18).next_to(slots[1], UP),
            Text("Đèn", font_size=18).next_to(slots[2], UP)
        )

        self.play(
            soup_circle.animate.scale(0).set_opacity(0),
            icons[0].animate.move_to(slots[0]),
            icons[1].animate.move_to(slots[1]),
            icons[2].animate.move_to(slots[2]),
            FadeOut(icons[3:]),
            FadeIn(slots),
            Write(labels),
            run_time=2
        )
        self.wait(2)


# --- Scene 005 ---
class Scene005(EduScene):
    def construct(self):
        title = self.create_title("Từ object detection đến học trung tâm đối tượng")
        formula = self.create_formula(r"\text{Scene} = \{O_1, O_2, \dots, O_K\}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Classical Detection (Boxes)
        car = RoundedRectangle(width=1.5, height=0.8, color=TEAL, fill_opacity=0.2).shift(LEFT * 2)
        person = Rectangle(width=0.6, height=1.5, color=BLUE, fill_opacity=0.2).shift(RIGHT * 2)

        box_car = SurroundingRectangle(car, color=RED, buff=0.1)
        label_car = Text("Car: 0.98", font_size=14, color=RED).next_to(box_car, UP, buff=0.05)

        box_person = SurroundingRectangle(person, color=RED, buff=0.1)
        label_person = Text("Person: 0.95", font_size=14, color=RED).next_to(box_person, UP, buff=0.05)

        self.play(FadeIn(car), FadeIn(person))
        self.play(Create(box_car), Write(label_car), Create(box_person), Write(label_person))
        self.wait(2)

        # 2. Transition to Object-Centric (Glow/Segmentation)
        self.play(FadeOut(box_car), FadeOut(label_car), FadeOut(box_person), FadeOut(label_person))

        # Custom Glow effect
        glow_car = car.copy().set_stroke(TEAL, width=8, opacity=0.5).set_fill(TEAL, opacity=0.4)
        glow_person = person.copy().set_stroke(BLUE, width=8, opacity=0.5).set_fill(BLUE, opacity=0.4)

        self.play(
            Transform(car, glow_car),
            Transform(person, glow_person),
            run_time=1.5
        )
        self.play(Indicate(car), Indicate(person))
        self.wait(2)
