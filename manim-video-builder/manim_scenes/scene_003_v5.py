from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene003(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_003/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        title = create_title("Representation là gì?")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        formula_panel = create_formula_panel("z = f_theta(X)")
        self.play(FadeIn(formula_panel, shift=UP*0.2), run_time=1.0)

        image_x = create_entity_box('pixels', 'Tensor ảnh X', color=COLOR_WARNING).shift(LEFT * 4.1 + UP * 0.25)
        encoder = create_entity_box('ai', 'Máy nén\nf_theta', color=COLOR_AI).shift(LEFT * 0.75 + UP * 0.25)
        vector_z = create_entity_box('vector', 'Vector z', color=COLOR_RESULT).shift(RIGHT * 3.2 + UP * 0.25)
        flow = VGroup(image_x, encoder, vector_z)
        if flow.width > 11.6:
            flow.scale_to_fit_width(11.6)
        a1 = create_flow_arrow(image_x, encoder)
        a2 = create_flow_arrow(encoder, vector_z)

        self.play(FadeIn(image_x, shift=UP*0.2), run_time=0.8)
        sync_to(5.2)
        self.play(GrowArrow(a1), FadeIn(encoder, shift=UP*0.2), run_time=1.0)
        sync_to(10.2)
        self.play(GrowArrow(a2), FadeIn(vector_z, shift=LEFT*0.2), run_time=1.0)
        sync_to(15.4)

        pixel_cloud = VGroup(*[
            Square(0.16, stroke_width=1, color=COLOR_WARNING, fill_opacity=0.22)
            for _ in range(48)
        ]).arrange_in_grid(6, 8, buff=0.03).move_to(image_x.box)
        compressed_nums = VGroup(*[
            Text(f"{v:.1f}", font_size=13, color=COLOR_RESULT)
            for v in [0.8, -0.2, 1.4, 0.1, 2.0, -0.7, 0.5, 1.1]
        ]).arrange(DOWN, buff=0.05).move_to(vector_z.box)
        compression_label = create_text_box("Nén triệu điểm ảnh\nthành chuỗi số", font_size=19, color=COLOR_MATH, width=3.2).shift(UP * 1.65)

        self.play(TransformFromCopy(image_x.box, pixel_cloud), FadeIn(compression_label, shift=UP*0.2), run_time=1.2)
        self.play(ReplacementTransform(pixel_cloud, compressed_nums), Indicate(encoder, color=COLOR_AI), run_time=1.6)
        sync_to(21.04)
        self.play(
            FadeOut(compression_label),
            FadeOut(compressed_nums),
            FadeOut(image_x),
            FadeOut(encoder),
            FadeOut(vector_z),
            FadeOut(a1),
            FadeOut(a2),
            run_time=0.55,
        )

        car = create_entity_box('car', 'Ảnh chiếc xe', color=COLOR_USER).shift(LEFT * 3.9 + DOWN * 0.65)
        traits = VGroup(
            create_text_box("Hình dáng", font_size=18, color=COLOR_USER, width=2.0),
            create_text_box("Màu sắc", font_size=18, color=COLOR_RESULT, width=2.0),
            create_text_box("Vị trí", font_size=18, color=COLOR_MATH, width=2.0),
            create_text_box("Hướng đi", font_size=18, color=COLOR_WARNING, width=2.0),
        ).arrange_in_grid(2, 2, buff=(0.32, 0.34)).shift(RIGHT * 2.2 + DOWN * 0.65)
        trait_arrows = VGroup(*[create_clean_arrow(car, t, color=t.box.get_color(), direction=RIGHT, buff=0.22) for t in traits])

        self.play(FadeIn(car, shift=RIGHT*0.2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.15) for t in traits], lag_ratio=0.18), run_time=1.4)
        self.play(LaggedStart(*[GrowArrow(a) for a in trait_arrows], lag_ratio=0.12), run_time=1.2)
        sync_to(30.26)
        self.play(
            Indicate(traits[0], color=COLOR_USER),
            Indicate(traits[1], color=COLOR_RESULT),
            Indicate(traits[2], color=COLOR_MATH),
            Indicate(traits[3], color=COLOR_WARNING),
            run_time=2.0
        )

        self.play(FadeOut(car), FadeOut(traits), FadeOut(trait_arrows), run_time=0.45)

        cnn_layers = VGroup(*[
            RoundedRectangle(width=0.28, height=1.1 + i*0.12, corner_radius=0.05, stroke_width=2, color=COLOR_AI, fill_opacity=0.12)
            for i in range(6)
        ]).arrange(RIGHT, buff=0.12).move_to(UP * 0.2)
        cnn_text = create_text_box("Tầng nơ ron chập\nlọc đặc trưng bất biến", font_size=17, color=COLOR_AI, width=3.5).next_to(cnn_layers, DOWN, buff=0.15)
        self.play(FadeIn(cnn_layers, shift=UP*0.2), FadeIn(cnn_text, shift=UP*0.2), run_time=1.1)
        self.play(LaggedStart(*[Indicate(layer, color=COLOR_AI) for layer in cnn_layers], lag_ratio=0.08), run_time=1.8)

        sync_to(37.752)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
