from manim import *
import numpy as np


config.background_color = "#06111f"

BG = "#06111f"
PANEL = "#10243c"
PANEL_2 = "#173252"
TEXT = "#F4D345"
MUTED = "#c3cfdd"
BLUE = "#4ea1ff"
CYAN = "#4dd7d7"
GREEN = "#5fd18b"
YELLOW = "#ffd166"
ORANGE = "#ff9f43"
RED = "#ff6b6b"
PURPLE = "#b692ff"
STROKE = "#4c6e95"

TITLE_Y = 3.30
SUBTITLE_Y = 2.68
CONTENT_TOP = 2.25
CONTENT_CENTER_Y = 0.15
CONTENT_BOTTOM = -2.15
FOOTER_Y = -3.25
SAFE_LEFT = -6.2
SAFE_RIGHT = 6.2
SAFE_TOP = 3.35
SAFE_BOTTOM = -3.35
LEFT_X = -3.4
CENTER_X = 0
RIGHT_X = 3.4
CARD_WIDTH = 3.4
CARD_HEIGHT = 1.35
PANEL_WIDTH = 5.6
PANEL_HEIGHT = 3.6

FONT = "Segoe UI"
Z_BG = 0
Z_PANEL = 1
Z_ARROW = 2
Z_CARD = 3
Z_TEXT = 4
Z_UI = 5


def _text(text, size=22, color=TEXT, weight=NORMAL, align="center"):
    mob = Text(
        text,
        font=FONT,
        font_size=size,
        color=color,
        weight=weight,
        line_spacing=1.0,
        disable_ligatures=True,
    )
    mob.set_text_align(align)
    mob.set_z_index(Z_TEXT)
    return mob


