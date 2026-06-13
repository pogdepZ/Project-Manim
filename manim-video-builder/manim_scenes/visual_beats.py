from __future__ import annotations

import re

from manim import *
from safe_layout import (
    fit_main_visual,
    place_caption,
    place_formula,
    place_title,
    safe_text,
)


config.background_color = "#161616"


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def make_ball():
    return Circle(0.26, color=ORANGE, fill_color=ORANGE, fill_opacity=0.85)


def make_box():
    return Rectangle(width=0.62, height=0.52, color=TEAL_D, fill_color=TEAL_D, fill_opacity=0.45)


def make_car():
    body = RoundedRectangle(width=0.95, height=0.35, corner_radius=0.08, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.45)
    roof = Polygon(LEFT * 0.25 + UP * 0.18, RIGHT * 0.15 + UP * 0.18, RIGHT * 0.32, LEFT * 0.38, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.35)
    wheels = VGroup(Circle(0.09, color=WHITE, fill_color=GREY_B, fill_opacity=0.9), Circle(0.09, color=WHITE, fill_color=GREY_B, fill_opacity=0.9))
    wheels.arrange(RIGHT, buff=0.48).next_to(body, DOWN, buff=-0.06)
    return VGroup(body, roof, wheels)


def make_person():
    head = Circle(0.12, color=WHITE, fill_color=GREY_A, fill_opacity=0.55).shift(UP * 0.32)
    body = Line(UP * 0.2, DOWN * 0.25, color=WHITE)
    arms = VGroup(Line(LEFT * 0.24 + UP * 0.04, RIGHT * 0.24 + UP * 0.04, color=WHITE))
    legs = VGroup(Line(DOWN * 0.25, LEFT * 0.2 + DOWN * 0.55, color=WHITE), Line(DOWN * 0.25, RIGHT * 0.2 + DOWN * 0.55, color=WHITE))
    return VGroup(head, body, arms, legs)


def make_traffic_light():
    pole = Line(DOWN * 0.62, DOWN * 1.0, color=GREY_B)
    frame = RoundedRectangle(width=0.34, height=0.88, corner_radius=0.08, color=GREY_B, fill_color="#111827", fill_opacity=1)
    lights = VGroup(
        Circle(0.08, color=MAROON_B, fill_color=MAROON_B, fill_opacity=0.85),
        Circle(0.08, color=GOLD_A, fill_color=GOLD_A, fill_opacity=0.65),
        Circle(0.08, color=TEAL_D, fill_color=TEAL_D, fill_opacity=0.65),
    ).arrange(DOWN, buff=0.08).move_to(frame)
    return VGroup(pole, frame, lights)


def make_door():
    panel = Rectangle(width=0.48, height=0.95, color=ORANGE, fill_color=ORANGE, fill_opacity=0.22)
    knob = Dot(panel.get_right() + LEFT * 0.08, radius=0.025, color=GOLD_A)
    return VGroup(panel, knob)


def make_table():
    top = Rectangle(width=0.72, height=0.16, color=TEAL_D, fill_color=TEAL_D, fill_opacity=0.4)
    legs = VGroup(
        Line(top.get_left() + RIGHT * 0.12, top.get_left() + RIGHT * 0.12 + DOWN * 0.45, color=TEAL_D),
        Line(top.get_right() + LEFT * 0.12, top.get_right() + LEFT * 0.12 + DOWN * 0.45, color=TEAL_D),
    )
    return VGroup(top, legs)


def make_chair():
    seat = Rectangle(width=0.42, height=0.18, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.35)
    back = Rectangle(width=0.16, height=0.5, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.28).next_to(seat, LEFT, buff=0)
    legs = VGroup(Line(seat.get_bottom(), seat.get_bottom() + DOWN * 0.3, color=BLUE_C), Line(seat.get_right(), seat.get_right() + DOWN * 0.3, color=BLUE_C))
    return VGroup(seat, back, legs)


def make_cup():
    cup = RoundedRectangle(width=0.34, height=0.46, corner_radius=0.06, color=GREY_A, fill_color=GREY_A, fill_opacity=0.22)
    handle = Arc(radius=0.12, angle=PI, color=GREY_A).rotate(PI / 2).next_to(cup, RIGHT, buff=-0.03)
    return VGroup(cup, handle)


def make_robot():
    head = RoundedRectangle(width=0.58, height=0.42, corner_radius=0.08, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.28).shift(UP * 0.32)
    eyes = VGroup(Circle(0.045, color=GOLD_A, fill_color=GOLD_A, fill_opacity=1), Circle(0.045, color=GOLD_A, fill_color=GOLD_A, fill_opacity=1)).arrange(RIGHT, buff=0.16).move_to(head)
    body = RoundedRectangle(width=0.72, height=0.62, corner_radius=0.08, color=TEAL_D, fill_color=TEAL_D, fill_opacity=0.22).next_to(head, DOWN, buff=0.08)
    antenna = Line(head.get_top(), head.get_top() + UP * 0.22, color=GREY_A)
    return VGroup(body, head, eyes, antenna)


