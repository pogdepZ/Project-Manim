from manim import *
import numpy as np

config.background_color = "#06111f"

OBJECT_SPECS = [
    {"color": BLUE_B, "position": np.array([-3.0, 1.25, 0.0]), "kind": Circle, "scale": 0.95},
    {"color": RED_C, "position": np.array([0.0, 1.4, 0.0]), "kind": Square, "scale": 1.0},
    {"color": YELLOW_C, "position": np.array([3.0, 1.0, 0.0]), "kind": Triangle, "scale": 1.05},
    {"color": GREEN_C, "position": np.array([-1.8, -1.0, 0.0]), "kind": RegularPolygon, "scale": 0.9, "sides": 5},
    {"color": TEAL_C, "position": np.array([1.8, -1.05, 0.0]), "kind": RoundedRectangle, "scale": 1.0},
]


def make_frame(width=11.0, height=6.0):
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.15)
    frame.set_stroke(color="#28405f", width=2)
    frame.set_fill(color="#0a1526", opacity=0.92)
    return frame


def build_object_cluster():
    objects = VGroup()
    for spec in OBJECT_SPECS:
        if spec["kind"] == Circle:
            shape = Circle(radius=0.48)
        elif spec["kind"] == Square:
            shape = Square(side_length=0.95)
        elif spec["kind"] == Triangle:
            shape = Triangle()
        elif spec["kind"] == RegularPolygon:
            shape = RegularPolygon(spec.get("sides", 5))
        else:
            shape = RoundedRectangle(width=1.0, height=0.7, corner_radius=0.18)

        shape.scale(spec["scale"])
        shape.move_to(spec["position"])
        shape.set_fill(spec["color"], opacity=0.88)
        shape.set_stroke(color=spec["color"], width=3)
        objects.add(shape)

    return objects


def build_pixel_mosaic(rows=12, cols=20, width=9.6, height=5.4):
    cell_w = width / cols
    cell_h = height / rows
    cells = VGroup()
    clusters = [VGroup() for _ in OBJECT_SPECS]

    for row in range(rows):
        for col in range(cols):
            x = -width / 2 + cell_w / 2 + col * cell_w
            y = height / 2 - cell_h / 2 - row * cell_h
            position = np.array([x, y, 0.0])

            weights = []
            for spec in OBJECT_SPECS:
                distance = np.linalg.norm(position - spec["position"])
                weights.append(np.exp(-(distance ** 2) / 1.7))

            dominant = int(np.argmax(weights))
            blend = 0.22 + 0.7 * float(weights[dominant])
            fill_color = interpolate_color(BLACK, OBJECT_SPECS[dominant]["color"], blend)

            cell = Square(side_length=min(cell_w, cell_h) * 0.95)
            cell.move_to(position)
            cell.set_fill(fill_color, opacity=0.95)
            cell.set_stroke(color="#12253d", width=0.3, opacity=0.4)
            cells.add(cell)
            clusters[dominant].add(cell)

    return cells, clusters


def build_slot_boxes():
    slots = VGroup()
    labels = VGroup()
    positions = [-3.5, 0.0, 3.5]

    for index, x in enumerate(positions, start=1):
        slot = RoundedRectangle(width=2.2, height=1.05, corner_radius=0.14)
        slot.move_to([x, 2.05, 0])
        slot.set_fill(color="#0d1a2d", opacity=0.65)
        slot.set_stroke(color="#3b577e", width=2)
        label = Text(f"slot {index}", font_size=18, color=GREY_B).next_to(slot, UP, buff=0.12)
        slots.add(slot)
        labels.add(label)

    return slots, labels


def build_attention_lines(slots, targets, color_map):
    lines = VGroup()
    for index, slot in enumerate(slots):
        for target_index, target in enumerate(targets):
            line = Line(
                slot.get_bottom(),
                target.get_center(),
                color=color_map[index],
                stroke_width=2.0,
            )
            line.set_opacity(0.12 if index != target_index else 0.78)
            lines.add(line)
    return lines


