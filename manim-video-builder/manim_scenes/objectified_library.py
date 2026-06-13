from __future__ import annotations
from manim import *
import numpy as np
import os
from safe_layout import fit_main_visual, place_formula, place_title, safe_text

# --- Style Constants (From Brief) ---
BG_COLOR = "#0F1117"
TITLE_YELLOW = "#FFD166"
TEAL = "#4ECDC4"
ORANGE = "#FF6B4A"
BLUE = "#4EA8DE"
RED = "#D76D77"
GREEN = "#6BCB77"
GREY_TEXT = "#B8B8B8"
GREY_OBJ = "#444444"

# --- HELPER FUNCTIONS ---

def create_person(color=WHITE, scale=0.8):
    head = Circle(radius=0.15, color=color, fill_opacity=0.3)
    body = Polygon([-0.2, -0.15, 0], [0.2, -0.15, 0], [0.3, -0.8, 0], [-0.3, -0.8, 0], 
                   color=color, fill_opacity=0.2).next_to(head, DOWN, buff=0.05)
    return VGroup(head, body).scale(scale)

def create_teacher_character(scale=0.8):
    p = create_person(color=RED, scale=scale)
    pointer = Line(ORIGIN, UP*1.2, color=GOLD_A).rotate(-45*DEGREES).next_to(p, RIGHT, buff=-0.3).shift(UP*0.2)
    return VGroup(p, pointer)

def create_student_character(scale=0.8, color=BLUE):
    p = create_person(color=color, scale=scale)
    book = Rectangle(width=0.4, height=0.3, color=WHITE, fill_opacity=0.2).next_to(p, RIGHT, buff=-0.2).shift(DOWN*0.2)
    return VGroup(p, book)

def create_car_icon(color=TEAL, scale=0.7):
    body = RoundedRectangle(width=1.2, height=0.4, corner_radius=0.1, color=color, fill_opacity=0.4)
    roof = Polygon([-0.3, 0.25, 0], [0.3, 0.25, 0], [0.5, 0, 0], [-0.5, 0, 0], color=color, fill_opacity=0.3).next_to(body, UP, buff=0)
    wheels = VGroup(Circle(0.12, color=WHITE, fill_opacity=0.8), Circle(0.12, color=WHITE, fill_opacity=0.8)).arrange(RIGHT, buff=0.5).next_to(body, DOWN, buff=-0.05)
    return VGroup(body, roof, wheels).scale(scale)

def create_room_scene():
    desk = Line(LEFT*2, RIGHT*2, color=GREY_TEXT)
    chair = VGroup(Line(UP*0.5, DOWN*0.5), Line(LEFT*0.3, RIGHT*0.3)).set_color(BLUE).next_to(desk, LEFT).shift(UP*0.3)
    cup = RoundedRectangle(width=0.2, height=0.3, color=WHITE, fill_opacity=0.2).next_to(desk, UP, buff=0).shift(LEFT*0.5)
    person = create_person(color=ORANGE, scale=0.6).next_to(desk, RIGHT).shift(UP*0.2)
    return VGroup(desk, chair, cup, person)

def create_camera_sensor(scale=1.0):
    body = RoundedRectangle(width=1.0, height=0.6, corner_radius=0.1, color=GREY_OBJ, fill_opacity=0.4)
    lens = Circle(radius=0.22, color=TEAL, fill_opacity=0.8).move_to(body)
    sensor_plane = Rectangle(width=0.1, height=0.8, color=GREEN, fill_opacity=0.5).next_to(body, LEFT, buff=0.5)
    return VGroup(sensor_plane, body, lens).scale(scale)

def create_image_tensor():
    return VGroup(*[Square(0.6, color=TEAL, fill_opacity=0.1).shift(IN * i * 0.2) for i in range(3)]).rotate(30*DEGREES, axis=OUT).rotate(60*DEGREES, axis=RIGHT)

def create_neural_network_tunnel():
    layers = VGroup(*[Ellipse(width=0.4, height=1.5 - i*0.2, color=BLUE, fill_opacity=0.2).shift(RIGHT*i*0.8) for i in range(5)])
    return layers

