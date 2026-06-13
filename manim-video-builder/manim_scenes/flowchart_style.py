from manim import *
import numpy as np

# --- Visual Standards ---
BG_COLOR = "#080D16"
TITLE_COLOR = "#FFD700"
ARROW_COLOR = "#B0B0B0"
FEEDBACK_COLOR = "#FF4500"
LABEL_COLOR_DEFAULT = "#FFFFFF"

# --- Premium Outline Icon Helpers ---
# Style rules: Stroke width 6-8, transparent/low-opacity fills, clean tech silhouettes

def create_chair_icon(color=WHITE):
    back = RoundedRectangle(width=0.6, height=0.8, corner_radius=0.1, stroke_width=6, color=color, fill_opacity=0.05)
    seat = RoundedRectangle(width=0.8, height=0.15, corner_radius=0.05, stroke_width=6, color=color, fill_opacity=0.2).next_to(back, DOWN, buff=0)
    leg_l = Line(seat.get_bottom() + LEFT*0.25, seat.get_bottom() + LEFT*0.25 + DOWN*0.6, stroke_width=6, color=color)
    leg_r = Line(seat.get_bottom() + RIGHT*0.25, seat.get_bottom() + RIGHT*0.25 + DOWN*0.6, stroke_width=6, color=color)
    return VGroup(back, seat, leg_l, leg_r).center()

def create_table_icon(color=WHITE):
    top = RoundedRectangle(width=1.4, height=0.15, corner_radius=0.05, stroke_width=6, color=color, fill_opacity=0.2)
    leg_l = Line(top.get_bottom() + LEFT*0.5, top.get_bottom() + LEFT*0.5 + DOWN*0.8, stroke_width=6, color=color)
    leg_r = Line(top.get_bottom() + RIGHT*0.5, top.get_bottom() + RIGHT*0.5 + DOWN*0.8, stroke_width=6, color=color)
    return VGroup(top, leg_l, leg_r).center()

def create_laptop_icon(color=WHITE):
    screen = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.1, stroke_width=6, color=color, fill_opacity=0.05)
    base = Polygon(
        screen.get_bottom() + LEFT*0.7, 
        screen.get_bottom() + RIGHT*0.7,
        screen.get_bottom() + RIGHT*0.9 + DOWN*0.2,
        screen.get_bottom() + LEFT*0.9 + DOWN*0.2,
        stroke_width=6, color=color, fill_opacity=0.2
    )
    return VGroup(screen, base).center()

def create_robot_icon(color=WHITE):
    head = RoundedRectangle(width=0.8, height=0.7, corner_radius=0.2, stroke_width=6, color=color, fill_opacity=0.05)
    eye_l = Line(head.get_center() + LEFT*0.2 + UP*0.1, head.get_center() + LEFT*0.2 + DOWN*0.05, stroke_width=6, color=color)
    eye_r = Line(head.get_center() + RIGHT*0.2 + UP*0.1, head.get_center() + RIGHT*0.2 + DOWN*0.05, stroke_width=6, color=color)
    smile = ArcBetweenPoints(head.get_center() + LEFT*0.2 + DOWN*0.2, head.get_center() + RIGHT*0.2 + DOWN*0.2, angle=-PI/4, stroke_width=6, color=color)
    antenna_stem = Line(head.get_top(), head.get_top() + UP*0.2, stroke_width=6, color=color)
    antenna_bulb = Circle(radius=0.1, stroke_width=6, color=color, fill_opacity=1).next_to(antenna_stem, UP, buff=0)
    ear_l = Rectangle(width=0.1, height=0.3, stroke_width=6, color=color, fill_opacity=1).next_to(head, LEFT, buff=0)
    ear_r = Rectangle(width=0.1, height=0.3, stroke_width=6, color=color, fill_opacity=1).next_to(head, RIGHT, buff=0)
    return VGroup(head, eye_l, eye_r, smile, antenna_stem, antenna_bulb, ear_l, ear_r).center()

def create_person_icon(color=WHITE):
    head = Circle(radius=0.3, stroke_width=6, color=color, fill_opacity=0.05)
    body = ArcBetweenPoints(DOWN*0.6 + LEFT*0.5, DOWN*0.6 + RIGHT*0.5, angle=PI*0.8, stroke_width=6, color=color).shift(UP*0.2)
    body_bottom = Line(DOWN*0.6 + LEFT*0.5, DOWN*0.6 + RIGHT*0.5, stroke_width=6, color=color).shift(UP*0.2)
    return VGroup(head.shift(UP*0.4), body, body_bottom).center()

def create_cup_icon(color=WHITE):
    body = RoundedRectangle(width=0.6, height=0.8, corner_radius=0.1, stroke_width=6, color=color, fill_opacity=0.05)
    handle = ArcBetweenPoints(body.get_right() + UP*0.2, body.get_right() + DOWN*0.2, angle=-PI, stroke_width=6, color=color)
    return VGroup(body, handle).center()

