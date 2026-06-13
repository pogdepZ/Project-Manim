from __future__ import annotations

import re
from dataclasses import dataclass, field


DEFAULT_SCENE_BLUEPRINTS: list[dict[str, object]] = [
    {
        "title": "Pixel to Object",
        "animation_type": "pixel_to_object",
        "animation_pattern": "Pixel to Object",
        "formulas": [r"X \in \mathbb{R}^{H \times W \times C}"],
        "keywords": ["pixel", "pích xơ", "matrix", "image", "ảnh", "ma trận", "điểm ảnh"],
        "colors": ["BLUE_C", "TEAL_D", "GOLD_A", "WHITE"],
    },
    {
        "title": "Object Slots",
        "animation_type": "object_slots",
        "animation_pattern": "Vector to Slots",
        "formulas": [r"Z = \{z_1, z_2, \ldots, z_K\}"],
        "keywords": ["slot", "object slot", "khay", "tách biệt", "biểu diễn trộn lẫn", "object detection", "representation", "véc tơ", "máy nén"],
        "colors": ["TEAL_D", "BLUE_C", "ORANGE", "WHITE"],
    },
    {
        "title": "Attention Flow",
        "animation_type": "object_slots",
        "animation_pattern": "Attention Flow",
        "formulas": [r"\operatorname{Attention}(Q,K,V)"],
        "keywords": ["attention", "chú ý", "truy vấn", "khóa", "softmax", "cập nhật", "cạnh tranh", "mảnh ghép"],
        "colors": ["BLUE_C", "GOLD_A", "GREY_B", "WHITE"],
    },
    {
        "title": "Reconstruction Layers",
        "animation_type": "object_slots",
        "animation_pattern": "Reconstruction Layers",
        "formulas": [r"\hat{x} = \sum_k m_k \hat{x}_k"],
        "keywords": ["reconstruction", "tái tạo", "mask", "mặt nạ", "giải mã", "decoded"],
        "colors": ["TEAL_D", "GOLD_A", "GREY_C", "WHITE"],
    },
    {
        "title": "Correlation",
        "animation_type": "correlation",
        "animation_pattern": "Correlation vs Causation",
        "formulas": [r"P(Y \mid X)"],
        "keywords": ["correlation", "tương quan", "p(y|x)", "p(y | x)", "thống kê"],
        "colors": ["GREY_B", "BLUE_C", "ORANGE", "WHITE"],
    },
    {
        "title": "Causation",
        "animation_type": "causation",
        "animation_pattern": "Correlation vs Causation",
        "formulas": [r"P(Y \mid do(X=x))"],
        "keywords": ["causation", "nhân quả", "do(", "intervention", "can thiệp"],
        "colors": ["GOLD_A", "ORANGE", "TEAL_D", "WHITE"],
    },
    {
        "title": "SCM Graph",
        "animation_type": "scm_graph",
        "animation_pattern": "Causal Graph",
        "formulas": [r"X_i = f_i(PA_i, N_i)"],
        "keywords": ["scm", "s c m", "structural", "graph", "đồ thị", "force", "collision", "va chạm", "lực", "động lượng", "quan hệ"],
        "colors": ["BLUE_C", "GOLD_A", "MAROON_B", "WHITE"],
    },
    {
        "title": "Intervention",
        "animation_type": "intervention",
        "animation_pattern": "Causal Graph",
        "formulas": [r"F = ma", r"\Delta p = F \Delta t"],
        "keywords": ["intervention", "do(", "speed", "velocity", "tốc độ", "can thiệp"],
        "colors": ["GOLD_A", "ORANGE", "BLUE_C", "WHITE"],
    },
    {
        "title": "Distribution Shift",
        "animation_type": "distribution_shift",
        "animation_pattern": "Distribution Shift",
        "formulas": [r"P_{train}(X,Y) \ne P_{test}(X,Y)"],
        "keywords": ["distribution shift", "train", "test", "rain", "fog", "night", "dịch chuyển", "mưa", "ban đêm"],
        "colors": ["BLUE_C", "GREY_B", "GOLD_A", "WHITE"],
    },
    {
        "title": "World Model Rollout",
        "animation_type": "scm_graph",
        "animation_pattern": "World Model Rollout",
        "formulas": [r"s_{t+1} = WorldModel(s_t, a_t)"],
        "keywords": ["world model", "mô hình thế giới", "rollout", "trạng thái tiếp theo", "lên kế hoạch", "tồn tại vĩnh viễn", "qua thời gian"],
        "colors": ["TEAL_D", "BLUE_C", "GOLD_A", "WHITE"],
    },
    {
        "title": "Applications",
        "animation_type": "applications",
        "animation_pattern": "Application Map",
        "formulas": [],
        "keywords": ["application", "ứng dụng", "robot", "robotics", "driving", "xe tự lái", "medical", "y tế", "city", "thành phố", "multimodal", "đa phương thức", "game"],
        "colors": ["BLUE_C", "TEAL_D", "ORANGE", "GOLD_A", "WHITE"],
    },
    {
        "title": "Conclusion",
        "animation_type": "conclusion",
        "animation_pattern": "Causal World Model Summary",
        "formulas": [],
        "keywords": ["conclusion", "kết luận", "tóm lại", "world model"],
        "colors": ["BLUE_C", "TEAL_D", "GOLD_A", "WHITE"],
    },
]


