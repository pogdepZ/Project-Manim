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
