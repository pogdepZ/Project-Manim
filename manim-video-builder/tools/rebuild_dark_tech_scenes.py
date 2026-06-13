from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SCENES = ROOT / "manim_scenes"
ASSETS = SCENES / "assets" / "realistic"
DOCS = ROOT / "docs"


HELPER = r'''
from __future__ import annotations

import json
import os
from pathlib import Path

from manim import *


BUILDER_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = BUILDER_ROOT / "output" / "final" / "manifest.json"
ASSET_DIR = Path(__file__).resolve().parent / "assets" / "realistic"

BG_COLOR = "#080D16"
BG_COLOR_2 = "#0A1118"
TITLE_COLOR = "#FFD700"
TEXT_COLOR = "#F4F7FB"
MUTED_TEXT = "#B8C4D6"
DATA_ARROW = "#C3CCD8"
FEEDBACK_ARROW = "#FF6B3D"

ROLE_COLORS = {
    "user": "#4EA8DE",
    "entity": "#4EA8DE",
    "module": "#9B6DFF",
    "model": "#4ECDC4",
    "output": "#6BCB77",
    "warning": "#FF9F43",
    "loss": "#FF6B3D",
    "math": "#FFE08A",
}

ENTITY_ASSETS = {
    "person": "person.png",
    "user": "person.png",
    "student": "person.png",
    "teacher": "teacher.png",
    "robot": "robot.png",
    "ai agent": "robot.png",
    "robot arm": "robot_arm.png",
    "laptop": "laptop.png",
    "computer": "laptop.png",
    "camera": "camera.png",
    "car": "car.png",
    "self-driving car": "car.png",
    "traffic light": "traffic_light.png",
    "door": "door.png",
    "table": "table.png",
    "chair": "chair.png",
    "cup": "cup.png",
    "red cup": "red_cup.png",
    "blue cup": "blue_cup.png",
    "bottle": "bottle.png",
    "ball": "ball.png",
    "box": "box.png",
    "wood box": "box.png",
    "hand": "hand.png",
    "key": "key.png",
    "city": "city.png",
    "xray": "xray.png",
    "game agent": "game_agent.png",
    "tree": "tree.png",
    "brain": "brain.png",
    "room": "room.png",
}


def _manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _short_text(text: str, limit: int = 30) -> str:
    text = str(text).strip()
    if len(text) <= limit:
        return text
    parts = text.split()
    out = []
    for part in parts:
        if len(" ".join(out + [part])) > limit:
            break
        out.append(part)
    return " ".join(out) or text[:limit]


def safe_text(text: str, font_size: int = 28, color=TEXT_COLOR, max_width: float = 3.0, weight=NORMAL):
    mob = Text(_short_text(text, 42), font_size=font_size, color=color, weight=weight)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def create_title(text: str) -> Text:
    title = safe_text(text, font_size=38, color=TITLE_COLOR, max_width=config.frame_width - 1.0, weight=BOLD)
    title.to_edge(UP, buff=0.36)
    return title


def create_formula_panel(formula: str | None) -> VGroup:
    if not formula:
        formula = "Audio-locked visual reasoning"
    formula = formula.replace("->", r"\rightarrow")
    panel = RoundedRectangle(
        width=11.7,
        height=0.58,
        corner_radius=0.08,
        stroke_color=ROLE_COLORS["math"],
        stroke_width=1.5,
        fill_color=BG_COLOR_2,
        fill_opacity=0.45,
    )
    try:
        label = MathTex(formula, font_size=28, color=ROLE_COLORS["math"])
    except Exception:
        label = safe_text(formula, font_size=24, color=ROLE_COLORS["math"], max_width=10.9)
    if label.width > 10.9:
        label.scale_to_fit_width(10.9)
    label.move_to(panel)
    group = VGroup(panel, label)
    group.to_edge(DOWN, buff=0.32)
    return group


def _asset_image(keyword: str, max_height: float = 1.25) -> Mobject | None:
    filename = ENTITY_ASSETS.get(keyword.lower())
    if not filename:
        return None
    path = ASSET_DIR / filename
    if not path.exists():
        return None
    img = ImageMobject(str(path))
    img.scale_to_fit_height(max_height)
    if img.width > 1.75:
        img.scale_to_fit_width(1.75)
    return img


def create_module_visual(label: str, role: str = "module") -> VGroup:
    color = ROLE_COLORS.get(role, ROLE_COLORS["module"])
    low = label.lower()
    if any(k in low for k in ["graph", "scm", "causal", "relation", "nhân quả"]):
        nodes = VGroup(
            Circle(0.15, color=color, fill_opacity=0.9).shift(LEFT * 0.65 + DOWN * 0.35),
            Circle(0.15, color=color, fill_opacity=0.9).shift(RIGHT * 0.65 + DOWN * 0.35),
            Circle(0.15, color=color, fill_opacity=0.9).shift(UP * 0.45),
        )
        edges = VGroup(
            Arrow(nodes[0].get_center(), nodes[2].get_center(), buff=0.18, stroke_width=5, color=color, tip_length=0.16),
            Arrow(nodes[2].get_center(), nodes[1].get_center(), buff=0.18, stroke_width=5, color=color, tip_length=0.16),
        )
        return VGroup(edges, nodes)
    if any(k in low for k in ["slot", "object"]):
        return VGroup(*[
            RoundedRectangle(width=0.62, height=0.9, corner_radius=0.12, color=color, stroke_width=4, fill_opacity=0.13)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.14)
    if any(k in low for k in ["tensor", "pixel", "rgb", "feature", "mask"]):
        grid = VGroup(*[
            Square(0.22, stroke_width=1.2, stroke_color=color, fill_color=color, fill_opacity=0.12 + (i % 4) * 0.08)
            for i in range(24)
        ]).arrange_in_grid(4, 6, buff=0.025)
        return grid
    if any(k in low for k in ["vit", "dino", "jepa", "mamba", "transformer", "decoder", "world model", "model"]):
        layers = VGroup(*[
            RoundedRectangle(width=0.22, height=1.15 - i * 0.08, corner_radius=0.05, color=color, stroke_width=3, fill_opacity=0.16)
            for i in range(5)
        ]).arrange(RIGHT, buff=0.16)
        return layers
    rect = RoundedRectangle(width=1.55, height=1.0, corner_radius=0.08, color=color, stroke_width=4, fill_opacity=0.12)
    core = safe_text(_short_text(label, 14), font_size=22, color=color, max_width=1.35, weight=BOLD)
    core.move_to(rect)
    return VGroup(rect, core)


class FlowBox(Group):
    def __init__(
        self,
        label: str,
        *,
        role: str = "module",
        entity: str | None = None,
        width: float = 2.32,
        height: float = 2.45,
        note: str | None = None,
    ):
        super().__init__()
        color = ROLE_COLORS.get(role, ROLE_COLORS["module"])
        glow = RoundedRectangle(
            width=width + 0.16,
            height=height + 0.16,
            corner_radius=0.13,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.055,
        )
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.11,
            stroke_color=color,
            stroke_width=2.4,
            fill_color=BG_COLOR_2,
            fill_opacity=0.20,
        )
        visual = _asset_image(entity or label, max_height=height * 0.52)
        if visual is None:
            visual = create_module_visual(label, role=role)
            visual.scale_to_fit_height(height * 0.45)
            if visual.width > width * 0.76:
                visual.scale_to_fit_width(width * 0.76)
        visual.move_to(frame.get_center() + UP * 0.31)
        label_mob = safe_text(label, font_size=21, color=TEXT_COLOR, max_width=width - 0.28, weight=BOLD)
        label_mob.move_to(frame.get_bottom() + UP * 0.38)
        self.frame = frame
        self.visual = visual
        self.label_mob = label_mob
        self.add(glow, frame, visual, label_mob)
        if note:
            note_mob = safe_text(note, font_size=16, color=MUTED_TEXT, max_width=width - 0.35)
            note_mob.next_to(label_mob, UP, buff=0.08)
            self.add(note_mob)


def create_flow_box(label: str, role: str = "module", **kwargs) -> FlowBox:
    return FlowBox(label, role=role, **kwargs)


def create_entity_image_box(label: str, entity: str, role: str = "entity", **kwargs) -> FlowBox:
    return FlowBox(label, role=role, entity=entity, **kwargs)


def create_module_box(label: str, role: str = "module", **kwargs) -> FlowBox:
    return FlowBox(label, role=role, **kwargs)


def create_output_box(label: str, entity: str | None = None, **kwargs) -> FlowBox:
    return FlowBox(label, role="output", entity=entity, **kwargs)


def create_data_arrow(left: Mobject, right: Mobject) -> Arrow:
    return Arrow(left.get_right(), right.get_left(), buff=0.16, color=DATA_ARROW, stroke_width=7, tip_length=0.28)


def create_feedback_arrow(left: Mobject, right: Mobject) -> DoubleArrow:
    return DoubleArrow(left.get_right(), right.get_left(), buff=0.16, color=FEEDBACK_ARROW, stroke_width=8, tip_length=0.28)


def place_flow_row(blocks: list[Mobject], *, y: float = -0.25, max_width: float = 12.1) -> tuple[VGroup, VGroup]:
    row = Group(*blocks).arrange(RIGHT, buff=0.58)
    if row.width > max_width:
        row.scale_to_fit_width(max_width)
    if row.height > 4.25:
        row.scale_to_fit_height(4.25)
    row.move_to([0, y, 0])
    arrows = VGroup(*[create_data_arrow(row[i], row[i + 1]) for i in range(len(row) - 1)])
    return row, arrows


def create_side_note(text: str) -> VGroup:
    box = RoundedRectangle(width=3.6, height=0.72, corner_radius=0.08, stroke_color=ROLE_COLORS["warning"], stroke_width=1.5, fill_opacity=0.12)
    label = safe_text(text, font_size=18, color=MUTED_TEXT, max_width=3.25)
    label.move_to(box)
    return VGroup(box, label)


def hold_visual_until_audio_end(scene: Scene, duration: float, focus: Mobject | None = None):
    current = scene.renderer.time
    remaining = max(0.0, duration - current)
    if remaining <= 0.05:
        return
    if focus is not None and remaining > 4.0:
        pulse_time = min(1.0, remaining * 0.18)
        scene.play(Indicate(focus, scale_factor=1.018, color=ROLE_COLORS["model"]), run_time=pulse_time)
        remaining = max(0.0, duration - scene.renderer.time)
    scene.wait(remaining)


SCENE_SPECS = {
    1: [("Pixels", "module", None), ("Objects", "output", "room"), ("Relations", "module", None), ("Causes", "warning", None), ("World Model", "model", None)],
    2: [("Real object", "output", "ball"), ("Camera", "entity", "camera"), ("RGB Tensor", "module", None), ("Pixel matrix", "module", None)],
    3: [("Image X", "module", None), ("Encoder f_theta", "model", None), ("Vector z", "output", None)],
    4: [("Car", "entity", "car"), ("Pedestrian", "entity", "person"), ("Traffic light", "entity", "traffic light"), ("Mixed vector", "warning", None)],
    5: [("Street scene", "output", "car"), ("Detection boxes", "warning", None), ("Object slots", "model", None), ("Unsupervised learning", "output", None)],
    6: [("Ball", "entity", "ball"), ("Slot z1", "model", None), ("Box", "entity", "box"), ("Slot z2", "model", None)],
    7: [("Image features", "module", None), ("Slot Attention", "model", None), ("Clean slots", "output", None)],
    8: [("Puzzle pieces", "entity", "table"), ("Competition", "warning", None), ("Disentangled slots", "output", None)],
    9: [("Slots", "model", None), ("Decoder", "model", None), ("Masks", "module", None), ("Reconstruction", "output", "room")],
    10: [("Synthetic world", "module", None), ("Reality gap", "warning", None), ("Real world", "output", "room")],
    11: [("Image", "module", None), ("ViT", "model", None), ("DINO features", "model", None), ("Semantic slots", "output", None)],
    12: [("Slots", "model", None), ("Feature decoder", "model", None), ("DINO target", "module", None), ("Feature loss", "loss", None)],
    13: [("Object zi", "output", "ball"), ("Relation g", "model", None), ("Object zj", "output", "box")],
    14: [("Observed X", "module", None), ("Correlation P(Y|X)", "warning", None), ("Result Y", "output", "box")],
    15: [("Intervention do(X)", "warning", "hand"), ("Physical system", "entity", "ball"), ("Outcome Y", "output", "box")],
    16: [("Passive observer", "user", "person"), ("Hidden confounder", "warning", None), ("Active intervention", "output", "traffic light")],
    17: [("Parents PA_i", "module", None), ("SCM function f_i", "model", None), ("Variable X_i", "output", None), ("Noise U_i", "warning", None)],
    18: [("Ball velocity", "entity", "ball"), ("Impact force", "warning", None), ("Box motion", "output", "box")],
    19: [("Mass and accel", "module", None), ("Force F=m a", "math", None), ("Momentum change", "warning", None), ("Slide distance", "output", "box")],
    20: [("Object slots", "model", None), ("Causal graph", "model", None), ("Behavior prediction", "output", None)],
    21: [("Sunny training", "entity", "car"), ("Distribution shift", "warning", None), ("Rainy testing", "output", "car"), ("Stable rules", "model", None)],
    22: [("Visible ball", "entity", "ball"), ("Occluder", "entity", "box"), ("Persistent slot", "model", None), ("Reappears", "output", "ball")],
    23: [("State s_t", "module", None), ("Action a_t", "entity", "robot arm"), ("World Model", "model", None), ("Future s_t+1", "output", None)],
    24: [("Robot arm", "entity", "robot arm"), ("Cup + bottle", "entity", "cup"), ("Causal plan", "model", None), ("Safe grasp", "output", "red cup")],
    25: [("Road entities", "entity", "car"), ("Relations", "model", None), ("Brake decision", "warning", None), ("Safe driving", "output", "traffic light")],
    26: [("Embodied agent", "entity", "game agent"), ("Key", "entity", "key"), ("Door rule", "model", None), ("Reward", "output", None)],
    27: [("Medical image", "entity", "xray"), ("Segments", "model", None), ("Lesion region", "warning", None), ("Diagnosis", "output", None)],
    28: [("Physical city", "entity", "city"), ("Camera streams", "entity", "camera"), ("Digital twin", "model", None), ("Traffic control", "output", "traffic light")],
    29: [("Text command", "module", None), ("Object grounding", "model", None), ("Red cup slot", "output", "red cup"), ("Robot action", "entity", "robot arm")],
    30: [("Ambiguous objects", "warning", "tree"), ("Hidden U", "warning", None), ("No intervention", "loss", None), ("Scale cost", "math", None)],
    31: [("Perception", "model", None), ("Causality", "model", None), ("Causal World Model", "output", "brain"), ("Safe action", "entity", "robot")],
}


def _blocks_for_scene(index: int) -> list[FlowBox]:
    spec = SCENE_SPECS.get(index, [("Input", "module", None), ("Model", "model", None), ("Output", "output", None)])
    width = 2.12 if len(spec) >= 5 else 2.42
    return [FlowBox(label, role=role, entity=entity, width=width) for label, role, entity in spec]


def _scene_note(entry: dict) -> str:
    hints = entry.get("visual_hints") or []
    if hints:
        return _short_text(hints[0], 54)
    return _short_text(entry.get("goal", ""), 54)


def create_scene_layout(entry: dict, index: int):
    blocks = _blocks_for_scene(index)
    row, arrows = place_flow_row(blocks)
    formula = create_formula_panel((entry.get("formulas") or entry.get("screen_formulas") or [None])[0])
    note = create_side_note(_scene_note(entry))
    note.next_to(row, DOWN, buff=0.28)
    if note.get_bottom()[1] < formula.get_top()[1] + 0.12:
        note.scale_to_fit_width(3.15)
        note.next_to(row, DOWN, buff=0.18)
    return row, arrows, formula, note


def render_dark_tech_scene(scene: Scene, index: int):
    entries = _manifest()
    entry = entries[index - 1]
    duration = float(entry.get("duration", 36.0))
    scene.camera.background_color = BG_COLOR
    audio_path = BUILDER_ROOT / entry["audio_file"]
    if audio_path.exists():
        scene.add_sound(str(audio_path))

    title = create_title(entry.get("title") or entry.get("scene_title") or f"Scene {index:03d}")
    row, arrows, formula, note = create_scene_layout(entry, index)

    scene.play(FadeIn(title, shift=DOWN * 0.12), run_time=min(0.8, duration * 0.04))
    scene.play(FadeIn(formula, shift=UP * 0.12), run_time=min(0.8, duration * 0.04))

    block_anims = [FadeIn(block, shift=UP * 0.22) for block in row]
    scene.play(LaggedStart(*block_anims, lag_ratio=0.18), run_time=min(3.2, duration * 0.16))
    if len(arrows) > 0:
        scene.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.18), run_time=min(2.2, duration * 0.10))
    scene.play(FadeIn(note, shift=UP * 0.10), run_time=min(0.9, duration * 0.04))

    if index in {13, 14, 15, 16, 18, 19, 20, 21, 25, 30, 31} and len(row) >= 2:
        fb = create_feedback_arrow(row[0], row[-1]).set_z_index(-1).shift(DOWN * 0.35)
        scene.play(Create(fb), run_time=min(1.4, duration * 0.06))
        row.add(fb)
        arrows.add(fb)

    focus = row[min(len(row) - 1, max(0, len(row) // 2))]
    scene.play(Circumscribe(focus, color=ROLE_COLORS["model"], time_width=0.75), run_time=min(1.1, duration * 0.04))
    hold_visual_until_audio_end(scene, duration, Group(row, arrows))
'''


