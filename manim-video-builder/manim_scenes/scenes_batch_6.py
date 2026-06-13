from __future__ import annotations

from manim import *

# --- Style Constants ---
BG_COLOR = "#0F1117"
TITLE_YELLOW = "#F2C94C"
TEAL = "#4ECDC4"
ORANGE = "#FF6B4A"
BLUE = "#3A86FF"
RED = "#D76D77"
GREEN = "#6BCB77"
GREY = "#444444"

config.background_color = BG_COLOR


class EduScene(Scene):
    def create_title(self, text):
        title = Text(text, font_size=32, color=TITLE_YELLOW, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        underline = Line(LEFT, RIGHT, color=GREY, stroke_width=1).scale(6).next_to(title, DOWN, buff=0.2)
        return VGroup(title, underline)

    def create_formula(self, tex):
        formula = MathTex(tex, font_size=36, color=TITLE_YELLOW)
        formula.to_edge(DOWN, buff=0.5)
        return formula


# --- Scene 026 ---
class Scene026(EduScene):
    def construct(self):
        title = self.create_title("A I hiện thân và agent trong môi trường game")
        formula = self.create_formula(r"\text{Embodied Agent: Action} \to \text{Environment} \to \text{Reward}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Game Environment (Maze)
        maze = VGroup(*[Line(UP * 0.5, DOWN * 0.5) for _ in range(4)]).arrange(RIGHT, buff=2).shift(DOWN * 1)
        agent = Text("🤖", font_size=30).move_to(maze[0].get_center() + LEFT * 1)
        
        self.play(Create(maze), FadeIn(agent))

        # 2. Logic Tree
        tree_base = Circle(radius=0.3, color=BLUE, fill_opacity=0.2).shift(UP * 1 + RIGHT * 2)
        node_key = Text("Chìa khóa", font_size=15).next_to(tree_base, UP)
        
        tree_left = Circle(radius=0.2, color=GREY).shift(RIGHT * 1.5)
        tree_right = Circle(radius=0.2, color=GREY).shift(RIGHT * 2.5)
        
        lines = VGroup(Line(tree_base.get_bottom(), tree_left.get_top()), Line(tree_base.get_bottom(), tree_right.get_top()))

        self.play(Create(tree_base), Write(node_key), Create(lines), FadeIn(tree_left), FadeIn(tree_right))

        # 3. Action Sequence
        key_icon = Text("🔑", font_size=20).shift(LEFT * 1 + DOWN * 1)
        self.play(FadeIn(key_icon))
        self.play(agent.animate.move_to(key_icon), run_time=1)
        self.play(FadeOut(key_icon), agent.animate.set_color(GOLD_A))
        
        door_icon = Text("🚪", font_size=30).shift(RIGHT * 4 + DOWN * 1)
        self.play(FadeIn(door_icon))
        self.play(agent.animate.move_to(door_icon), run_time=1.5)
        self.play(Flash(door_icon, color=GREEN))
        
        self.wait(2)


# --- Scene 027 ---
class Scene027(EduScene):
    def construct(self):
        title = self.create_title("Hỗ trợ chẩn đoán y tế")
        formula = self.create_formula(r"\text{Medical Image} \to \text{Segments} \to \text{Diagnosis}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Medical Image (X-ray proxy)
        chest = Rectangle(width=3, height=4, color=GREY, fill_opacity=0.1)
        ribs = VGroup(*[Line(LEFT * 1.2, RIGHT * 1.2, color=GREY, stroke_opacity=0.3).shift(UP * (1.5 - i * 0.6)) for i in range(6)])
        xray = VGroup(chest, ribs).center()

        self.play(Create(xray))

        # 2. Segmenting (Saliency Spotlight)
        lesion_site = Dot(color=RED, radius=0.1).shift(UP * 0.5 + RIGHT * 0.6)
        spotlight = Annulus(inner_radius=0, outer_radius=0.8, color=RED, fill_opacity=0.2).move_to(lesion_site)
        label_lesion = Text("Tổn thương", font_size=16, color=RED).next_to(spotlight, UR)

        self.play(FadeIn(spotlight, scale=0.1), Create(lesion_site))
        self.play(spotlight.animate.scale(5).set_opacity(0.1), run_time=1)
        self.play(Write(label_lesion))
        self.play(Indicate(lesion_site, color=RED))
        
        self.wait(2)


# --- Scene 028 ---
class Scene028(EduScene):
    def construct(self):
        title = self.create_title("Thành phố thông minh và bản sao số")
        formula = self.create_formula(r"\text{Physical City} \to \text{Digital Twin (Entities)}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Video Grid
        cam_grid = VGroup(*[Rectangle(width=1.2, height=0.8, color=GREY, stroke_opacity=0.5) for _ in range(6)]).arrange_in_grid(2, 3)
        self.play(LaggedStartMap(FadeIn, cam_grid, lag_ratio=0.1))

        # 2. Digitize (Transition to Vector Dots)
        dots = VGroup(*[Dot(radius=0.08, color=TEAL).shift(np.random.randn(3) * 1.5) for _ in range(12)])
        grid_overlay = NumberPlane(x_range=[-4, 4], y_range=[-3, 3], background_line_style={"stroke_opacity": 0.2}).scale(0.8)

        self.play(
            ReplacementTransform(cam_grid, grid_overlay),
            LaggedStartMap(FadeIn, dots, lag_ratio=0.05),
            run_time=2
        )
        
        # 3. Causal prediction (Flow)
        flow_arrows = VGroup(*[Arrow(d.get_center(), d.get_center() + RIGHT * 1, color=ORANGE) for d in dots[:5]])
        self.play(Create(flow_arrows))
        self.play(dots[:5].animate.shift(RIGHT * 1))
        
        self.wait(2)


# --- Scene 029 ---
class Scene029(EduScene):
    def construct(self):
        title = self.create_title("A I đa phương thức: ngôn ngữ và hình ảnh")
        formula = self.create_formula(r"\text{Text Command} \to \text{Object Grounding} \to \text{Execution}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Text Command
        cmd_box = RoundedRectangle(width=5, height=1, color=BLUE, fill_opacity=0.1).shift(UP * 1)
        cmd_text = Text('"Lấy chiếc cốc màu đỏ trên bàn"', font_size=20, color=WHITE).move_to(cmd_box)
        self.play(Create(cmd_box), Write(cmd_text))

        # 2. Object Slots
        slots = VGroup(
            VGroup(Circle(radius=0.4, color=RED, fill_opacity=0.5), Text("Cốc", font_size=12).next_to(ORIGIN, DOWN)),
            VGroup(Circle(radius=0.4, color=BLUE, fill_opacity=0.5), Text("Bình", font_size=12).next_to(ORIGIN, DOWN))
        ).arrange(RIGHT, buff=2).shift(DOWN * 1)
        
        self.play(FadeIn(slots))

        # 3. Grounding (Arrow)
        link = Arrow(cmd_box.get_bottom(), slots[0].get_top(), color=GOLD_A)
        word_highlight = Text("chiếc cốc màu đỏ", font_size=20, color=GOLD_A).move_to(cmd_text)
        
        self.play(Write(word_highlight), Create(link))
        self.play(Indicate(slots[0], color=GOLD_A))
        
        self.wait(2)


# --- Scene 030 ---
class Scene030(EduScene):
    def construct(self):
        title = self.create_title("Các thách thức lớn trong tương lai")
        formula = self.create_formula(r"\text{Ambiguity + Confounding} \to \text{Causal Discovery Limits}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Ambiguity (Foggy tree)
        tree = VGroup(Line(ORIGIN, UP * 1.5, color=GREY), Circle(radius=0.8, color=GREEN, fill_opacity=0.2).shift(UP * 1.5)).shift(LEFT * 3)
        fog = VGroup(*[Dot(radius=0.2, color=WHITE, fill_opacity=0.1).shift(tree.get_center() + np.random.randn(3) * 0.5) for _ in range(20)])
        label_amb = Text("Mơ hồ ranh giới", font_size=18).next_to(tree, DOWN)

        self.play(Create(tree), FadeIn(fog), Write(label_amb))

        # 2. Confounding (Mystery node)
        node_u = Circle(radius=0.4, color=RED, fill_opacity=0.1).shift(RIGHT * 3 + UP * 1)
        label_u = MathTex("U", color=RED).move_to(node_u)
        node_a = Circle(radius=0.3, color=GREY).shift(RIGHT * 2 + DOWN * 1)
        node_b = Circle(radius=0.3, color=GREY).shift(RIGHT * 4 + DOWN * 1)
        
        lines = VGroup(Arrow(node_u.get_bottom(), node_a.get_top(), color=RED), Arrow(node_u.get_bottom(), node_b.get_top(), color=RED))
        label_conf = Text("Yếu tố nhiễu ẩn", font_size=18, color=RED).next_to(node_u, UP)

        self.play(Create(node_u), Write(label_u), Create(lines), FadeIn(node_a), FadeIn(node_b), Write(label_conf))
        self.play(Flash(node_u, color=RED))
        
        self.wait(2)


# --- Scene 031 ---
class Scene031(EduScene):
    def construct(self):
        title = self.create_title("Kết luận: mô hình thế giới nhân quả")
        formula = self.create_formula(r"\text{Perception + Causality = Causal World Model}")

        self.play(Write(title), FadeIn(formula, shift=UP))

        # 1. Integration
        perception = Circle(radius=1, color=BLUE, fill_opacity=0.2).shift(LEFT * 2)
        label_p = Text("Nhận thức", font_size=20).move_to(perception)
        
        causality = Circle(radius=1, color=TEAL, fill_opacity=0.2).shift(RIGHT * 2)
        label_c = Text("Nhân quả", font_size=20).move_to(causality)

        self.play(FadeIn(perception), Write(label_p))
        self.play(FadeIn(causality), Write(label_c))

        # 2. The Final Brain
        brain = VGroup(
            Ellipse(width=2, height=1.5, color=GOLD_A, fill_opacity=0.3),
            *[Line(ORIGIN, np.random.randn(3) * 0.5, color=GOLD_A, stroke_opacity=0.5) for _ in range(10)]
        ).shift(UP * 0.5)
        
        self.play(
            ReplacementTransform(perception, brain),
            ReplacementTransform(causality, brain),
            FadeOut(label_p),
            FadeOut(label_c),
            run_time=2
        )
        self.play(Indicate(brain, color=GOLD_A))
        
        thanks = Text("Cảm ơn đã theo dõi!", font_size=32, color=TITLE_YELLOW).shift(DOWN * 1.5)
        self.play(Write(thanks))
        
        self.wait(3)