class SlotAttentionIntro(MovingCameraScene):
    def construct(self):
        frame = make_frame()
        objects = build_object_cluster()
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-3.5, 3.5, 1],
            background_line_style={"stroke_color": "#13304a", "stroke_width": 1, "stroke_opacity": 0.2},
        ).scale(0.9)

        title = Text("Object-Centric Learning", font_size=36, weight=BOLD, color=WHITE).to_edge(UP)
        caption = Text("one scene, many objects", font_size=20, color=GREY_B).next_to(frame, DOWN, buff=0.25)

        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(grid, run_time=1.4))
        self.play(Create(frame), run_time=1.1)
        self.play(LaggedStart(*[GrowFromCenter(obj) for obj in objects], lag_ratio=0.12, run_time=2.0))
        self.play(FadeIn(caption, shift=UP * 0.1))
        self.play(self.camera.frame.animate.scale(0.88).move_to(frame.get_center() + UP * 0.15), run_time=2.0)
        self.play(Indicate(objects[1], color=RED_C), Indicate(objects[2], color=YELLOW_C), run_time=1.8)
        self.play(self.camera.frame.animate.scale(1.12).move_to(frame.get_center()), run_time=1.4)
        self.wait(0.4)
        self.play(FadeOut(title), FadeOut(caption), FadeOut(grid), FadeOut(frame), FadeOut(objects))


class PixelsToObjects(MovingCameraScene):
    def construct(self):
        title = Text("Traditional models see pixels", font_size=24, color=GREY_B).to_edge(UP)
        frame = make_frame(width=10.6, height=5.7).shift(DOWN * 0.15)
        mosaic, clusters = build_pixel_mosaic()
        mosaic.move_to(frame.get_center())

        self.play(FadeIn(title), Create(frame), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(cell, scale=0.8) for cell in mosaic], lag_ratio=0.005, run_time=2.5))
        self.play(self.camera.frame.animate.scale(0.96).move_to(frame.get_center()), run_time=1.2)
        self.play(Indicate(mosaic[8], color=BLUE_B), run_time=0.8)

        pixel_label = Text("raw pixels", font_size=20, color=BLUE_B).next_to(frame, DOWN, buff=0.18)
        self.play(FadeIn(pixel_label, shift=UP * 0.08))

        for cluster in clusters:
            focus = SurroundingRectangle(cluster, buff=0.08, color=GREY_B, stroke_width=1.5)
            self.play(Create(focus), run_time=0.5)
            self.play(FadeOut(focus), run_time=0.25)

        self.play(self.camera.frame.animate.scale(1.08).move_to(frame.get_center()), run_time=1.0)
        self.play(FadeOut(title), FadeOut(pixel_label), FadeOut(frame), FadeOut(mosaic))


class SlotAttentionMechanism(MovingCameraScene):
    def construct(self):
        title = Text("Slots are empty containers", font_size=24, color=GREY_B).to_edge(UP)
        frame = make_frame(width=10.8, height=5.8).shift(DOWN * 0.15)
        mosaic, clusters = build_pixel_mosaic()
        mosaic.move_to(frame.get_center())
        mosaic.set_opacity(0.48)

        slots, labels = build_slot_boxes()
        slot_colors = [BLUE_B, RED_C, YELLOW_C]

        self.play(FadeIn(title), Create(frame), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(cell, scale=0.85) for cell in mosaic], lag_ratio=0.005, run_time=1.8))
        self.play(LaggedStart(*[Create(slot) for slot in slots], lag_ratio=0.08, run_time=1.2))
        self.play(FadeIn(labels, shift=UP * 0.06), run_time=0.7)

        object_cards = VGroup()
        card_positions = [np.array([-3.5, -0.55, 0.0]), np.array([0.0, -0.55, 0.0]), np.array([3.5, -0.55, 0.0])]

        for index, spec in enumerate(OBJECT_SPECS[:3]):
            if spec["kind"] == Circle:
                shape = Circle(radius=0.34)
            elif spec["kind"] == Square:
                shape = Square(side_length=0.62)
            else:
                shape = Triangle().scale(0.63)

            shape.set_fill(spec["color"], opacity=0.9)
            shape.set_stroke(color=spec["color"], width=3)
            shape.move_to(card_positions[index])
            object_cards.add(shape)

        self.play(
            LaggedStart(
                *[TransformFromCopy(clusters[index], object_cards[index]) for index in range(3)],
                lag_ratio=0.18,
                run_time=2.0,
            )
        )

        arrows = VGroup(
            Arrow(slots[0].get_bottom(), object_cards[0].get_top(), buff=0.1, stroke_width=2.5, color=slot_colors[0]),
            Arrow(slots[1].get_bottom(), object_cards[1].get_top(), buff=0.1, stroke_width=2.5, color=slot_colors[1]),
            Arrow(slots[2].get_bottom(), object_cards[2].get_top(), buff=0.1, stroke_width=2.5, color=slot_colors[2]),
        )
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.12, run_time=1.3))

        emphasis = VGroup(
            SurroundingRectangle(object_cards[0], color=slot_colors[0], buff=0.14),
            SurroundingRectangle(object_cards[1], color=slot_colors[1], buff=0.14),
            SurroundingRectangle(object_cards[2], color=slot_colors[2], buff=0.14),
        )
        self.play(LaggedStart(*[Create(box) for box in emphasis], lag_ratio=0.12, run_time=0.9))
        self.play(self.camera.frame.animate.scale(0.96).move_to(frame.get_center()), run_time=1.1)
        self.wait(0.3)
        self.play(FadeOut(title), FadeOut(labels), FadeOut(frame), FadeOut(mosaic), FadeOut(object_cards), FadeOut(arrows), FadeOut(emphasis), FadeOut(slots))