def make_pixel_grid(rows=5, cols=7, size=0.18):
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            alpha = (r + c) / max(1, rows + cols - 2)
            cells.add(Square(size, stroke_width=0.8, stroke_color=BLUE_E, fill_color=interpolate_color(BLUE_E, TEAL_D, alpha), fill_opacity=0.58))
    return cells.arrange_in_grid(rows, cols, buff=0.018)


def make_tensor_stack():
    colors = [MAROON_B, TEAL_D, BLUE_C]
    layers = VGroup()
    labels = VGroup()
    for i, color in enumerate(colors):
        grid = make_pixel_grid(4, 5, 0.17).set_stroke(color, opacity=0.75)
        grid.shift(RIGHT * i * 0.18 + UP * i * 0.13)
        layers.add(grid)
        labels.add(safe_text("RGB"[i], 14, color).next_to(grid, UP, buff=0.04))
    return VGroup(layers, labels)


def make_slot(label="slot", color=TEAL_D):
    shell = RoundedRectangle(width=0.78, height=0.56, corner_radius=0.12, color=color, fill_color=color, fill_opacity=0.16)
    txt = safe_text(label, 13, WHITE).move_to(shell)
    return VGroup(shell, txt)


def make_node(label, color=BLUE_C):
    node = Circle(0.32, color=color, fill_color=color, fill_opacity=0.18)
    txt = safe_text(label, 16, WHITE, width=0.62).move_to(node)
    return VGroup(node, txt)



def make_icon(label: str, color=TEAL_D):
    box = RoundedRectangle(width=0.8, height=0.6, corner_radius=0.1, color=color, fill_color=color, fill_opacity=0.35)
    txt = safe_text(label, 14, WHITE).move_to(box)
    return VGroup(box, txt)

