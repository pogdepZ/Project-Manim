from manim import *
from pathlib import Path
import os

# ---------------------------------------------------------
# 1. GLOBAL DESIGN SYSTEM
# ---------------------------------------------------------
# Colors
NAVY_BG = "#0A1118"
GOLD_TITLE = "#FFD700"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#E2E8F0"

# Roles / Borders
COLOR_USER = "#3A86FF"    # Blue
COLOR_AI = "#9D4EDD"      # Purple
COLOR_RESULT = "#06D6A0"  # Green
COLOR_WARNING = "#FF6B6B" # Orange/Red
COLOR_MATH = "#F9C74F"    # Yellow

# Default Arrow
ARROW_COLOR = "#94A3B8"   # Light Gray
FEEDBACK_ARROW = "#FF6B6B"# Orange/Red

# Assets Directory
ASSET_DIR = Path("/home/pognova/SkillManim/images/general")

# ---------------------------------------------------------
# 2. HELPER FUNCTIONS
# ---------------------------------------------------------
def create_title(text):
    """Creates a top-centered golden title."""
    title = Text(text, font_size=36, color=GOLD_TITLE, weight=BOLD)
    title.to_edge(UP, buff=0.4)
    return title

def get_image_path(entity_name):
    """Maps an entity name to its photorealistic image path."""
    mapping = {
        "person": "user.png",
        "user": "user.png",
        "robot": "robot.png",
        "ai": "ai.png",
        "computer": "computer.png",
        "car": "car.png",
        "table": "table.png",
        "chair": "chair.png",
        "cup": "cup.png",
        "camera": "camera.png",
        "pixels": "pixels.png",
        "world": "world.png",
        "door": "cửa.png",
        "traffic_light": "đèn đỏ.png",
        "objects": "đối tượng.png",
        "relations": "quan hệ.png",
        "causes": "nguyên nhân.png",
        "world_model": "mô hình thế giới.png"
    }
    file_name = mapping.get(entity_name.lower())
    if file_name and (ASSET_DIR / file_name).exists():
        return str(ASSET_DIR / file_name)
    # Default fallback
    if (ASSET_DIR / f"{entity_name}.png").exists():
        return str(ASSET_DIR / f"{entity_name}.png")
    return None

class PhotorealBlock(Group):
    """
    A flowchart block containing a photorealistic image and a label.
    """
    def __init__(self, entity_name, label_text, role_color=COLOR_AI, width=2.2, height=2.8, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Outline Box (Rounded Rectangle with clear semantic border)
        self.box = RoundedRectangle(
            width=width, 
            height=height, 
            corner_radius=0.15,
            stroke_width=4, 
            stroke_color=role_color,
            fill_color=NAVY_BG,
            fill_opacity=0.8
        )
        
        # 2. Image (Photorealistic)
        img_path = get_image_path(entity_name)
        if img_path:
            self.image = ImageMobject(img_path)
            # Scale image to fit inside the box nicely
            self.image.scale_to_fit_width(width * 0.75)
            if self.image.height > height * 0.6:
                self.image.scale_to_fit_height(height * 0.6)
            self.image.move_to(self.box.get_center() + UP * 0.2)
        else:
            # Fallback if no image found (should not happen if rules are followed)
            self.image = Square(side_length=width*0.5, color=role_color, stroke_width=2)
            self.image.move_to(self.box.get_center() + UP * 0.2)
        
        # 3. Label
        self.label = Text(label_text, font_size=20, color=TEXT_WHITE, weight=BOLD)
        self.label.next_to(self.image, DOWN, buff=0.2)
        
        # 4. Subtle Glow
        self.glow = RoundedRectangle(
            width=width+0.1, 
            height=height+0.1, 
            corner_radius=0.2,
            stroke_width=0, 
            fill_color=role_color,
            fill_opacity=0.15
        )
        self.glow.move_to(self.box.get_center())

        self.add(self.glow, self.box, self.image, self.label)
        self.rect = self.box # Expose for easy arrow connection

class ModuleBlock(VGroup):
    """
    A block for algorithms, pipelines, or abstract concepts without specific real-world images.
    """
    def __init__(self, label_text, sub_text=None, role_color=COLOR_AI, width=3.0, height=1.5, **kwargs):
        super().__init__(**kwargs)
        
        self.box = RoundedRectangle(
            width=width, 
            height=height, 
            corner_radius=0.15,
            stroke_width=4, 
            stroke_color=role_color,
            fill_color=NAVY_BG,
            fill_opacity=0.8
        )
        
        self.label = Text(label_text, font_size=24, color=TEXT_WHITE, weight=BOLD)
        
        self.add(self.box, self.label)
        if sub_text:
            sub = Text(sub_text, font_size=16, color=TEXT_MUTED)
            self.label.shift(UP * 0.2)
            sub.next_to(self.label, DOWN, buff=0.15)
            self.add(sub)
            
        self.rect = self.box

def create_flow_arrow(start_block, end_block, color=ARROW_COLOR, double=False):
    """Creates a thick, clear connecting arrow."""
    if double:
        return DoubleArrow(
            start_block.get_right(), end_block.get_left(),
            color=color, stroke_width=8, tip_length=0.3, buff=0.2
        )
    return Arrow(
        start_block.get_right(), end_block.get_left(),
        color=color, stroke_width=8, tip_length=0.3, buff=0.2
    )

def hold_visual(scene, duration):
    """Helper to hold the visual on screen."""
    scene.wait(duration)