@dataclass
class SceneSpec:
    scene_index: int
    scene_title: str
    voice_text: str
    animation_type: str
    goal: str = ""
    voice_text_raw: str = ""
    visual_hints: list[str] = field(default_factory=list)
    screen_formulas: list[str] = field(default_factory=list)
    formula_speech: list[str] = field(default_factory=list)
    animation_pattern: str = ""
    colors: list[str] = field(default_factory=list)
    formulas: list[str] = field(default_factory=list)
    chunks: list[str] = field(default_factory=list)
    duration: float = 0.0
    audio_file: str = ""
    chunk_audio_files: list[str] = field(default_factory=list)
    start: float = 0.0
    end: float = 0.0


def split_into_scenes(body_text: str, tts_text: str, max_chars: int, scene_duration: int = 60) -> list[SceneSpec]:
    raw_sections = _split_sections(body_text)
    tts_sections = _split_sections(tts_text)
    voice_sections = tts_sections if len(tts_sections) == len(raw_sections) else raw_sections

    if not raw_sections:
        return []

    has_explicit_scenes = False
    for sec in raw_sections:
        lines = sec.splitlines()
        if lines:
            first = lines[0].strip()
            if first.startswith(("#", "##")) or re.match(r"^\d+[\).:-]\s+", first):
                has_explicit_scenes = True
                break

    if not has_explicit_scenes:
        raw_sections = _split_to_target_voice_length(raw_sections, scene_duration=scene_duration)
        voice_sections = _split_to_target_voice_length(voice_sections, scene_duration=scene_duration)

    scenes: list[SceneSpec] = []
    used_types: set[str] = set()
    for index, section in enumerate(raw_sections, start=1):
        voice_section = voice_sections[index - 1] if index <= len(voice_sections) else section
        blueprint = _choose_blueprint(section, index, used_types)
        used_types.add(str(blueprint["animation_type"]))

        raw_fields = _parse_section_fields(section)
        tts_fields = _parse_section_fields(voice_section)
        parsed_formulas = raw_fields["formulas"]
        parsed_voice = str(tts_fields["voice_text"])

        scene = SceneSpec(
            scene_index=index,
            scene_title=str(_extract_heading(section) or blueprint["title"]),
            voice_text=parsed_voice,
            animation_type=str(blueprint["animation_type"]),
            goal=_infer_goal(section),
            voice_text_raw=str(raw_fields["voice_text"]),
            visual_hints=list(raw_fields["visual_hints"]),
            screen_formulas=parsed_formulas if parsed_formulas else list(blueprint["formulas"]),
            formula_speech=list(raw_fields["formula_speech"]),
            animation_pattern=str(blueprint.get("animation_pattern") or blueprint["animation_type"]),
            colors=list(blueprint.get("colors") or []),
            formulas=parsed_formulas if parsed_formulas else list(blueprint["formulas"]),
        )
        scene.chunks = split_voice_chunks(scene.voice_text, max_chars=max_chars)
        scenes.append(scene)
    return scenes