def _draw_shadow(draw: ImageDraw.ImageDraw, xy, radius=8):
    layer = Image.new("RGBA", (240, 180), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(xy, fill=(0, 0, 0, 95))
    layer = layer.filter(ImageFilter.GaussianBlur(radius))
    return layer


def _gradient_body(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        col = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,)
        draw.line((x0, y, x1, y), fill=col)


def make_asset(name: str, kind: str):
    img = Image.new("RGBA", (240, 180), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((45, 142, 195, 168), fill=(0, 0, 0, 70))
    if kind == "person":
        draw.ellipse((92, 22, 148, 78), fill=(228, 176, 132, 255), outline=(245, 215, 180, 255), width=3)
        _gradient_body(draw, (72, 82, 168, 158), (52, 132, 210), (22, 48, 86))
        draw.rounded_rectangle((72, 82, 168, 158), radius=22, outline=(175, 220, 255, 255), width=3)
    elif kind == "teacher":
        make_asset(name, "person")
        return
    elif kind == "robot":
        draw.rounded_rectangle((64, 45, 176, 142), radius=20, fill=(165, 184, 205, 255), outline=(235, 245, 255, 255), width=4)
        draw.rectangle((92, 28, 148, 48), fill=(110, 128, 150, 255))
        draw.ellipse((86, 78, 105, 96), fill=(30, 240, 220, 255))
        draw.ellipse((135, 78, 154, 96), fill=(30, 240, 220, 255))
        draw.rounded_rectangle((96, 112, 144, 123), radius=5, fill=(45, 62, 80, 255))
    elif kind == "robot_arm":
        draw.rounded_rectangle((36, 125, 84, 160), radius=8, fill=(95, 105, 122, 255), outline=(230, 235, 245, 255), width=3)
        draw.line((72, 128, 118, 72), fill=(82, 174, 222, 255), width=18)
        draw.line((118, 72, 172, 96), fill=(120, 94, 245, 255), width=16)
        draw.ellipse((104, 58, 132, 86), fill=(210, 220, 235, 255))
        draw.line((174, 96, 198, 78), fill=(230, 235, 245, 255), width=6)
        draw.line((174, 96, 198, 114), fill=(230, 235, 245, 255), width=6)
    elif kind == "laptop":
        draw.rounded_rectangle((58, 35, 182, 122), radius=8, fill=(30, 38, 52, 255), outline=(120, 200, 245, 255), width=4)
        draw.rectangle((70, 48, 170, 108), fill=(20, 105, 150, 255))
        draw.polygon([(42, 130), (198, 130), (218, 154), (22, 154)], fill=(88, 99, 116, 255), outline=(230, 235, 245, 255))
    elif kind == "camera":
        draw.rounded_rectangle((48, 55, 192, 140), radius=18, fill=(42, 48, 58, 255), outline=(210, 225, 238, 255), width=4)
        draw.ellipse((86, 62, 154, 130), fill=(20, 32, 44, 255), outline=(70, 220, 205, 255), width=6)
        draw.ellipse((108, 84, 132, 108), fill=(120, 235, 255, 255))
    elif kind == "car":
        draw.rounded_rectangle((34, 86, 206, 135), radius=18, fill=(30, 128, 210, 255), outline=(180, 225, 255, 255), width=4)
        draw.polygon([(72, 86), (99, 50), (152, 50), (180, 86)], fill=(28, 60, 88, 255), outline=(180, 225, 255, 255))
        draw.ellipse((62, 124, 94, 156), fill=(20, 24, 30, 255), outline=(230, 235, 245, 255), width=4)
        draw.ellipse((150, 124, 182, 156), fill=(20, 24, 30, 255), outline=(230, 235, 245, 255), width=4)
    elif kind == "traffic_light":
        draw.rounded_rectangle((92, 22, 148, 150), radius=14, fill=(32, 38, 48, 255), outline=(220, 228, 238, 255), width=4)
        for y, c in [(48, (240, 60, 46)), (86, (244, 190, 50)), (124, (70, 210, 100))]:
            draw.ellipse((107, y - 13, 133, y + 13), fill=c + (255,))
    elif kind == "door":
        draw.rounded_rectangle((78, 25, 162, 158), radius=4, fill=(120, 72, 38, 255), outline=(235, 200, 150, 255), width=4)
        draw.ellipse((143, 90, 153, 100), fill=(255, 210, 90, 255))
    elif kind == "table":
        draw.rounded_rectangle((45, 72, 195, 94), radius=7, fill=(145, 92, 48, 255), outline=(235, 184, 110, 255), width=3)
        draw.rectangle((62, 92, 76, 156), fill=(105, 66, 38, 255))
        draw.rectangle((164, 92, 178, 156), fill=(105, 66, 38, 255))
    elif kind == "chair":
        draw.rounded_rectangle((80, 38, 160, 104), radius=12, fill=(56, 120, 190, 255), outline=(190, 230, 255, 255), width=4)
        draw.rounded_rectangle((67, 105, 173, 126), radius=8, fill=(48, 92, 150, 255), outline=(190, 230, 255, 255), width=3)
        draw.line((88, 126, 76, 158), fill=(210, 225, 235, 255), width=5)
        draw.line((152, 126, 164, 158), fill=(210, 225, 235, 255), width=5)
    elif kind in {"cup", "red_cup", "blue_cup"}:
        color = (220, 55, 50) if kind == "red_cup" else (45, 125, 220) if kind == "blue_cup" else (230, 235, 240)
        draw.rounded_rectangle((82, 55, 150, 146), radius=18, fill=color + (255,), outline=(255, 255, 255, 255), width=4)
        draw.arc((139, 76, 183, 120), -70, 70, fill=(255, 255, 255, 255), width=7)
    elif kind == "bottle":
        draw.rounded_rectangle((95, 35, 145, 152), radius=18, fill=(70, 180, 170, 210), outline=(210, 255, 245, 255), width=4)
        draw.rectangle((104, 18, 136, 42), fill=(80, 120, 130, 255))
    elif kind == "ball":
        draw.ellipse((70, 35, 170, 135), fill=(220, 48, 58, 255), outline=(255, 205, 210, 255), width=4)
        draw.arc((82, 44, 160, 130), 80, 280, fill=(255, 230, 230, 255), width=4)
        draw.ellipse((90, 52, 122, 82), fill=(255, 130, 130, 95))
    elif kind == "box":
        draw.polygon([(78, 64), (138, 36), (188, 68), (126, 98)], fill=(180, 115, 55, 255), outline=(245, 200, 145, 255))
        draw.polygon([(78, 64), (126, 98), (126, 154), (78, 120)], fill=(126, 78, 42, 255), outline=(245, 200, 145, 255))
        draw.polygon([(126, 98), (188, 68), (188, 124), (126, 154)], fill=(150, 92, 45, 255), outline=(245, 200, 145, 255))
    elif kind == "hand":
        draw.ellipse((66, 48, 148, 130), fill=(228, 178, 132, 255), outline=(255, 225, 190, 255), width=4)
        draw.rectangle((135, 42, 168, 112), fill=(228, 178, 132, 255))
        draw.polygon([(168, 42), (205, 52), (169, 70)], fill=(228, 178, 132, 255))
    elif kind == "key":
        draw.ellipse((58, 72, 118, 132), outline=(255, 210, 60, 255), width=12)
        draw.line((112, 102, 188, 102), fill=(255, 210, 60, 255), width=12)
        draw.line((168, 102, 168, 124), fill=(255, 210, 60, 255), width=8)
        draw.line((188, 102, 188, 120), fill=(255, 210, 60, 255), width=8)
    elif kind == "city":
        for x, h, c in [(42, 82, (70, 115, 160)), (82, 118, (80, 150, 190)), (126, 94, (54, 98, 145)), (164, 130, (90, 165, 205))]:
            draw.rectangle((x, 150 - h, x + 32, 150), fill=c + (255,), outline=(210, 230, 245, 255))
            for wy in range(150 - h + 14, 145, 24):
                draw.rectangle((x + 9, wy, x + 16, wy + 8), fill=(255, 220, 120, 255))
    elif kind == "xray":
        draw.rounded_rectangle((55, 22, 185, 158), radius=14, fill=(13, 55, 72, 255), outline=(170, 230, 245, 255), width=4)
        draw.ellipse((78, 45, 119, 134), outline=(210, 245, 255, 210), width=5)
        draw.ellipse((121, 45, 162, 134), outline=(210, 245, 255, 210), width=5)
        draw.ellipse((135, 91, 153, 110), fill=(255, 75, 75, 210))
    elif kind == "game_agent":
        draw.rounded_rectangle((86, 42, 154, 132), radius=18, fill=(70, 210, 130, 255), outline=(225, 255, 235, 255), width=4)
        draw.ellipse((100, 60, 116, 76), fill=(20, 40, 32, 255))
        draw.ellipse((126, 60, 142, 76), fill=(20, 40, 32, 255))
        draw.polygon([(120, 18), (138, 42), (102, 42)], fill=(255, 210, 60, 255))
    elif kind == "tree":
        draw.rectangle((111, 88, 131, 154), fill=(108, 69, 38, 255))
        for xy, col in [((58, 32, 130, 112), (48, 155, 92)), ((105, 25, 184, 111), (42, 125, 82)), ((78, 62, 164, 142), (56, 172, 100))]:
            draw.ellipse(xy, fill=col + (235,), outline=(170, 230, 180, 255), width=3)
    elif kind == "brain":
        draw.ellipse((55, 45, 130, 125), fill=(126, 96, 230, 255), outline=(220, 210, 255, 255), width=4)
        draw.ellipse((110, 45, 185, 125), fill=(92, 205, 195, 255), outline=(220, 255, 250, 255), width=4)
        for p1, p2 in [((90, 84), (142, 65)), ((95, 108), (152, 106)), ((128, 84), (164, 92))]:
            draw.line((*p1, *p2), fill=(255, 230, 120, 255), width=4)
    elif kind == "room":
        draw.rectangle((35, 52, 205, 142), fill=(55, 63, 76, 255), outline=(210, 225, 240, 255), width=3)
        draw.rectangle((55, 98, 128, 116), fill=(150, 92, 48, 255))
        draw.rectangle((140, 75, 177, 130), fill=(55, 120, 190, 255))
        draw.ellipse((82, 68, 112, 98), fill=(230, 235, 240, 255))
    img.save(ASSETS / name)


def build_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    kinds = {
        "person.png": "person", "teacher.png": "teacher", "robot.png": "robot", "robot_arm.png": "robot_arm",
        "laptop.png": "laptop", "camera.png": "camera", "car.png": "car", "traffic_light.png": "traffic_light",
        "door.png": "door", "table.png": "table", "chair.png": "chair", "cup.png": "cup",
        "red_cup.png": "red_cup", "blue_cup.png": "blue_cup", "bottle.png": "bottle",
        "ball.png": "ball", "box.png": "box", "hand.png": "hand", "key.png": "key",
        "city.png": "city", "xray.png": "xray", "game_agent.png": "game_agent",
        "tree.png": "tree", "brain.png": "brain", "room.png": "room",
    }
    for name, kind in kinds.items():
        make_asset(name, kind)


def build_scene_files():
    for i in range(1, 32):
        content = dedent(f"""\
            from __future__ import annotations

            from manim import *
            import os
            import sys

            sys.path.append(os.path.dirname(__file__))
            from dark_tech_renderer import render_dark_tech_scene


            class GeneratedVideo(Scene):
                def construct(self):
                    render_dark_tech_scene(self, {i})
            """)
        (SCENES / f"scene_{i:03d}.py").write_text(content, encoding="utf-8")


def build_docs():
    DOCS.mkdir(exist_ok=True)
    manifest = json.loads((ROOT / "output" / "final" / "manifest.json").read_text(encoding="utf-8"))[:31]
    lines = [
        "# Dark-Tech Redesign Plan for Scenes 001-031",
        "",
        "## Global Design System",
        "- Background: #080D16 / #0A1118 navy-black.",
        "- Title: centered top, #FFD700, bold sans-serif, one title per scene.",
        "- Blocks: rounded rectangles with transparent fill, semantic border colors.",
        "- Entity visuals: raster cutout-style semi-photoreal assets inside bordered blocks.",
        "- Arrows: thick light-gray data arrows; orange-red double arrows for feedback/causal tension.",
        "- Layout: main row occupies the central 60-70% usable width; formula/note stay in bottom annotation zone.",
        "- Audio sync: scene audio starts at t=0; visuals reveal in order and are held until `manifest.duration`.",
        "",
        "## Scene-by-scene Redesign Plan",
    ]
    specs = json.loads(json.dumps({str(k): v for k, v in {
        1: "Pixels -> real room objects -> relations -> causes -> world model",
        2: "real object -> camera -> RGB tensor -> pixel matrix",
        3: "image tensor -> encoder -> compact representation vector",
        4: "car/person/traffic light split from one mixed vector",
        5: "street scene -> detection boxes -> object slots -> unsupervised structure",
        6: "ball and box mapped into separate slots",
        7: "image features enter Slot Attention and leave as clean slots",
        8: "competition resolves mixed pieces into disentangled slots",
        9: "slots -> decoder -> masks -> reconstruction",
        10: "synthetic world contrasted with real-world complexity",
        11: "image -> ViT -> DINO features -> semantic slots",
        12: "slots reconstruct DINO features instead of raw pixels",
        13: "object pair enters relation function",
        14: "observed condition -> correlation -> result, with warning role",
        15: "intervention hand changes physical system and outcome",
        16: "passive observation contrasted with active intervention",
        17: "parents/noise feed SCM function to produce variable",
        18: "ball velocity causes impact force and box motion",
        19: "mass/acceleration create force, momentum and slide distance",
        20: "slots become causal graph and behavior prediction",
        21: "sunny training shifts to rainy testing while stable rule remains",
        22: "visible ball, occluder, persistent slot, reappearance",
        23: "state/action feed world model to predict next state",
        24: "robot perception -> cup/bottle slots -> causal plan -> safe grasp",
        25: "road entities -> relations -> brake decision -> safe driving",
        26: "embodied agent uses key-door rule to obtain reward",
        27: "medical image -> segments -> lesion highlight -> diagnosis",
        28: "physical city and cameras map to digital twin and traffic control",
        29: "text command grounds to red cup slot and robot action",
        30: "ambiguity, hidden U, missing intervention and scaling cost",
        31: "perception plus causality forms a causal world model",
    }.items()}))
    for e in manifest:
        idx = e["scene_index"]
        formula = (e.get("formulas") or [""])[0]
        lines.extend([
            f"### Scene {idx:03d}: {e['title']}",
            f"- Core idea: {e['goal']}",
            f"- Voiceover summary: {e['voice_text'][:220]}...",
            f"- Main entities/modules: {specs[str(idx)]}.",
            f"- Formula panel: `{formula}`.",
            "- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.",
            "- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.",
            f"- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until {e['duration']:.3f}s.",
            "- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.",
            "",
        ])
    lines.extend([
        "## Voiceover / Visual Sync Map",
        "- 0.0s: audio starts; title appears immediately with no future-scene content.",
        "- 0.8-1.6s: formula panel appears only for the current scene formula.",
        "- 1.6-4.8s: flow blocks appear left-to-right in the same order as the spoken concept chain.",
        "- 4.8-7.0s: arrows are created after both connected blocks exist.",
        "- 7.0s-end: note/highlight may appear, but the core visual remains visible until `manifest.duration`.",
        "- Feedback scenes add orange-red double-arrow only after causal/comparison blocks are on screen.",
    ])
    (DOCS / "dark_tech_redesign_plan.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    (SCENES / "dark_tech_renderer.py").write_text(HELPER.lstrip(), encoding="utf-8")
    build_assets()
    build_scene_files()
    build_docs()


if __name__ == "__main__":
    main()
