from manim import *
import os

def create_asset(name, mobject, color=BLUE):
    """Renders a single mobject to a transparent PNG file."""
    # Create a small scene just for this asset
    class AssetScene(Scene):
        def construct(self):
            self.camera.background_color = "#00000000" # Transparent
            mobject.center()
            self.add(mobject)
            
    # Configure manim for a small, transparent render
    config.pixel_height = 512
    config.pixel_width = 512
    config.frame_height = 4.0
    config.frame_width = 4.0
    config.transparent = True
    config.format = "png"
    
    scene = AssetScene()
    scene.render()
    
    # Path where Manim saves the image
    # By default: media/images/AssetScene.png
    # We want to move it to our images folder
    os.makedirs("images/general", exist_ok=True)
    target_path = f"images/general/{name}.png"
    
    # Locate the rendered file
    # In recent Manim, it's often in media/images/generate_assets/AssetScene.png
    source_path = "media/images/generate_assets/AssetScene.png"
    if not os.path.exists(source_path):
        # Alternative location
        source_path = "media/images/AssetScene.png"
        
    if os.path.exists(source_path):
        import shutil
        shutil.move(source_path, target_path)
        print(f"Created asset: {target_path}")
    else:
        print(f"Error: Could not find rendered asset for {name}")

def generate_all():
    # 1. Define high-quality procedural icons that look "photorealistic" in style
    # (using gradients and depth where possible)
    
    # PERSON / USER
    person = VGroup(
        Circle(radius=0.6, color=WHITE, fill_opacity=1).shift(UP*0.8), # Head
        RoundedRectangle(width=2.0, height=1.5, corner_radius=0.3, color=WHITE, fill_opacity=1).shift(DOWN*0.5) # Body
    ).set_color_by_gradient(BLUE, WHITE)
    
    # AI ROBOT
    robot = VGroup(
        RoundedRectangle(width=1.5, height=1.2, corner_radius=0.2, color=GRAY, fill_opacity=1), # Head
        Circle(radius=0.15, color=BLUE_A, fill_opacity=1).shift(LEFT*0.35 + UP*0.1), # Eye L
        Circle(radius=0.15, color=BLUE_A, fill_opacity=1).shift(RIGHT*0.35 + UP*0.1), # Eye R
        Rectangle(width=0.8, height=0.1, color=BLUE_A).shift(DOWN*0.3) # Mouth
    ).set_color_by_gradient(GRAY_B, GRAY_D)
    
    # CAR
    car = VGroup(
        RoundedRectangle(width=2.5, height=0.8, corner_radius=0.2, color=BLUE, fill_opacity=1),
        RoundedRectangle(width=1.5, height=0.6, corner_radius=0.2, color=BLUE, fill_opacity=1).shift(UP*0.4),
        Circle(radius=0.3, color=BLACK, fill_opacity=1).shift(LEFT*0.7 + DOWN*0.4),
        Circle(radius=0.3, color=BLACK, fill_opacity=1).shift(RIGHT*0.7 + DOWN*0.4)
    ).set_color_by_gradient(BLUE_C, BLUE_E)
    
    # TABLE
    table = VGroup(
        Rectangle(width=2.5, height=0.2, color="#8B4513", fill_opacity=1),
        Line(LEFT*1.1, LEFT*1.1 + DOWN*1.0, stroke_width=8, color="#8B4513"),
        Line(RIGHT*1.1, RIGHT*1.1 + DOWN*1.0, stroke_width=8, color="#8B4513")
    )
    
    # CHAIR
    chair = VGroup(
        Rectangle(width=1.0, height=1.0, color=ORANGE, fill_opacity=1),
        Rectangle(width=0.2, height=1.5, color=ORANGE, fill_opacity=1).next_to(ORIGIN, LEFT, buff=0).shift(UP*0.5),
        Line(ORIGIN, DOWN*0.8, stroke_width=6, color=ORANGE)
    )
    
    # CUP
    cup = VGroup(
        RoundedRectangle(width=0.8, height=1.0, corner_radius=0.1, color=WHITE, fill_opacity=1),
        Arc(radius=0.3, start_angle=-PI/2, angle=PI, color=WHITE, stroke_width=8).shift(RIGHT*0.4)
    )
    
    # CAMERA
    camera = VGroup(
        RoundedRectangle(width=1.8, height=1.2, corner_radius=0.1, color=GRAY, fill_opacity=1),
        Circle(radius=0.4, color=BLACK, fill_opacity=1),
        Circle(radius=0.1, color=WHITE, fill_opacity=0.5).shift(UP*0.4 + RIGHT*0.6)
    )
    
    # PIXELS
    pixels = VGroup(*[
        Square(0.4, fill_opacity=1, color=interpolate_color(BLUE, GREEN, i/16)).shift(RIGHT*(i%4-1.5)*0.5 + UP*(i//4-1.5)*0.5)
        for i in range(16)
    ])
    
    # WORLD / EARTH
    world = VGroup(
        Circle(radius=1.2, color=BLUE, fill_opacity=1),
        # Abstract landmasses
        Circle(radius=0.4, color=GREEN, fill_opacity=1).shift(UP*0.3 + LEFT*0.2),
        Circle(radius=0.5, color=GREEN, fill_opacity=1).shift(DOWN*0.4 + RIGHT*0.3)
    )

    # 2. Map of assets to create
    assets = {
        "user": person,
        "person": person,
        "ai_robot": robot,
        "car": car,
        "table": table,
        "chair": chair,
        "cup": cup,
        "camera": camera,
        "pixels": pixels,
        "world": world,
        "physical_world": world,
        "computer": robot.scale(1.2),
        "thế giới": world,
        "đối tượng": pixels.set_color(ORANGE),
        "quan hệ": Arrow(LEFT, RIGHT, color=YELLOW),
        "nguyên nhân": Flash(Dot(), color=ORANGE),
        "mô hình thế giới": world.set_color(PURPLE),
        "cửa": Rectangle(width=1.0, height=1.8, color=ORANGE, fill_opacity=0.5),
        "đèn đỏ": Circle(radius=0.5, color=RED, fill_opacity=1),
    }

    for name, mob in assets.items():
        create_asset(name, mob)

if __name__ == "__main__":
    generate_all()
