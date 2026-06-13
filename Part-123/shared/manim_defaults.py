"""Common Manim defaults used by all local video projects."""

from manim import Text


def configure_vietnamese_text(default_font="Noto Sans"):
    """Use a font that handles Vietnamese text when no font is provided."""
    if getattr(Text, "_skillmanim_vietnamese_font_patch", False):
        return

    original_init = Text.__init__

    def patched_init(self, text, *args, **kwargs):
        if len(args) < 6 and "font" not in kwargs:
            kwargs["font"] = default_font
        elif kwargs.get("font") == "":
            kwargs["font"] = default_font
        original_init(self, text, *args, **kwargs)

    Text.__init__ = patched_init
    Text._skillmanim_vietnamese_font_patch = True
