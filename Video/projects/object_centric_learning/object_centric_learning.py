from manim import *
import numpy as np
from shared.manim_defaults import configure_vietnamese_text

configure_vietnamese_text()

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


def make_vector(values, color):
    mobs = VGroup(*[Text(f"{val:.1f}", font_size=18, color=WHITE) for val in values])
    mobs.arrange(DOWN, buff=0.15)
    
    h = mobs.height + 0.16
    w = 0.15
    margin = 0.1
    
    left_x = mobs.get_left()[0] - margin
    right_x = mobs.get_right()[0] + margin
    y_top = mobs.get_center()[1] + h/2
    y_bottom = mobs.get_center()[1] - h/2
    
    l_bracket = VMobject(color=color)
    l_bracket.set_points_as_corners([
        np.array([left_x + w, y_top, 0.0]),
        np.array([left_x, y_top, 0.0]),
        np.array([left_x, y_bottom, 0.0]),
        np.array([left_x + w, y_bottom, 0.0])
    ])
    l_bracket.set_stroke(width=2.5)
    
    r_bracket = VMobject(color=color)
    r_bracket.set_points_as_corners([
        np.array([right_x - w, y_top, 0.0]),
        np.array([right_x, y_top, 0.0]),
        np.array([right_x, y_bottom, 0.0]),
        np.array([right_x - w, y_bottom, 0.0])
    ])
    r_bracket.set_stroke(width=2.5)
    
    return VGroup(l_bracket, mobs, r_bracket)


