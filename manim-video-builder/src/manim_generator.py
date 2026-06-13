from __future__ import annotations

import re
from pathlib import Path


def generate_manim_scene(manifest: list[dict], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(_build_code(manifest), encoding="utf-8")


def _build_code(manifest: list[dict]) -> str:
    method_calls = "\n".join(_scene_call(entry) for entry in manifest)
    return f'''from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
{method_calls}
'''


def _scene_call(entry: dict) -> str:
    title = repr(str(entry.get("scene_title") or entry.get("title") or f"Scene {entry.get('scene_index', '')}"))
    voice = repr(str(entry.get("voice_text_tts_safe") or entry.get("voice_text") or entry.get("voice_text_raw") or ""))
    formulas = entry.get("screen_formulas") or entry.get("formulas") or []
    formula = repr(_normalize_formula(str(formulas[0]))) if formulas else "''"
    visual_hints = repr([str(hint) for hint in (entry.get("visual_hints") or [])])
    pattern = repr(str(entry.get("animation_pattern") or entry.get("animation_type") or ""))
    duration = float(entry.get("duration") or 0.0)
    return f'''        self.show_scene(
            title={title},
            voice={voice},
            formula={formula},
            visual_hints={visual_hints},
            pattern={pattern},
            duration={duration:.3f},
        )'''


def _slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value or "scene"


def _normalize_formula(value: str) -> str:
    formula = value.strip()
    formula = formula.replace("→", r"\to")
    formula = formula.replace("⇒", r"\Rightarrow")
    formula = formula.replace("≠", r"\ne")
    formula = formula.replace("≤", r"\le")
    formula = formula.replace("≥", r"\ge")
    formula = formula.replace("×", r"\times")
    formula = formula.replace("...", r"\ldots").replace("…", r"\ldots")
    formula = re.sub(r"\bin\b", r"\\in", formula)
    formula = re.sub(r"\bR\^", r"\\mathbb{R}^", formula)
    formula = re.sub(r"(?<=\w)\s+x\s+(?=\w)", r" \\times ", formula)
    formula = formula.replace("->", r"\to")

    # User-facing scripts often use braces for sets. In TeX, unescaped braces
    # group content and disappear, so escape braces that are not exponent groups.
    result = []
    for index, char in enumerate(formula):
        if char == "{" and not _is_tex_syntax_group_start(formula, index):
            result.append(r"\{")
        elif char == "}" and not _closes_tex_syntax_group(formula, index):
            result.append(r"\}")
        else:
            result.append(char)
    return "".join(result)


def _is_tex_syntax_group_start(formula: str, open_index: int) -> bool:
    if open_index > 0 and formula[open_index - 1] == "^":
        return True
    return bool(re.search(r"\\[A-Za-z]+$", formula[:open_index]))


def _closes_tex_syntax_group(formula: str, close_index: int) -> bool:
    depth = 0
    for index in range(close_index, -1, -1):
        char = formula[index]
        if char == "}":
            depth += 1
        elif char == "{":
            depth -= 1
            if depth == 0:
                return _is_tex_syntax_group_start(formula, index)
    return False
