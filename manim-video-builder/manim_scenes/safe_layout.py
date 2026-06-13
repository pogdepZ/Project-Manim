from __future__ import annotations

from dataclasses import dataclass

from manim import *


@dataclass(frozen=True)
class LayoutZones:
    top_margin: float = 0.28
    title_height: float = 0.62
    secondary_height: float = 0.46
    bottom_height: float = 0.82
    side_margin: float = 0.48
    gap: float = 0.18

    @property
    def title_y(self) -> float:
        return config.frame_height / 2 - self.top_margin

    @property
    def title_bottom_y(self) -> float:
        return config.frame_height / 2 - self.top_margin - self.title_height

    @property
    def secondary_y(self) -> float:
        return self.title_bottom_y - self.gap

    @property
    def visual_top_y(self) -> float:
        return self.title_bottom_y - self.secondary_height - self.gap

    @property
    def visual_bottom_y(self) -> float:
        return -config.frame_height / 2 + self.bottom_height + self.gap

    @property
    def visual_height(self) -> float:
        return self.visual_top_y - self.visual_bottom_y

    @property
    def usable_width(self) -> float:
        return config.frame_width - self.side_margin * 2


ZONES = LayoutZones()


def safe_text(text: str, font_size: int = 28, color=WHITE, width: float | None = None, **kwargs):
    max_width = width or (config.frame_width - 1.0)
    mob = Text(text, font_size=font_size, color=color, **kwargs)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def place_title(title: Mobject) -> Mobject:
    title.scale_to_fit_width(min(title.width, config.frame_width - 1.0))
    title.to_edge(UP, buff=ZONES.top_margin)
    return title


def place_secondary(text: Mobject) -> Mobject:
    text.scale_to_fit_width(min(text.width, config.frame_width - 1.25))
    text.next_to(ORIGIN, UP, buff=0)
    text.set_y(ZONES.secondary_y - text.height / 2)
    return text


def place_caption(caption: Mobject) -> Mobject:
    caption.scale_to_fit_width(min(caption.width, config.frame_width - 1.2))
    caption.to_edge(DOWN, buff=0.36)
    return caption


def place_formula(formula: Mobject) -> Mobject:
    formula.scale_to_fit_width(min(formula.width, config.frame_width - 1.4))
    formula.to_edge(DOWN, buff=0.38)
    return formula


def fit_main_visual(group: Mobject, width_ratio: float = 0.64, height_ratio: float = 0.58) -> Mobject:
    max_width = config.frame_width * min(width_ratio, 0.70)
    max_height = ZONES.visual_height * min(height_ratio / 0.58, 1.0)
    target_width = config.frame_width * max(width_ratio, 0.55)
    if group.width > 0 and group.width < target_width and group.height < max_height:
        group.scale_to_fit_width(target_width)
    if group.width > max_width:
        group.scale_to_fit_width(max_width)
    if group.height > max_height:
        group.scale_to_fit_height(max_height)
    group.move_to([0, (ZONES.visual_top_y + ZONES.visual_bottom_y) / 2, 0])
    return group


def fit_split_layout(left: Mobject, right: Mobject, gap: float = 0.68) -> VGroup:
    max_block_width = config.frame_width * 0.38
    max_height = ZONES.visual_height * 0.86
    for mob in (left, right):
        if mob.width > max_block_width:
            mob.scale_to_fit_width(max_block_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
    group = VGroup(left, right).arrange(RIGHT, buff=gap)
    fit_main_visual(group, width_ratio=0.68, height_ratio=0.62)
    return group


def bbox_overlap(a: Mobject, b: Mobject, padding: float = 0.04) -> bool:
    return not (
        a.get_right()[0] + padding < b.get_left()[0]
        or b.get_right()[0] + padding < a.get_left()[0]
        or a.get_top()[1] + padding < b.get_bottom()[1]
        or b.get_top()[1] + padding < a.get_bottom()[1]
    )


def push_below(upper: Mobject, lower: Mobject, gap: float = 0.18) -> Mobject:
    if bbox_overlap(upper, lower, gap):
        lower.next_to(upper, DOWN, buff=gap)
    return lower


def assert_no_layout_overlap(pairs: list[tuple[str, Mobject, str, Mobject]], padding: float = 0.04) -> list[str]:
    issues = []
    for a_name, a, b_name, b in pairs:
        if bbox_overlap(a, b, padding):
            issues.append(f"{a_name} overlaps {b_name}")
    return issues
