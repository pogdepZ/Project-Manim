from manim import *
import numpy as np


config.background_color = BLACK


CYAN_GRID = "#00d7ff"
SOFT_CYAN = "#6ee7ff"
CAR_A = "#58c4dd"
CAR_B = "#ff7f50"
PED = "#ffd166"
LIGHT_RED = "#ff4d5a"
SLOT_BLUE = "#7aa2ff"
TEXT_GREY = "#c7d0d9"


def soft_text(text, font_size=28, color=WHITE):
    return Text(text, font_size=font_size, color=color, weight="MEDIUM")


def make_car(color=CAR_A, label="Car A"):
    body = RoundedRectangle(width=1.15, height=0.42, corner_radius=0.09)
    body.set_fill(color, opacity=0.88).set_stroke(WHITE, width=1.5)

    cabin = Polygon(
        [-0.35, 0.21, 0],
        [-0.12, 0.52, 0],
        [0.33, 0.52, 0],
        [0.54, 0.21, 0],
    )
    cabin.set_fill(interpolate_color(color, WHITE, 0.25), opacity=0.9)
    cabin.set_stroke(WHITE, width=1.4)

    wheels = VGroup(
        Circle(radius=0.12).move_to([-0.35, -0.24, 0]),
        Circle(radius=0.12).move_to([0.38, -0.24, 0]),
    )
    wheels.set_fill(BLACK, opacity=1).set_stroke(WHITE, width=1.2)

    name = soft_text(label, 18, color).next_to(body, DOWN, buff=0.18)
    return VGroup(body, cabin, wheels, name)


def make_pedestrian():
    head = Circle(radius=0.16).set_fill(PED, opacity=0.9).set_stroke(WHITE, width=1.5)
    torso = Line(ORIGIN, DOWN * 0.55, stroke_width=5, color=PED)
    arms = VGroup(
        Line(UP * -0.18, LEFT * 0.32 + DOWN * 0.4, stroke_width=4, color=PED),
        Line(UP * -0.18, RIGHT * 0.32 + DOWN * 0.37, stroke_width=4, color=PED),
    )
    legs = VGroup(
        Line(DOWN * 0.55, LEFT * 0.28 + DOWN * 0.92, stroke_width=4, color=PED),
        Line(DOWN * 0.55, RIGHT * 0.28 + DOWN * 0.92, stroke_width=4, color=PED),
    )
    head.move_to(UP * 0.12)
    label = soft_text("Pedestrian", 18, PED).next_to(legs, DOWN, buff=0.12)
    return VGroup(head, torso, arms, legs, label).scale(0.9)


def make_red_light():
    post = Line(DOWN * 0.9, UP * 0.15, stroke_width=5, color=GREY_B)
    case = RoundedRectangle(width=0.45, height=1.1, corner_radius=0.08)
    case.set_fill("#111820", opacity=1).set_stroke(WHITE, width=1.4)
    case.move_to(UP * 0.47)

    lights = VGroup(
        Circle(radius=0.11).set_fill(LIGHT_RED, opacity=1).set_stroke(WHITE, width=0.8),
        Circle(radius=0.11).set_fill("#3a2b00", opacity=0.85).set_stroke(GREY_C, width=0.6),
        Circle(radius=0.11).set_fill("#083a22", opacity=0.85).set_stroke(GREY_C, width=0.6),
    )
    lights.arrange(DOWN, buff=0.08).move_to(case)
    glow = Circle(radius=0.2).move_to(lights[0]).set_fill(LIGHT_RED, opacity=0.18).set_stroke(LIGHT_RED, width=0)
    label = soft_text("Red light", 18, LIGHT_RED).next_to(post, DOWN, buff=0.14)
    return VGroup(post, case, glow, lights, label)


def make_slot(index, color, position):
    box = RoundedRectangle(width=1.65, height=0.95, corner_radius=0.12)
    box.set_fill("#071018", opacity=0.92).set_stroke(color, width=2.2)
    box.move_to(position)

    title = soft_text(f"Slot {index}", 20, color).move_to(box.get_top() + DOWN * 0.2)
    dot = Circle(radius=0.08).set_fill(color, opacity=1).set_stroke(color, width=1)
    dot.move_to(box.get_bottom() + UP * 0.24)
    return VGroup(box, title, dot)


def thin_arrow(start, end, color):
    return Arrow(
        start,
        end,
        buff=0.16,
        stroke_width=3.2,
        color=color,
        max_tip_length_to_length_ratio=0.11,
    )


class AutonomousDrivingScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK

        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4.5, 4.5, 1],
            background_line_style={
                "stroke_color": CYAN_GRID,
                "stroke_width": 1.0,
                "stroke_opacity": 0.18,
            },
            axis_config={
                "stroke_color": CYAN_GRID,
                "stroke_width": 1.5,
                "stroke_opacity": 0.35,
            },
        )
        plane.set_z_index(-5)

        title = soft_text("Object-Centric Learning", 34, WHITE).to_edge(UP, buff=0.35)
        pipeline = soft_text("Objects \u2192 Slots \u2192 Decision", 26, SOFT_CYAN)
        pipeline.next_to(title, DOWN, buff=0.18)

        observation_frame = RoundedRectangle(width=7.15, height=5.2, corner_radius=0.12)
        observation_frame.move_to(LEFT * 2.25 + DOWN * 0.12)
        observation_frame.set_fill("#02070b", opacity=0.24).set_stroke(SOFT_CYAN, width=1.6, opacity=0.65)
        observation_label = soft_text("scene", 18, SOFT_CYAN).next_to(observation_frame, UP, buff=0.12)

        road = VGroup(
            Line(LEFT * 3.25, RIGHT * 3.25, color="#6d7b8a", stroke_width=3),
            DashedLine(LEFT * 3.15 + DOWN * 0.55, RIGHT * 3.15 + DOWN * 0.55, color=GREY_B, stroke_width=2),
        )
        road.move_to(observation_frame.get_center() + DOWN * 1.35)

        car_a = make_car(CAR_A, "Car A").move_to(observation_frame.get_center() + LEFT * 2.15 + DOWN * 1.0)
        car_b = make_car(CAR_B, "Car B").scale(0.88).move_to(observation_frame.get_center() + RIGHT * 0.55 + DOWN * 0.6)
        pedestrian = make_pedestrian().move_to(observation_frame.get_center() + LEFT * 0.7 + UP * 0.85)
        red_light = make_red_light().scale(0.86).move_to(observation_frame.get_center() + RIGHT * 2.45 + UP * 1.08)

        objects = VGroup(car_a, car_b, pedestrian, red_light)
        object_colors = [CAR_A, CAR_B, PED, LIGHT_RED]

        slot_positions = [
            np.array([4.6, 1.65, 0]),
            np.array([6.35, 1.65, 0]),
            np.array([4.6, 0.25, 0]),
            np.array([6.35, 0.25, 0]),
        ]
        slots = VGroup(*[make_slot(i + 1, object_colors[i], slot_positions[i]) for i in range(4)])
        slot_label = soft_text("slot representations", 18, TEXT_GREY).next_to(slots, UP, buff=0.22)

        self.play(FadeIn(plane, run_time=1.4), FadeIn(title, shift=DOWN * 0.15), FadeIn(pipeline, shift=DOWN * 0.12))
        self.play(Create(observation_frame), FadeIn(observation_label), Create(road), run_time=1.2)

        for mob, color in zip(objects, object_colors):
            halo = SurroundingRectangle(mob, color=color, buff=0.12, stroke_width=2)
            self.play(GrowFromCenter(mob), Create(halo), run_time=0.8)
            self.play(FadeOut(halo), run_time=0.25)

        self.play(LaggedStart(*[Create(slot) for slot in slots], lag_ratio=0.12), FadeIn(slot_label), run_time=1.4)

        miniatures = VGroup()
        arrows = VGroup()
        for i, (obj, slot, color) in enumerate(zip(objects, slots, object_colors)):
            arrow = thin_arrow(obj.get_right(), slot[0].get_left(), color)
            arrows.add(arrow)

            miniature = obj.copy()
            miniature.generate_target()
            miniature.target.scale(0.42 if i != 2 else 0.36)
            miniature.target.move_to(slot[0].get_center() + DOWN * 0.08)
            miniatures.add(miniature)

            self.play(GrowArrow(arrow), run_time=0.55)
            self.play(TransformFromCopy(obj, miniature.target), slot.animate.scale(1.04), run_time=0.9)
            self.play(slot.animate.scale(1 / 1.04), run_time=0.2)

        self.play(
            self.camera.frame.animate.move_to(RIGHT * 1.4 + DOWN * 0.05).scale(0.92),
            run_time=1.3,
            rate_func=smooth,
        )

        separator = Line([3.65, -1.45, 0], [7.15, -1.45, 0], color=SOFT_CYAN, stroke_width=1.6)
        decision_title = soft_text("Decision", 28, WHITE).next_to(separator, DOWN, buff=0.22)
        stop_text = soft_text("Red light \u2192 Stop", 24, LIGHT_RED).next_to(decision_title, DOWN, buff=0.28)
        slow_text = soft_text("Pedestrian \u2192 Slow down", 24, PED).next_to(stop_text, DOWN, buff=0.2)

        red_focus = SurroundingRectangle(red_light, color=LIGHT_RED, buff=0.12, stroke_width=2.5)
        ped_focus = SurroundingRectangle(pedestrian, color=PED, buff=0.12, stroke_width=2.5)
        self.play(Create(red_focus), Create(ped_focus), run_time=0.8)
        self.play(Create(separator), FadeIn(decision_title, shift=UP * 0.1), run_time=0.8)
        self.play(TransformFromCopy(slots[3], stop_text), run_time=0.9)
        self.play(TransformFromCopy(slots[2], slow_text), run_time=0.9)

        stop_vector = thin_arrow(red_light.get_right(), stop_text.get_left(), LIGHT_RED)
        slow_vector = thin_arrow(pedestrian.get_right(), slow_text.get_left(), PED)
        self.play(GrowArrow(stop_vector), GrowArrow(slow_vector), run_time=0.9)

        self.play(
            Indicate(stop_text, color=LIGHT_RED, scale_factor=1.05),
            Indicate(slow_text, color=PED, scale_factor=1.05),
            run_time=1.2,
        )
        self.wait(1.2)