class SlotAttentionIntro(MovingCameraScene):
    def construct(self):
        frame = make_frame()
        objects = build_object_cluster()
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-3.5, 3.5, 1],
            background_line_style={"stroke_color": "#13304a", "stroke_width": 1, "stroke_opacity": 0.2},
        ).scale(0.9)

        title = Text("Object-Centric Learning", font_size=36, weight=BOLD, color="#F4D345").to_edge(UP).set_z_index(100)
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
        title = Text("Traditional models see pixels", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
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
        title = Text("Slots are empty containers", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
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
        title = Text("Slots compete to explain the scene", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
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
        title = Text("Object vectors stay stable", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
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




# Customized classes for the 13 scenes of the new script
class Scene1(MovingCameraScene):
    def construct(self):
        title = Text("Chúng ta nhìn thế giới như thế nào?", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
        frame = make_frame(width=10.0, height=5.5).shift(DOWN * 0.1)
        self.play(FadeIn(title), Create(frame), run_time=1.5)
        self.wait(2.0)
        
        road = ImageMobject("assets/road.png").set_width(10.0).shift(DOWN * 1.8)
        self.play(FadeIn(road), run_time=1.5)
        
        tree = ImageMobject("assets/tree.png").set_height(2.5).shift(LEFT * 3.5 + DOWN * 0.5)
        ped = ImageMobject("assets/pedestrian.png").set_height(1.8).shift(LEFT * 1.2 + DOWN * 0.8)
        car = ImageMobject("assets/car.png").set_height(1.8).shift(RIGHT * 1.5 + DOWN * 0.8)
        sign = ImageMobject("assets/sign.png").set_height(1.8).shift(RIGHT * 3.8 + DOWN * 0.8)
        
        self.play(LaggedStart(
            FadeIn(tree, shift=UP*0.1),
            FadeIn(ped, shift=UP*0.1),
            FadeIn(car, shift=LEFT*0.2),
            FadeIn(sign, shift=UP*0.1),
            lag_ratio=0.3, run_time=2.5
        ))
        
        box_car = SurroundingRectangle(car, color=BLUE_B, buff=0.15, stroke_width=2.5)
        label_car = Text("Xe ô tô", font_size=18, color=BLUE_B).next_to(box_car, UP, buff=0.1)
        
        box_ped = SurroundingRectangle(ped, color=RED, buff=0.15, stroke_width=2.5)
        label_ped = Text("Người đi bộ", font_size=18, color=RED).next_to(box_ped, UP, buff=0.1)
        
        box_tree = SurroundingRectangle(tree, color=GREEN_C, buff=0.15, stroke_width=2.5)
        label_tree = Text("Cây", font_size=18, color=GREEN_C).next_to(box_tree, UP, buff=0.1)
        
        box_sign = SurroundingRectangle(sign, color=YELLOW_C, buff=0.15, stroke_width=2.5)
        label_sign = Text("Biển báo", font_size=18, color=YELLOW_C).next_to(box_sign, UP, buff=0.1)
        
        self.wait(2.5)
        self.play(Create(box_car), FadeIn(label_car), run_time=1.0)
        self.wait(2.5)
        self.play(Create(box_ped), FadeIn(label_ped), run_time=1.0)
        self.wait(2.5)
        self.play(Create(box_tree), FadeIn(label_tree), run_time=1.0)
        self.wait(3.5)
        self.play(Create(box_sign), FadeIn(label_sign), run_time=1.0)
        
        self.wait(5.0)
        self.play(Indicate(box_car, color=BLUE_B), Indicate(box_ped, color=RED), Indicate(box_tree, color=GREEN_C), Indicate(box_sign, color=YELLOW_C), run_time=2.5)
        self.wait(14.0)

class Scene2(MovingCameraScene):
    def construct(self):
        title = Text("Máy tính chỉ nhìn thấy pixels", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
        frame = make_frame(width=10.0, height=5.5).shift(DOWN * 0.1)
        
        car = ImageMobject("assets/car.png").set_height(2.5).shift(DOWN * 0.5)
        
        self.play(FadeIn(title), Create(frame), FadeIn(car), run_time=1.5)
        self.wait(2.5)
        
        self.play(self.camera.frame.animate.scale(0.35).move_to(car.get_center()), run_time=2.5)
        
        pixel_grid = VGroup()
        rows, cols = 6, 8
        cell_size = 0.18
        for r in range(rows):
            for c in range(cols):
                val = np.random.uniform(0.1, 0.9)
                col = interpolate_color(BLACK, BLUE_B, val)
                sq = Square(side_length=cell_size, color="#12253d", stroke_width=0.3)
                sq.set_fill(col, opacity=0.95)
                sq.move_to(car.get_center() + np.array([(c - cols/2)*cell_size, (r - rows/2)*cell_size, 0]))
                pixel_grid.add(sq)
                
        self.play(FadeOut(car), FadeIn(pixel_grid), run_time=2.0)
        self.wait(2.5)
        
        num_grid = VGroup()
        for sq in pixel_grid[::4]: 
            num = DecimalNumber(np.random.uniform(0, 1), num_decimal_places=1, font_size=6, color=WHITE, mob_class=Text)
            num.move_to(sq.get_center())
            num_grid.add(num)
            
        self.play(FadeIn(num_grid), run_time=2.0)
        self.wait(4.0)
        
        self.play(self.camera.frame.animate.scale(1/0.35).move_to(ORIGIN), run_time=2.0)
        self.wait(3.0)

class Scene3(Scene):
    def construct(self):
        title = Text("Machine Learning hoạt động ra sao?", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
        
        nodes = VGroup()
        input_layer = VGroup(*[Circle(radius=0.15, color=BLUE, fill_opacity=0.8).shift(LEFT*2.5 + UP*y) for y in [-1.2, -0.4, 0.4, 1.2]])
        hidden_layer = VGroup(*[Circle(radius=0.15, color=TEAL, fill_opacity=0.8).shift(UP*y) for y in [-1.5, -0.7, 0.1, 0.9, 1.7]])
        output_layer = VGroup(*[Circle(radius=0.15, color=YELLOW, fill_opacity=0.8).shift(RIGHT*2.5 + UP*y) for y in [-0.5, 0.5]])
        
        nodes.add(input_layer, hidden_layer, output_layer)
        
        connections = VGroup()
        for i_node in input_layer:
            for h_node in hidden_layer:
                connections.add(Line(i_node.get_right(), h_node.get_left(), stroke_width=1, color=GRAY, stroke_opacity=0.4))
        for h_node in hidden_layer:
            for o_node in output_layer:
                connections.add(Line(h_node.get_right(), o_node.get_left(), stroke_width=1, color=GRAY, stroke_opacity=0.4))
                
        self.play(FadeIn(title), FadeIn(nodes), FadeIn(connections), run_time=1.5)
        self.wait(2.0)
        
        cat_box = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.1, color=BLUE, fill_opacity=0.2).scale(0.8).shift(LEFT * 4.5 + UP * 0.5)
        cat_img = ImageMobject("assets/cat.png").set_height(0.6).move_to(cat_box.get_center())
        cat_sample = Group(cat_box, cat_img)

        not_cat_box = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.1, color=RED, fill_opacity=0.2).scale(0.8).shift(LEFT * 4.5 + DOWN * 0.5)
        not_cat_img = ImageMobject("assets/not_cat.png").set_height(0.6).move_to(not_cat_box.get_center())
        not_cat_sample = Group(not_cat_box, not_cat_img)

        self.play(FadeIn(cat_sample), FadeIn(not_cat_sample), run_time=1.5)
        self.play(cat_sample.animate.shift(RIGHT * 1.8), not_cat_sample.animate.shift(RIGHT * 1.8), run_time=2.0)
        self.play(FadeOut(cat_sample), FadeOut(not_cat_sample), run_time=1.0)
        self.wait(1.5)
        
        signals = VGroup()
        for _ in range(15):
            line = connections[np.random.randint(len(connections))]
            signal = Dot(color=YELLOW_B, radius=0.06).move_to(line.get_start())
            signals.add(signal)
            self.play(signal.animate.move_to(line.get_end()), run_time=0.4, rate_func=linear)
            
        self.play(FadeOut(signals))
        self.wait(1.5)
        
        accuracy_label = Text("Độ chính xác (Train):", font_size=18, color=GREY_B).shift(DOWN * 2.2 + LEFT * 1.0)
        accuracy_num = DecimalNumber(10, num_decimal_places=0, font_size=24, color=GREEN_C, mob_class=Text).next_to(accuracy_label, RIGHT, buff=0.15)
        percent_sign = Text("%", font_size=24, color=GREEN_C).next_to(accuracy_num, RIGHT, buff=0.05)
        self.play(FadeIn(accuracy_label), FadeIn(accuracy_num), FadeIn(percent_sign), run_time=1.0)
        
        self.play(ChangeDecimalToValue(accuracy_num, 98), run_time=3.5)
        self.wait(2.0)
        
        cat_result_box = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.1, color=GREEN, fill_opacity=0.3).shift(RIGHT * 2.5 + UP * 2.0)
        cat_text = Text("Mèo: 98%", font_size=20, color=GREEN).move_to(cat_result_box.get_center())
        self.play(Create(cat_result_box), Write(cat_text), run_time=1.5)
        self.wait(6.5)

class Scene4(Scene):
    def construct(self):
        title = Text("Thách thức ngoài thế giới thực (Out-of-Distribution)", font_size=22, color=GREY_B).to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(2.0)
        
        left_box = RoundedRectangle(width=5.0, height=4.2, corner_radius=0.12, color=GRAY_D, fill_opacity=0.3).shift(LEFT * 3.1 + DOWN * 0.2)
        left_title = Text("Huấn luyện (Quen thuộc)", font_size=16, color=WHITE).next_to(left_box, UP, buff=0.1)
        self.play(Create(left_box), FadeIn(left_title), run_time=1.5)
        
        grass = Rectangle(width=4.8, height=0.6, color=GREEN_D, fill_opacity=0.8).move_to(left_box.get_bottom() + UP * 0.4)
        cat_img = ImageMobject("assets/cat.png").set_height(1.4).move_to(left_box.get_center() + DOWN * 0.25)
        cat = Group(grass, cat_img)
        self.play(FadeIn(cat), run_time=1.5)
        self.wait(2.0)
        
        pred_left = Text("Dự đoán: Mèo (99%)", font_size=18, color=GREEN_C).move_to(left_box.get_center() + UP * 1.2)
        check = Text("✓ Nhận diện đúng", font_size=20, color=GREEN).next_to(pred_left, DOWN, buff=0.15)
        self.play(FadeIn(pred_left), FadeIn(check), run_time=1.5)
        self.wait(4.0)
        
        right_box = RoundedRectangle(width=5.0, height=4.2, corner_radius=0.12, color=GRAY_D, fill_opacity=0.3).shift(RIGHT * 3.1 + DOWN * 0.2)
        right_title = Text("Thực tế (Mới lạ / Thay đổi)", font_size=16, color=WHITE).next_to(right_box, UP, buff=0.1)
        self.play(Create(right_box), FadeIn(right_title), run_time=1.5)
        
        snow = Rectangle(width=4.8, height=0.6, color=WHITE, fill_opacity=0.9).move_to(right_box.get_bottom() + UP * 0.4)
        cat_snow = ImageMobject("assets/cat_snow.png").set_height(1.4).move_to(right_box.get_center() + DOWN * 0.25)
        self.play(FadeIn(Group(snow, cat_snow)), run_time=1.5)
        self.wait(2.5)
        
        cat_hidden = ImageMobject("assets/cat_hidden.png").set_height(1.4).move_to(right_box.get_center() + DOWN * 0.25)
        self.play(FadeTransform(cat_snow, cat_hidden), run_time=1.5)
        self.wait(3.0)
        
        pred_right = Text("Dự đoán: Không rõ (92%)", font_size=18, color=RED_C).move_to(right_box.get_center() + UP * 1.2)
        cross = Text("✗ Nhận diện sai", font_size=20, color=RED).next_to(pred_right, DOWN, buff=0.15)
        self.play(FadeIn(pred_right), FadeIn(cross), run_time=1.5)
        self.wait(18.0)

class Scene5(Scene):
    def construct(self):
        title = Text("Structured Representation (Biểu diễn có cấu trúc)", font_size=22, color=GREY_B).to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(4.0)
        
        car_node = Group(Circle(radius=0.9, color=BLUE_B, fill_opacity=0.2), ImageMobject("assets/car.png").set_height(0.8), Text("Xe ô tô", font_size=16).shift(UP*1.2)).shift(UP * 1.2)
        ped_node = Group(Circle(radius=0.9, color=RED, fill_opacity=0.2), ImageMobject("assets/pedestrian.png").set_height(0.8), Text("Người đi bộ", font_size=16).shift(UP*1.2)).shift(LEFT * 3.2 + DOWN * 1.2)
        road_node = Group(Circle(radius=0.9, color=GRAY, fill_opacity=0.2), ImageMobject("assets/road.png").set_width(1.0), Text("Mặt đường", font_size=16).shift(UP*1.2)).shift(RIGHT * 3.2 + DOWN * 1.2)
        sign_node = Group(Circle(radius=0.9, color=YELLOW_C, fill_opacity=0.2), ImageMobject("assets/sign.png").set_height(0.8), Text("Biển báo", font_size=16).shift(UP*1.2)).shift(DOWN * 1.2)
        
        self.play(FadeIn(car_node), FadeIn(ped_node), FadeIn(road_node), FadeIn(sign_node), run_time=2.0)
        self.wait(4.0)
        
        arrow1 = Arrow(ped_node[0].get_top(), car_node[0].get_left(), color=YELLOW_C, stroke_width=3)
        label1 = Text("Đứng cạnh", font_size=14, color=YELLOW_C).next_to(arrow1.get_center(), UP * 0.5 + LEFT * 0.2)
        
        arrow2 = Arrow(car_node[0].get_right(), road_node[0].get_top(), color=YELLOW_C, stroke_width=3)
        label2 = Text("Di chuyển trên", font_size=14, color=YELLOW_C).next_to(arrow2.get_center(), UP * 0.5 + RIGHT * 0.2)
        
        arrow3 = Arrow(ped_node[0].get_right(), sign_node[0].get_left(), color=YELLOW_C, stroke_width=3)
        label3 = Text("Gần", font_size=14, color=YELLOW_C).next_to(arrow3.get_center(), DOWN * 0.5)
        
        arrow4 = Arrow(sign_node[0].get_right(), road_node[0].get_left(), color=YELLOW_C, stroke_width=3)
        label4 = Text("Nằm cạnh", font_size=14, color=YELLOW_C).next_to(arrow4.get_center(), DOWN * 0.5)
        
        self.play(GrowArrow(arrow1), FadeIn(label1), run_time=1.5)
        self.play(GrowArrow(arrow2), FadeIn(label2), run_time=1.5)
        self.play(GrowArrow(arrow3), FadeIn(label3), run_time=1.5)
        self.play(GrowArrow(arrow4), FadeIn(label4), run_time=1.5)
        self.wait(20.0)

class Scene6(Scene):
    def construct(self):
        title = Text("Khả năng tổng quát hóa có hệ thống (Compositionality)", font_size=22, color=GREY_B).to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(3.0)
        
        # Define 2D building blocks
        b1 = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.1, color=RED_C, fill_opacity=0.95)
        b1.shift(LEFT * 2.5 + DOWN * 1.5)
        b2 = RoundedRectangle(width=1.2, height=1.2, corner_radius=0.1, color=BLUE_C, fill_opacity=0.95)
        b2.shift(DOWN * 1.5)
        b3 = RoundedRectangle(width=1.6, height=0.8, corner_radius=0.1, color=YELLOW_C, fill_opacity=0.95)
        b3.shift(RIGHT * 2.5 + DOWN * 1.5)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(b3), run_time=2.0)
        self.wait(3.0)
        
        # Build House
        house_b1 = b1.animate.move_to(LEFT * 0.8 + DOWN * 0.6)
        house_b3 = b3.animate.move_to(RIGHT * 1.0 + DOWN * 0.6)
        house_b2 = b2.animate.move_to(UP * 0.4)
        
        self.play(house_b1, house_b3, run_time=1.5)
        self.play(house_b2, run_time=1.0)
        
        roof = Polygon(np.array([-2.2, 1.0, 0]), np.array([2.2, 1.0, 0]), np.array([0, 2.5, 0]), color=ORANGE, fill_opacity=0.95)
        self.play(FadeIn(roof, shift=DOWN*0.2), run_time=1.5)
        self.wait(4.0)
        
        # Build Truck
        truck_b1 = b1.animate.move_to(LEFT * 0.5 + DOWN * 0.1)
        truck_b2 = b2.animate.move_to(RIGHT * 1.1 + UP * 0.1)
        truck_b3 = b3.animate.move_to(LEFT * 0.5 + UP * 0.7)
        
        wheel1 = Circle(radius=0.35, color=GRAY_E, fill_opacity=1.0)
        wheel1.set_stroke(color=WHITE, width=3)
        wheel1.move_to(LEFT * 1.0 + DOWN * 0.5)
        
        wheel2 = Circle(radius=0.35, color=GRAY_E, fill_opacity=1.0)
        wheel2.set_stroke(color=WHITE, width=3)
        wheel2.move_to(RIGHT * 1.1 + DOWN * 0.5)
        
        self.play(FadeOut(roof), truck_b1, truck_b2, truck_b3, FadeIn(wheel1), FadeIn(wheel2), run_time=2.5)
        self.wait(15.0)

class Scene7(Scene):
    def construct(self):
        title = Text("Object-Centric Learning", font_size=22, color="#F4D345").to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(5.0)
        
        car = ImageMobject("assets/car.png").set_height(1.2).shift(LEFT * 3.0 + UP * 1.2)
        ped = ImageMobject("assets/pedestrian.png").set_height(1.2).shift(LEFT * 3.0 + DOWN * 0.2)
        tree = ImageMobject("assets/tree.png").set_height(1.5).shift(LEFT * 3.0 + DOWN * 1.5)
        self.play(FadeIn(car), FadeIn(ped), FadeIn(tree), run_time=2.0)
        self.wait(4.0)
        
        v1 = make_vector([0.9, 0.1, 0.8, 0.2], BLUE_B).shift(RIGHT * 1.5 + UP * 1.2).scale(0.8)
        v2 = make_vector([0.1, 0.9, 0.2, 0.7], RED).shift(RIGHT * 1.5 + DOWN * 0.2).scale(0.8)
        v3 = make_vector([0.3, 0.2, 0.9, 0.1], GREEN_C).shift(RIGHT * 1.5 + DOWN * 1.5).scale(0.8)
        
        l1 = Text("Vector 1 (Xe ô tô)", font_size=16, color=BLUE_B).next_to(v1, RIGHT, buff=0.2)
        l2 = Text("Vector 2 (Người đi bộ)", font_size=16, color=RED).next_to(v2, RIGHT, buff=0.2)
        l3 = Text("Vector 3 (Cây)", font_size=16, color=GREEN_C).next_to(v3, RIGHT, buff=0.2)
        
        a1 = Arrow(car.get_right(), v1.get_left(), color=BLUE_B, stroke_width=3)
        a2 = Arrow(ped.get_right(), v2.get_left(), color=RED, stroke_width=3)
        a3 = Arrow(tree.get_right(), v3.get_left(), color=GREEN_C, stroke_width=3)
        
        self.play(GrowArrow(a1), FadeIn(v1), FadeIn(l1), run_time=1.5)
        self.play(GrowArrow(a2), FadeIn(v2), FadeIn(l2), run_time=1.5)
        self.play(GrowArrow(a3), FadeIn(v3), FadeIn(l3), run_time=1.5)
        self.wait(12.0)

class Scene8(Scene):
    def construct(self):
        title = Text("Từ Feature Map đến Slots", font_size=22, color="#F4D345").to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(2.0)
        
        mesh = NumberPlane(
            x_range=[-3, 0, 0.5],
            y_range=[-2, 2, 0.5],
            background_line_style={"stroke_color": TEAL, "stroke_width": 1.5, "stroke_opacity": 0.3}
        ).shift(LEFT * 2.8 + DOWN * 0.2)
        mesh_label = Text("Bản đồ đặc trưng (Feature Map)", font_size=16, color=TEAL).next_to(mesh, UP, buff=0.15)
        self.play(Create(mesh), FadeIn(mesh_label), run_time=2.0)
        self.wait(3.0)
        
        slots = VGroup()
        for i, y in enumerate([1.2, -0.2, -1.6]):
            slot = RoundedRectangle(width=2.5, height=0.9, corner_radius=0.1, color=GRAY_C, stroke_width=2.5)
            slot.shift(RIGHT * 2.5 + UP * y)
            label = Text(f"Slot {i+1} [Trống]", font_size=16, color=GRAY_B).move_to(slot.get_center())
            slots.add(VGroup(slot, label))
            
        self.play(LaggedStart(*[FadeIn(s, shift=UP*0.1) for s in slots], lag_ratio=0.3, run_time=2.5))
        self.wait(3.0)
        
        flows = VGroup()
        for s in slots:
            flow = Arrow(mesh.get_right(), s[0].get_left(), color=TEAL, stroke_width=2.5)
            flows.add(flow)
            
        self.play(LaggedStart(*[GrowArrow(f) for f in flows], lag_ratio=0.2, run_time=2.0))
        self.wait(8.0)

class Scene9(Scene):
    def construct(self):
        title = Text("Cơ chế cạnh tranh (Competitive Attention)", font_size=22, color=GREY_B).to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(4.0)
        
        s1 = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.1, color=BLUE_B, stroke_width=3).shift(LEFT*2.8 + UP*1.8)
        s1_lbl = Text("Slot 1 (Xe)", font_size=14, color=BLUE_B).move_to(s1.get_center())
        s2 = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.1, color=RED, stroke_width=3).shift(UP*1.8)
        s2_lbl = Text("Slot 2 (Người)", font_size=14, color=RED).move_to(s2.get_center())
        s3 = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.1, color=GREEN_C, stroke_width=3).shift(RIGHT*2.8 + UP*1.8)
        s3_lbl = Text("Slot 3 (Cây)", font_size=14, color=GREEN_C).move_to(s3.get_center())
        
        slots = VGroup(s1, s1_lbl, s2, s2_lbl, s3, s3_lbl)
        self.play(FadeIn(slots), run_time=2.0)
        self.wait(3.0)
        
        obj_car = ImageMobject("assets/car.png").set_height(1.0).shift(LEFT*2.8 + DOWN*1.8)
        obj_ped = ImageMobject("assets/pedestrian.png").set_height(1.0).shift(DOWN*1.8)
        obj_tree = ImageMobject("assets/tree.png").set_height(1.2).shift(RIGHT*2.8 + DOWN*1.8)
        
        objs = Group(obj_car, obj_ped, obj_tree)
        self.play(FadeIn(objs), run_time=2.0)
        self.wait(3.0)
        
        lines = VGroup()
        for slot in [s1, s2, s3]:
            for obj in [obj_car, obj_ped, obj_tree]:
                line = Line(slot.get_bottom(), obj.get_top(), stroke_width=1.5, color=YELLOW_C, stroke_opacity=0.3)
                lines.add(line)
        self.play(Create(lines), run_time=2.0)
        self.wait(5.0)
        
        strong_lines = VGroup(
            Line(s1.get_bottom(), obj_car.get_top(), stroke_width=4.5, color=BLUE_B, stroke_opacity=0.9),
            Line(s2.get_bottom(), obj_ped.get_top(), stroke_width=4.5, color=RED, stroke_opacity=0.9),
            Line(s3.get_bottom(), obj_tree.get_top(), stroke_width=4.5, color=GREEN_C, stroke_opacity=0.9)
        )
        
        self.play(FadeOut(lines), Create(strong_lines), run_time=2.5)
        self.wait(12.0)