def _split_to_target_voice_length(sections: list[str], scene_duration: int) -> list[str]:
    target_chars = max(450, int(scene_duration * 13))
    max_scene_chars = max(target_chars + 220, int(target_chars * 1.35))
    result: list[str] = []
    for section in sections:
        body = _strip_heading(section)
        if len(body) <= max_scene_chars:
            result.append(section)
            continue

        heading = _extract_heading(section)
        pieces = _split_long_body(body, target_chars=target_chars)
        for index, piece in enumerate(pieces, start=1):
            if heading:
                result.append(f"{heading} - phần {index}\n\n{piece}")
            else:
                result.append(piece)
    return result


def split_voice_chunks(text: str, max_chars: int = 800, target_min: int = 500) -> list[str]:
    if max_chars < 200:
        raise ValueError("--max-chars must be at least 200")
    target_min = min(target_min, max_chars)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        for piece in _split_paragraph(paragraph, max_chars):
            candidate = f"{current}\n\n{piece}".strip() if current else piece
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current.strip())
                current = piece
            if len(current) >= target_min:
                chunks.append(current.strip())
                current = ""
    if current:
        chunks.append(current.strip())
    return chunks


def _split_sections(text: str) -> list[str]:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    sections: list[str] = []
    current: list[str] = []
    has_seen_heading = False
    has_any_headings = any(_looks_like_heading(b) for b in blocks)
    for block in blocks:
        if _looks_like_heading(block):
            has_seen_heading = True
            if current:
                sections.append("\n\n".join(current).strip())
            current = [block]
        else:
            if has_any_headings and not has_seen_heading:
                continue
            current.append(block)
    if current:
        sections.append("\n\n".join(current).strip())
    return sections


def _split_long_body(text: str, target_chars: int) -> list[str]:
    sentences = _split_sentences(text)
    if len(text) <= target_chars or len(sentences) <= 1:
        return sentences
    sections: list[str] = []
    current = ""
    for sentence in sentences:
        candidate = f"{current} {sentence}".strip()
        if len(candidate) <= target_chars or not current:
            current = candidate
        else:
            sections.append(current)
            current = sentence
    if current:
        sections.append(current)
    return sections


def _choose_blueprint(text: str, index: int, used_types: set[str]) -> dict[str, object]:
    lowered = text.lower()
    heading = (_extract_heading(text) or "").lower()
    scored: list[tuple[int, dict[str, object]]] = []
    for blueprint in DEFAULT_SCENE_BLUEPRINTS:
        score = 0
        for keyword in blueprint["keywords"]:  # type: ignore[index]
            lowered_keyword = str(keyword).lower()
            if lowered_keyword in lowered:
                score += 1
            if heading and lowered_keyword in heading:
                score += 2
        scored.append((score, blueprint))
    best_score, best = max(scored, key=lambda item: item[0])
    if best_score > 0:
        return best
    return DEFAULT_SCENE_BLUEPRINTS[min(index - 1, len(DEFAULT_SCENE_BLUEPRINTS) - 1)]