class AlphaChannelBlending(MovingCameraScene):
    def construct(self):
        title = Text("Slots compete to explain the scene", font_size=24, color=GREY_B).to_edge(UP)
        frame = make_frame(width=10.8, height=5.8).shift(DOWN * 0.15)
        mosaic, clusters = build_pixel_mosaic()
        mosaic.move_to(frame.get_center())
        mosaic.set_opacity(0.42)

        slots, labels = build_slot_boxes()
        slot_colors = [BLUE_B, RED_C, YELLOW_C]

        self.play(FadeIn(title), Create(frame), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(cell, scale=0.85) for cell in mosaic], lag_ratio=0.005, run_time=1.7))
        self.play(LaggedStart(*[Create(slot) for slot in slots], lag_ratio=0.08, run_time=1.1))
        self.play(FadeIn(labels, shift=UP * 0.06), run_time=0.7)

        targets = [clusters[0], clusters[1], clusters[2]]
        attention_lines = build_attention_lines(slots, targets, slot_colors)
        self.play(LaggedStart(*[Create(line) for line in attention_lines], lag_ratio=0.02, run_time=1.1))

        for index, cluster in enumerate(targets):
            focus_box = SurroundingRectangle(cluster, buff=0.08, color=slot_colors[index], stroke_width=2.5)
            chosen_line = attention_lines[index * len(targets) + index]
            self.play(Create(focus_box), chosen_line.animate.set_opacity(0.95).set_stroke(width=4.0), run_time=0.8)
            self.play(Indicate(focus_box, color=slot_colors[index]), run_time=0.7)
            self.play(FadeOut(focus_box), run_time=0.25)

        alpha_tags = VGroup(
            Text("mask", font_size=18, color=slot_colors[0]).next_to(slots[0], DOWN, buff=0.16),
            Text("mask", font_size=18, color=slot_colors[1]).next_to(slots[1], DOWN, buff=0.16),
            Text("mask", font_size=18, color=slot_colors[2]).next_to(slots[2], DOWN, buff=0.16),
        )
        self.play(FadeIn(alpha_tags, shift=UP * 0.05), run_time=0.7)
        self.play(self.camera.frame.animate.scale(0.95).move_to(frame.get_center()), run_time=1.0)
        self.wait(0.3)
        self.play(FadeOut(title), FadeOut(labels), FadeOut(alpha_tags), FadeOut(frame), FadeOut(mosaic), FadeOut(attention_lines), FadeOut(slots))