class Scene10(Scene):
    def construct(self):
        title = Text("Từ Grid đến Set Representation", font_size=22, color="#F4D345").to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(2.0)
        
        grid = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            background_line_style={"stroke_color": TEAL, "stroke_width": 2, "stroke_opacity": 0.5}
        ).scale(0.65).shift(LEFT * 3.0 + DOWN * 0.2)
        grid_lbl = Text("Lưới không gian (Grid)", font_size=16, color=TEAL).next_to(grid, UP, buff=0.15)
        
        self.play(Create(grid), FadeIn(grid_lbl), run_time=2.0)
        self.wait(3.0)
        
        arrow = Arrow(LEFT * 0.6, RIGHT * 0.6, color=YELLOW_C, stroke_width=4.5).shift(DOWN * 0.2)
        arrow_lbl = Text("Slot Attention", font_size=14, color=YELLOW_C).next_to(arrow, UP, buff=0.1)
        self.play(GrowArrow(arrow), FadeIn(arrow_lbl), run_time=1.5)
        self.wait(3.0)
        
        set_text = Text(
            "S = { v1, v2, v3 }",
            font_size=36,
            color=WHITE
        ).shift(RIGHT * 3.0 + DOWN * 0.2)
        set_lbl = Text("Tập hợp Vector (Set)", font_size=16, color=WHITE).next_to(set_text, UP, buff=0.4)
        
        self.play(Write(set_text), FadeIn(set_lbl), run_time=2.0)
        self.wait(8.0)

