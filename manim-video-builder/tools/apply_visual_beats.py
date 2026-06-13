from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "output" / "final" / "manifest.json"
SCENE_DIR = ROOT / "manim_scenes"
PLAN = ROOT / "VISUAL_BEAT_PLAN.md"


def py_string(value: str) -> str:
    return repr(value)


def scene_code(item: dict) -> str:
    idx = int(item["scene_index"])
    title = item.get("scene_title") or item.get("title") or f"Scene {idx:03d}"
    voice = item.get("voice_text_tts_safe") or item.get("voice_text") or item.get("voice_text_raw") or ""
    formulas = item.get("screen_formulas") or item.get("formulas") or []
    formula = formulas[0] if formulas else ""
    hints = item.get("visual_hints") or []
    pattern = item.get("animation_pattern") or item.get("animation_type") or ""
    duration = float(item.get("duration") or 0.0)
    return f'''from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title={py_string(title)},
            voice={py_string(voice)},
            formula={py_string(formula)},
            visual_hints={repr(hints)},
            pattern={py_string(pattern)},
            duration={duration:.3f},
        )
'''


def split_sentences(text: str) -> list[str]:
    import re

    chunks = re.split(r"(?<=[.!?])\s+", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def objects_for(sentence: str) -> list[str]:
    s = sentence.lower()
    checks = [
        ("pích xơ/ma trận số", ["pích xơ", "ma trận số", "điểm ảnh"]),
        ("ảnh/tensor/H-W-C/RGB", ["ảnh", "ten xơ", "hát", "vê kép", "sê", "r g b", "kênh màu"]),
        ("object/vật thể/đối tượng", ["object", "đối tượng", "vật thể", "thực thể"]),
        ("slot", ["slot", "vị trí nhớ"]),
        ("attention/chú ý", ["attention", "chú ý"]),
        ("quả bóng", ["quả bóng", "vùng màu tròn"]),
        ("cái hộp", ["cái hộp", "hộp", "khối vuông"]),
        ("robot/A I", ["robot", "a i"]),
        ("xe", ["xe"]),
        ("người đi bộ/con người", ["người đi bộ", "con người", "người"]),
        ("đèn giao thông/đèn đỏ", ["đèn giao thông", "đèn đỏ"]),
        ("tương quan", ["tương quan", "correlation"]),
        ("nhân quả/nguyên nhân", ["nhân quả", "nguyên nhân", "gây ra", "tác động"]),
        ("can thiệp", ["can thiệp", "do operator", "thí nghiệm"]),
        ("graph/đồ thị", ["graph", "đồ thị"]),
        ("distribution shift", ["distribution shift", "dịch chuyển phân phối", "train", "test"]),
        ("world model", ["world model", "mô hình thế giới", "state", "action"]),
        ("véc tơ/biểu diễn", ["véc tơ", "vector", "biểu diễn", "nén", "hàm"]),
    ]
    found = [name for name, keys in checks if any(k in s for k in keys)]
    return found or ["keyword node"]


def action_for(sentence: str) -> str:
    s = sentence.lower()
    if any(k in s for k in ["lăn", "di chuyển", "dừng", "đẩy", "mở", "chuyển động"]):
        return "Animate object movement/impact with shift and Flash."
    if any(k in s for k in ["dẫn tới", "tác động", "gây ra", "nguyên nhân", "nhân quả"]):
        return "Create causal Arrow and highlight the effect node."
    if any(k in s for k in ["tách", "biến", "chuyển", "gom", "nén"]):
        return "Use ReplacementTransform/Transform from source representation to target object/slot/vector."
    if any(k in s for k in ["so sánh", "khác", "nhưng", "thay vì", "trong khi"]):
        return "Split screen into two panels and indicate the contrast."
    return "Grow/Fade/Create the relevant visual object and indicate it."


def visual_for(sentence: str) -> str:
    objs = objects_for(sentence)
    if "tương quan" in objs:
        return "Draw ball/object pair with a grey DashedLine."
    if "nhân quả/nguyên nhân" in objs:
        return "Draw cause/effect nodes, a GOLD_A Arrow, then animate effect change."
    if "can thiệp" in objs:
        return "Draw do button, press arrow, and animate changed outcome."
    if "distribution shift" in objs:
        return "Draw train/test panels with sunny versus rainy/night conditions."
    if "world model" in objs:
        return "Draw state -> action -> next state rollout."
    if "attention/chú ý" in objs:
        return "Draw feature dots, slot containers, and attention lines."
    if "slot" in objs:
        return "Draw slots bound to object icons with arrows."
    if "ảnh/tensor/H-W-C/RGB" in objs:
        return "Draw RGB tensor stack, H/W braces, and channel arrow."
    if "pích xơ/ma trận số" in objs:
        return "Draw pixel grid, cluster boxes, and transform groups into objects."
    return "Draw the mentioned icons/shapes and animate highlight or movement."


def write_plan(items: list[dict]) -> None:
    lines = [
        "# Visual Beat Plan",
        "",
        "Generated from `output/final/manifest.json`. Each sentence maps to a Manim visual beat, not only text.",
        "",
    ]
    for item in items:
        idx = int(item["scene_index"])
        title = item.get("scene_title") or item.get("title") or f"Scene {idx:03d}"
        voice = item.get("voice_text_tts_safe") or item.get("voice_text") or item.get("voice_text_raw") or ""
        lines.append(f"## Scene {idx:03d}: {title}")
        lines.append("")
        lines.append("| Sentence | Objects mentioned | Action | Visual beat | Manim objects/animations |")
        lines.append("| --- | --- | --- | --- | --- |")
        for sentence in split_sentences(voice):
            objs = ", ".join(objects_for(sentence))
            action = action_for(sentence)
            visual = visual_for(sentence)
            manim = "Circle, Rectangle, RoundedRectangle, Arrow/DashedLine, Create, GrowFromCenter, FadeIn, ReplacementTransform, Indicate/Circumscribe"
            clean = sentence.replace("|", "/")
            lines.append(f"| {clean} | {objs} | {action} | {visual} | {manim} |")
        lines.append("")
    PLAN.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for item in data:
        idx = int(item["scene_index"])
        path = SCENE_DIR / f"scene_{idx:03d}.py"
        if not path.exists():
            raise FileNotFoundError(path)
        backup = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup)
        path.write_text(scene_code(item), encoding="utf-8")
    write_plan(data)
    print(f"updated {len(data)} scenes")
    print(f"wrote {PLAN.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