def _split_paragraph(paragraph: str, max_chars: int) -> list[str]:
    if len(paragraph) <= max_chars:
        return [paragraph]
    pieces: list[str] = []
    current = ""
    for sentence in _split_sentences(paragraph):
        if len(sentence) > max_chars:
            if current:
                pieces.append(current)
                current = ""
            pieces.extend(_hard_split(sentence, max_chars))
            continue
        candidate = f"{current} {sentence}".strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                pieces.append(current)
            current = sentence
    if current:
        pieces.append(current)
    return pieces


def _split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?。])\s+", text) if part.strip()]


def _hard_split(text: str, max_chars: int) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks


def _looks_like_heading(block: str) -> bool:
    first = block.splitlines()[0].strip()
    if first.startswith(("#", "##")):
        return True
    if re.match(r"^\d+[\).:-]\s+", first):
        return True
    if first.lower().startswith((
        "công thức màn hình:", "cách đọc công thức:", "nội dung voice:",
        "visual gợi ý:", "mô tả ngắn:", "thời lượng mục tiêu:", "ghi chú cho tool:"
    )):
        return False
    return len(first) <= 80 and not re.search(r"[.!?。]$", first) and len(block.splitlines()) <= 2


def _extract_heading(section: str) -> str | None:
    first = section.splitlines()[0].strip().lstrip("#").strip()
    if _looks_like_heading(first):
        return re.sub(r"^\d+[\).:-]\s*", "", first).strip() or None
    return None


def _strip_heading(section: str) -> str:
    lines = section.splitlines()
    if lines and _looks_like_heading(lines[0]):
        return "\n".join(lines[1:]).strip() or lines[0].strip()
    return section.strip()


def _parse_section_fields(section: str) -> dict[str, object]:
    formulas = []
    read_formula_parts = []
    voice_parts = []
    visual_hints = []
    
    current_state = None  # 'formula', 'read_formula', or 'voice'
    
    for line in section.splitlines():
        line_strip = line.strip()
        if not line_strip:
            continue
        hint_match = re.match(r"\[Gợi ý hiển thị:\s*(.*?)\]", line_strip, flags=re.IGNORECASE)
        if hint_match:
            visual_hints.append(hint_match.group(1).strip())
            continue
            
        line_lower = line_strip.lower()
        if line_lower.startswith("công thức màn hình:"):
            current_state = "formula"
            content = line_strip[len("công thức màn hình:"):].strip()
            if content:
                formulas.append(content)
            continue
        elif line_lower.startswith("cách đọc công thức:"):
            current_state = "read_formula"
            content = line_strip[len("cách đọc công thức:"):].strip()
            if content:
                read_formula_parts.append(content)
            continue
        elif line_lower.startswith("nội dung voice:"):
            current_state = "voice"
            content = line_strip[len("nội dung voice:"):].strip()
            if content:
                voice_parts.append(content)
            continue
        elif line_strip.startswith("##"):
            current_state = None
            continue
            
        if current_state == "formula":
            formulas.append(line_strip)
        elif current_state == "read_formula":
            read_formula_parts.append(line_strip)
        elif current_state == "voice":
            voice_parts.append(line_strip)
            
    combined_voice = []
    if read_formula_parts:
        combined_voice.extend(read_formula_parts)
    if voice_parts:
        combined_voice.extend(voice_parts)
        
    voice_text = " ".join(combined_voice).strip()
    voice_text = re.sub(r"\[Gợi ý hiển thị:[^\]]*\]", "", voice_text, flags=re.IGNORECASE)
    voice_text = re.sub(r"\s+", " ", voice_text).strip()

    return {
        "formulas": formulas,
        "formula_speech": read_formula_parts,
        "voice_text": voice_text,
        "visual_hints": visual_hints,
    }


def _infer_goal(section: str) -> str:
    heading = _extract_heading(section)
    if heading:
        return f"Giúp người xem hiểu: {heading}."
    voice = str(_parse_section_fields(section)["voice_text"])
    first_sentence = _split_sentences(voice)
    if first_sentence:
        return first_sentence[0]
    return "Giúp người xem nắm ý chính của scene."