def create_vector_column():
    return VGroup(*[Rectangle(width=0.6, height=0.2, color=ORANGE, fill_opacity=0.6) for _ in range(6)]).arrange(DOWN, buff=0.05)

def create_object_slot_tray(color=BLUE):
    return RoundedRectangle(width=1.2, height=1.2, corner_radius=0.2, color=color, fill_opacity=0.1)

def create_feature_grid(rows=6, cols=6):
    return VGroup(*[Square(side_length=0.3, stroke_width=0.5, color=GREY_OBJ, fill_opacity=np.random.rand()*0.3).set_fill(TEAL) for _ in range(rows*cols)]).arrange_in_grid(rows, cols, buff=0)

def create_intervention_hand(scale=1.0):
    hand = Text("👆", font_size=40)
    return hand.scale(scale)

def create_robot_arm():
    base = Square(0.6, color=GREY_OBJ, fill_opacity=0.5)
    joint1 = Line(ORIGIN, UP*1.5 + RIGHT*1, stroke_width=8, color=BLUE).next_to(base, UP, buff=0)
    joint2 = Line(joint1.get_end(), joint1.get_end() + RIGHT*1.5, stroke_width=6, color=TEAL)
    gripper = VGroup(Line(UP*0.2, DOWN*0.2), Line(UP*0.2, DOWN*0.2)).arrange(RIGHT, buff=0.3).next_to(joint2, DOWN, buff=0)
    return VGroup(base, joint1, joint2, gripper)

def create_document_card(color=WHITE, scale=0.6):
    paper = Rectangle(width=1, height=1.3, color=color, fill_opacity=0.1)
    lines = VGroup(*[Line(LEFT*0.3, RIGHT*0.3, color=color, stroke_width=1).shift(UP*i*0.2) for i in range(-2, 3)])
    return VGroup(paper, lines).scale(scale)

def create_laptop(color=BLUE, scale=1.0):
    screen = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.1, color=color, fill_opacity=0.2)
    base = Polygon([-0.6, 0, 0], [0.6, 0, 0], [0.75, -0.15, 0], [-0.75, -0.15, 0], color=color, fill_opacity=0.3).next_to(screen, DOWN, buff=0)
    lines = VGroup(*[Line(LEFT*0.3, RIGHT*0.3, stroke_width=1, color=color).shift(UP*i*0.1) for i in range(-2, 2)]).move_to(screen)
    return VGroup(screen, base, lines).scale(scale)

def create_database_cylinder(color=TEAL, scale=1.0):
    top = Ellipse(width=1, height=0.4, color=color, fill_opacity=0.4)
    body = Rectangle(width=1, height=1, color=color, fill_opacity=0.2).next_to(top, DOWN, buff=0)
    bottom = Ellipse(width=1, height=0.4, color=color, fill_opacity=0.2).move_to(body.get_bottom())
    return VGroup(body, bottom, top).scale(scale)


# --- BASE CLASS ---
class EduScene(Scene):
    def create_title(self, text):
        return place_title(safe_text(text, font_size=32, color=TITLE_YELLOW, width=config.frame_width - 1.0, weight=BOLD))

    def create_formula(self, tex):
        formula = MathTex(tex, font_size=30, color=GREY_TEXT)
        return place_formula(formula)

    def fit_main_visual(self, group, width_ratio=0.64, height_ratio=0.62):
        return fit_main_visual(group, width_ratio=width_ratio, height_ratio=height_ratio)

    def get_duration(self, default=30.0):
        try:
            return float(os.environ.get("TARGET_DURATION", str(default)))
        except ValueError:
            return default

    def auto_wait(self, pulse_obj=None):
        target_duration = self.get_duration()
        current_time = self.renderer.time
        if target_duration > current_time:
            wait_time = target_duration - current_time
            if pulse_obj is not None and wait_time > 2:
                loops = int(wait_time // 2)
                for _ in range(loops):
                    self.play(Indicate(pulse_obj, scale_factor=1.05, color=TEAL), run_time=1)
                    self.wait(1)
                remaining = wait_time - (loops * 2)
                if remaining > 0:
                    self.wait(remaining)
            else:
                self.wait(wait_time)
        else:
            self.wait(1)