class Scene11(Scene):
    def construct(self):
        title = Text("Thành công trên dữ liệu nhân tạo (CLEVR)", font_size=22, color=GREY_B).to_edge(UP).set_z_index(100)
        frame = make_frame(width=10.0, height=5.5).shift(DOWN * 0.1)
        self.play(FadeIn(title), Create(frame), run_time=1.5)
        self.wait(3.0)
        
        sphere = Circle(radius=0.55, color=RED, fill_opacity=0.9).shift(LEFT * 2.5 + DOWN * 0.5)
        cube = Square(side_length=1.1, color=BLUE, fill_opacity=0.9).shift(DOWN * 0.5)
        cylinder = RoundedRectangle(width=0.8, height=1.3, corner_radius=0.1, color=YELLOW, fill_opacity=0.9).shift(RIGHT * 2.5 + DOWN * 0.4)
        
        self.play(LaggedStart(FadeIn(sphere), FadeIn(cube), FadeIn(cylinder), lag_ratio=0.3, run_time=2.5))
        self.wait(5.0)
        
        mask1 = Circle(radius=0.62, color=RED, stroke_width=4.5).move_to(sphere)
        mask2 = Square(side_length=1.2, color=BLUE, stroke_width=4.5).move_to(cube)
        mask3 = RoundedRectangle(width=0.9, height=1.4, corner_radius=0.1, color=YELLOW, stroke_width=4.5).move_to(cylinder)
        
        lbl_mask = Text("Phân vùng không giám sát", font_size=18, color=GREEN_C).next_to(frame, DOWN, buff=0.18)
        
        self.play(Create(mask1), Create(mask2), Create(mask3), FadeIn(lbl_mask), run_time=2.5)
        self.wait(8.0)

