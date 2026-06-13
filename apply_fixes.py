import os

scenes_code = {}

scenes_code["scene_009"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_009/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Học không giám sát qua Reconstruction")
        
        formula = MathTex(r"\\hat{x} = \\sum_{k=1}^K m_k \\cdot \\hat{x}_k", font_size=54, color=GOLD_A).move_to(ORIGIN)
        self.wait(0.979)
        self.play(Write(formula), run_time=1.469)
        self.play(Flash(formula, color=GOLD_A), run_time=0.612)
        self.wait(5.508)
        self.play(FadeOut(formula), run_time=0.612)

        slot = FlowchartBlock(map_keyword_to_path("slots", "scene_009"), "Slot k", color=BLUE).shift(LEFT * 5)
        comp_x = FlowchartBlock(map_keyword_to_path("reconstruction", "scene_009"), "Component x_k", color=GREY).shift(LEFT * 1.5 + UP * 1)
        mask_m = FlowchartBlock(map_keyword_to_path("masking", "scene_009"), "Mask m_k", color=WHITE).shift(RIGHT * 2.5 + UP * 1)
        
        arrow1 = get_flow_arrow(slot, comp_x)
        arrow2 = get_flow_arrow(slot, mask_m)
        
        self.play(FadeIn(slot), run_time=0.979)
        self.play(Create(arrow1), Create(arrow2), FadeIn(comp_x), FadeIn(mask_m), run_time=1.836)
        self.wait(6.365)
        self.play(FadeOut(slot), FadeOut(arrow1), FadeOut(arrow2), run_time=0.612)

        dot_product = MathTex("\\times", font_size=48, color=GOLD_A).move_to(VGroup(comp_x, mask_m).get_center() + DOWN*1)
        self.play(Write(dot_product), run_time=0.979)
        
        reconstructed_img = FlowchartBlock(map_keyword_to_path("decoder", "scene_009"), "Reconstructed (x_hat)", color=GOLD_A).shift(DOWN * 1.5)
        
        self.play(
            ReplacementTransform(VGroup(comp_x, mask_m, dot_product), reconstructed_img),
            run_time=2.448
        )
        self.wait(6.977)
        self.play(FadeOut(reconstructed_img), run_time=0.612)

        loss_formula = MathTex(r"\\mathcal{L} = \\|x - \\hat{x}\\|^2", font_size=64, color=RED).move_to(ORIGIN)
        loss_label = safe_text("RECONSTRUCTION LOSS", 32, RED, weight=BOLD).next_to(loss_formula, UP, buff=0.5)
        
        self.play(Write(loss_label), run_time=1.224)
        self.play(FadeIn(loss_formula, shift=DOWN), run_time=1.469)
        
        opt_arrows = VGroup(
            Arrow(loss_formula.get_bottom(), DOWN*2.5 + LEFT*2, color=GOLD_A),
            Arrow(loss_formula.get_bottom(), DOWN*2.5 + RIGHT*2, color=GOLD_A)
        )
        opt_labels = VGroup(
            safe_text("Update Encoder", 18, GOLD_A).next_to(opt_arrows[0], DOWN),
            safe_text("Update Decoder", 18, GOLD_A).next_to(opt_arrows[1], DOWN)
        )
        
        self.play(Create(opt_arrows), Write(opt_labels), run_time=1.836)
        self.wait(2.291)
        self.wait(0.612)
"""

scenes_code["scene_010"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_010/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Sim-to-Real: Khoảng cách từ mô phỏng đến đời thực")
        
        formula = safe_text("Synthetic (Simple) -> Real World (Complex)", 36, GOLD_A).shift(UP * 0.5)
        self.wait(0.0)
        self.play(Write(formula), run_time=1.467)
        self.wait(2.812)
        self.play(FadeOut(formula), run_time=0.611)
        
        sim_block = FlowchartBlock(map_keyword_to_path("simulation", "scene_010"), "Simulation", color=GREY).shift(LEFT * 3 + DOWN * 0.5)
        self.play(FadeIn(sim_block), run_time=0.978)
        self.wait(1.222)
        self.wait(5.134)
        
        real_block = FlowchartBlock(map_keyword_to_path("real world", "scene_010"), "Real World (Shadows/Texture)", color=ACCENT_COLOR).shift(RIGHT * 3 + DOWN * 0.5)
        self.play(FadeIn(real_block), run_time=0.978)
        self.wait(1.834)
        self.wait(6.968)
        
        barrier = FlowchartBlock(map_keyword_to_path("generalization gap", "scene_010"), "Generalization Gap", color=RED).move_to(ORIGIN)
        self.play(FadeIn(barrier), run_time=1.222)
        self.wait(0.978)
        self.wait(5.134)
        
        bridge = get_flow_arrow(sim_block, real_block, color=GOLD_A)
        self.play(Create(bridge), run_time=1.467)
        self.play(Indicate(bridge, color=GOLD_A), run_time=1.222)
        self.wait(3.335)
        self.wait(1.222)
"""

scenes_code["scene_011"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_011/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Vision Transformer & DINO")
        
        formula = safe_text("Image -> ViT -> Semantic Features", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.485)
        self.wait(2.847)
        self.play(FadeOut(formula), run_time=0.619)
        
        raw_img = FlowchartBlock(map_keyword_to_path("image", "scene_011"), "Raw Image", color=GREY).shift(LEFT * 4 + DOWN * 0.5)
        vit_block = FlowchartBlock(map_keyword_to_path("vit", "scene_011"), "ViT", color=ACCENT_COLOR).shift(DOWN * 0.5)
        arrow1 = get_flow_arrow(raw_img, vit_block)
        
        self.play(FadeIn(raw_img, shift=RIGHT), run_time=1.238)
        self.play(Create(arrow1), FadeIn(vit_block), run_time=1.485)
        self.wait(4.704)
        
        dino_block = FlowchartBlock(map_keyword_to_path("dino features", "scene_011"), "DINO Features", color=GOLD_A).shift(RIGHT * 4 + DOWN * 0.5)
        arrow2 = get_flow_arrow(vit_block, dino_block)
        
        self.play(Create(arrow2), run_time=1.238)
        self.play(FadeIn(dino_block), run_time=1.857)
        self.wait(6.808)
        
        semantic_block = FlowchartBlock(map_keyword_to_path("semantic objects", "scene_011"), "Semantic Objects", color=GREEN).shift(RIGHT * 4 + UP * 2.5)
        arrow3 = get_flow_arrow(dino_block, semantic_block)
        
        self.play(FadeIn(semantic_block), Create(arrow3), run_time=1.485)
        self.play(Indicate(semantic_block, color=GOLD_A), run_time=1.238)
        self.wait(7.179)
        
        self.play(vit_block.animate.set_opacity(0.6), run_time=1.857)
        self.wait(2.48)
        self.wait(1.238)
"""

scenes_code["scene_012"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_012/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "DINOSAUR: Feature Reconstruction")
        
        formula = MathTex(r"L = \|F_{ViT} - F_{decoded}\|^2", font_size=42, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.455)
        self.wait(4.001)
        self.play(FadeOut(formula), run_time=0.606)
        
        pixel_grid = FlowchartBlock(map_keyword_to_path("image", "scene_012"), "Image", color=GREY_D).shift(LEFT * 4 + DOWN * 0.5)
        dino_feat = FlowchartBlock(map_keyword_to_path("vit encoder", "scene_012"), "ViT Encoder", color=GOLD_A).shift(LEFT * 1 + DOWN * 0.5)
        arrow1 = get_flow_arrow(pixel_grid, dino_feat)
        
        self.play(FadeIn(pixel_grid), run_time=0.97)
        self.play(Create(arrow1), run_time=0.728)
        self.play(FadeIn(dino_feat, shift=RIGHT), run_time=1.213)
        self.wait(6.79)
        
        feat_maps = FlowchartBlock(map_keyword_to_path("feature maps", "scene_012"), "Feature Maps", color=GREEN).shift(RIGHT * 3 + DOWN * 0.5)
        arrow2 = get_flow_arrow(dino_feat, feat_maps)
        
        self.play(FadeIn(feat_maps, shift=UP), Create(arrow2), run_time=1.213)
        self.play(Indicate(feat_maps), run_time=1.819)
        self.wait(7.881)
        
        slot_box = FlowchartBlock(map_keyword_to_path("slot attention", "scene_012"), "Slot Attention", color=ACCENT_COLOR).shift(RIGHT * 5 + DOWN * 0.5)
        arrow3 = get_flow_arrow(feat_maps, slot_box)
        
        self.wait(1.213)
        self.play(FadeIn(slot_box), run_time=1.455)
        self.play(Create(arrow3), run_time=1.213)
        self.wait(7.779)
        self.wait(1.213)
"""

scenes_code["scene_013"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_013/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Từ Đối tượng đến Mối quan hệ")
        
        formula = MathTex(r"r_{ij} = g(z_i, z_j)", font_size=48, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.201)
        self.wait(2.303)
        self.play(FadeOut(formula), run_time=0.501)
        
        obj1 = FlowchartBlock(map_keyword_to_path("objects", "scene_013"), "Object 1", color=BLUE).shift(LEFT * 3.4 + UP * 1.15)
        obj2 = FlowchartBlock(map_keyword_to_path("objects", "scene_013"), "Object 2", color=BLUE).shift(ORIGIN + UP * 0.35)
        obj3 = FlowchartBlock(map_keyword_to_path("objects", "scene_013"), "Object 3", color=BLUE).shift(RIGHT * 3.35 + DOWN * 0.55)
        
        self.play(FadeIn(obj1, shift=DOWN), run_time=0.801)
        self.play(FadeIn(obj2, shift=UP), run_time=0.801)
        self.play(FadeIn(obj3, shift=LEFT), run_time=1.001)
        self.wait(5.406)
        
        rel1 = get_flow_arrow(obj1, obj2, color=GOLD_A)
        rel2 = get_flow_arrow(obj2, obj3, color=ACCENT_COLOR)
        
        label1 = safe_text("Relationships", 20, GOLD_A).next_to(rel1.get_center(), UP, buff=0.2)
        
        self.play(Create(rel1), Write(label1), run_time=1.001)
        self.play(Create(rel2), run_time=1.001)
        self.wait(5.506)
        self.play(FadeOut(label1), run_time=0.501)
        
        gnn = FlowchartBlock(map_keyword_to_path("gnn", "scene_013"), "GNN", color=GOLD_A).shift(DOWN * 2)
        arrow_gnn = get_flow_arrow(obj2, gnn)
        semantic = FlowchartBlock(map_keyword_to_path("semantic context", "scene_013"), "Semantic Context", color=GREEN).next_to(gnn, RIGHT, buff=1.0)
        arrow_sem = get_flow_arrow(gnn, semantic)
        
        self.play(FadeIn(gnn), FadeIn(semantic), run_time=1.201)
        self.play(Create(arrow_gnn), Create(arrow_sem), run_time=1.001)
        self.play(Indicate(gnn, color=GOLD_A), run_time=1.001)
        self.wait(5.398)
        self.wait(7.761)
        self.wait(1.001)
"""

scenes_code["scene_014"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_014/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Correlation không phải Causation")
        
        formula = MathTex(r"P(Y | X)", font_size=54, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.236)
        self.wait(2.368)
        self.play(FadeOut(formula), run_time=0.515)
        
        stat_block = FlowchartBlock(map_keyword_to_path("statistical correlation", "scene_014"), "Statistical Correlation", color=BLUE).shift(LEFT * 2)
        
        self.play(FadeIn(stat_block), run_time=1.03)
        self.wait(1.545)
        self.wait(1.03)
        self.wait(3.604)
        
        spur_block = FlowchartBlock(map_keyword_to_path("spurious correlation", "scene_014"), "Spurious Correlation", color=ACCENT_COLOR).shift(RIGHT * 3 + UP * 1.5)
        arrow1 = get_flow_arrow(stat_block, spur_block, color=GOLD_A)
        
        self.play(Create(arrow1), FadeIn(spur_block), run_time=1.236)
        self.play(Indicate(spur_block, color=GOLD_A), run_time=1.03)
        self.wait(5.973)
        
        hidden_block = FlowchartBlock(map_keyword_to_path("hidden cause", "scene_014"), "Hidden Cause (Confounder)", color=RED).shift(RIGHT * 3 + DOWN * 1.5)
        arrow2 = get_flow_arrow(hidden_block, spur_block, is_feedback=True)
        
        self.play(FadeIn(hidden_block), run_time=1.03)
        self.play(Create(arrow2), run_time=1.03)
        self.wait(0.824)
        self.wait(0.515)
        self.wait(5.351)
        self.wait(6.352)
        self.wait(1.03)
"""

scenes_code["scene_015"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_015/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Can thiệp (Intervention)")
        
        formula = MathTex(r"P(Y | do(X = x))", font_size=54, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.201)
        self.wait(2.303)
        self.play(FadeOut(formula), run_time=0.501)
        
        inter_block = FlowchartBlock(map_keyword_to_path("intervention", "scene_015"), "Intervention", color=ORANGE).shift(LEFT * 3)
        do_op = FlowchartBlock(map_keyword_to_path("do(x) operator", "scene_015"), "do(X) operator", color=GOLD_A).shift(RIGHT * 3)
        arrow1 = get_flow_arrow(inter_block, do_op)
        
        self.play(FadeIn(inter_block), run_time=1.001)
        self.play(FadeIn(do_op), Create(arrow1), run_time=1.201)
        self.wait(5.807)
        
        cause_block = FlowchartBlock(map_keyword_to_path("cause-effect", "scene_015"), "Cause-Effect", color=BLUE).shift(DOWN * 2)
        arrow2 = get_flow_arrow(do_op, cause_block)
        
        self.play(Create(arrow2), run_time=0.501)
        self.play(FadeIn(cause_block), run_time=0.801)
        self.wait(1.001)
        self.wait(0.501)
        self.wait(1.502)
        self.wait(0.801)
        self.wait(4.906)
        
        discovery_block = FlowchartBlock(map_keyword_to_path("discovery", "scene_015"), "Discovery", color=GREEN).next_to(cause_block, RIGHT, buff=1.0)
        arrow3 = get_flow_arrow(cause_block, discovery_block)
        
        self.play(Create(arrow3), FadeIn(discovery_block), run_time=1.201)
        self.play(Indicate(discovery_block), run_time=1.001)
        self.wait(5.286)
        self.wait(7.304)
        self.wait(1.001)
"""

scenes_code["scene_016"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_016/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Quan sát vs Can thiệp")
        
        header = safe_text("Observation vs Intervention", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(header), run_time=1.213)
        self.wait(2.325)
        self.play(FadeOut(header), run_time=0.505)
        
        passive = FlowchartBlock(map_keyword_to_path("passive observation", "scene_016"), "Passive Observation", color=GREY).shift(LEFT * 3)
        
        self.play(FadeIn(passive), run_time=0.809)
        self.wait(0.809)
        self.wait(4.043)
        self.wait(2.426)
        self.play(FadeOut(passive), run_time=0.5)
        
        active = FlowchartBlock(map_keyword_to_path("active interaction", "scene_016"), "Active Interaction", color=ACCENT_COLOR).shift(RIGHT * 3)
        
        self.play(FadeIn(active), run_time=0.809)
        self.wait(0.809)
        self.wait(1.516)
        self.wait(2.022)
        self.wait(0.505)
        self.wait(2.426)
        
        self.play(FadeOut(active), run_time=0.607)
        real_intel = FlowchartBlock(map_keyword_to_path("real intelligence", "scene_016"), "Real Intelligence", color=GOLD_A).move_to(ORIGIN)
        
        self.play(FadeIn(real_intel), run_time=1.213)
        self.play(Indicate(real_intel, color=GOLD_A), run_time=1.011)
        self.wait(6.033)
        self.wait(7.278)
        self.wait(1.011)
"""

scenes_code["scene_017"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_017/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Mô hình Nhân quả Cấu trúc (SCM)")
        
        formula = MathTex(r"X_i = f_i(PA_i, U_i)", font_size=54, color=GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.201)
        self.wait(3.803)
        
        parents = FlowchartBlock(map_keyword_to_path("parents", "scene_017"), "Parents (Cause Nodes)", color=ACCENT_COLOR).shift(LEFT * 3 + DOWN * 1.5)
        noise = FlowchartBlock(map_keyword_to_path("noise", "scene_017"), "Noise (U)", color=MAROON_B).shift(RIGHT * 3 + DOWN * 1.5)
        
        self.play(FadeIn(parents, shift=UP), run_time=1.001)
        self.play(FadeIn(noise, shift=UP), run_time=1.001)
        self.wait(6.004)
        
        self.play(FadeOut(VGroup(parents, noise, formula)), run_time=0.5)
        
        scm = FlowchartBlock(map_keyword_to_path("scm", "scene_017"), "SCM", color=GOLD_A).shift(UP * 1.5)
        effect = FlowchartBlock(map_keyword_to_path("effect nodes", "scene_017"), "Effect Nodes", color=GREEN).shift(DOWN * 1.5)
        arrow = get_flow_arrow(scm, effect)
        
        self.play(FadeIn(scm), run_time=1.201)
        self.play(Create(arrow), FadeIn(effect), run_time=1.501)
        self.wait(5.804)
        
        self.play(Indicate(effect, color=GOLD_A), run_time=1.001)
        self.wait(1.001)
        self.wait(5.292)
        self.wait(7.277)
        self.wait(1.001)
"""

scenes_code["scene_018"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_018/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Chuỗi nhân quả vật lý")
        
        formula = safe_text("Ball -> Force -> Box", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.31)
        self.wait(2.511)
        self.play(FadeOut(formula), run_time=0.546)
        
        physics = FlowchartBlock(map_keyword_to_path("physics collision", "scene_018"), "Physics Collision", color=BLUE).shift(LEFT * 4)
        self.wait(0.873)
        self.play(FadeIn(physics, shift=RIGHT), run_time=1.31)
        self.wait(4.366)
        
        force = FlowchartBlock(map_keyword_to_path("force", "scene_018"), "Force", color=ORANGE).shift(ORIGIN)
        arrow1 = get_flow_arrow(physics, force)
        
        self.play(Create(arrow1), run_time=0.873)
        self.wait(1.637)
        self.play(FadeIn(force), run_time=0.873)
        self.wait(1.31)
        self.wait(2.947)
        
        chain = FlowchartBlock(map_keyword_to_path("causal chain", "scene_018"), "Causal Chain", color=GREEN).shift(RIGHT * 4)
        arrow2 = get_flow_arrow(force, chain)
        
        self.play(Create(arrow2), FadeIn(chain, shift=DOWN), run_time=1.637)
        self.play(Indicate(chain, color=GOLD_A), run_time=1.092)
        self.wait(6.859)
        self.wait(7.047)
        self.wait(1.092)
"""

scenes_code["scene_019"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_019/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Quy luật vật lý là Cơ chế ổn định")
        
        formulas = VGroup(
            MathTex(r"F = m \cdot a", font_size=48, color=GOLD_A),
            MathTex(r"\Delta p = F \cdot \Delta t", font_size=48, color=ACCENT_COLOR)
        ).arrange(DOWN, buff=0.5).shift(UP * 0.5)
        
        self.play(Write(formulas[0]), run_time=0.998)
        self.play(Write(formulas[1]), run_time=0.998)
        self.wait(1.995)
        self.play(FadeOut(formulas), run_time=0.399)
        
        force = FlowchartBlock(map_keyword_to_path("force", "scene_019"), "Force", color=ORANGE).shift(LEFT * 3)
        momentum = FlowchartBlock(map_keyword_to_path("momentum", "scene_019"), "Momentum", color=BLUE).shift(RIGHT * 3)
        arrow1 = get_flow_arrow(force, momentum)
        
        self.play(FadeIn(force), FadeIn(momentum), run_time=0.998)
        self.wait(0.998)
        self.play(Create(arrow1), run_time=1.197)
        self.play(Indicate(force, color=GOLD_A), run_time=0.798)
        self.wait(3.991)
        
        invariance = FlowchartBlock(map_keyword_to_path("invariance", "scene_019"), "Invariance", color=GREEN).shift(DOWN * 2)
        arrow2 = get_flow_arrow(momentum, invariance)
        
        self.wait(1.197)
        self.play(Create(arrow2), run_time=0.798)
        self.play(FadeIn(invariance), run_time=1.497)
        self.wait(5.687)
        
        stable = FlowchartBlock(map_keyword_to_path("stable mechanisms", "scene_019"), "Stable Mechanisms", color=GOLD_A).shift(UP * 2)
        
        self.play(FadeOut(VGroup(force, momentum, invariance, arrow1, arrow2)), run_time=0.499)
        self.play(FadeIn(stable, shift=DOWN), run_time=1.497)
        self.play(Indicate(stable, color=GOLD_A), run_time=0.998)
        self.wait(4.705)
        self.wait(6.154)
        self.wait(0.998)
"""

scenes_code["scene_020"] = """from __future__ import annotations
from manim import *
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from visual_beats import safe_text
from flowchart_style import FlowchartBlock, get_flow_arrow, setup_flowchart_scene
from image_map import map_keyword_to_path

class GeneratedVideo(Scene):
    def construct(self):
        audio_path = "output/scenes/scene_020/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
            
        GOLD_A = "#F2C94C"
        ACCENT_COLOR = "#3A86FF"
        TEXT_COLOR = "#E6EDF3"
        
        title = setup_flowchart_scene(self, "Tại sao cần Slots cho Nhân quả?")
        
        formula = safe_text("Slots -> Causal Graph -> Prediction", 36, GOLD_A).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.17)
        self.wait(2.243)
        self.play(FadeOut(formula), run_time=0.488)
        
        slots = FlowchartBlock(map_keyword_to_path("slots", "scene_020"), "Slots (Decomposition)", color=BLUE).shift(LEFT * 3)
        causal = FlowchartBlock(map_keyword_to_path("causal graph", "scene_020"), "Causal Graph", color=ACCENT_COLOR).shift(RIGHT * 3)
        arrow1 = get_flow_arrow(slots, causal)
        
        self.play(FadeIn(slots, shift=RIGHT), FadeIn(causal, shift=LEFT), run_time=0.975)
        self.play(Create(arrow1), run_time=0.975)
        self.wait(5.851)
        
        obj_causal = FlowchartBlock(map_keyword_to_path("object-level causality", "scene_020"), "Object-level Causality", color=GOLD_A).shift(DOWN * 2)
        arrow2 = get_flow_arrow(causal, obj_causal)
        
        self.wait(0.78)
        self.wait(0.585)
        self.play(Create(arrow2), FadeIn(obj_causal), run_time=1.17)
        self.wait(5.266)
        
        self.play(FadeOut(VGroup(slots, causal, arrow1, arrow2)), run_time=0.488)
        
        self.play(Indicate(obj_causal, color=GOLD_A), run_time=1.463)
        self.wait(0.975)
        self.wait(7.692)
        self.wait(6.998)
        self.wait(0.975)
"""

import os
base_path = "manim-video-builder/manim_scenes"
for scene_name, code in scenes_code.items():
    file_path = os.path.join(base_path, f"{scene_name}.py")
    with open(file_path, "w") as f:
        f.write(code)
    print(f"Updated {file_path}")
