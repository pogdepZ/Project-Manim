from __future__ import annotations

import re
from dataclasses import dataclass


SYMBOL_REPLACEMENTS: list[tuple[str, str]] = [
    ("∈", " thuộc "),
    ("∀", " với mọi "),
    ("∃", " tồn tại "),
    ("≤", " nhỏ hơn hoặc bằng "),
    ("≥", " lớn hơn hoặc bằng "),
    ("≠", " khác "),
    ("→", " dẫn tới "),
    ("⇒", " suy ra "),
    ("×", " nhân "),
    ("Δ", " delta "),
    ("|", " given "),
]


@dataclass(frozen=True)
class CleanedScript:
    title: str | None
    body: str
    tts_text: str


def clean_script(raw_text: str) -> CleanedScript:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.strip() for line in text.splitlines()).strip()

    title: str | None = None
    lines = text.splitlines()
    if lines:
        first = lines[0].strip().lstrip("#").strip()
        if first.lower().startswith(("tiêu đề:", "title:")):
            _, value = first.split(":", 1)
            title = value.strip() or None
            text = "\n".join(lines[1:]).strip()
        elif len(first) <= 100 and len(lines) > 1 and not re.search(r"[.!?。]$", first):
            title = first
            text = "\n".join(lines[1:]).strip()

    return CleanedScript(title=title, body=text, tts_text=make_tts_readable(text))


def make_tts_readable(text: str) -> str:
    paragraphs = text.split("\n\n")
    cleaned_paragraphs = []
    for p in paragraphs:
        lines = p.split("\n")
        cleaned_lines = []
        for line in lines:
            readable = line
            readable = re.sub(
                r"P\s*\(\s*Y\s*\|\s*do\s*\(\s*X\s*=\s*x\s*\)\s*\)",
                "P Y given do X bằng x",
                readable,
                flags=re.IGNORECASE,
            )
            readable = re.sub(
                r"P\s*\(\s*Y\s*\|\s*X\s*\)",
                "P Y given X",
                readable,
                flags=re.IGNORECASE,
            )
            readable = re.sub(
                r"X\s*∈\s*(?:R|\\mathbb\{R\})\s*\^\s*\{?H\s*[×x*]\s*W\s*[×x*]\s*C\}?",
                "X thuộc R mũ H nhân W nhân C",
                readable,
                flags=re.IGNORECASE,
            )
            for symbol, replacement in SYMBOL_REPLACEMENTS:
                readable = readable.replace(symbol, replacement)
            readable = re.sub(r"\\mathbb\{R\}", "R", readable)
            readable = re.sub(r"\bdo\s*\(([^)]+)\)", lambda m: "do " + _read_equation(m.group(1)), readable)
            readable = re.sub(r"([A-Za-z])_([A-Za-z0-9]+)", r"\1 dưới \2", readable)
            readable = readable.replace("...", ", ").replace("…", ", ")
            readable = re.sub(r"[ \t]+", " ", readable).strip()
            cleaned_lines.append(readable)
        cleaned_paragraphs.append("\n".join(cleaned_lines))
    return "\n\n".join(cleaned_paragraphs)


def _read_equation(value: str) -> str:
    return value.replace("=", " bằng ").replace("_", " ").strip()