class Scene12(Scene):
    def construct(self):
        title = Text("Nhưng thế giới thực phức tạp hơn", font_size=22, color="#F4D345").to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(2.0)
        
        left_box = RoundedRectangle(width=5.0, height=4.2, corner_radius=0.12, color=GRAY_D, fill_opacity=0.3).shift(LEFT * 3.1 + DOWN * 0.2)
        left_title = Text("Mô phỏng (Đơn giản)", font_size=16, color=WHITE).next_to(left_box, UP, buff=0.1)
        self.play(Create(left_box), FadeIn(left_title), run_time=1.5)
        
        sphere = Circle(radius=0.6, color=RED, fill_opacity=0.9).move_to(left_box.get_center() + DOWN * 0.3)
        self.play(FadeIn(sphere), run_time=1.5)
        self.wait(3.0)
        
        right_box = RoundedRectangle(width=5.0, height=4.2, corner_radius=0.12, color=GRAY_D, fill_opacity=0.3).shift(RIGHT * 3.1 + DOWN * 0.2)
        right_title = Text("Thế giới thực (Phức tạp)", font_size=16, color=WHITE).next_to(right_box, UP, buff=0.1)
        self.play(Create(right_box), FadeIn(right_title), run_time=1.5)
        
        real_car = ImageMobject("assets/car_realistic.png").set_height(2.0).move_to(right_box.get_center() + DOWN * 0.2)
        self.play(FadeIn(real_car), run_time=2.0)
        self.wait(5.0)
        
        fail_mask = Polygon(
            right_box.get_center() + np.array([-1.2, -0.6, 0]),
            right_box.get_center() + np.array([1.3, -0.6, 0]),
            right_box.get_center() + np.array([0.8, 0.4, 0]),
            right_box.get_center() + np.array([-1.0, 0.6, 0]),
            color=RED, stroke_width=3, fill_opacity=0.15
        )
        fail_lbl = Text("Mặt nạ phân vùng bị lỗi/nhiễu", font_size=14, color=RED).next_to(right_box.get_bottom(), UP, buff=0.18)
        
        self.play(Create(fail_mask), FadeIn(fail_lbl), run_time=2.0)
        self.wait(10.0)