def make_global_pipeline():
    BLOCK1_FILL = "#2C5545"  
    BLOCK2_FILL = "#A85B5B"  
    BLOCK4_FILL = "#4A90E2"  
    CIRCLE1_FILL = "#D95F50" 
    CIRCLE2_FILL = "#7BB369" 
    CIRCLE3_FILL = "#4A90E2" 
    TITLE_COLOR = "#FFD700"
    
    block_h = 1.6
    block1 = Rectangle(width=2.0, height=block_h, fill_color=BLOCK1_FILL, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
    text1 = safe_text("Pixels", 24, WHITE).move_to(block1)
    group1 = VGroup(block1, text1)
    
    block2 = Rectangle(width=2.4, height=block_h, fill_color=BLOCK2_FILL, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
    text2 = safe_text("Objects", 24, WHITE).move_to(block2)
    group2 = VGroup(block2, text2)
    
    grid = VGroup(*[Square(side_length=0.4, stroke_color=WHITE, stroke_width=1, fill_opacity=0) for _ in range(16)])
    grid.arrange_in_grid(4, 4, buff=0)
    text3 = safe_text("Relations", 20, TITLE_COLOR).next_to(grid, UP, buff=0.1)
    group3 = VGroup(grid, text3)
    
    block4 = Rectangle(width=2.4, height=block_h, fill_color=BLOCK4_FILL, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
    text4 = safe_text("Causes", 24, WHITE).move_to(block4)
    group4 = VGroup(block4, text4)
    
    circle1 = Circle(radius=0.35, fill_color=CIRCLE1_FILL, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
    circle2 = Circle(radius=0.35, fill_color=CIRCLE2_FILL, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
    circle3 = Circle(radius=0.35, fill_color=CIRCLE3_FILL, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
    circles = VGroup(circle1, circle2, circle3).arrange(DOWN, buff=0.15)
    text5 = safe_text("World\nModel", 18, WHITE).next_to(circles, UP, buff=0.1)
    group5 = VGroup(circles, text5)
    
    pipeline = VGroup(group1, group2, group3, group4, group5)
    pipeline.arrange(RIGHT, buff=0.34).center().shift(DOWN * 2.35)
    
    if pipeline.width > config.frame_width - 1:
        pipeline.scale_to_fit_width(config.frame_width - 1)
        
    return pipeline

class VisualBeatScene(Scene):

    def _extract_objects_from_text(self, s):
        objects = []
        if "bàn" in s: objects.append(make_table())
        if "ghế" in s: objects.append(make_chair())
        if "ly" in s or "cốc" in s: objects.append(make_cup())
        if "cửa" in s: objects.append(make_door())
        if "xe" in s or "ô tô" in s: objects.append(make_car().scale(0.8))
        if "đèn" in s: objects.append(make_traffic_light().scale(0.8))
        if "người" in s or "chúng ta" in s or "con người" in s or "họ" in s or "tôi" in s or "bạn" in s or "ai đó" in s: 
            objects.append(make_person())
        if "bóng" in s: objects.append(make_ball())
        if "hộp" in s: objects.append(make_box())
        if "robot" in s or "a i" in s or "trí tuệ nhân tạo" in s or "máy tính" in s or "hệ thống" in s: 
            objects.append(make_robot().scale(0.8))
        if "chó" in s: objects.append(make_icon("Chó", ORANGE))
        if "mèo" in s: objects.append(make_icon("Mèo", ORANGE))
        if "mưa" in s: objects.append(make_icon("Mưa", BLUE_C))
        if "nắng" in s: objects.append(make_icon("Nắng", GOLD_A))
        if "trời" in s: objects.append(make_icon("Trời", BLUE_C))
        if "mắt" in s: objects.append(make_icon("Mắt", GOLD_A))
        if "chuyện" in s: objects.append(make_icon("Chuyện", GREY_A))
        
        if not objects:
            objects = [make_icon("Dữ liệu", GREY_B)]
            
        return objects

    def _highlight_pipeline(self, pattern):
        p = pattern.lower()
        if not hasattr(self, "global_pipeline"): return
        pl = self.global_pipeline
        # reset
        for i in range(5): pl[i].set_opacity(0.3)
        if "pixel to object" in p:
            pl[0].set_opacity(1)
            pl[1].set_opacity(1)
        elif "vector to slots" in p or "attention" in p:
            pl[1].set_opacity(1)
            pl[2].set_opacity(1)
        elif "causal" in p or "intervention" in p or "confounder" in p:
            pl[2].set_opacity(1)
            pl[3].set_opacity(1)
        elif "world model" in p or "permanence" in p:
            pl[4].set_opacity(1)
        else:
            for i in range(5): pl[i].set_opacity(1)

    def show_scene(self, *, title: str, voice: str, formula: str = "", visual_hints: list[str] | None = None, pattern: str = "", duration: float | None = None):
        self._all_mobs = []
        self._beat_pause = self._pause_for_duration(voice, duration)
        
        self.global_pipeline = make_global_pipeline()
        self.play(FadeIn(self.global_pipeline, shift=UP*0.2), run_time=0.8)
        self._all_mobs.append(self.global_pipeline)
        self._highlight_pipeline(pattern)
        
        title_mob = place_title(safe_text(title, 31, "#FFD700", config.frame_width - 0.8, weight=BOLD))
        self.play(Write(title_mob), run_time=0.55)
        self._all_mobs.append(title_mob)
        if formula:
            formula_mob = place_formula(safe_text(self._formula_safe(formula), 21, GOLD_A, config.frame_width - 1.2))
            self.play(FadeIn(formula_mob, shift=UP * 0.12), run_time=0.45)
            self._all_mobs.append(formula_mob)
        sentences = split_sentences(voice)
        for idx, sentence in enumerate(sentences):
            self._sentence_caption(sentence, idx + 1, len(sentences))
            self._visual_beat(sentence, idx, pattern, visual_hints or [])
            if self._beat_pause > 0:
                self.wait(self._beat_pause)
            # FADE OUT after each beat if requested
            self._clear_focus()
            
        self.wait(0.45)
        self.play(*[FadeOut(mob) for mob in list(self._all_mobs) if mob in self.mobjects], run_time=0.45)

    def _pause_for_duration(self, voice: str, duration: float | None) -> float:
        sentences = split_sentences(voice)
        if not duration or not sentences:
            return 0.0
        # Most beats spend about 1.4-1.8 seconds in play calls. The padding
        # keeps the rendered video close to narration length so audio is not cut.
        estimated_fixed = 1.4 + len(sentences) * 1.65
        return max(0.0, (float(duration) - estimated_fixed) / len(sentences))

    def _formula_safe(self, text):
        return (
            text.replace("\\to", " -> ")
            .replace("\\ldots", "...")
            .replace("\\Delta", "Delta")
            .replace("\\mathbb", "R")
            .replace("\\times", " x ")
            .replace("\\sqrt", "sqrt")
            .replace("{", "")
            .replace("}", "")
        )

    def _sentence_caption(self, sentence, index, total):
        old = getattr(self, "_caption", None)
        short = sentence
        if len(short) > 92:
            short = short[:89].rsplit(" ", 1)[0] + "..."
        caption = place_caption(safe_text(f"{index}/{total}  {short}", 16, GREY_A, config.frame_width - 1.0))
        if old and old in self.mobjects:
            self.play(ReplacementTransform(old, caption), run_time=0.22)
        else:
            self.play(FadeIn(caption, shift=UP * 0.08), run_time=0.22)
        self._caption = caption
        self._all_mobs.append(caption)

    def _clear_focus(self):
        old = getattr(self, "_focus", None)
        if old and any(m in self.mobjects for m in old.family_members_with_points()):
            self.play(FadeOut(old), run_time=0.25)

    def _visual_beat(self, sentence, idx, pattern, hints):
        s = sentence.lower()
        p = pattern.lower()
        self._clear_focus()
        
        if "pixel to object" in p or "tensor stack" in p:
            self._beat_pixels(s, idx)
        elif "vector to slots" in p:
            self._beat_slots(s, idx)
        elif "attention competition" in p or "attention flow" in p:
            self._beat_attention(s, idx)
        elif "mask and reconstruction" in p or "reconstruction" in p:
            self._beat_mask_and_reconstruction(s, idx)
        elif "correlation vs causation" in p:
            self._beat_correlation(s, idx)
        elif "causal graph flow" in p or "causal graph" in p:
            self._beat_graph(s, idx)
        elif "intervention experiment" in p:
            self._beat_intervention(s, idx)
        elif "hidden confounder reveal" in p:
            self._beat_hidden_confounder(s, idx)
        elif "distribution shift" in p:
            self._beat_distribution_shift(s, idx)
        elif "object permanence" in p:
            self._beat_object_permanence(s, idx)
        elif "world model rollout" in p:
            self._beat_world_model(s, idx)
        elif "application orbit" in p or "application map" in p:
            self._beat_application_orbit(s, idx)
        elif "visual recap cards" in p or "summary" in p:
            self._beat_visual_recap(s, idx)
        elif "split-screen visual metaphor" in p:
            self._beat_split_screen_visual_metaphor(s, idx)
        elif "paper figure pipeline" in p:
            self._beat_transform_representation(s, idx)
        else:
            self._beat_keyword(sentence, idx)

    def _place_focus(self, group):
        fit_main_visual(group, width_ratio=0.64, height_ratio=0.62)
        self._focus = group
        self._all_mobs.append(group)

    def _beat_pixels(self, s, idx):
        grid = make_pixel_grid(6, 8, 0.2).shift(LEFT * 1.5)
        objects = self._extract_objects_from_text(s)
        obj_group = VGroup(*objects).arrange(DOWN, buff=0.25).shift(RIGHT * 1.7)
        if obj_group.height > 2.5: obj_group.scale_to_fit_height(2.5)
        
        arrows = VGroup(*[Arrow(grid.get_right(), o.get_left(), buff=0.08, color=GOLD_A) for o in obj_group])
        group = VGroup(grid, obj_group, arrows)
        self._place_focus(group)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in grid], lag_ratio=0.004), run_time=0.55)
        self.play(LaggedStart(*[GrowFromCenter(o) for o in obj_group], lag_ratio=0.1), Create(arrows), run_time=0.62)
        self.play(Indicate(obj_group[min(idx % len(obj_group), len(obj_group)-1)], color=GOLD_A), run_time=0.38)

    def _beat_tensor(self, s, idx):
        tensor = make_tensor_stack().shift(LEFT * 1.2)
        h = Brace(tensor[0][0], LEFT, color=GREY_A)
        w = Brace(tensor[0][0], DOWN, color=GREY_A)
        c_arrow = Arrow(tensor[0][0].get_right(), tensor[0][-1].get_right(), color=GOLD_A, buff=0.04)
        labels = VGroup(safe_text("H", 16, GREY_A).next_to(h, LEFT, buff=0.05), safe_text("W", 16, GREY_A).next_to(w, DOWN, buff=0.05), safe_text("C=3", 16, GOLD_A).next_to(c_arrow, RIGHT, buff=0.05))
        output = RoundedRectangle(width=1.25, height=0.82, corner_radius=0.1, color=TEAL_D, fill_opacity=0.18).shift(RIGHT * 2.15)
        out_label = safe_text("X tensor", 18, TEAL_D).move_to(output)
        arrow = Arrow(tensor.get_right(), output.get_left(), color=GOLD_A, buff=0.18)
        group = VGroup(tensor, h, w, c_arrow, labels, output, out_label, arrow)
        self._place_focus(group)
        self.play(FadeIn(tensor, shift=RIGHT * 0.2), run_time=0.55)
        self.play(GrowFromCenter(h), GrowFromCenter(w), Create(c_arrow), Write(labels), run_time=0.55)
        self.play(Create(arrow), ReplacementTransform(tensor.copy(), output), Write(out_label), run_time=0.55)

    def _beat_objects(self, s, idx):
        objects = []
        labels = []
        if "quả bóng" in s:
            objects.append(make_ball())
            labels.append("ball")
        if "cái hộp" in s or "hộp" in s or "khối vuông" in s:
            objects.append(make_box())
            labels.append("box")
        if "xe" in s:
            objects.append(make_car().scale(0.85))
            labels.append("car")
        if "người đi bộ" in s or "con người" in s or "người" in s:
            objects.append(make_person())
            labels.append("person")
        if "đèn giao thông" in s or "đèn đỏ" in s:
            objects.append(make_traffic_light().scale(0.8))
            labels.append("light")
        if "robot" in s or "a i" in s:
            objects.append(make_robot().scale(0.8))
            labels.append("AI")
        if "cửa" in s:
            objects.append(make_door())
            labels.append("door")
        if "bàn" in s:
            objects.append(make_table())
            labels.append("table")
        if "ghế" in s:
            objects.append(make_chair())
            labels.append("chair")
        if "ly" in s:
            objects.append(make_cup())
            labels.append("cup")
        if not objects:
            objects = [make_ball(), make_box(), make_car().scale(0.7)]
            labels = ["obj 1", "obj 2", "obj 3"]
        mobs = VGroup(*objects).arrange(RIGHT, buff=0.65)
        texts = VGroup(*[safe_text(label, 14, GREY_A).next_to(mobs[i], DOWN, buff=0.08) for i, label in enumerate(labels)])
        group = VGroup(mobs, texts)
        self._place_focus(group)
        self.play(LaggedStart(*[GrowFromCenter(o) for o in mobs], lag_ratio=0.12), Write(texts), run_time=0.65)
        anims = []
        if any(k in s for k in ["lăn", "di chuyển", "dừng", "đẩy", "mở", "chuyển động"]):
            anims.append(mobs[0].animate.shift(RIGHT * 0.45))
            if len(mobs) > 1:
                anims.append(mobs[-1].animate.shift(RIGHT * 0.22))
        if anims:
            self.play(*anims, run_time=0.55)
            self.play(Flash(mobs[0].get_center(), color=GOLD_A), run_time=0.35)
        else:
            self.play(LaggedStart(*[Indicate(o, color=GOLD_A) for o in mobs], lag_ratio=0.14), run_time=0.7)

    def _beat_slots(self, s, idx):
        objects = self._extract_objects_from_text(s)
        n_slots = min(4, len(objects) + 1)
        slots = VGroup(*[make_slot(f"s{i+1}", [ORANGE, TEAL_D, BLUE_C, GOLD_A][i % 4]) for i in range(n_slots)]).arrange(RIGHT, buff=0.28).shift(UP * 0.45)
        objs = VGroup(*objects).arrange(RIGHT, buff=0.64).next_to(slots, DOWN, buff=0.55)
        if objs.width > 6: objs.scale_to_fit_width(6)
        
        binds = VGroup(*[Arrow(slots[min(i, n_slots-1)].get_bottom(), objs[i].get_top(), buff=0.08, color=GREY_B) for i in range(len(objs))])
        group = VGroup(slots, objs, binds)
        self._place_focus(group)
        self.play(LaggedStart(*[GrowFromCenter(s_) for s_ in slots], lag_ratio=0.08), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in objs], lag_ratio=0.08), Create(binds), run_time=0.65)
        self.play(Indicate(slots[idx % n_slots], color=GOLD_A), run_time=0.45)

    def _beat_attention(self, s, idx):
        dots = VGroup(*[Dot(color=interpolate_color(BLUE_C, TEAL_D, i / 13)).shift(LEFT * 2.5 + RIGHT * ((i % 7) * 0.32) + UP * (0.7 - (i // 7) * 0.42)) for i in range(14)])
        slots = VGroup(*[make_slot(f"s{i+1}", [ORANGE, TEAL_D, BLUE_C][i]) for i in range(3)]).arrange(DOWN, buff=0.3).shift(RIGHT * 2.25)
        lines = VGroup(*[Line(d.get_center(), slots[i % 3].get_left(), color=GREY_B, stroke_opacity=0.45, stroke_width=1.2) for i, d in enumerate(dots)])
        group = VGroup(dots, slots, lines)
        self._place_focus(group)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.02), GrowFromCenter(slots), run_time=0.55)
        self.play(Create(lines), run_time=0.55)
        self.play(slots[idx % 3].animate.set_color(GOLD_A).scale(1.08), lines.animate.set_opacity(0.25), run_time=0.55)

    def _beat_correlation(self, s, idx):
        ball = make_ball().shift(LEFT * 0.85)
        box = make_box().shift(RIGHT * 0.85)
        line = DashedLine(ball.get_right(), box.get_left(), color=GREY_B)
        label = safe_text("correlation", 18, GREY_A).next_to(line, UP, buff=0.18)
        group = VGroup(ball, box, line, label)
        self._place_focus(group)
        self.play(FadeIn(ball), FadeIn(box), run_time=0.45)
        self.play(Create(line), Write(label), run_time=0.45)
        self.play(Wiggle(line), run_time=0.45)

    def _beat_causation(self, s, idx):
        a = make_node("cause", ORANGE).shift(LEFT * 1.6)
        b = make_node("effect", TEAL_D).shift(RIGHT * 1.6)
        arrow = Arrow(a.get_right(), b.get_left(), color=GOLD_A, buff=0.12)
        ball = make_ball().move_to(a.get_center() + DOWN * 0.95)
        box = make_box().move_to(b.get_center() + DOWN * 0.95)
        group = VGroup(a, b, arrow, ball, box)
        self._place_focus(group)
        self.play(GrowFromCenter(a), GrowFromCenter(b), run_time=0.42)
        self.play(Create(arrow), run_time=0.42)
        self.play(FadeIn(ball), FadeIn(box), ball.animate.move_to(box.get_left() + LEFT * 0.08), run_time=0.65)
        self.play(box.animate.shift(RIGHT * 0.3), Flash(box.get_center(), color=GOLD_A), Indicate(arrow, color=GOLD_A), run_time=0.55)

    def _beat_intervention(self, s, idx):
        x = make_node("X", BLUE_C).shift(LEFT * 2.15)
        y = make_node("Y", TEAL_D).shift(RIGHT * 2.15)
        arrow = Arrow(x.get_right(), y.get_left(), color=GREY_B, buff=0.12)
        button = RoundedRectangle(width=1.05, height=0.55, corner_radius=0.12, color=ORANGE, fill_color=ORANGE, fill_opacity=0.2).shift(UP * 0.9)
        label = safe_text("do", 20, ORANGE).move_to(button)
        press = Arrow(button.get_bottom(), x.get_top(), color=ORANGE, buff=0.08)
        group = VGroup(x, y, arrow, button, label, press)
        self._place_focus(group)
        self.play(GrowFromCenter(x), GrowFromCenter(y), Create(arrow), run_time=0.55)
        self.play(FadeIn(button), Write(label), Create(press), run_time=0.5)
        self.play(button.animate.scale(0.88), x.animate.set_color(ORANGE), arrow.animate.set_color(GOLD_A), y.animate.shift(UP * 0.28).set_color(GOLD_A), run_time=0.65)

    def _beat_graph(self, s, idx):
        nodes = VGroup(make_node("A", BLUE_C), make_node("B", TEAL_D), make_node("C", ORANGE), make_node("D", GOLD_A)).arrange_in_grid(2, 2, buff=1.0)
        edges = VGroup(
            Arrow(nodes[0].get_right(), nodes[1].get_left(), color=GOLD_A, buff=0.1),
            Arrow(nodes[0].get_bottom(), nodes[2].get_top(), color=GOLD_A, buff=0.1),
            Arrow(nodes[2].get_right(), nodes[3].get_left(), color=GOLD_A, buff=0.1),
            Arrow(nodes[1].get_bottom(), nodes[3].get_top(), color=GREY_B, buff=0.1),
        )
        group = VGroup(nodes, edges)
        self._place_focus(group)
        self.play(LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.08), run_time=0.55)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.08), run_time=0.6)
        self.play(Indicate(edges[idx % len(edges)], color=GOLD_A), run_time=0.42)

    def _beat_distribution_shift(self, s, idx):
        left = RoundedRectangle(width=2.25, height=1.45, corner_radius=0.12, color=GOLD_A, fill_opacity=0.16).shift(LEFT * 2.0)
        right = RoundedRectangle(width=2.25, height=1.45, corner_radius=0.12, color=BLUE_C, fill_opacity=0.12).shift(RIGHT * 2.0)
        sun = Circle(0.16, color=GOLD_A, fill_color=GOLD_A, fill_opacity=0.9).move_to(left.get_corner(UR) + LEFT * 0.35 + DOWN * 0.25)
        rain = VGroup(*[Line(UP * 0.08, DOWN * 0.08, color=BLUE_C).rotate(-0.25).shift(right.get_left() + RIGHT * (0.45 + i * 0.28) + UP * (0.45 - (i % 3) * 0.28)) for i in range(8)])
        labels = VGroup(safe_text("train", 18, GOLD_A).next_to(left, UP, buff=0.08), safe_text("test", 18, BLUE_C).next_to(right, UP, buff=0.08))
        car1 = make_car().scale(0.55).move_to(left.get_center() + DOWN * 0.25)
        car2 = make_car().scale(0.55).move_to(right.get_center() + DOWN * 0.25)
        crack = VGroup(Line(UP * 0.35, LEFT * 0.08, color=MAROON_B), Line(LEFT * 0.08, RIGHT * 0.08 + DOWN * 0.18, color=MAROON_B), Line(RIGHT * 0.08 + DOWN * 0.18, DOWN * 0.45, color=MAROON_B))
        group = VGroup(left, right, sun, rain, labels, car1, car2, crack)
        self._place_focus(group)
        self.play(FadeIn(left), FadeIn(sun), FadeIn(car1), Write(labels[0]), run_time=0.5)
        self.play(ReplacementTransform(left.copy(), right), FadeIn(rain), FadeIn(car2), Write(labels[1]), run_time=0.62)
        self.play(Create(crack), Wiggle(car2), run_time=0.55)

    def _beat_world_model(self, s, idx):
        s0 = make_node("state", BLUE_C).shift(LEFT * 2.5)
        action = make_node("action", ORANGE)
        s1 = make_node("next", TEAL_D).shift(RIGHT * 2.5)
        arrows = VGroup(Arrow(s0.get_right(), action.get_left(), color=GOLD_A, buff=0.1), Arrow(action.get_right(), s1.get_left(), color=GOLD_A, buff=0.1))
        ghost = DashedVMobject(Circle(0.42, color=GREY_B).move_to(s1.get_center() + RIGHT * 0.8), num_dashes=18)
        group = VGroup(s0, action, s1, arrows, ghost)
        self._place_focus(group)
        self.play(GrowFromCenter(s0), GrowFromCenter(action), GrowFromCenter(s1), run_time=0.55)
        self.play(Create(arrows), run_time=0.5)
        self.play(ReplacementTransform(s0.copy(), ghost), Indicate(s1, color=GOLD_A), run_time=0.6)

    def _beat_transform_representation(self, s, idx):
        image = make_pixel_grid(4, 5, 0.19).shift(LEFT * 2.2)
        encoder = RoundedRectangle(width=0.9, height=0.68, corner_radius=0.12, color=BLUE_C, fill_opacity=0.16)
        vec = VGroup(*[Rectangle(width=0.12, height=0.62, color=TEAL_D, fill_opacity=0.45) for _ in range(10)]).arrange(RIGHT, buff=0.025).shift(RIGHT * 2.1)
        arrows = VGroup(Arrow(image.get_right(), encoder.get_left(), color=GOLD_A, buff=0.12), Arrow(encoder.get_right(), vec.get_left(), color=GOLD_A, buff=0.12))
        label = safe_text("z", 22, TEAL_D).next_to(vec, UP, buff=0.1)
        group = VGroup(image, encoder, vec, arrows, label)
        self._place_focus(group)
        self.play(FadeIn(image), GrowFromCenter(encoder), run_time=0.5)
        self.play(Create(arrows[0]), run_time=0.3)
        self.play(Create(arrows[1]), ReplacementTransform(image.copy(), vec), Write(label), run_time=0.65)
        self.play(vec.animate.set_color(GOLD_A), run_time=0.35)

    def _beat_comparison(self, s, idx):
        left = VGroup(RoundedRectangle(width=2.2, height=1.35, corner_radius=0.1, color=GREY_B, fill_opacity=0.1), safe_text("old", 20, GREY_A))
        right = VGroup(RoundedRectangle(width=2.2, height=1.35, corner_radius=0.1, color=TEAL_D, fill_opacity=0.14), safe_text("new", 20, TEAL_D))
        left[1].move_to(left[0])
        right[1].move_to(right[0])
        panels = VGroup(left, right).arrange(RIGHT, buff=0.8)
        arrow = Arrow(left.get_right(), right.get_left(), color=GOLD_A, buff=0.12)
        group = VGroup(panels, arrow)
        self._place_focus(group)
        self.play(FadeIn(left), FadeIn(right), run_time=0.45)
        self.play(Create(arrow), Indicate(right, color=GOLD_A), run_time=0.55)

    def _beat_keyword(self, sentence, idx):
        keyword = sentence
        if len(keyword) > 48:
            keyword = keyword[:45].rsplit(" ", 1)[0] + "..."
        node = make_node(keyword, [BLUE_C, TEAL_D, ORANGE, GOLD_A][idx % 4]).scale(1.25)
        pulse = Circle(0.72, color=GOLD_A, stroke_opacity=0.55).move_to(node)
        group = VGroup(node, pulse)
        self._place_focus(group)
        self.play(GrowFromCenter(node), run_time=0.42)
        self.play(Create(pulse), pulse.animate.scale(1.2).set_opacity(0.0), run_time=0.5)

    def _beat_mask_and_reconstruction(self, s, idx):
        layers = VGroup(*[RoundedRectangle(width=1.5, height=1.5, corner_radius=0.1, color=[BLUE_C, TEAL_D, ORANGE][i], fill_opacity=0.3) for i in range(3)])
        for i, l in enumerate(layers):
            l.shift(RIGHT * i * 0.4 + UP * i * 0.4)
        layers.move_to(LEFT * 1.5)
        arrow = Arrow(layers.get_right(), layers.get_right() + RIGHT * 1.5, color=GOLD_A, buff=0.2)
        output = make_pixel_grid(4, 4, 0.35).move_to(arrow.get_right() + RIGHT * 1.5)
        group = VGroup(layers, arrow, output)
        self._place_focus(group)
        self.play(LaggedStart(*[FadeIn(l, shift=UP*0.2) for l in layers], lag_ratio=0.1), run_time=0.6)
        self.play(Create(arrow), run_time=0.4)
        self.play(FadeIn(output, scale=0.5), run_time=0.5)

    def _beat_hidden_confounder(self, s, idx):
        a = make_node("A", BLUE_C).shift(LEFT * 2)
        b = make_node("B", TEAL_D).shift(RIGHT * 2)
        dash = DashedLine(a.get_right(), b.get_left(), color=GREY_A)
        c = make_node("C (Hidden)", ORANGE).shift(UP * 1.5)
        arr1 = Arrow(c.get_bottom(), a.get_top(), color=GOLD_A, buff=0.1)
        arr2 = Arrow(c.get_bottom(), b.get_top(), color=GOLD_A, buff=0.1)
        group = VGroup(a, b, dash, c, arr1, arr2)
        self._place_focus(group)
        self.play(GrowFromCenter(a), GrowFromCenter(b), Create(dash), run_time=0.6)
        self.play(GrowFromCenter(c), run_time=0.5)
        self.play(Create(arr1), Create(arr2), dash.animate.set_opacity(0.1), run_time=0.6)

    def _beat_object_permanence(self, s, idx):
        ball = make_ball().shift(LEFT * 3)
        wall = Rectangle(width=1.5, height=2.5, color=GREY_B, fill_color=GREY_B, fill_opacity=0.8).set_z_index(10)
        group = VGroup(ball, wall)
        self._place_focus(group)
        self.play(FadeIn(wall), FadeIn(ball), run_time=0.5)
        self.play(ball.animate.shift(RIGHT * 3), run_time=0.5)
        ghost_ball = make_ball().set_opacity(0.3).move_to(ball)
        self.play(ghost_ball.animate.shift(RIGHT * 3), run_time=0.5)
        ball.move_to(ghost_ball.get_center())
        self.play(ball.animate.shift(RIGHT * 1), run_time=0.5)

    def _beat_application_orbit(self, s, idx):
        center = make_node("Core AI", TEAL_D)
        apps = ["Robotics", "Self-Driving", "Healthcare", "Smart City", "Gaming"]
        nodes = VGroup(*[make_node(app, BLUE_C).scale(0.7) for app in apps])
        for i, n in enumerate(nodes):
            angle = i * TAU / len(apps)
            n.move_to(center.get_center() + np.array([np.cos(angle)*2.5, np.sin(angle)*2.5, 0]))
        lines = VGroup(*[Line(center.get_center(), n.get_center(), color=GREY_B) for n in nodes])
        group = VGroup(center, lines, nodes)
        self._place_focus(group)
        self.play(GrowFromCenter(center), run_time=0.4)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.05), LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.05), run_time=0.8)
        self.play(Indicate(nodes[idx % len(nodes)], color=GOLD_A), run_time=0.4)

    def _beat_visual_recap(self, s, idx):
        cards = VGroup(*[RoundedRectangle(width=1.8, height=1.2, corner_radius=0.1, color=TEAL_D, fill_opacity=0.15) for _ in range(4)])
        cards.arrange_in_grid(2, 2, buff=0.5)
        for i, c in enumerate(cards):
            txt = safe_text(f"Idea {i+1}", 20, GOLD_A).move_to(c)
            c.add(txt)
        flow_arrow = Arrow(LEFT * 2, RIGHT * 2, color=ORANGE, stroke_width=6).shift(DOWN * 1.5)
        group = VGroup(cards, flow_arrow)
        self._place_focus(group)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.1) for c in cards], lag_ratio=0.1), run_time=0.8)
        self.play(cards[idx % 4].animate.set_color(ORANGE), run_time=0.4)
        if idx == 3:
            self.play(Create(flow_arrow), run_time=0.5)

    def _beat_split_screen_visual_metaphor(self, s, idx):
        stage = Line(LEFT * 3, RIGHT * 3, color=GREY_A).shift(UP * 0.2)
        bottom_box = RoundedRectangle(width=4, height=1.5, corner_radius=0.1, color=TEAL_D, fill_opacity=0.1).shift(DOWN * 0.8)
        bottom_txt = safe_text("Data Representation", 20, TEAL_D).move_to(bottom_box)
        group = VGroup(stage, bottom_box, bottom_txt)
        
        objects = self._extract_objects_from_text(s)
        mobs = VGroup(*objects).arrange(RIGHT, buff=0.8).next_to(stage, UP, buff=0.1)
        if mobs.width > 5: mobs.scale_to_fit_width(5)
        group.add(mobs)
        self._place_focus(group)
        self.play(FadeIn(stage), FadeIn(bottom_box), Write(bottom_txt), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(o, shift=UP*0.2) for o in mobs], lag_ratio=0.1), run_time=0.6)
        
        anims = []
        if any(k in s for k in ["lăn", "di chuyển", "dừng", "đẩy", "mở", "chuyển động"]):
            anims.append(mobs[0].animate.shift(RIGHT * 0.45))
        if anims:
            self.play(*anims, run_time=0.5)
            
        arrow = Arrow(stage.get_bottom(), bottom_box.get_top(), color=GOLD_A, buff=0.1)
        self.play(Create(arrow), run_time=0.4)
        group.add(arrow)