class CausalIntervention(MovingCameraScene):
    def construct(self):
        title = Text("Object vectors stay stable", font_size=24, color=GREY_B).to_edge(UP)
        left_frame = make_frame(width=5.0, height=4.6).shift(LEFT * 3.1 + DOWN * 0.25)
        right_frame = make_frame(width=5.0, height=4.6).shift(RIGHT * 3.1 + DOWN * 0.25)
        left_objects = build_object_cluster()
        right_objects = build_object_cluster().copy()
        right_objects.shift(RIGHT * 0.2 + DOWN * 0.15)

        latent_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=4.1,
            y_length=3.3,
            axis_config={"stroke_color": "#40617f", "stroke_width": 2, "include_tip": False},
        ).scale(0.85)
        latent_axes.move_to(RIGHT * 0.35 + DOWN * 0.1)

        points = VGroup()
        vectors = VGroup()
        latent_positions = [np.array([1.1, 2.6, 0.0]), np.array([2.4, 1.6, 0.0]), np.array([3.2, 2.8, 0.0])]
        colors = [BLUE_B, RED_C, YELLOW_C]

        for index, position in enumerate(latent_positions):
            dot = Dot(point=latent_axes.c2p(position[0], position[1]), radius=0.08, color=colors[index])
            vector = Arrow(latent_axes.c2p(0, 0), dot.get_center(), buff=0.0, stroke_width=4, color=colors[index])
            points.add(dot)
            vectors.add(vector)

        captions = VGroup(
            Text("generalize", font_size=20, color=GREY_B),
            Text("reason", font_size=20, color=GREY_B),
            Text("intervene", font_size=20, color=GREY_B),
        ).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.35)

        self.play(FadeIn(title), Create(left_frame), Create(right_frame), run_time=1.1)
        self.play(LaggedStart(*[GrowFromCenter(obj) for obj in left_objects], lag_ratio=0.12, run_time=1.5))
        self.play(LaggedStart(*[FadeIn(obj, shift=RIGHT * 0.1) for obj in right_objects], lag_ratio=0.08, run_time=1.2))
        self.play(Create(latent_axes), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(vector) for vector in vectors], lag_ratio=0.1, run_time=1.2))
        self.play(LaggedStart(*[FadeIn(dot, scale=0.8) for dot in points], lag_ratio=0.1, run_time=0.8))
        self.play(FadeIn(captions, shift=UP * 0.1), run_time=0.8)

        stable_box = SurroundingRectangle(right_objects[1], color=RED_C, buff=0.12)
        self.play(Create(stable_box), Flash(points[1], color=RED_C, flash_radius=0.55, line_length=0.15), run_time=0.9)
        self.play(self.camera.frame.animate.scale(0.92).move_to(RIGHT * 0.35 + DOWN * 0.05), run_time=1.0)
        self.wait(0.4)
        self.play(FadeOut(title), FadeOut(left_frame), FadeOut(right_frame), FadeOut(left_objects), FadeOut(right_objects), FadeOut(latent_axes), FadeOut(vectors), FadeOut(points), FadeOut(captions), FadeOut(stable_box))


class EndingScene(MovingCameraScene):
    def construct(self):
        pixels = Text("pixels", font_size=30, color=BLUE_B)
        objects = Text("objects", font_size=30, color=GREEN_C)
        reasoning = Text("reasoning", font_size=30, color=YELLOW_C)
        chain = VGroup(pixels, objects, reasoning).arrange(RIGHT, buff=1.6).move_to(UP * 0.65)

        arrow1 = Arrow(pixels.get_right(), objects.get_left(), buff=0.18, color=BLUE_B, stroke_width=4)
        arrow2 = Arrow(objects.get_right(), reasoning.get_left(), buff=0.18, color=GREEN_C, stroke_width=4)
        summary = Text("From pixels to objects, from objects to reasoning.", font_size=30, color=WHITE, weight=BOLD)
        summary.move_to(DOWN * 0.8)
        accent = Line(LEFT * 4.0, RIGHT * 4.0, color="#2b4665", stroke_width=2).next_to(summary, DOWN, buff=0.35)

        self.play(FadeIn(chain, shift=UP * 0.15), run_time=1.0)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), run_time=0.9)
        self.play(Create(accent), run_time=0.7)
        self.play(Write(summary, run_time=1.8))
        self.play(self.camera.frame.animate.scale(1.02), run_time=0.9)
        self.wait(1.0)