class Scene13(Scene):
    def construct(self):
        title = Text("Chuyển sang phần tiếp theo", font_size=24, color="#F4D345").to_edge(UP).set_z_index(100)
        self.play(FadeIn(title), run_time=1.5)
        self.wait(2.0)
        
        start_pt = LEFT * 3.5 + DOWN * 0.5
        end_pt = RIGHT * 3.5 + DOWN * 0.5
        bridge = Line(start_pt, end_pt, color=GRAY, stroke_width=5)
        lbl_start = Text("Dữ liệu nhân tạo\n(Đơn giản)", font_size=16, color=WHITE).next_to(start_pt, DOWN, buff=0.15)
        lbl_end = Text("Dữ liệu thực tế\n(Phức tạp)", font_size=16, color=WHITE).next_to(end_pt, DOWN, buff=0.15)
        
        self.play(Create(bridge), FadeIn(lbl_start), FadeIn(lbl_end), run_time=2.5)
        self.wait(3.0)
        
        question = Text("?", font_size=48, color=YELLOW_C, weight=BOLD).move_to(DOWN * 0.1)
        self.play(FadeIn(question, shift=UP * 0.2), Flash(question, color=YELLOW_C, flash_radius=0.7), run_time=2.0)
        self.wait(4.0)
        
        slogan = Text("Từ điểm ảnh đến đối tượng, từ đối tượng đến suy luận.", font_size=26, color=WHITE, weight=BOLD).shift(UP * 1.5)
        self.play(Write(slogan), run_time=3.5)
        self.wait(5.0)