def create_camera_icon(color=WHITE):
    body = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.1, stroke_width=6, color=color, fill_opacity=0.05)
    lens_outer = Circle(radius=0.3, stroke_width=6, color=color, fill_opacity=0.05).move_to(body)
    lens_inner = Circle(radius=0.15, stroke_width=4, color=color, fill_opacity=0.2).move_to(body)
    flash = RoundedRectangle(width=0.3, height=0.15, corner_radius=0.05, stroke_width=6, color=color, fill_opacity=1).next_to(body.get_top() + LEFT*0.3, UP, buff=0)
    btn = Rectangle(width=0.15, height=0.1, stroke_width=6, color=color, fill_opacity=1).next_to(body.get_top() + RIGHT*0.3, UP, buff=0)
    return VGroup(body, lens_outer, lens_inner, flash, btn).center()

def create_car_icon(color=WHITE):
    bottom = RoundedRectangle(width=1.6, height=0.4, corner_radius=0.1, stroke_width=6, color=color, fill_opacity=0.1)
    top = Polygon(
        bottom.get_top() + LEFT*0.4, bottom.get_top() + RIGHT*0.2,
        bottom.get_top() + RIGHT*0.6 + UP*0.4, bottom.get_top() + LEFT*0.2 + UP*0.4,
        stroke_width=6, color=color, fill_opacity=0.05
    )
    wheel_l = Circle(radius=0.2, stroke_width=6, color=color, fill_opacity=1).move_to(bottom.get_bottom() + LEFT*0.4)
    wheel_r = Circle(radius=0.2, stroke_width=6, color=color, fill_opacity=1).move_to(bottom.get_bottom() + RIGHT*0.4)
    return VGroup(bottom, top, wheel_l, wheel_r).center()

def create_door_icon(color=WHITE):
    frame = Rectangle(width=0.8, height=1.4, stroke_width=6, color=color, fill_opacity=0.05)
    inner = Rectangle(width=0.6, height=1.2, stroke_width=4, color=color, fill_opacity=0)
    handle = Line(inner.get_right() + LEFT*0.1 + UP*0.1, inner.get_right() + LEFT*0.1 + DOWN*0.1, stroke_width=6, color=color)
    return VGroup(frame, inner, handle).center()

def create_traffic_light_icon(color=WHITE):
    box = RoundedRectangle(width=0.4, height=1.0, corner_radius=0.1, stroke_width=6, color=color, fill_opacity=0.05)
    l1 = Circle(radius=0.1, stroke_width=4, color=color, fill_opacity=1).move_to(box.get_center() + UP*0.3)
    l2 = Circle(radius=0.1, stroke_width=4, color=color).move_to(box.get_center())
    l3 = Circle(radius=0.1, stroke_width=4, color=color).move_to(box.get_center() + DOWN*0.3)
    return VGroup(box, l1, l2, l3).center()