def fit_to_width(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def fit_to_height(mob, max_height):
    if mob.height > max_height:
        mob.scale_to_fit_height(max_height)
    return mob


def keep_inside_frame(mob, margin=0.25):
    left = SAFE_LEFT + margin
    right = SAFE_RIGHT - margin
    top = SAFE_TOP - margin
    bottom = SAFE_BOTTOM + margin
    if mob.width > right - left:
        mob.scale_to_fit_width(right - left)
    if mob.height > top - bottom:
        mob.scale_to_fit_height(top - bottom)
    if mob.get_left()[0] < left:
        mob.shift(RIGHT * (left - mob.get_left()[0]))
    if mob.get_right()[0] > right:
        mob.shift(LEFT * (mob.get_right()[0] - right))
    if mob.get_top()[1] > top:
        mob.shift(DOWN * (mob.get_top()[1] - top))
    if mob.get_bottom()[1] < bottom:
        mob.shift(UP * (bottom - mob.get_bottom()[1]))
    return mob


def add_background(scene):
    base = Rectangle(width=config.frame_width, height=config.frame_height)
    base.set_fill(BG, 1).set_stroke(width=0)
    header = Rectangle(width=config.frame_width, height=1.12)
    header.set_fill("#0a1728", 0.74).set_stroke(width=0).to_edge(UP, buff=0)
    footer = Rectangle(width=config.frame_width, height=0.82)
    footer.set_fill("#0a1728", 0.54).set_stroke(width=0).to_edge(DOWN, buff=0)
    grid = VGroup()
    for x in np.linspace(SAFE_LEFT, SAFE_RIGHT, 10):
        grid.add(Line([x, CONTENT_BOTTOM, 0], [x, CONTENT_TOP, 0], color=STROKE, stroke_width=0.5).set_opacity(0.10))
    for y in np.linspace(CONTENT_BOTTOM, CONTENT_TOP, 5):
        grid.add(Line([SAFE_LEFT, y, 0], [SAFE_RIGHT, y, 0], color=STROKE, stroke_width=0.5).set_opacity(0.08))
    bg = VGroup(base, header, footer, grid)
    bg.set_z_index(Z_BG)
    scene.add(bg)


def make_title(text):
    mob = _text(text, 30, TEXT, BOLD)
    fit_to_width(mob, 8.2)
    mob.move_to([CENTER_X, TITLE_Y, 0]).set_z_index(Z_UI)
    return mob


def make_subtitle(text):
    mob = _text(text, 18, MUTED)
    fit_to_width(mob, 8.9)
    mob.move_to([CENTER_X, SUBTITLE_Y, 0]).set_z_index(Z_UI)
    return mob


def make_section_tag(number, label, color):
    num = make_pill(number, color, width=0.78)
    lab = _text(label, 12, MUTED)
    fit_to_width(lab, 1.85)
    tag = VGroup(num, lab).arrange(RIGHT, buff=0.16)
    tag.move_to([4.95, TITLE_Y, 0]).set_z_index(Z_UI)
    return tag


def make_footer_takeaway(text, color=ORANGE):
    label = _text(text, 15, color, MEDIUM)
    fit_to_width(label, 10.6)
    bg = RoundedRectangle(width=max(4.0, label.width + 0.62), height=0.48, corner_radius=0.14)
    bg.set_fill("#08101d", 0.96).set_stroke(color, width=1.0, opacity=0.62)
    bg.move_to([CENTER_X, FOOTER_Y, 0]).set_z_index(Z_UI)
    label.move_to(bg).set_z_index(Z_UI + 1)
    return VGroup(bg, label)


def make_card(title, body=None, color=BLUE, width=CARD_WIDTH, height=CARD_HEIGHT):
    bg = RoundedRectangle(width=width, height=height, corner_radius=0.14)
    bg.set_fill(PANEL, 0.97).set_stroke(color, width=1.4, opacity=0.82).set_z_index(Z_CARD)
    title_mob = _text(title, 19, TEXT, MEDIUM)
    fit_to_width(title_mob, width - 0.34)
    if body:
        body_mob = _text(body, 13, MUTED)
        fit_to_width(body_mob, width - 0.42)
        group_text = VGroup(title_mob, body_mob).arrange(DOWN, buff=0.16)
        fit_to_height(group_text, height - 0.24)
        group_text.move_to(bg)
        card = VGroup(bg, group_text).set_z_index(Z_CARD)
        group_text.set_z_index(Z_TEXT)
        return card
    title_mob.move_to(bg)
    fit_to_height(title_mob, height - 0.18)
    return VGroup(bg, title_mob).set_z_index(Z_CARD)


def make_pill(text, color=BLUE, width=None):
    label = _text(text, 13, color, MEDIUM)
    w = width or max(label.width + 0.42, 1.05)
    bg = RoundedRectangle(width=w, height=0.34, corner_radius=0.17)
    bg.set_fill(color, 0.14).set_stroke(color, width=1.0, opacity=0.78).set_z_index(Z_CARD)
    label.move_to(bg).set_z_index(Z_TEXT)
    return VGroup(bg, label).set_z_index(Z_CARD)


def make_icon_label(icon_mob, label, color=BLUE):
    lab = _text(label, 15, color, MEDIUM)
    return VGroup(icon_mob, lab).arrange(DOWN, buff=0.14).set_z_index(Z_TEXT)


def connect_mobs(start_mob, end_mob, color=MUTED, buff=0.15):
    dx = abs(start_mob.get_center()[0] - end_mob.get_center()[0])
    dy = abs(start_mob.get_center()[1] - end_mob.get_center()[1])
    if dx >= dy:
        start = start_mob.get_right() if start_mob.get_center()[0] < end_mob.get_center()[0] else start_mob.get_left()
        end = end_mob.get_left() if start_mob.get_center()[0] < end_mob.get_center()[0] else end_mob.get_right()
    else:
        start = start_mob.get_bottom() if start_mob.get_center()[1] > end_mob.get_center()[1] else start_mob.get_top()
        end = end_mob.get_top() if start_mob.get_center()[1] > end_mob.get_center()[1] else end_mob.get_bottom()
    arrow = Arrow(start, end, buff=buff, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.15)
    arrow.set_z_index(Z_ARROW)
    return arrow


def routed_arrow(start_mob, end_mob, color=MUTED):
    start = start_mob.get_bottom()
    end = end_mob.get_top()
    mid_y = (start[1] + end[1]) / 2
    line = VMobject()
    line.set_points_as_corners([start, [start[0], mid_y, 0], [end[0], mid_y, 0], end])
    line.set_stroke(color, width=3).set_z_index(Z_ARROW)
    tip = Triangle().scale(0.10).rotate(PI).set_fill(color, 1).set_stroke(width=0)
    tip.move_to(end + DOWN * 0.05).set_z_index(Z_ARROW)
    return VGroup(line, tip)


def make_pipeline(labels, colors=None, max_width=11.2):
    colors = colors or [BLUE] * len(labels)
    nodes = VGroup(*[make_card(label, color=colors[i], width=1.72, height=0.82) for i, label in enumerate(labels)])
    nodes.arrange(RIGHT, buff=0.46)
    fit_to_width(nodes, max_width)
    arrows = VGroup(*[connect_mobs(nodes[i], nodes[i + 1], colors[min(i + 1, len(colors) - 1)], buff=0.1) for i in range(len(nodes) - 1)])
    return VGroup(nodes, arrows), nodes, arrows


def fade_replace(scene, old_group, new_group, run_time=0.8):
    keep_inside_frame(new_group, margin=0.18)
    if old_group is None:
        scene.play(FadeIn(new_group, shift=UP * 0.08), run_time=run_time)
    else:
        scene.play(FadeOut(old_group), run_time=run_time * 0.45)
        scene.play(FadeIn(new_group, shift=UP * 0.08), run_time=run_time * 0.55)
    return new_group


def dim_group(group, opacity=0.25):
    group.generate_target()
    group.target.set_opacity(opacity)
    return MoveToTarget(group)


def boxes_overlap(a, b, padding=0.05):
    ax1, ax2 = a.get_left()[0], a.get_right()[0]
    ay1, ay2 = a.get_bottom()[1], a.get_top()[1]
    bx1, bx2 = b.get_left()[0], b.get_right()[0]
    by1, by2 = b.get_bottom()[1], b.get_top()[1]
    return not (
        ax2 + padding < bx1 or
        bx2 + padding < ax1 or
        ay2 + padding < by1 or
        by2 + padding < ay1
    )


def warn_overlap(scene_name, pairs):
    for i, (name_a, mob_a) in enumerate(pairs):
        for name_b, mob_b in pairs[i + 1:]:
            if boxes_overlap(mob_a, mob_b, padding=0.03):
                print(f"[LAYOUT WARNING] {scene_name} overlap: {name_a}, {name_b}")


def car_icon(color=BLUE):
    body = RoundedRectangle(width=1.45, height=0.46, corner_radius=0.12)
    body.set_fill(color, 0.78).set_stroke(color, 1.2)
    cabin = Polygon([-0.42, 0.23, 0], [-0.03, 0.56, 0], [0.48, 0.56, 0], [0.76, 0.23, 0])
    cabin.set_fill("#9fcfff", 0.68).set_stroke(color, 1)
    wheels = VGroup(Circle(0.12), Circle(0.12)).arrange(RIGHT, buff=0.78)
    wheels.move_to(body.get_bottom() + DOWN * 0.03).set_fill("#07121f", 1).set_stroke(TEXT, 1)
    car = VGroup(body, cabin, wheels)
    car.set_z_index(Z_TEXT)
    return car


def tree_icon(color=GREEN):
    trunk = Rectangle(width=0.10, height=0.34).set_fill("#8a5a2b", 0.95).set_stroke("#8a5a2b", 0.8)
    crown = Triangle().scale(0.28).set_fill(color, 0.82).set_stroke(color, 1.0)
    crown.next_to(trunk, UP, buff=-0.02)
    tree = VGroup(trunk, crown)
    tree.set_z_index(Z_TEXT)
    return tree


def pole_icon(color=YELLOW):
    mast = Line(ORIGIN, UP * 0.72, color=color, stroke_width=3.0)
    sign = RoundedRectangle(width=0.42, height=0.22, corner_radius=0.04)
    sign.set_fill(color, 0.72).set_stroke(color, 1.0).next_to(mast, UP, buff=-0.03)
    pole = VGroup(mast, sign)
    pole.set_z_index(Z_TEXT)
    return pole


def asset_cutout(name, height=None, width=None):
    mob = ImageMobject(f"assets/cutouts/{name}_cutout.png")
    if height is not None:
        mob.set_height(height)
    if width is not None:
        mob.set_width(width)
    mob.set_z_index(Z_TEXT)
    return mob


def scene_panel(title, color=BLUE, width=PANEL_WIDTH, height=PANEL_HEIGHT):
    bg = RoundedRectangle(width=width, height=height, corner_radius=0.16)
    bg.set_fill(PANEL, 0.96).set_stroke(color, 1.4, opacity=0.75).set_z_index(Z_PANEL)
    label = _text(title, 16, color, MEDIUM)
    fit_to_width(label, width - 0.4)
    label.move_to(bg.get_top() + DOWN * 0.28).set_z_index(Z_TEXT)
    return VGroup(bg, label)


def synthetic_scene():
    panel = scene_panel("Synthetic Data", ORANGE, 5.2, 3.25)
    ground = Line(panel[0].get_left() + RIGHT * 0.6 + DOWN * 0.9, panel[0].get_right() + LEFT * 0.6 + DOWN * 0.9, color=STROKE)
    ground.set_z_index(Z_ARROW)
    objs = VGroup(
        Square(0.5).set_fill(BLUE, 0.75).set_stroke(BLUE),
        Circle(0.28).set_fill(GREEN, 0.75).set_stroke(GREEN),
        Triangle().scale(0.34).set_fill(YELLOW, 0.75).set_stroke(YELLOW),
    ).arrange(RIGHT, buff=0.38)
    objs.move_to(panel[0].get_center() + DOWN * 0.18).set_z_index(Z_TEXT)
    return VGroup(panel, ground, objs)


def real_scene():
    panel = scene_panel("Real-world Data", RED, 5.2, 3.25)
    car = asset_cutout("car", height=0.78).move_to(panel[0].get_center() + DOWN * 0.08)
    tree = asset_cutout("tree", height=0.70).move_to(panel[0].get_center() + LEFT * 1.65 + DOWN * 0.12)
    sign = asset_cutout("sign", height=0.58).move_to(panel[0].get_center() + RIGHT * 1.75 + DOWN * 0.03)
    clutter = VGroup()
    for i in range(18):
        dot = Dot(radius=0.035, color=[BLUE, GREEN, YELLOW, PURPLE, ORANGE][i % 5]).set_opacity(0.55)
        dot.move_to(panel[0].get_center() + np.array([-2.0 + (i % 6) * 0.75, -1.0 + (i // 6) * 0.45, 0]))
        clutter.add(dot)
    clutter.set_z_index(Z_ARROW)
    return Group(panel, clutter, tree, car, sign)


def vector_field(color=CYAN):
    field = VGroup()
    for r in range(3):
        for c in range(5):
            start = np.array([-1.55 + c * 0.75, -0.48 + r * 0.42, 0])
            field.add(Arrow(start, start + np.array([0.34, 0.10, 0]), color=color, buff=0, stroke_width=2.0, max_tip_length_to_length_ratio=0.28))
    field.set_z_index(Z_TEXT)
    return field


def feature_grid(color=YELLOW):
    cells = VGroup()
    for r in range(4):
        for c in range(6):
            rect = Square(0.22).set_fill([color, PURPLE, BLUE][(r + c) % 3], 0.42).set_stroke(STROKE, 0.7)
            cells.add(rect)
    cells.arrange_in_grid(rows=4, cols=6, buff=0.04)
    cells.set_z_index(Z_TEXT)
    return cells


class StoryScene(Scene):
    section_no = ""
    section_label = ""
    section_color = BLUE
    title_text = ""
    subtitle_text = ""

    def setup_story(self):
        add_background(self)
        self.title = make_title(self.title_text)
        self.subtitle = make_subtitle(self.subtitle_text)
        self.add(self.title, self.subtitle)
        self.current = None
        self.footer = None

    def beat(self, group, hold=5.0, run_time=0.8):
        self.current = fade_replace(self, self.current, group, run_time=run_time)
        warn_overlap(self.__class__.__name__, [("title", self.title), ("subtitle", self.subtitle), ("main", group)])
        self.wait(hold)
        return group

    def footer_takeaway(self, text, color=None, hold=4.0):
        color = color or self.section_color
        footer = make_footer_takeaway(text, color)
        if self.footer is None:
            self.play(FadeIn(footer), run_time=0.45)
        else:
            self.play(FadeOut(self.footer), FadeIn(footer), run_time=0.45)
        self.footer = footer
        warn_overlap(self.__class__.__name__, [("main", self.current), ("footer", footer)])
        self.wait(hold)

    def finish(self):
        mobs = [m for m in [self.current, self.footer] if m is not None]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.7)


class Part04BridgeFromSlotAttention(StoryScene):
    section_no = "4.0"
    section_label = "Cầu nối"
    section_color = PURPLE
    title_text = "Từ Slot Attention đến Reconstruction Target"
    subtitle_text = "Slots là object-like representations; target định hình tín hiệu học"

    def construct(self):
        self.setup_story()
        # Source: Slot Attention. Safe claim: abstract slots/object-like representations.
        image = make_card("Image / Frame", "visual input", BLUE, 2.8, 1.1)
        sa = make_card("Slot Attention", "gom nhóm cạnh tranh", PURPLE, 3.0, 1.1)
        pair = VGroup(image, sa).arrange(RIGHT, buff=0.75).move_to([CENTER_X, 0.35, 0])
        self.beat(VGroup(pair, connect_mobs(image, sa, PURPLE)), hold=9)

        image2 = make_card("Scene", "không phải một khối đặc", BLUE, 2.7, 1.05).move_to([-3.2, 0.45, 0])
        slots = VGroup(*[make_pill(f"slot {i}", [BLUE, GREEN, YELLOW, PURPLE][i - 1], width=1.1) for i in range(1, 5)])
        slots.arrange(RIGHT, buff=0.25).move_to([1.85, 0.45, 0])
        split_arrow = connect_mobs(image2, slots, PURPLE)
        beat2 = VGroup(image2, slots, split_arrow)
        self.current = fade_replace(self, self.current, beat2)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in slots], lag_ratio=0.18), run_time=1.2)
        self.current = beat2
        self.wait(9)

        target = make_card("Reconstruction Target?", "slots nên dựng lại gì?", ORANGE, 3.5, 1.15).move_to([CENTER_X, 0.25, 0])
        decoder = make_card("Decoder", color=CYAN, width=2.2, height=0.9).move_to([-2.9, 0.25, 0])
        slot_group = slots.copy().scale(0.92).move_to([-5.0, 0.25, 0])
        self.beat(VGroup(slot_group, decoder, target, connect_mobs(slot_group, decoder, CYAN), connect_mobs(decoder, target, ORANGE)), hold=10)

        question = make_card("Slots nên reconstruct gì?", color=ORANGE, width=5.2, height=0.9).move_to([CENTER_X, 1.15, 0])
        left = make_card("Synthetic-to-Real Gap", color=ORANGE, width=3.4, height=1.0).move_to([LEFT_X, -0.45, 0])
        right = make_card("Reconstruct Beyond RGB", color=CYAN, width=3.4, height=1.0).move_to([RIGHT_X, -0.45, 0])
        self.beat(VGroup(question, left, right, routed_arrow(question, left, ORANGE), routed_arrow(question, right, CYAN)), hold=10)
        self.footer_takeaway("Từ slots, ta chuyển sang câu hỏi về reconstruction target.", PURPLE, hold=8)
        self.finish()


class Part04SyntheticVsRealOverview(StoryScene):
    section_no = "4.1"
    section_label = "Mô phỏng và thực tế"
    section_color = ORANGE
    title_text = "Synthetic Data và Real-world Data"
    subtitle_text = "Môi trường kiểm soát rất hữu ích; thế giới thật khó hơn"

    def construct(self):
        self.setup_story()
        self.beat(synthetic_scene().move_to([CENTER_X, 0.05, 0]), hold=10)

        syn = synthetic_scene().move_to([LEFT_X, 0.05, 0])
        labels = VGroup(make_pill("môi trường kiểm soát", ORANGE, 2.6), make_pill("ranh giới sạch", GREEN, 2.0), make_pill("ít biến thể", BLUE, 1.6))
        labels.arrange(DOWN, buff=0.2).move_to([RIGHT_X, 0.05, 0])
        self.beat(Group(syn, labels), hold=11)

        real = real_scene().move_to([CENTER_X, 0.05, 0])
        tags = VGroup(make_pill("texture", PURPLE), make_pill("lighting", YELLOW), make_pill("occlusion", RED), make_pill("clutter", ORANGE))
        tags.arrange(RIGHT, buff=0.2).next_to(real, DOWN, buff=0.25)
        self.beat(Group(real, tags), hold=12)

        left = synthetic_scene().scale(0.9).move_to([LEFT_X, 0.05, 0])
        right = real_scene().scale(0.9).move_to([RIGHT_X, 0.05, 0])
        arrow = Arrow(left.get_right(), right.get_left(), color=ORANGE, buff=0.25, stroke_width=3)
        line = make_pill("Thế giới kiểm soát -> thế giới mở", ORANGE, 4.0).move_to([CENTER_X, -1.95, 0])
        self.beat(Group(left, right, arrow, line), hold=13)
        self.footer_takeaway("Synthetic data hữu ích, nhưng real-world data ít được kiểm soát hơn.", ORANGE, hold=7)
        self.finish()


class Part04RealWorldComplexity(StoryScene):
    section_no = "4.2"
    section_label = "Độ phức tạp"
    section_color = RED
    title_text = "Vì sao Real-world Data khó?"
    subtitle_text = "Appearance, lighting, occlusion, clutter và motion làm tín hiệu phức tạp hơn"

    def construct(self):
        self.setup_story()
        # SIMPLIFIED_VISUAL: conceptual object and scene factors, not computed from real data.
        car = asset_cutout("car", height=1.05).move_to([CENTER_X, 0.15, 0])
        self.beat(Group(car, make_pill("base object", RED, 1.65).next_to(car, DOWN, buff=0.42)), hold=8)

        car2 = asset_cutout("car", height=1.05).move_to([CENTER_X, 0.2, 0])
        texture = VGroup(*[Line(car2.get_left() + RIGHT * (0.35 + i * 0.32) + DOWN * 0.18, car2.get_left() + RIGHT * (0.58 + i * 0.32) + UP * 0.12, color=YELLOW, stroke_width=2) for i in range(7)])
        self.beat(Group(car2, texture, make_pill("appearance / texture", YELLOW, 2.45).next_to(car2, DOWN, buff=0.42)), hold=9)

        car3 = asset_cutout("car", height=1.05).move_to([CENTER_X, 0.2, 0])
        beam = Polygon([-1.6, 1.6, 0], [1.4, 0.8, 0], [0.7, -0.55, 0]).set_fill(YELLOW, 0.16).set_stroke(YELLOW, 0.8)
        shadow = Ellipse(width=2.7, height=0.26).set_fill("#020814", 0.65).set_stroke(width=0).next_to(car3, DOWN, buff=0.02)
        self.beat(Group(beam, shadow, car3, make_pill("lighting / shadow", ORANGE, 2.15).next_to(car3, DOWN, buff=0.52)), hold=9)

        car4 = asset_cutout("car", height=1.05).move_to([CENTER_X, 0.2, 0])
        occ = Rectangle(width=0.68, height=1.08).set_fill(PURPLE, 0.72).set_stroke(PURPLE, 1).move_to(car4.get_center() + RIGHT * 0.60)
        self.beat(Group(car4, occ, make_pill("partial occlusion", PURPLE, 2.25).next_to(car4, DOWN, buff=0.52)), hold=9)

        car5 = asset_cutout("car", height=0.95).move_to([CENTER_X, 0.2, 0])
        clutter = VGroup(*[Dot(radius=0.04, color=[BLUE, GREEN, YELLOW, PURPLE][i % 4]).move_to([-2.6 + (i % 9) * 0.65, -1.05 + (i // 9) * 0.38, 0]) for i in range(27)])
        self.beat(Group(clutter, car5, make_pill("cluttered background", ORANGE, 2.55).next_to(car5, DOWN, buff=0.45)), hold=9)

        car6 = asset_cutout("car", height=1.00).move_to([CENTER_X, 0.2, 0])
        arrows = VGroup(
            Arrow(car6.get_center() + LEFT * 1.0, car6.get_center() + RIGHT * 1.25, color=CYAN, buff=0.1, stroke_width=3),
            CurvedArrow([-2.8, 1.0, 0], [-1.3, 1.2, 0], color=PURPLE, stroke_width=2.5),
            Arrow([2.1, -0.8, 0], [3.0, -0.45, 0], color=GREEN, buff=0, stroke_width=2.5),
        )
        tags = VGroup(make_pill("rigid", CYAN), make_pill("camera", PURPLE), make_pill("non-rigid", GREEN)).arrange(RIGHT, buff=0.25).next_to(car6, DOWN, buff=0.55)
        self.beat(Group(car6, arrows, tags), hold=9)
        self.footer_takeaway("Hình ảnh càng phức tạp, tín hiệu học càng khó.", RED, hold=5)
        self.finish()


class Part04RGBReconstructionProblem(StoryScene):
    section_no = "4.3"
    section_label = "Target RGB"
    section_color = RED
    title_text = "Vấn đề của RGB Reconstruction"
    subtitle_text = "Reconstruct pixel hữu ích, nhưng không trực tiếp hỏi về object"

    def construct(self):
        self.setup_story()
        pipe, nodes, arrows = make_pipeline(["RGB\nFrame", "Encoder", "Slots", "Decoder", "RGB\nOutput"], [RED, BLUE, GREEN, PURPLE, RED], max_width=11.0)
        pipe.move_to([CENTER_X, 0.4, 0])
        self.play(FadeIn(nodes[0]), run_time=0.7)
        self.wait(4)
        for i in range(1, len(nodes)):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(nodes[i]), run_time=0.75)
            self.wait(4)
        self.current = pipe

        loss = make_card("Loss mức pixel", "làm pixel giống nhau", RED, 3.4, 0.95).move_to([CENTER_X, -1.25, 0])
        loss_lines = VGroup(DashedLine(nodes[0].get_bottom(), loss.get_left() + RIGHT * 0.65, color=RED), DashedLine(nodes[-1].get_bottom(), loss.get_right() + LEFT * 0.65, color=RED))
        self.play(FadeIn(loss), Create(loss_lines), run_time=0.8)
        self.current = VGroup(pipe, loss, loss_lines)
        self.wait(10)

        q1 = make_card("RGB hỏi", "Mỗi pixel màu gì?", RED, 4.2, 1.1).move_to([LEFT_X, 0.25, 0])
        q2 = make_card("Object understanding hỏi", "Entity nào tồn tại?", GREEN, 4.2, 1.1).move_to([RIGHT_X, 0.25, 0])
        self.beat(VGroup(q1, q2), hold=11)

        compare = VGroup(make_card("Pixel detail", "màu, texture, nền", RED, 3.6, 1.05), make_card("Object-level structure", "entity và quan hệ", GREEN, 3.8, 1.05))
        compare.arrange(RIGHT, buff=1.0).move_to([CENTER_X, 0.15, 0])
        self.beat(compare, hold=10)

        # SIMPLIFIED_VISUAL: conceptual RGB detail factors, not a real image decomposition.
        car = asset_cutout("car", height=0.98).move_to([CENTER_X, 0.25, 0])
        tags1 = VGroup(make_pill("color", RED), make_pill("texture", ORANGE), make_pill("shadow", PURPLE))
        tags1.arrange(RIGHT, buff=0.28).next_to(car, DOWN, buff=0.48)
        self.beat(Group(car, tags1), hold=12)

        car2 = asset_cutout("car", height=0.98).move_to([CENTER_X, 0.25, 0])
        tags2 = VGroup(make_pill("reflection", CYAN, 1.45), make_pill("background", YELLOW, 1.55), make_pill("occlusion", GREEN, 1.35))
        tags2.arrange(RIGHT, buff=0.28).next_to(car2, DOWN, buff=0.48)
        self.beat(Group(car2, tags2), hold=12)

        pixel_q = make_card("Câu hỏi pixel", "Pixel này màu gì?", RED, 4.2, 1.05).move_to([CENTER_X, 0.35, 0])
        self.beat(pixel_q, hold=12)

        object_q = make_card("Câu hỏi object", "Entity nào tồn tại?", GREEN, 4.2, 1.05).move_to([CENTER_X, 0.35, 0])
        self.beat(object_q, hold=15)
        self.footer_takeaway("RGB hữu ích, nhưng không phải lúc nào cũng là target tốt nhất.", RED, hold=6)
        self.finish()


class Part04ResearchQuestionBeyondRGB(StoryScene):
    section_no = "4.4"
    section_label = "Câu hỏi"
    section_color = CYAN
    title_text = "Câu hỏi chính: Beyond RGB"
    subtitle_text = "Chọn training signal khớp với cấu trúc ta muốn học"

    def construct(self):
        self.setup_story()
        rgb = make_card("Raw RGB pixels", "target mặc định", RED, 3.8, 1.15).move_to([CENTER_X, 0.35, 0])
        self.beat(rgb, hold=9)
        question = make_card("Có luôn reconstruct raw RGB?", color=ORANGE, width=5.4, height=0.95).move_to([CENTER_X, 0.45, 0])
        self.beat(question, hold=9)
        center = make_card("Beyond RGB", color=CYAN, width=2.7, height=0.9).move_to([CENTER_X, 1.2, 0])
        motion = make_card("Motion", color=CYAN, width=2.4, height=0.9).move_to([-3.7, -0.55, 0])
        geom = make_card("Geometry", color=GREEN, width=2.4, height=0.9).move_to([CENTER_X, -0.55, 0])
        feat = make_card("Features", color=PURPLE, width=2.4, height=0.9).move_to([3.7, -0.55, 0])
        self.beat(VGroup(center, motion, geom, feat, routed_arrow(center, motion, CYAN), routed_arrow(center, geom, GREEN), routed_arrow(center, feat, PURPLE)), hold=15)
        self.footer_takeaway("Chọn target khớp với cấu trúc ta muốn model học.", CYAN, hold=6)
        self.finish()


class Part05BeyondRGBOverview(StoryScene):
    section_no = "5.1"
    section_label = "Tổng quan"
    section_color = CYAN
    title_text = "Tổng quan Beyond RGB"
    subtitle_text = "Mỗi reconstruction target nhấn mạnh một loại cấu trúc"

    def construct(self):
        self.setup_story()
        center = make_card("Reconstruction\nTarget", color=CYAN, width=2.6, height=1.0).move_to([CENTER_X, 0.25, 0])
        self.beat(center, hold=8)
        cards = [
            make_card("RGB", "Appearance", RED, 2.3, 0.9).move_to([-4.0, 1.15, 0]),
            make_card("Optical Flow", "Motion", CYAN, 2.6, 0.9).move_to([4.0, 1.15, 0]),
            make_card("Depth / LiDAR", "Geometry", GREEN, 2.5, 0.9).move_to([-4.0, -1.0, 0]),
            make_card("SSL Features", "structured representation", PURPLE, 2.8, 0.9).move_to([4.0, -1.0, 0]),
        ]
        live = VGroup(center)
        waits = [5, 5, 5, 6]
        for i, card in enumerate(cards):
            arrow = connect_mobs(center, card, [RED, CYAN, GREEN, PURPLE][i], buff=0.18)
            arrow.set_stroke(width=4).set_z_index(Z_ARROW)
            self.play(FadeIn(card), GrowArrow(arrow), run_time=0.75)
            live.add(card, arrow)
            self.wait(waits[i])
        rows = VGroup(
            make_card("RGB -> Appearance", color=RED, width=5.0, height=0.55),
            make_card("Optical Flow -> Motion", color=CYAN, width=5.0, height=0.55),
            make_card("Depth/LiDAR -> Geometry", color=GREEN, width=5.0, height=0.55),
            make_card("SSL Features -> Structured representation", color=PURPLE, width=5.4, height=0.55),
        ).arrange(DOWN, buff=0.18).move_to([CENTER_X, 0.15, 0])
        self.current = live
        self.beat(rows, hold=15)
        self.footer_takeaway("Target khác nhau nhấn mạnh cấu trúc khác nhau.", CYAN, hold=5)
        self.finish()


class Part05OpticalFlowMotionCue(StoryScene):
    section_no = "5.2"
    section_label = "Motion"
    section_color = CYAN
    title_text = "Optical Flow như Motion Cue"
    subtitle_text = "Minh họa vector field giữa hai frame liên tiếp"

    def construct(self):
        self.setup_story()
        # SIMPLIFIED_VISUAL: conceptual vector field, not computed optical flow.
        # Source: SAVi. Claim: optical flow can be used as a prediction target for video object-centric learning.
        f1 = scene_panel("Frame t", CYAN, 4.2, 2.6).move_to([LEFT_X, 0.2, 0])
        obj1 = asset_cutout("car", height=0.46).move_to(f1[0].get_center() + LEFT * 0.45)
        self.beat(Group(f1, obj1), hold=6)

        f2 = scene_panel("Frame t+1", CYAN, 4.2, 2.6).move_to([RIGHT_X, 0.2, 0])
        obj2 = asset_cutout("car", height=0.46).move_to(f2[0].get_center() + RIGHT * 0.35)
        self.beat(Group(f1, obj1, f2, obj2), hold=8)

        disp = Arrow(obj1.get_center(), obj2.get_center(), color=CYAN, buff=0.2, stroke_width=3.2).set_z_index(Z_ARROW)
        cap = make_pill("Conceptual vector field, not computed optical flow.", CYAN, 4.8).move_to([CENTER_X, -1.85, 0])
        self.beat(Group(f1, obj1, f2, obj2, disp, cap), hold=9)

        field = vector_field(CYAN).move_to([CENTER_X, 0.2, 0])
        self.beat(VGroup(field, cap), hold=8)

        q = VGroup(make_card("RGB hỏi", "Màu gì?", RED, 3.0, 1.0), make_card("Flow hỏi", "Di chuyển thế nào?", CYAN, 3.0, 1.0))
        q.arrange(RIGHT, buff=1.0).move_to([CENTER_X, 0.15, 0])
        self.beat(q, hold=8)

        support = VGroup(make_pill("grouping", CYAN, 1.35), make_pill("tracking", GREEN, 1.25), make_pill("temporal consistency", PURPLE, 2.45))
        support.arrange(RIGHT, buff=0.35).move_to([CENTER_X, 0.1, 0])
        self.beat(support, hold=8)
        self.footer_takeaway("Motion là cue hữu ích, không phải object detection hoàn hảo.", CYAN, hold=4.5)
        self.finish()


class Part05MotionLimitations(StoryScene):
    section_no = "5.3"
    section_label = "Giới hạn"
    section_color = CYAN
    title_text = "Motion hữu ích, nhưng có giới hạn"
    subtitle_text = "Motion cue hỗ trợ học object, nhưng một mình nó chưa đủ"

    def construct(self):
        self.setup_story()
        helpful = make_card("Trường hợp thuận lợi", "object di chuyển trên nền tĩnh", CYAN, 4.2, 1.2).move_to([CENTER_X, 0.25, 0])
        arr = Arrow([-1.0, -0.65, 0], [1.0, -0.65, 0], color=CYAN, buff=0, stroke_width=3)
        self.beat(VGroup(helpful, arr), hold=9)

        cases = [
            ("Static object", "motion cue yếu", MUTED),
            ("Moving camera", "background cũng có flow", CYAN),
            ("Shared motion", "nhiều object giống nhau", ORANGE),
            ("Non-rigid motion", "local motion khác nhau", PURPLE),
        ]
        panels = VGroup(*[make_card(t, b, c, 2.85, 1.2) for t, b, c in cases])
        panels.arrange_in_grid(rows=2, cols=2, buff=(0.48, 0.38)).move_to([CENTER_X, 0.2, 0])
        for i in range(1, 5):
            self.beat(VGroup(*panels[:i]), hold=6.5)
        self.footer_takeaway("Cue hữu ích không đồng nghĩa với lời giải hoàn chỉnh.", CYAN, hold=4)
        self.finish()


class Part05DepthLidarGeometryCue(StoryScene):
    section_no = "5.4"
    section_label = "Geometry"
    section_color = GREEN
    title_text = "Depth, LiDAR và Geometry Cue"
    subtitle_text = "Geometry giúp định vị cấu trúc, nhưng không phải semantic label"

    def construct(self):
        self.setup_story()
        # SIMPLIFIED_VISUAL: conceptual driving scene and point cloud.
        # Source: SAVi++. Claim: sparse LiDAR depth can be a self-supervision target.
        road = scene_panel("Driving scene", GREEN, 5.6, 3.3).move_to([CENTER_X, 0.05, 0])
        road_center = road[0].get_center()
        road_bottom = road[0].get_bottom()
        lane1 = Line(road_bottom + UP * 0.48 + LEFT * 2.15, road_center + LEFT * 0.42 + UP * 0.42, color=STROKE).set_z_index(Z_ARROW)
        lane2 = Line(road_bottom + UP * 0.48 + RIGHT * 2.15, road_center + RIGHT * 0.42 + UP * 0.42, color=STROKE).set_z_index(Z_ARROW)
        center_dash = VGroup(
            *[
                Line(road_bottom + UP * (0.72 + i * 0.34), road_bottom + UP * (0.88 + i * 0.34), color=YELLOW, stroke_width=2.0)
                for i in range(4)
            ]
        ).set_z_index(Z_ARROW)
        ego = Triangle().scale(0.24).set_fill(GREEN, 0.9).set_stroke(GREEN).rotate(PI).move_to(road_bottom + UP * 0.54).set_z_index(Z_TEXT)
        near = asset_cutout("car", height=0.58).move_to(road_center + UP * 0.04)
        far = asset_cutout("car", height=0.25).move_to(road_center + UP * 0.86)
        left_tree = asset_cutout("tree", height=0.90).move_to(road_center + LEFT * 1.78 + UP * 0.12)
        right_pole = asset_cutout("sign", height=0.78).move_to(road_center + RIGHT * 1.70 + UP * 0.08)
        object_labels = VGroup(
            _text("car", 14, ORANGE, MEDIUM).next_to(near, DOWN, buff=0.08).shift(RIGHT * 0.45),
            _text("far car", 13, YELLOW, MEDIUM).next_to(far, UP, buff=0.05),
            _text("tree", 13, GREEN, MEDIUM).next_to(left_tree, DOWN, buff=0.05),
            _text("pole", 13, CYAN, MEDIUM).next_to(right_pole, DOWN, buff=0.05),
        )
        driving = Group(road, lane1, lane2, center_dash, ego, near, far, left_tree, right_pole, object_labels)
        self.beat(driving, hold=11)

        labels = VGroup(make_pill("gần", ORANGE), make_pill("xa", YELLOW), make_pill("trước / sau", GREEN, 1.75))
        labels.arrange(RIGHT, buff=0.28).move_to([CENTER_X, -1.9, 0])
        self.beat(Group(driving, labels), hold=10)

        ray_targets = [
            near.get_left(),
            near.get_center() + UP * 0.08,
            near.get_right(),
            far.get_center(),
            left_tree.get_center() + UP * 0.16,
            right_pole.get_center() + UP * 0.25,
            road_center + LEFT * 2.05 + UP * 0.65,
            road_center + RIGHT * 2.05 + UP * 0.65,
        ]
        rays = VGroup(
            *[
                Line(ego.get_center() + UP * 0.10, target, color=GREEN, stroke_width=1.7)
                .set_opacity(0.70)
                .set_z_index(Z_ARROW)
                for target in ray_targets
            ]
        )
        self.beat(Group(driving, rays), hold=11)

        cloud_panel = scene_panel("Sparse point cloud", GREEN, 5.4, 3.1).move_to([CENTER_X, 0.1, 0])
        cloud_center = cloud_panel[0].get_center()
        road_points = VGroup(
            *[
                Dot(cloud_center + np.array([-2.10 + i * 0.35, -0.84 + 0.10 * (i % 2), 0]), radius=0.018, color=GREEN)
                .set_z_index(Z_TEXT)
                for i in range(13)
            ]
        )
        car_points = VGroup(
            *[
                Dot(cloud_center + np.array([-0.58 + (i % 8) * 0.16, -0.05 + (i // 8) * 0.13, 0]), radius=0.026, color=ORANGE)
                .set_z_index(Z_TEXT)
                for i in range(24)
            ]
        )
        far_car_points = VGroup(
            *[
                Dot(cloud_center + np.array([-0.28 + (i % 6) * 0.10, 0.77 + (i // 6) * 0.08, 0]), radius=0.019, color=YELLOW)
                .set_z_index(Z_TEXT)
                for i in range(12)
            ]
        )
        tree_points = VGroup(
            *[
                Dot(cloud_center + np.array([-1.82 + (i % 4) * 0.09, 0.08 + (i // 4) * 0.12, 0]), radius=0.022, color=GREEN)
                .set_z_index(Z_TEXT)
                for i in range(16)
            ]
        )
        pole_points = VGroup(
            *[
                Dot(cloud_center + np.array([1.68 + (i % 2) * 0.05, -0.10 + i * 0.08, 0]), radius=0.018, color=CYAN)
                .set_z_index(Z_TEXT)
                for i in range(12)
            ]
        )
        outlines = VGroup(
            SurroundingRectangle(car_points, color=ORANGE, buff=0.12),
            SurroundingRectangle(far_car_points, color=YELLOW, buff=0.09),
            SurroundingRectangle(tree_points, color=GREEN, buff=0.10),
            SurroundingRectangle(pole_points, color=CYAN, buff=0.08),
        ).set_z_index(Z_ARROW)
        cloud_labels = VGroup(
            _text("car cluster", 13, ORANGE, MEDIUM).next_to(outlines[0], DOWN, buff=0.05),
            _text("far car", 12, YELLOW, MEDIUM).next_to(outlines[1], UP, buff=0.04),
            _text("tree", 12, GREEN, MEDIUM).next_to(outlines[2], UP, buff=0.04),
            _text("pole", 12, CYAN, MEDIUM).next_to(outlines[3], RIGHT, buff=0.06),
        )
        dots = VGroup(road_points, car_points, far_car_points, tree_points, pole_points, outlines, cloud_labels)
        caption = make_pill("Sparse depth signal, không phải semantic label.", GREEN, 4.5).move_to([CENTER_X, -1.85, 0])
        self.beat(VGroup(cloud_panel, dots, caption), hold=13)

        waymo = make_card("Waymo Open Dataset", "perception cho xe tự hành\ncamera + LiDAR-related data", GREEN, 4.8, 1.35).move_to([CENTER_X, 0.25, 0])
        caution = make_pill("Không chỉ là dataset LiDAR.", ORANGE, 3.0).next_to(waymo, DOWN, buff=0.35)
        self.beat(VGroup(waymo, caution), hold=10)
        self.footer_takeaway("Geometry hỗ trợ, nhưng không tự cung cấp semantic labels.", GREEN, hold=5)
        self.finish()


class Part05DinosaurFeatureReconstruction(StoryScene):
    section_no = "5.5"
    section_label = "Features"
    section_color = PURPLE
    title_text = "DINOSAUR Feature Reconstruction"
    subtitle_text = "Target chuyển từ raw pixels sang self-supervised features"

    def construct(self):
        self.setup_story()
        # Source: DINOSAUR. Claim: DINOSAUR reconstructs self-supervised features, not flow or LiDAR.
        pixel_pipe, _, _ = make_pipeline(["Image", "Slots", "Decoder", "RGB\npixels"], [BLUE, GREEN, PURPLE, RED], max_width=8.7)
        pixel_pipe.move_to([CENTER_X, 0.6, 0])
        low = make_pill("low-level details: color, texture, lighting", RED, 4.4).move_to([CENTER_X, -0.95, 0])
        self.beat(VGroup(pixel_pipe, low), hold=13.5)

        ssl_pipe, _, _ = make_pipeline(["Image", "SSL\nBackbone", "Feature\nMap"], [BLUE, PURPLE, YELLOW], max_width=7.4)
        ssl_pipe.move_to([CENTER_X, 0.85, 0])
        grid = feature_grid(YELLOW).scale(1.15).move_to([CENTER_X, -0.75, 0])
        self.beat(VGroup(ssl_pipe, grid), hold=13.5)

        feat_pipe, _, _ = make_pipeline(["Image", "Slots", "Decoder", "Feature\nMap"], [BLUE, GREEN, PURPLE, YELLOW], max_width=8.8)
        feat_pipe.move_to([CENTER_X, 0.65, 0])
        grid2 = feature_grid(YELLOW).scale(0.85).move_to([CENTER_X, -0.35, 0])
        target = make_pill("Target đổi: pixels -> features", PURPLE, 3.5).move_to([CENTER_X, -1.35, 0])
        self.beat(VGroup(feat_pipe, grid2, target), hold=14.5)

        caution = make_card("DINOSAUR", "feature reconstruction\nkhông dùng flow hay LiDAR", PURPLE, 4.4, 1.25).move_to([CENTER_X, 0.2, 0])
        self.beat(caution, hold=10.5)
        self.footer_takeaway("DINOSAUR reconstruct self-supervised features, không phải raw RGB pixels.", PURPLE, hold=5)
        self.finish()


class Part05FinalSynthesisToEncoder(StoryScene):
    section_no = "5.6"
    section_label = "Tổng kết"
    section_color = YELLOW
    title_text = "Tóm lại"
    subtitle_text = "Target định hình model học gì; encoder ảnh hưởng cách trích xuất tín hiệu"

    def construct(self):
        self.setup_story()
        rows = VGroup(
            make_card("RGB -> Appearance", color=RED, width=5.2, height=0.58),
            make_card("Optical Flow -> Motion", color=CYAN, width=5.2, height=0.58),
            make_card("Depth/LiDAR -> Geometry", color=GREEN, width=5.2, height=0.58),
            make_card("SSL Features -> Structured representation", color=PURPLE, width=5.6, height=0.58),
        ).arrange(DOWN, buff=0.18).move_to([CENTER_X, 0.25, 0])
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.12) for row in rows], lag_ratio=0.2), run_time=1.4)
        self.current = rows
        self.wait(18)

        takeaway = make_card("Reconstruction target định hình model học gì", color=YELLOW, width=6.2, height=0.9).move_to([CENTER_X, 0.3, 0])
        self.beat(takeaway, hold=14)

        pipe, nodes, _ = make_pipeline(["Input", "Encoder", "Slots", "Target"], [BLUE, CYAN, PURPLE, YELLOW], max_width=8.8)
        pipe.move_to([CENTER_X, 0.35, 0])
        highlight = SurroundingRectangle(nodes[1], color=CYAN, buff=0.12)
        note = make_pill("target chỉ là một nửa câu chuyện", MUTED, 3.8).move_to([CENTER_X, -1.1, 0])
        self.beat(VGroup(pipe, highlight, note), hold=18)

        next_card = make_card("Tiếp theo: Upgrading Encoder", "model nên encode input thế nào?", CYAN, 5.4, 1.25).move_to([CENTER_X, 0.3, 0])
        self.beat(next_card, hold=16)
        self.footer_takeaway("Target tốt hơn định hướng học gì; encoder tốt hơn cải thiện cách lấy tín hiệu.", CYAN, hold=15)
        self.finish()