def create_pixels_icon(color=WHITE):
    grid = VGroup(*[
        Square(side_length=0.25, stroke_width=4, color=color, fill_opacity=0.1).shift(RIGHT*(i%3-1)*0.25 + UP*(i//3-1)*0.25)
        for i in range(9)
    ])
    return grid.center()

def create_world_icon(color=WHITE):
    globe = Circle(radius=0.6, stroke_width=6, color=color, fill_opacity=0.05)
    arc1 = Ellipse(width=0.4, height=1.2, stroke_width=4, color=color, fill_opacity=0)
    arc2 = Line(globe.get_left(), globe.get_right(), stroke_width=4, color=color)
    return VGroup(globe, arc1, arc2).center()

def create_object_icon(color=WHITE):
    box = Square(side_length=0.8, stroke_width=6, color=color, fill_opacity=0.05)
    lid = Polygon(
        box.get_top() + LEFT*0.4, box.get_top() + RIGHT*0.4,
        box.get_top() + RIGHT*0.6 + UP*0.2, box.get_top() + LEFT*0.2 + UP*0.2,
        stroke_width=6, color=color, fill_opacity=0.2
    )
    return VGroup(box, lid).center()

def create_relations_icon(color=WHITE):
    n1 = Circle(radius=0.15, stroke_width=6, color=color, fill_opacity=1).shift(LEFT*0.5 + DOWN*0.3)
    n2 = Circle(radius=0.15, stroke_width=6, color=color, fill_opacity=1).shift(RIGHT*0.5 + DOWN*0.3)
    n3 = Circle(radius=0.15, stroke_width=6, color=color, fill_opacity=1).shift(UP*0.4)
    l1 = Line(n1, n2, stroke_width=6, color=color)
    l2 = Line(n2, n3, stroke_width=6, color=color)
    l3 = Line(n3, n1, stroke_width=6, color=color)
    return VGroup(l1, l2, l3, n1, n2, n3).center()

def create_causes_icon(color=WHITE):
    arrow = Arrow(LEFT*0.4 + UP*0.4, RIGHT*0.4 + DOWN*0.4, stroke_width=8, color=color, max_tip_length_to_length_ratio=0.3)
    flash = VGroup(*[Line(ORIGIN, UP*0.2, stroke_width=4, color=color).rotate(a, about_point=ORIGIN) for a in [0, PI/2, PI, 3*PI/2]]).move_to(arrow.get_end() + RIGHT*0.2 + UP*0.2)
    return VGroup(arrow, flash).center()

def create_database_icon(color=WHITE):
    e1 = Ellipse(width=1.0, height=0.3, stroke_width=6, color=color, fill_opacity=0.2)
    e2 = Ellipse(width=1.0, height=0.3, stroke_width=6, color=color, fill_opacity=0.2).shift(DOWN*0.3)
    e3 = Ellipse(width=1.0, height=0.3, stroke_width=6, color=color, fill_opacity=0.2).shift(DOWN*0.6)
    l1 = Line(e1.get_left(), e3.get_left(), stroke_width=6, color=color)
    l2 = Line(e1.get_right(), e3.get_right(), stroke_width=6, color=color)
    return VGroup(e3, e2, e1, l1, l2).center() # Layering order

ICON_MAP = {
    "chair": create_chair_icon,
    "table": create_table_icon,
    "laptop": create_laptop_icon,
    "computer": create_laptop_icon,
    "robot": create_robot_icon,
    "ai_robot": create_robot_icon,
    "ai": create_robot_icon,
    "person": create_person_icon,
    "user": create_person_icon,
    "cup": create_cup_icon,
    "camera": create_camera_icon,
    "car": create_car_icon,
    "door": create_door_icon,
    "traffic_light": create_traffic_light_icon,
    "pixels": create_pixels_icon,
    "pích xơ": create_pixels_icon,
    "điểm ảnh": create_pixels_icon,
    "world": create_world_icon,
    "mô hình thế giới": create_world_icon,
    "objects": create_object_icon,
    "đối tượng": create_object_icon,
    "relations": create_relations_icon,
    "quan hệ": create_relations_icon,
    "causes": create_causes_icon,
    "nguyên nhân": create_causes_icon,
    "database": create_database_icon
    }

class FlowchartBlock(VGroup):
    def __init__(self, keyword, label=None, color=BLUE, width=2.5, height=2.5, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Subtle Background Glow for the tech feel
        glow = Circle(radius=width*0.4, color=color, fill_opacity=0.08, stroke_width=0)
        
        # 2. The Visual Content
        kw = keyword.lower()
        if kw in ICON_MAP:
            self.visual = ICON_MAP[kw](color=color)
        else:
            # Fallback box
            self.visual = Square(side_length=1.0, color=color, stroke_width=6)
            self.visual.add(Text(kw, font_size=20, color=color).move_to(self.visual))
            
        # Scale visual to fit 50-70% of area as requested
        self.visual.scale_to_fit_height(height * 0.5)
        if self.visual.width > width * 0.7:
            self.visual.scale_to_fit_width(width * 0.7)
            
        self.visual.move_to(ORIGIN)
        glow.move_to(ORIGIN)
        
        self.rect = self.visual # Compatibility for scenes using .rect
        self.add(glow, self.visual)
        
        # 3. The Label (Minimalist, contrasting)
        if label:
            self.label_mob = Text(label, font_size=22, color=LABEL_COLOR_DEFAULT, weight=BOLD)
            self.label_mob.next_to(self.visual, DOWN, buff=0.4)
            self.add(self.label_mob)

def get_flow_arrow(start_obj, end_obj, color=ARROW_COLOR, is_feedback=False):
    stroke_width = 8 if is_feedback else 6
    if is_feedback:
        color = FEEDBACK_COLOR
        arrow = DoubleArrow(
            start_obj.get_right() if start_obj.get_center()[0] < end_obj.get_center()[0] else start_obj.get_left(),
            end_obj.get_left() if start_obj.get_center()[0] < end_obj.get_center()[0] else end_obj.get_right(),
            color=color,
            stroke_width=stroke_width,
            tip_length=0.3
        )
    else:
        arrow = Arrow(
            start_obj.get_right(),
            end_obj.get_left(),
            color=color,
            stroke_width=stroke_width,
            buff=0.3,
            tip_length=0.3
        )
    return arrow

def setup_flowchart_scene(scene: Scene, title_text: str):
    scene.camera.background_color = BG_COLOR
    title = Text(title_text, font_size=40, color=TITLE_COLOR, weight=BOLD)
    title.to_edge(UP, buff=0.5)
    scene.add(title)
    return title
