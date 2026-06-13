from pathlib import Path

from manim import *

# ─── COLOR PALETTE (3Blue1Brown Style) ───────────────
BG_COLOR = "#06111f"
TEXT_COLOR = "#e0e0e0"
HIGHLIGHT_COLOR = YELLOW_D
ACCENT_COLOR = TEAL_C
SECONDARY_ACCENT = MAROON_C
BLUE_COLOR = BLUE_C

config.background_color = BG_COLOR
VIETNAMESE_FONT_FILE = Path(__file__).with_name("NotoSans-Regular.ttf")
VIETNAMESE_FONT = "Noto Sans"

config.font = VIETNAMESE_FONT

ManimText = Text

def Text(text, *args, **kwargs):
    """Render text with the bundled Vietnamese-capable font."""
    kwargs.setdefault("font", VIETNAMESE_FONT)
    if VIETNAMESE_FONT_FILE.exists():
        with register_font(VIETNAMESE_FONT_FILE):
            return ManimText(text, *args, **kwargs)
    return ManimText(text, *args, **kwargs)

def create_title_and_bullets(scene_obj, title_text, bullets_text):
    """Utility to create a title and animated bullet points"""
    import textwrap
    wrapped_title = "\n".join(textwrap.wrap(title_text, width=40))
    title = Text(wrapped_title, font_size=40, weight=BOLD, color=HIGHLIGHT_COLOR)
    title.to_edge(UP)
    
    bullets = VGroup()
    for text in bullets_text:
        wrapped_bullet = "\n".join(textwrap.wrap(f"• {text}", width=55))
        bullet = Text(wrapped_bullet, font_size=28, color=TEXT_COLOR, line_spacing=1.0)
        bullets.add(bullet)
    
    bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    bullets.next_to(title, DOWN, buff=1.0)
    bullets.set_x(-4)

    scene_obj.play(FadeIn(title, shift=UP))
    scene_obj.wait(0.5)

    for bullet in bullets:
        scene_obj.play(FadeIn(bullet, shift=RIGHT))
        scene_obj.wait(1.0)
        
    scene_obj.wait(2.0)
    # FADE OUT REMOVED so the frame freezes and stretches over audio length

def create_centered_text(scene_obj, text_content):
    """Utility to show big centered text"""
    t = Text(text_content, font_size=48, color=ACCENT_COLOR, weight=BOLD)
    scene_obj.play(Write(t))
    scene_obj.wait(2)
    scene_obj.play(FadeOut(t))

def fit_mobject(mobject, max_width, max_height):
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject

def safe_text(text_content, font_size=20, color=WHITE, max_width=None, max_height=None, weight="NORMAL"):
    t = Text(text_content, font_size=font_size, color=color, weight=weight)
    if max_width is not None and t.width > max_width:
        t.scale_to_fit_width(max_width)
    if max_height is not None and t.height > max_height:
        t.scale_to_fit_height(max_height)
    return t

def labeled_box(text_content, width=2.2, height=1.0, color=BLUE_COLOR, fill_opacity=0.18,
                font_size=20, text_color=WHITE):
    box = Rectangle(width=width, height=height, color=color, stroke_width=2)
    box.set_fill(color, opacity=fill_opacity)
    label = safe_text(text_content, font_size=font_size, color=text_color,
                      max_width=width - 0.25, max_height=height - 0.2)
    label.move_to(box.get_center())
    return VGroup(box, label)

def title_mob(title_text):
    return safe_text(title_text, font_size=40, color=HIGHLIGHT_COLOR,
                     weight=BOLD, max_width=12.5).to_edge(UP)

def caption_mob(text_content):
    return safe_text(text_content, font_size=22, color=ACCENT_COLOR,
                     max_width=12.5).to_edge(DOWN).shift(UP * 0.35)

def play_diagram(scene_obj, title_text, diagram, caption_text=None, run_time=1.8):
    title = title_mob(title_text)
    fit_mobject(diagram, 12.4, 5.5)
    diagram.move_to(ORIGIN).shift(DOWN * 0.1)
    scene_obj.play(FadeIn(title, shift=UP))
    scene_obj.play(FadeIn(diagram, shift=UP * 0.2), run_time=run_time)
    if caption_text:
        caption = caption_mob(caption_text)
        scene_obj.play(Write(caption))
    scene_obj.wait(2)

def feature_grid(rows=3, cols=3, cell=0.28, color=PURPLE, fill_opacity=0.65):
    grid = VGroup(*[
        Square(side_length=cell, stroke_color=WHITE, stroke_width=1)
        .set_fill(color, opacity=fill_opacity)
        for _ in range(rows * cols)
    ])
    grid.arrange_in_grid(rows, cols, buff=0.04)
    return grid

def slot_stack(labels=None, colors=None, radius=0.28):
    labels = labels or ["s1", "s2", "s3"]
    colors = colors or [RED_C, GREEN_C, BLUE_C, YELLOW_C]
    slots = VGroup()
    for i, label_text in enumerate(labels):
        slot = Circle(radius=radius, color=colors[i % len(colors)], stroke_width=2)
        slot.set_fill(colors[i % len(colors)], opacity=0.45)
        label = safe_text(label_text, font_size=14, max_width=radius * 1.4, max_height=radius * 1.0)
        label.move_to(slot)
        slots.add(VGroup(slot, label))
    slots.arrange(DOWN, buff=0.12)
    return slots

def simple_image(width=1.45, height=1.05):
    frame = Rectangle(width=width, height=height, color=TEAL_C, stroke_width=2)
    frame.set_fill(TEAL_E, opacity=0.28)
    sun = Circle(radius=0.12, color=YELLOW, fill_opacity=0.85).move_to(
        frame.get_corner(UR) + LEFT * 0.28 + DOWN * 0.22
    )
    hill = Polygon(
        frame.get_corner(DL) + RIGHT * 0.05,
        frame.get_bottom() + RIGHT * width * 0.1 + UP * 0.45,
        frame.get_corner(DR) + LEFT * 0.05,
        color=GREEN_C,
    ).set_fill(GREEN_E, opacity=0.65)
    obj = Circle(radius=0.18, color=RED_C, fill_opacity=0.8).move_to(frame.get_center() + LEFT * 0.28)
    return VGroup(frame, hill, sun, obj)

def mini_face(scale=1.0):
    head = Circle(radius=0.55 * scale, color=YELLOW_D, stroke_width=2).set_fill("#d9a66a", opacity=0.25)
    left_eye = Circle(radius=0.05 * scale, color=WHITE, fill_opacity=1).shift(LEFT * 0.18 * scale + UP * 0.12 * scale)
    right_eye = left_eye.copy().shift(RIGHT * 0.36 * scale)
    mouth = Arc(radius=0.22 * scale, start_angle=PI, angle=PI, color=RED_C).shift(DOWN * 0.13 * scale)
    return VGroup(head, left_eye, right_eye, mouth)

def checkmark_vector(color=GREEN_C, stroke_width=4, size=0.25):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        [-0.7 * size, -0.2 * size, 0],
        [-0.2 * size, -0.7 * size, 0],
        [0.7 * size, 0.7 * size, 0]
    ])
    return checkmark

def crossmark_vector(color=RED_C, stroke_width=4, size=0.25):
    cross = VGroup(
        Line([-0.7 * size, 0.7 * size, 0], [0.7 * size, -0.7 * size, 0], color=color, stroke_width=stroke_width),
        Line([-0.7 * size, -0.7 * size, 0], [0.7 * size, 0.7 * size, 0], color=color, stroke_width=stroke_width)
    )
    return cross

def pipeline(nodes, colors=None, buff=0.45):
    colors = colors or [TEAL_C, BLUE_C, MAROON_C, GREEN_C, PURPLE_C]
    groups = VGroup()
    for i, node in enumerate(nodes):
        groups.add(labeled_box(node, width=1.75, height=0.82, color=colors[i % len(colors)], font_size=17))
    groups.arrange(RIGHT, buff=buff)
    arrows = VGroup(*[
        Arrow(groups[i].get_right(), groups[i + 1].get_left(), buff=0.08, color=GREY_B)
        for i in range(len(groups) - 1)
    ])
    return VGroup(groups, arrows)

class S6_01_CNNFailure(Scene):
    def construct(self):
        # [AUDIO]: "Slot Attention ban đầu sử dụng một bộ encoder CNN nhỏ với 4 convolutional layer để trích xuất feature từ ảnh đầu vào."
        title = Text("Tại sao Encoder CNN cũ thất bại?", font_size=40, weight=BOLD, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(FadeIn(title, shift=UP))

        # Vẽ 4 layer CNN stacked
        cnn_layers = VGroup()
        layer_colors = [BLUE_C, BLUE_D, BLUE_E, BLUE_E]
        layer_widths = [1.6, 1.3, 1.0, 0.7]
        for i in range(4):
            layer = Rectangle(width=layer_widths[i], height=0.55, color=layer_colors[i], stroke_width=2).set_fill(layer_colors[i], opacity=0.35)
            cnn_layers.add(layer)
        cnn_layers.arrange(RIGHT, buff=0.12)
        cnn_border = SurroundingRectangle(cnn_layers, color=BLUE_COLOR, buff=0.2)
        cnn_label = Text("CNN Encoder (4 layers)", font_size=22, color=TEXT_COLOR).next_to(cnn_border, DOWN, buff=0.15)
        cnn_group = VGroup(cnn_layers, cnn_border, cnn_label).move_to(ORIGIN)

        self.play(FadeIn(cnn_border), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(layer, shift=RIGHT * 0.3) for layer in cnn_layers], lag_ratio=0.2), run_time=1)
        self.play(Write(cnn_label))
        self.wait(1)

        # [AUDIO]: "Phương pháp này hoạt động tốt trên các tập dữ liệu synthetic như CLEVR và Multi-dSprites..."
        self.play(cnn_group.animate.scale(0.7).shift(UP * 0.1), run_time=0.8)

        # Input CLEVR
        clevr_label = Text("Synthetic (CLEVR)", font_size=20, color=GREEN_C).shift(LEFT * 4.5 + UP * 2.8)
        circle_obj = Circle(radius=0.4, color=RED_C, fill_opacity=0.9)
        square_obj = Square(side_length=0.65, color=GREEN_C, fill_opacity=0.9).next_to(circle_obj, RIGHT, buff=0.2)
        clevr_objs = VGroup(circle_obj, square_obj).next_to(clevr_label, DOWN, buff=0.3)

        self.play(FadeIn(clevr_label), FadeIn(clevr_objs, shift=DOWN * 0.3))
        arr_in = Arrow(clevr_objs.get_right(), cnn_group.get_left(), buff=0.15, color=GREY_B)
        self.play(GrowArrow(arr_in))

        masks_good = VGroup(
            Circle(radius=0.4, color=WHITE, stroke_width=2).set_fill(RED_C, opacity=0.75),
            Square(side_length=0.65, color=WHITE, stroke_width=2).set_fill(GREEN_C, opacity=0.75)
        ).arrange(RIGHT, buff=0.3).shift(RIGHT * 4 + UP * 1)
        arr_out = Arrow(cnn_group.get_right(), masks_good.get_left(), buff=0.15, color=GREY_B)
        good_label = Text("Phân tách tốt", font_size=20, color=GREEN_C).next_to(masks_good, DOWN, buff=0.15)
        
        self.play(GrowArrow(arr_out))
        self.play(FadeIn(masks_good, shift=RIGHT * 0.3), Write(good_label))
        self.wait(1)

        # [AUDIO]: "...nhưng khi áp dụng lên dữ liệu thực tế, kết quả hoàn toàn thất bại. Mô hình không thể phân tách các object và tạo ra mask không có ý nghĩa."
        real_label = Text("Dữ liệu thực tế", font_size=20, color=RED_C).shift(LEFT * 4.5 + DOWN * 0.5)
        real_img = simple_image().scale(1.2).next_to(real_label, DOWN, buff=0.3)

        self.play(FadeIn(real_label), FadeIn(real_img, shift=DOWN * 0.3))
        arr_in2 = Arrow(real_img.get_right(), cnn_group.get_left() + DOWN * 0.7, buff=0.15, color=GREY_B)
        self.play(GrowArrow(arr_in2))

        # Broken striped masks animation
        bad_mask_bg = Rectangle(width=1.5, height=1.2, color=WHITE, stroke_width=2)
        stripes = VGroup(*[Line(bad_mask_bg.get_left() + UP * k * 0.17, bad_mask_bg.get_right() + UP * k * 0.17, color=GREY_C, stroke_width=2) for k in range(-3, 4)])
        bad_mask_group = VGroup(bad_mask_bg, stripes).shift(RIGHT * 4 + DOWN * 1.2)
        arr_out2 = Arrow(cnn_group.get_right(), bad_mask_group.get_left(), buff=0.15, color=GREY_B)
        bad_label = Text("Mask vô nghĩa", font_size=20, color=RED_C).next_to(bad_mask_group, DOWN, buff=0.15)

        self.play(GrowArrow(arr_out2))
        self.play(FadeIn(bad_mask_group, shift=RIGHT * 0.3), Write(bad_label))
        self.play(bad_mask_group.animate.set_color(RED_C), rate_func=there_and_back, run_time=1)
        self.wait(3)

        # Cleanup phase 1 & 2
        phase2_all = VGroup(clevr_label, clevr_objs, arr_in, arr_out, masks_good, good_label,
                            real_label, real_img, arr_in2, arr_out2, bad_mask_group, bad_label, cnn_group)
        self.play(FadeOut(phase2_all))

        # [AUDIO]: "Nguyên nhân cốt lõi: pixel reconstruction tạo ra signal quá yếu cho object-centricness. Mô hình tập trung vào các low-level features như thống kê màu sắc và texture, thay vì phát hiện object thực sự."
        cause_title = Text("Nguyên nhân: Pixel Reconstruction tạo signal quá yếu", font_size=32, weight=BOLD, color=YELLOW).next_to(title, DOWN, buff=0.6)
        self.play(Write(cause_title))
        
        low_level_box = labeled_box("Low-level features (Màu sắc, Texture)", width=4.5, height=1.5, color=RED_C, font_size=20).shift(LEFT * 3)
        high_level_box = labeled_box("Object Structure (Cấu trúc vật thể)", width=4.5, height=1.5, color=GREEN_C, font_size=20).shift(RIGHT * 3)
        
        self.play(FadeIn(low_level_box), FadeIn(high_level_box))
        
        # Mũi tên chỉ sự lệch hướng của mô hình
        cnn_focus = Text("CNN Focus", font_size=18, color=RED_C, weight=BOLD).next_to(low_level_box, UP)
        cross_mark = crossmark_vector(color=RED_C, size=0.4).move_to(high_level_box)
        
        self.play(Write(cnn_focus), low_level_box[0].animate.set_fill(RED_C, opacity=0.4))
        self.play(FadeIn(cross_mark, scale=1.5))
        self.wait(8)

        # [AUDIO]: "Trên dataset synthetic, object được phân biệt bằng màu sắc rõ ràng."
        self.play(FadeOut(low_level_box), FadeOut(high_level_box), FadeOut(cnn_focus), FadeOut(cross_mark))

        synth_demo = VGroup(
            Circle(radius=0.6, color=RED_C).set_fill(RED_C, opacity=1),
            Text("Màu sắc rõ ràng", font_size=18, color=GREEN_C).next_to(ORIGIN, DOWN, buff=0.8)
        ).shift(LEFT * 4)
        
        self.play(FadeIn(synth_demo))
        self.wait(1)

        # [AUDIO]: "Nhưng trên dữ liệu thực tế, hai object khác nhau có thể có màu tương tự do ánh sáng, bóng đổ, và occlusion."
        # Minigame minh hoạ Ánh sáng / Bóng đổ / Occlusion
        real_demo_title = Text("Dữ liệu thực tế", font_size=22, color=RED_C).shift(RIGHT * 2 + UP * 1.5)
        self.play(Write(real_demo_title))

        # 1. Ánh sáng / Bóng đổ (Một quả bóng bị chia nửa sáng tối)
        light_shadow_group = VGroup()
        ball_light = Arc(start_angle=-PI/2, angle=PI, radius=0.6, color=YELLOW_C).set_fill(YELLOW_C, opacity=1)
        ball_shadow = Arc(start_angle=PI/2, angle=PI, radius=0.6, color=YELLOW_E).set_fill(YELLOW_E, opacity=1)
        ball = VGroup(ball_light, ball_shadow)
        ls_label = Text("Ánh sáng & Bóng đổ", font_size=16, color=GREY_B).next_to(ball, DOWN)
        light_shadow_group.add(ball, ls_label).shift(RIGHT * 0.5)

        # 2. Occlusion (Che khuất làm màu hòa vào nhau)
        occlusion_group = VGroup()
        obj_back = Square(side_length=1.0, color=BLUE_E).set_fill(BLUE_E, opacity=1)
        obj_front = Circle(radius=0.5, color=BLUE_C).set_fill(BLUE_C, opacity=1).shift(RIGHT * 0.3 + DOWN * 0.3)
        occ_label = Text("Occlusion (Che khuất)", font_size=16, color=GREY_B).next_to(obj_back, DOWN, buff=0.45)
        occlusion_group.add(obj_back, obj_front, occ_label).shift(RIGHT * 4)

        self.play(FadeIn(light_shadow_group), FadeIn(occlusion_group))
        
        # Chỉ ra CNN cắt nhầm
        cut_line = DashedLine(ball.get_top() + UP*0.2, ball.get_bottom() + DOWN*0.2, color=RED_C)
        err_txt1 = Text("CNN tách làm 2", font_size=14, color=RED_C).next_to(cut_line, UP)
        
        merge_circle = Circle(radius=0.8, color=RED_C, stroke_width=3).move_to(obj_back.get_center() + RIGHT * 0.15 + DOWN * 0.15)
        err_txt2 = Text("CNN gộp làm 1", font_size=14, color=RED_C).next_to(merge_circle, UP)

        self.play(Create(cut_line), Write(err_txt1))
        self.play(Create(merge_circle), Write(err_txt2))
        self.wait(5)

        # [AUDIO]: "Nhóm DINOSAUR đã thử nghiệm với ViT-B/16 encoder theo ba chế độ..."
        self.play(FadeOut(synth_demo), FadeOut(real_demo_title), FadeOut(light_shadow_group), FadeOut(occlusion_group), FadeOut(cut_line), FadeOut(err_txt1), FadeOut(merge_circle), FadeOut(err_txt2))

        exp_title = Text("Thí nghiệm với ViT-B/16", font_size=28, weight=BOLD, color=ACCENT_COLOR).move_to(cause_title.get_center())
        self.play(ReplacementTransform(cause_title, exp_title))

        # [AUDIO]: "...training from scratch khiến training bị diverge hoàn toàn..."
        box_scratch = labeled_box("From Scratch", width=2.5, height=1.2, color=GREY_B, font_size=18).shift(LEFT * 3.5 + UP * 0.5)
        div_arrow = Arrow(box_scratch.get_bottom(), box_scratch.get_bottom() + DOWN * 0.8, color=RED_C)
        div_text = Text("Diverge (Phân kỳ)", font_size=16, color=RED_C).next_to(div_arrow, DOWN)
        
        self.play(FadeIn(box_scratch))
        self.play(GrowArrow(div_arrow), Write(div_text))
        self.play(Wiggle(div_arrow))

        # [AUDIO]: "...frozen DINO weights tạo ra các mask dạng sọc không có ý nghĩa..."
        box_frozen = labeled_box("Frozen DINO", width=2.5, height=1.2, color=BLUE_C, font_size=18).shift(UP * 0.5)
        striped_mask = VGroup(Rectangle(width=1.0, height=0.8, color=WHITE), *[Line(LEFT*0.5 + UP*k*0.15, RIGHT*0.5 + UP*k*0.15, color=GREY_C) for k in range(-2, 3)])
        striped_mask.next_to(box_frozen, DOWN, buff=0.5)
        s_text = Text("Mask dạng sọc", font_size=16, color=RED_C).next_to(striped_mask, DOWN)

        self.play(FadeIn(box_frozen))
        self.play(FadeIn(striped_mask, shift=UP*0.2), Write(s_text))

        # [AUDIO]: "...và finetuning DINO weights cũng thất bại tương tự."
        box_fine = labeled_box("Finetuning", width=2.5, height=1.2, color=TEAL_C, font_size=18).shift(RIGHT * 3.5 + UP * 0.5)
        fail_cross = crossmark_vector(color=RED_C, size=0.4).next_to(box_fine, DOWN, buff=0.8)
        f_text = Text("Thất bại tương tự", font_size=16, color=RED_C).next_to(fail_cross, DOWN)

        self.play(FadeIn(box_fine))
        self.play(FadeIn(fail_cross, scale=1.5), Write(f_text))
        self.wait(1.5)

        # [AUDIO]: "Cả ba đều chứng tỏ image reconstruction không cung cấp đủ signal để tạo ra semantic grouping."
        conclusion_text = Text("Kết luận: Image reconstruction KHÔNG ĐỦ SIGNAL cho semantic grouping", font_size=24, color=YELLOW, weight=BOLD).to_edge(DOWN).shift(UP * 0.2)
        
        self.play(Write(conclusion_text))
        self.wait(3)

class S6_02_FeatureReconstruction(Scene):
    def construct(self):
        title = Text("Tầm nhìn mới: Feature Reconstruction", font_size=40, weight=BOLD, color=HIGHLIGHT_COLOR)
        title.to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Nếu pixel reconstruction quá yếu, thì signal nào đủ mạnh? 
        # Câu trả lời đến từ Self-Supervised Learning."
        # ══════════════════════════════════════════════════════════════════════
        q_text = Text("Signal nào đủ mạnh?", font_size=32, color=TEXT_COLOR).shift(UP * 1.5)
        ssl_text = Text("Self-Supervised Learning (SSL)", font_size=36, color=GREEN_C, weight=BOLD).next_to(q_text, DOWN, buff=0.4)
        
        self.play(Write(q_text))
        self.wait(2)
        self.play(FadeIn(ssl_text, shift=UP*0.2))
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Các thuật toán SSL như DINO, MoCo-v3, MAE đã chứng minh chúng 
        # có thể học powerful representations từ hình ảnh một cách unsupervised, 
        # chỉ dựa vào cấu trúc hình ảnh mà không cần nhãn dữ liệu."
        # ══════════════════════════════════════════════════════════════════════
        algo_text = Text("DINO, MoCo-v3, MAE", font_size=28, color=YELLOW_C).next_to(ssl_text, DOWN, buff=0.3)
        self.play(FadeIn(algo_text, shift=UP*0.2))
        self.wait(5)

        # Thêm minh hoạ: Bỏ "Nhãn", giữ "Cấu trúc"
        no_label_group = VGroup()
        label_tag = labeled_box("Nhãn dữ liệu\n(Labels)", width=1.5, height=0.8, color=GREY_B, font_size=16)
        cross = crossmark_vector(color=RED_C, size=0.4).move_to(label_tag)
        struct_tag = labeled_box("Cấu trúc ảnh\n(Structure)", width=1.5, height=0.8, color=GREEN_C, font_size=16)
        no_label_group.add(VGroup(label_tag, cross), struct_tag).arrange(RIGHT, buff=1.0).next_to(algo_text, DOWN, buff=0.6)

        self.play(FadeIn(label_tag), FadeIn(struct_tag))
        self.play(Create(cross)) # Gạch chéo nhãn dữ liệu
        self.play(Indicate(struct_tag, color=YELLOW)) # Nhấn mạnh cấu trúc
        self.wait(5)
        
        self.play(FadeOut(q_text), FadeOut(ssl_text), FadeOut(algo_text), FadeOut(no_label_group))
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Ý tưởng chính của DINOSAUR: thay vì tái tạo lại ảnh gốc RGB 
        # pixels, hãy tái tạo lại các feature maps từ một mô hình self-supervised..."
        # ══════════════════════════════════════════════════════════════════════
        idea_title = Text("Paradigm Shift (Thay đổi tư duy)", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.3)
        self.play(Write(idea_title))

        # Minh hoạ sự thay đổi tư duy: Tái tạo RGB (Sai) -> Tái tạo Feature (Đúng)
        old_way = labeled_box("Reconstruct RGB Pixels", width=2.8, height=0.8, color=RED_C, font_size=18).shift(LEFT * 2.5 + UP * 1)
        old_cross = crossmark_vector(color=RED_C, size=0.3).next_to(old_way, RIGHT)
        
        new_way = labeled_box("Reconstruct Feature Maps", width=2.8, height=0.8, color=GREEN_C, font_size=18).shift(RIGHT * 2.5 + UP * 1)
        new_check = checkmark_vector(color=GREEN_C, size=0.3).next_to(new_way, RIGHT)

        self.play(FadeIn(old_way))
        self.play(Create(old_cross))
        self.play(FadeIn(new_way))
        self.play(Create(new_check))
        self.wait(3)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "...đã pre-trained trên ImageNet. Điều này tạo ra training 
        # signal mang tính semantic cao hơn rất nhiều. Cơ chế này hoạt động theo 
        # mô hình Student-Teacher Knowledge Distillation."
        # ══════════════════════════════════════════════════════════════════════
        self.play(FadeOut(idea_title), FadeOut(old_way), FadeOut(old_cross), FadeOut(new_way), FadeOut(new_check))

        # Setup lại Pipeline nhưng có cấu trúc Teacher - Student rõ ràng
        imagenet_db = Cylinder(radius=0.5, height=0.6, direction=UP, color=PURPLE_C).set_fill(PURPLE_E, opacity=0.8)
        db_text = Text("ImageNet", font_size=16).next_to(imagenet_db, DOWN, buff=0.1)
        imagenet_group = VGroup(imagenet_db, db_text).shift(LEFT * 2.5 + UP * 0.7)

        image_box = Square(side_length=1.2, fill_color=TEAL, fill_opacity=0.3)
        img_text = Text("Image", font_size=18).move_to(image_box)
        image_group = VGroup(image_box, img_text).shift(LEFT * 5 + DOWN * 1.2)

        vit_box = Rectangle(width=2, height=1.5, fill_color=SECONDARY_ACCENT, fill_opacity=0.8)
        vit_text = Text("DINO ViT\n(Teacher)", font_size=20, weight=BOLD).move_to(vit_box)
        vit_group = VGroup(vit_box, vit_text).shift(LEFT * 2.5 + DOWN * 1.2)

        grid = feature_grid(4, 4, cell=0.25, color=YELLOW_C).shift(ORIGIN + DOWN * 1.2)
        feature_text = Text("Target Features\n(Giàu Semantic)", font_size=16, color=YELLOW_C).next_to(grid, UP, buff=0.2)
        grid_group = VGroup(grid, feature_text)

        # Hiện ImageNet truyền data cho Teacher
        self.play(FadeIn(imagenet_group, shift=DOWN*0.5))
        db_arrow = Arrow(imagenet_group.get_bottom(), vit_group.get_top(), color=PURPLE_C)
        self.play(GrowArrow(db_arrow), FadeIn(vit_group))
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Teacher là DINO ViT pre-trained trên ImageNet, tạo ra feature 
        # maps giàu semantic. Student là Slot Attention..."
        # ══════════════════════════════════════════════════════════════════════
        arrow1 = Arrow(image_group.get_right(), vit_group.get_left(), color=GREY_B)
        self.play(FadeIn(image_group, shift=RIGHT*0.5))
        self.play(GrowArrow(arrow1))
        
        arrow2 = Arrow(vit_group.get_right(), grid.get_left(), color=GREY_B)
        self.play(GrowArrow(arrow2), Create(grid), Write(feature_text))
        
        # Hiệu ứng pulse sáng lên chứng tỏ "Giàu Semantic"
        self.play(grid.animate.set_fill(YELLOW, opacity=0.8), run_time=0.5)
        self.play(grid.animate.set_fill(YELLOW, opacity=0.4), run_time=0.5)

        # Vẽ Student
        slot_box = Rectangle(width=2, height=1.5, fill_color=BLUE_COLOR, fill_opacity=0.8)
        slot_text = Text("Slot Attention\n(Student)", font_size=20, weight=BOLD).move_to(slot_box)
        slot_group = VGroup(slot_box, slot_text).shift(RIGHT * 2.5 + DOWN * 1.2)
        
        arrow3 = Arrow(grid.get_right(), slot_group.get_left(), color=GREY_B)
        self.play(GrowArrow(arrow3), FadeIn(slot_group))

        # Vòng ngoặc Student-Teacher KD
        kd_group = VGroup(vit_group, slot_group)
        brace = Brace(kd_group, DOWN, color=ACCENT_COLOR)
        brace_text = brace.get_text("Student-Teacher Knowledge Distillation").set_color(ACCENT_COLOR).scale(0.8)
        self.play(GrowFromCenter(brace), Write(brace_text))
        self.wait(5)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "...với bottleneck K slots phải nén toàn bộ thông tin từ teacher 
        # features vào dạng có cấu trúc nhỏ hơn. Quá trình này ép buộc các slot 
        # phải học cách biểu diễn thông tin hiệu quả."
        # ══════════════════════════════════════════════════════════════════════
        slots = slot_stack(["s1", "s2", "s3"], [RED_C, GREEN_C, BLUE_C], radius=0.25).shift(RIGHT * 5 + DOWN * 1.2)
        slot_label = Text("K Slots\n(Bottleneck)", font_size=16, color=RED_C).next_to(slots, UP, buff=0.2)
        
        # Vẽ cái phễu (funnel) minh hoạ chữ "Bottleneck"
        funnel = Polygon(
            slot_group.get_right() + UP*0.6,
            slots.get_left() + UP*0.3,
            slots.get_left() + DOWN*0.3,
            slot_group.get_right() + DOWN*0.6,
            color=YELLOW_D, fill_opacity=0.2
        )
        self.play(Create(funnel))

        # Hạt data bay qua phễu nén lại
        self.play(Write(slot_label))
        for i in range(3):
            dot = Dot(color=YELLOW_C, radius=0.1).move_to(grid.get_center())
            self.add(dot)
            self.play(dot.animate.move_to(slot_group.get_center()), run_time=0.3)
            # Bay qua phễu
            self.play(dot.animate.move_to(slots[i].get_center()), run_time=0.3)
            self.play(FadeIn(slots[i], scale=0.5), FadeOut(dot), run_time=0.2)

        self.wait(8)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Teacher không chỉ cung cấp target features, mà còn vận chuyển 
        # knowledge từ bộ dữ liệu lớn ImageNet sang các dataset nhỏ hơn. Đây là 
        # lần đầu tiên transfer learning được áp dụng cho object-centric learning."
        # ══════════════════════════════════════════════════════════════════════
        # Minh hoạ dòng chảy Transfer Learning
        transfer_arrow = CurvedArrow(
            imagenet_group.get_top(), 
            slot_group.get_top(), 
            angle=-PI/3, color=YELLOW_D, stroke_width=4
        )
        transfer_text = Text("Vận chuyển Knowledge", font_size=16, color=YELLOW_D).next_to(transfer_arrow, UP, buff=0.1)
        
        self.play(Create(transfer_arrow), Write(transfer_text))
        
        # Làm sáng nguyên khối ImageNet -> Transfer -> Student
        self.play(
            imagenet_db.animate.set_fill(YELLOW, opacity=0.8),
            slot_box.animate.set_fill(YELLOW, opacity=0.8),
            rate_func=there_and_back, run_time=2
        )

        # Badge kỉ niệm
        badge = labeled_box("First Time: Transfer Learning in OCL!", width=4.0, height=0.8, color=HIGHLIGHT_COLOR, font_size=20)
        badge.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(badge, shift=DOWN))
        self.play(Wiggle(badge))

        # Lưu ý: Phần loss L_MSE mình bỏ đi hoặc bạn có thể giữ lại, 
        # vì trong script này kịch bản tập trung nhấn mạnh vào "Transfer Learning" 
        # chứ chưa đề cập đến loss.
        
        self.wait(3)

class S6_03_ViTArchitecture(Scene):
    def construct(self):
        title = Text("Vision Transformer (ViT)", font_size=40, weight=BOLD, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Vision Transformer (ViT) đã tạo bước ngoặt lớn trong Computer Vision. 
        # Thay vì dùng convolutional layer, ViT chia ảnh thành các patch 16x16 pixels..."
        # ══════════════════════════════════════════════════════════════════════
        img_box = Square(side_length=2.4, fill_color=TEAL, fill_opacity=0.3).shift(LEFT * 4.5 + UP * 0.5)
        img_text = Text("Image", font_size=20).move_to(img_box)
        self.play(Create(img_box), Write(img_text))
        self.wait(3)
        
        # Grid đại diện cho các patch (Minh hoạ 16 patch 4x4 cho dễ nhìn)
        grid = VGroup(*[Square(side_length=0.6, stroke_color=WHITE, stroke_width=1) for _ in range(16)]).arrange_in_grid(4, 4, buff=0)
        grid.move_to(img_box.get_center())
        
        patch_text = Text("Chia thành Patches\n(VD: 16x16 px)", font_size=18, color=YELLOW).next_to(img_box, DOWN, buff=0.2)
        self.play(Create(grid), FadeOut(img_text), Write(patch_text))
        self.wait(0.5)
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "...biến mỗi patch thành token và xử lý bằng kiến trúc Transformer."
        # ══════════════════════════════════════════════════════════════════════
        # Flatten to Sequence (Lấy 8 token đại diện)
        seq = VGroup(*[Square(side_length=0.45, fill_color=TEAL, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1) for _ in range(8)])
        seq.arrange(RIGHT, buff=0.15).shift(DOWN * 2 + LEFT * 1)
        
        flatten_text = Text("1D Token Sequence", font_size=18, color=YELLOW).next_to(seq, DOWN, buff=0.2)
        self.play(ReplacementTransform(grid[:8].copy(), seq), ReplacementTransform(patch_text, flatten_text))
        
        # Positional Encodings
        pos_enc = VGroup(*[Text(f"{i}", font_size=14).move_to(s) for i, s in enumerate(seq)])
        self.play(FadeIn(pos_enc))
        self.wait(1)
        
        # Đưa vào Transformer Blocks
        transformer = Rectangle(width=3.5, height=1.5, fill_color=SECONDARY_ACCENT, fill_opacity=0.8).shift(UP * 1 + RIGHT * 1)
        trans_text = Text("Transformer Blocks", font_size=20, weight=BOLD).move_to(transformer)
        arrow_up = Arrow(seq.get_top(), transformer.get_bottom() + LEFT * 1, color=GREY_B)
        
        self.play(GrowArrow(arrow_up), Create(transformer), Write(trans_text))
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "ViT có ưu điểm vượt trội cho object-centric learning: 
        # cơ chế global self-attention nắm bắt mối quan hệ giữa mọi vùng trong ảnh..."
        # ══════════════════════════════════════════════════════════════════════
        vit_adv_text = Text("ViT: Global Self-Attention", font_size=20, color=GREEN_C, weight=BOLD).next_to(transformer, UP, buff=0.3)
        self.play(Write(vit_adv_text))

        # Hiệu ứng kết nối TOÀN CỤC (Global) trên sequence
        global_lines = VGroup()
        source_token = seq[3] # Lấy token số 3 làm ví dụ
        for target in seq:
            if target != source_token:
                line = Line(source_token.get_top(), target.get_top(), path_arc=-0.8, stroke_width=2, color=GREEN_C)
                global_lines.add(line)
        
        self.play(Indicate(source_token, color=GREEN_C))
        self.play(Create(global_lines), run_time=1.5)
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "...trong khi CNN chỉ có receptive field giới hạn."
        # ══════════════════════════════════════════════════════════════════════
        cnn_adv_text = Text("CNN: Local Receptive Field", font_size=18, color=RED_C).next_to(img_box, UP, buff=0.2)
        self.play(Write(cnn_adv_text))

        # Hiệu ứng CỤC BỘ (Local) trượt trên ảnh
        sliding_window = Square(side_length=1.2, color=RED_C, stroke_width=4).move_to(grid.get_corner(UL) + RIGHT*0.6 + DOWN*0.6)
        self.play(Create(sliding_window))
        self.play(sliding_window.animate.shift(RIGHT * 0.6), run_time=0.5)
        self.play(sliding_window.animate.shift(DOWN * 0.6), run_time=0.5)
        
        self.wait(3)
        self.play(FadeOut(global_lines), FadeOut(sliding_window), FadeOut(cnn_adv_text))

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Các layer sâu của ViT tự nhiên phân tách ảnh thành vùng semantic 
        # tương ứng với object, một đặc tính gọi là object property. Đặc biệt, 
        # DINO-trained ViT tạo ra attention maps gần giống object segmentation masks."
        # ══════════════════════════════════════════════════════════════════════
        obj_prop_text = Text("Deep layers: Object Property", font_size=20, color=YELLOW_C, weight=BOLD).move_to(vit_adv_text)
        self.play(ReplacementTransform(vit_adv_text, obj_prop_text))
        self.wait(4)

        # Output Attention Maps -> Segmentation Masks
        arrow_out = Arrow(transformer.get_right(), transformer.get_right() + RIGHT * 1.5, color=GREY_B)
        
        # Vẽ các đám blob đại diện cho Segmentation Mask
        mask1 = VGroup(Circle(radius=0.3, fill_color=RED_C, fill_opacity=0.8, stroke_width=0), Circle(radius=0.2, fill_color=RED_C, fill_opacity=0.8, stroke_width=0).shift(RIGHT*0.2+UP*0.1))
        mask2 = VGroup(Circle(radius=0.35, fill_color=GREEN_C, fill_opacity=0.8, stroke_width=0), Circle(radius=0.25, fill_color=GREEN_C, fill_opacity=0.8, stroke_width=0).shift(LEFT*0.2+DOWN*0.1))
        mask3 = Circle(radius=0.3, fill_color=BLUE_C, fill_opacity=0.8, stroke_width=0)
        
        att_maps = VGroup(mask1, mask2, mask3).arrange(RIGHT, buff=0.3).next_to(arrow_out, RIGHT)
        att_text = Text("Attention Maps\n~ Segmentation Masks", font_size=16, color=YELLOW).next_to(att_maps, DOWN)
        
        self.play(GrowArrow(arrow_out))
        self.play(FadeIn(att_maps, shift=RIGHT*0.5), Write(att_text))
        
        # Nhịp đập để nhấn mạnh tính chất phân tách
        self.play(att_maps.animate.scale(1.1), rate_func=there_and_back, run_time=1.5)
        self.wait(5)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Kết quả thí nghiệm cho thấy feature reconstruction signal 
        # chính là key component quan trọng nhất, chứ không phải việc chọn encoder nào."
        # ══════════════════════════════════════════════════════════════════════
        # Dọn dẹp màn hình hoàn toàn
        self.play(
            FadeOut(img_box), FadeOut(grid), FadeOut(seq), FadeOut(pos_enc), FadeOut(flatten_text), FadeOut(arrow_up),
            FadeOut(transformer), FadeOut(trans_text), FadeOut(obj_prop_text), FadeOut(arrow_out), FadeOut(att_maps), FadeOut(att_text)
        )
        
        key_box = labeled_box("Key Component: Feature Reconstruction Signal", width=6.0, height=0.8, color=ACCENT_COLOR, font_size=20)
        key_box.shift(UP * 1.0)
        
        encoder_note = Text("(Việc chọn Encoder nào không phải yếu tố quyết định 100%)", font_size=14, color=GREY_B).next_to(key_box, DOWN, buff=0.1)
        
        self.play(FadeIn(key_box, shift=UP), FadeIn(encoder_note))
        self.wait(1)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Tuy nhiên, pre-trained ViT vẫn được ưu tiên vì hội tụ nhanh hơn 
        # và tính toán hiệu quả hơn."
        # ══════════════════════════════════════════════════════════════════════
        # Bảng so sánh nhỏ
        vit_adv = VGroup(
            Text("Pre-trained ViT", font_size=18, color=GREEN_C, weight=BOLD),
            VGroup(checkmark_vector(color=GREEN_C, size=0.2), Text(" Hội tụ nhanh", font_size=16)).arrange(RIGHT, buff=0.1),
            VGroup(checkmark_vector(color=GREEN_C, size=0.2), Text(" Tính toán hiệu quả", font_size=16)).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(encoder_note, DOWN, buff=1.0).shift(LEFT * 2.0)

        resnet_adv = VGroup(
            Text("ResNet (CNN)", font_size=18, color=RED_C, weight=BOLD),
            VGroup(crossmark_vector(color=RED_C, size=0.2), Text(" Hội tụ chậm", font_size=16)).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(vit_adv, RIGHT, buff=2.5).align_to(vit_adv, UP)

        vs_text = Text("VS", font_size=24, color=YELLOW, weight=BOLD).move_to((vit_adv.get_center() + resnet_adv.get_center()) / 2).shift(UP*0.3)

        self.play(FadeIn(vit_adv, shift=RIGHT*0.3))
        self.play(FadeIn(vs_text))
        self.play(FadeIn(resnet_adv, shift=LEFT*0.3))
        
        # Nhấn mạnh ViT là lựa chọn ưu tiên
        vit_highlight = SurroundingRectangle(vit_adv, color=GREEN_C, buff=0.2, stroke_width=3)
        self.play(Create(vit_highlight))
        
        self.wait(3)

class S6_04_DINOSAURModel(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "DINOSAUR là mô hình đầu tiên đưa object-centric learning 
        # lên dữ liệu thực tế một cách unsupervised. Kiến trúc gồm ba thành phần."
        # ══════════════════════════════════════════════════════════════════════
        title = Text("DINOSAUR Architecture", font_size=40, weight=BOLD, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        
        # Huy hiệu nhấn mạnh Unsupervised trên Real Data
        badge = labeled_box("1st Unsupervised on Real Data", width=4.0, height=0.6, color=ACCENT_COLOR, font_size=18).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(badge))
        self.wait(2)
        
        base_y = DOWN * 0.8 # Trục y chuẩn cho toàn bộ pipeline
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Encoder: frozen DINO ViT pre-trained trên ImageNet, 
        # chia ảnh thành patch features."
        # ══════════════════════════════════════════════════════════════════════
        # 1. Image & Patching
        img = Square(side_length=1.5, fill_color=TEAL, fill_opacity=0.3).move_to(LEFT*5.5 + base_y)
        img_label = Text("Image", font_size=20).move_to(img)
        self.play(Create(img), Write(img_label))
        
        # Hiệu ứng chia Patch
        patch_grid = VGroup(*[Square(side_length=0.375, stroke_color=WHITE, stroke_width=1) for _ in range(16)]).arrange_in_grid(4, 4, buff=0).move_to(img)
        self.play(Create(patch_grid), FadeOut(img_label), run_time=1)

        # 2. Encoder ViT
        vit = Rectangle(width=1.8, height=1.5, fill_color=SECONDARY_ACCENT, fill_opacity=0.8).next_to(img, RIGHT, buff=0.8)
        vit_label = Text("DINO ViT\n(Frozen)", font_size=18, weight=BOLD).move_to(vit)
        arrow1 = Arrow(img.get_right(), vit.get_left(), color=GREY_B)
        
        num1 = Text("1. Encoder", font_size=18, color=YELLOW_C, weight=BOLD).next_to(vit, DOWN, buff=0.2)
        
        self.play(GrowArrow(arrow1))
        self.play(Create(vit), Write(vit_label), Write(num1))
        
        # Nhấn mạnh Frozen
        self.play(Indicate(vit_label[1], color=RED_C), run_time=1)
        self.wait(3)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Các feature có thể dùng trực tiếp làm target, 
        # hoặc đưa qua ResNet34 encoder."
        # ══════════════════════════════════════════════════════════════════════
        # Xuất ra Target Features
        feats = feature_grid(3, 3, cell=0.3, color=PURPLE).next_to(vit, UP, buff=1.2)
        feat_label = Text("Target Features", font_size=16, color=YELLOW).next_to(feats, UP)
        arrow_feat = Arrow(vit.get_top(), feats.get_bottom(), color=GREY_B)
        
        self.play(GrowArrow(arrow_feat), Create(feats), Write(feat_label))
        self.wait(3)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Không giống bản gốc, DINOSAUR không thêm positional encoding 
        # lên ViT features trước Slot Attention vì position encoding của ViT đã đủ."
        # ══════════════════════════════════════════════════════════════════════
        pe_box = labeled_box("+ Positional Encoding", width=2.0, height=0.5, color=GREY_B, font_size=14).move_to(vit.get_right() + RIGHT*1.2 + UP*0.5)
        self.play(FadeIn(pe_box))
        
        # Đánh dấu X đỏ bỏ đi Positional Encoding
        cross_pe = crossmark_vector(color=RED_C, size=0.3).move_to(pe_box)
        pe_note = Text("(ViT PE đã đủ)", font_size=14, color=GREEN_C).next_to(pe_box, DOWN, buff=0.1)
        self.play(Create(cross_pe), Write(pe_note))
        self.wait(1)
        self.play(FadeOut(pe_box), FadeOut(cross_pe), FadeOut(pe_note))
        self.wait(1)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Slot Attention: K slot cạnh tranh qua competitive attention 
        # để phân nhóm features thành object slots. Mỗi slot đại diện một object trong scene."
        # ══════════════════════════════════════════════════════════════════════
        sa = Rectangle(width=1.8, height=1.5, fill_color=BLUE_COLOR, fill_opacity=0.8).next_to(vit, RIGHT, buff=1.8)
        sa_label = Text("Slot\nAttention", font_size=18, weight=BOLD).move_to(sa).shift(UP*0.2)
        arrow2 = Arrow(vit.get_right(), sa.get_left(), color=GREY_B)
        num2 = Text("2. Slot Attention", font_size=18, color=YELLOW_C, weight=BOLD).next_to(sa, DOWN, buff=0.2)
        
        self.play(GrowArrow(arrow2), Create(sa), Write(sa_label), Write(num2))

        # Minh hoạ cạnh tranh (Competitive Attention)
        slots_vis = VGroup(*[Circle(radius=0.18, fill_color=c, fill_opacity=1) for c in [RED_C, GREEN_C, BLUE_C]]).arrange(RIGHT, buff=0.1).next_to(sa_label, DOWN, buff=0.2)
        self.play(FadeIn(slots_vis))
        
        self.wait(2)
        
        dots = VGroup(*[Dot(color=PURPLE).move_to(vit.get_right()) for _ in range(5)])
        self.play(FadeIn(dots))
        # Hạt data chui vào các slot (Phân nhóm / Grouping)
        self.play(
            dots[0].animate.move_to(slots_vis[0].get_center()),
            dots[1].animate.move_to(slots_vis[0].get_center()),
            dots[2].animate.move_to(slots_vis[1].get_center()),
            dots[3].animate.move_to(slots_vis[2].get_center()),
            dots[4].animate.move_to(slots_vis[2].get_center()),
            run_time=1.5
        )
        self.play(FadeOut(dots))
        self.wait(5)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Decoder: MLP decoder xử lý từng slot độc lập, hoặc Transformer 
        # decoder reconstruct autoregressive có điều kiện trên tất cả slots."
        # ══════════════════════════════════════════════════════════════════════
        dec = Rectangle(width=2.2, height=1.5, fill_color=GREEN_E, fill_opacity=0.8).next_to(sa, RIGHT, buff=1.0)
        num3 = Text("3. Decoder", font_size=18, color=YELLOW_C, weight=BOLD).next_to(dec, DOWN, buff=0.2)
        arrow3 = Arrow(sa.get_right(), dec.get_left(), color=GREY_B)
        
        self.play(GrowArrow(arrow3), Create(dec), Write(num3))
        
        # 2 Lựa chọn Decoder
        mlp_text = Text("- MLP (Độc lập)", font_size=14, color=WHITE).move_to(dec).shift(UP*0.2)
        trans_text = Text("- Trans (Autoregressive)", font_size=14, color=WHITE).move_to(dec).shift(DOWN*0.2)
        
        self.play(Write(mlp_text))
        self.play(Write(trans_text))
        self.wait(4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "Loss function minimize MSE giữa reconstructed features và 
        # target features trong semantic space thay vì pixel space."
        # ══════════════════════════════════════════════════════════════════════
        # Reconstructed Features
        recon_feats = feature_grid(3, 3, cell=0.3, color=PURPLE).next_to(dec, UP, buff=1.2)
        recon_label = Text("Reconstructed", font_size=16, color=YELLOW).next_to(recon_feats, UP)
        arrow_recon = Arrow(dec.get_top(), recon_feats.get_bottom(), color=GREY_B)
        
        self.play(GrowArrow(arrow_recon), Create(recon_feats), Write(recon_label))
        
        # So sánh MSE Loss
        loss_line = DashedLine(recon_feats.get_left(), feats.get_right(), color=YELLOW_C)
        loss_text = Text("MSE Loss", font_size=18, color=YELLOW_C, weight=BOLD).next_to(loss_line, UP, buff=0.1)
        
        space_semantic = Text("Semantic Space", font_size=14, color=GREEN_C).next_to(loss_line, DOWN, buff=0.1)
        space_pixel = Text("Pixel Space", font_size=14, color=RED_C).next_to(space_semantic, DOWN, buff=0.1)
        cross_pixel = crossmark_vector(color=RED_C, size=0.2).next_to(space_pixel, RIGHT, buff=0.1)
        
        self.play(Create(loss_line), Write(loss_text))
        self.play(Wiggle(loss_text))
        self.play(Write(space_semantic))
        self.play(Write(space_pixel), Create(cross_pixel)) # Gạch chéo Pixel Space
        self.wait(3)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO]: "DINOSAUR out-perform toàn bộ model trên dataset synthetic, 
        # và là mô hình unsupervised đầu tiên scale được lên PASCAL VOC và COCO."
        # ══════════════════════════════════════════════════════════════════════
        # Không clear phần trên nữa, để dataset ở dưới cùng
        
        datasets_title = Text("Thành công trên các Datasets:", font_size=22, color=ACCENT_COLOR).move_to(DOWN * 2.5)
        self.play(FadeIn(datasets_title))
        
        datasets = VGroup(
            VGroup(Text("CLEVR (Synthetic)", font_size=18, color=GREEN_C), checkmark_vector(color=GREEN_C, size=0.25)).arrange(RIGHT, buff=0.1),
            VGroup(Text("PASCAL VOC (Real)", font_size=18, color=BLUE_C), checkmark_vector(color=BLUE_C, size=0.25)).arrange(RIGHT, buff=0.1),
            VGroup(Text("COCO (Real, Phức tạp)", font_size=18, color=RED_C), checkmark_vector(color=RED_C, size=0.25)).arrange(RIGHT, buff=0.1)
        ).arrange(RIGHT, buff=0.5).next_to(datasets_title, DOWN, buff=0.3).set_x(0)
        
        self.play(FadeIn(datasets[0], shift=UP*0.2))
        self.wait(0.5)
        self.play(FadeIn(datasets[1], shift=UP*0.2))
        self.wait(0.5)
        self.play(FadeIn(datasets[2], shift=UP*0.2))
        
        self.wait(3)

class S6_05_SSLComparison(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:05: "Self-supervised algorithm nào phù hợp nhất cho 
        # object-centric learning? Nhóm DINOSAUR thí nghiệm trên bốn phương pháp: 
        # DINO, MoCo-v3, MSN, và MAE."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("So sánh các phương pháp SSL")
        self.play(FadeIn(title, shift=UP))
        
        # Tạo trục toạ độ
        base_y = -1.5
        axis = Line(LEFT * 5, RIGHT * 2, color=GREY_B).shift(UP * base_y)
        y_label = safe_text("Semantic Bias\n(Phù hợp cho OCL)", font_size=16, color=YELLOW).next_to(axis, UP, buff=0.2).to_edge(LEFT)
        self.play(Create(axis), Write(y_label), run_time=1)

        # Định nghĩa 4 cột biểu đồ
        bars = VGroup()
        specs = [
            ("DINO", 2.8, GREEN_C),
            ("MoCo-v3", 2.3, BLUE_C),
            ("MSN", 2.0, TEAL_C),
            ("MAE", 1.2, MAROON_C),
        ]
        
        for i, (name, height, color) in enumerate(specs):
            bar = Rectangle(width=1.0, height=height, color=color, stroke_width=2).set_fill(color, opacity=0.6)
            bar.move_to(LEFT * 3.5 + RIGHT * i * 1.5 + UP * (base_y + height / 2))
            label = safe_text(name, font_size=18).next_to(bar, DOWN, buff=0.15)
            bars.add(VGroup(bar, label))

        # Show 4 cột ra
        self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(VGroup(*[b[1] for b in bars])))
        self.wait(1) # Chờ hết 5s đầu

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:05 - 0:12: "Tất cả đều hoạt động tốt, chứng minh self-supervised 
        # pre-training tạo ra useful general bias cho object discovery."
        # ══════════════════════════════════════════════════════════════════════
        # Bật lên các dấu tick xanh cho cả 4 cột
        ticks = VGroup(*[checkmark_vector(color=GREEN_C, size=0.25).next_to(b[0], UP, buff=0.1) for b in bars])
        bias_text = safe_text("Useful General Bias", font_size=24, color=YELLOW_C, weight=BOLD).next_to(ticks, UP, buff=0.5)
        
        self.play(FadeIn(ticks, shift=UP*0.1), run_time=1)
        self.play(Write(bias_text), run_time=1.5)
        self.wait(7) # Tổng đoạn này ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:12 - 0:20: "DINO dùng Vision Transformer với self-distillation, 
        # được chọn làm phương pháp chính vì hiệu năng tốt và dễ tiếp cận."
        # ══════════════════════════════════════════════════════════════════════
        self.play(FadeOut(ticks), FadeOut(bias_text))
        
        # Highlight cột DINO
        dino_highlight = SurroundingRectangle(bars[0], color=YELLOW, stroke_width=4, buff=0.1)
        dino_note1 = safe_text("+ Self-distillation", font_size=16, color=GREEN_C).next_to(dino_highlight, UP, buff=0.1)
        dino_note2_text = safe_text("Lựa chọn chính (Dễ tiếp cận)", font_size=16, color=YELLOW)
        dino_note2_icon = Triangle(color=YELLOW).set_fill(YELLOW, opacity=1).scale(0.08).rotate(-PI/2)
        dino_note2 = VGroup(dino_note2_icon, dino_note2_text).arrange(RIGHT, buff=0.1).next_to(dino_note1, UP, buff=0.1)
        
        self.play(Create(dino_highlight))
        self.play(Write(dino_note1), run_time=1)
        self.play(Write(dino_note2), run_time=1.5)
        self.wait(3) # Tổng đoạn này ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:20 - 0:25: "MoCo-v3 hoạt động tốt nhưng cài đặt phức tạp hơn."
        # ══════════════════════════════════════════════════════════════════════
        moco_note = safe_text("! Setup phức tạp", font_size=16, color=RED_C).next_to(bars[1][0], UP, buff=0.2)
        
        self.play(bars[1][0].animate.set_fill(opacity=0.9), Write(moco_note))
        self.play(Wiggle(moco_note)) # Rung lắc thể hiện sự phức tạp
        self.wait(2.5) # Tổng đoạn này ~5s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:25 - 0:34: "MAE mask 75 phần trăm patches và reconstruct lại, 
        # học representation mạnh nhưng thiên về low-level features."
        # ══════════════════════════════════════════════════════════════════════
        # Chỉ vào MAE
        self.play(bars[3][0].animate.set_color(RED_C))
        
        # Mini-animation góc phải màn hình minh hoạ MAE
        mae_group = VGroup()
        mae_title = safe_text("Cơ chế MAE", font_size=18, color=YELLOW).shift(RIGHT*4 + UP*1.5)
        
        # Grid 4x4 đại diện ảnh
        patch_grid = VGroup(*[Square(side_length=0.4, stroke_color=WHITE, stroke_width=1).set_fill(TEAL, opacity=0.8) for _ in range(16)])
        patch_grid.arrange_in_grid(4, 4, buff=0.05).next_to(mae_title, DOWN, buff=0.3)
        
        self.play(Write(mae_title), FadeIn(patch_grid), run_time=1)
        
        # Chọn ra 12 patches (75%) để mask (xoá mờ đi)
        import random
        random.seed(42) # Fix seed để animation luôn giống nhau
        masked_indices = random.sample(range(16), 12)
        masked_patches = VGroup(*[patch_grid[i] for i in masked_indices])
        
        mask_text = safe_text("Mask 75% Patches", font_size=16, color=RED_C).next_to(patch_grid, DOWN, buff=0.2)
        self.play(masked_patches.animate.set_fill(opacity=0.1), Write(mask_text), run_time=1.5)
        
        # Reconstruct lại
        recon_text = safe_text("Reconstruct", font_size=16, color=GREEN_C).move_to(mask_text)
        self.play(masked_patches.animate.set_fill(opacity=0.8), ReplacementTransform(mask_text, recon_text), run_time=1.5)
        
        # Chốt ý: Low-level features
        low_level_warn_text = safe_text("Thiên về Low-level features", font_size=16, color=RED_C, weight=BOLD)
        low_level_warn_icon = Triangle(color=RED_C).set_fill(RED_C, opacity=1).scale(0.08).rotate(-PI/2)
        low_level_warn = VGroup(low_level_warn_icon, low_level_warn_text).arrange(RIGHT, buff=0.1).next_to(recon_text, DOWN, buff=0.2)
        self.play(Write(low_level_warn))
        self.wait(2) # Tổng đoạn này ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:34 - 0:44: "Nhóm cũng phát hiện ViT cho kết quả tốt hơn đáng kể 
        # so với ResNet cho cả encoder và target feature provider."
        # ══════════════════════════════════════════════════════════════════════
        # Xoá chart và MAE demo để lấy chỗ trống
        phase1 = VGroup(axis, y_label, bars, dino_highlight, dino_note1, dino_note2, moco_note, mae_title, patch_grid, recon_text, low_level_warn)
        self.play(FadeOut(phase1), run_time=1)

        # ViT vs ResNet
        vit_box = labeled_box("ViT (Vision Transformer)", width=3.5, height=1.0, color=GREEN_C, font_size=20)
        vit_check = checkmark_vector(color=GREEN_C, size=0.4).next_to(vit_box, RIGHT, buff=0.3)
        vit_row = VGroup(vit_box, vit_check).shift(UP*0.5)

        resnet_box = labeled_box("ResNet (CNN)", width=3.5, height=1.0, color=MAROON_C, font_size=20)
        resnet_cross = crossmark_vector(color=MAROON_C, size=0.4).next_to(resnet_box, RIGHT, buff=0.3)
        resnet_row = VGroup(resnet_box, resnet_cross).shift(DOWN*1.0)

        self.play(FadeIn(vit_row, shift=RIGHT * 0.3), run_time=1)
        self.play(FadeIn(resnet_row, shift=RIGHT * 0.3), run_time=1)
        
        # Nhấn mạnh: Áp dụng cho CẢ Encoder và Target Feature
        both_note = safe_text("Áp dụng tốt cho cả: Encoder & Target Feature Provider", font_size=20, color=YELLOW, weight=BOLD).to_edge(DOWN).shift(UP*0.5)
        self.play(Write(both_note), run_time=2)
        
        self.wait(4) # Chờ kết thúc audio (Tổng đoạn này ~9-10s)

class S6_06_EncoderUpgradeChallenge(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:05: "Việc thay CNN encoder bằng ViT không đơn giản 
        # như nhiều người nghĩ."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Tại sao nâng cấp Encoder không đơn giản?")
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        self.wait(2.5) # Tổng 5s
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:05 - 0:13: "Vấn đề cốt lõi: encoder càng sâu và lớn, 
        # không gian feature ở đầu ra càng cách xa tín hiệu RGB gốc."
        # ══════════════════════════════════════════════════════════════════════
        # Image
        img = simple_image().shift(LEFT * 5 + UP * 1)
        img_label = safe_text("Image", font_size=16).next_to(img, DOWN)
        
        # Deep ViT (Vẽ nhiều layer chồng lên nhau để thể hiện sự "sâu và lớn")
        vit_layers = VGroup(*[Rectangle(width=0.4, height=1.2, fill_color=SECONDARY_ACCENT, fill_opacity=0.8) for _ in range(4)]).arrange(RIGHT, buff=0.05)
        vit_layers.shift(LEFT * 2.5 + UP * 1)
        vit_label = safe_text("Deep ViT\nEncoder", font_size=16, color=YELLOW).next_to(vit_layers, DOWN)
        
        arr_img_vit = Arrow(img.get_right(), vit_layers.get_left(), color=GREY_B)
        
        # Semantic Space (Feature Map)
        semantic_space = feature_grid(4, 4, cell=0.25, color=PURPLE).shift(ORIGIN + UP * 1)
        semantic_label = safe_text("Semantic Space", font_size=16, color=PURPLE_B).next_to(semantic_space, DOWN)
        arr_vit_sem = Arrow(vit_layers.get_right(), semantic_space.get_left(), color=GREY_B)
        
        # RGB Space (Ảnh gốc)
        rgb_space = Rectangle(width=1.5, height=1.5, color=TEAL_C).set_fill(TEAL_E, opacity=0.3).shift(RIGHT * 4.5 + UP * 1)
        rgb_label = safe_text("RGB Space", font_size=16, color=TEAL_C).next_to(rgb_space, DOWN)
        
        self.play(FadeIn(img), Write(img_label), GrowArrow(arr_img_vit), run_time=1.5)
        self.play(FadeIn(vit_layers), Write(vit_label), GrowArrow(arr_vit_sem), run_time=1.5)
        self.play(FadeIn(semantic_space), Write(semantic_label), FadeIn(rgb_space), Write(rgb_label), run_time=1.5)
        
        # Khoảng cách xa
        gap_arrow = DoubleArrow(semantic_space.get_right(), rgb_space.get_left(), color=RED_C, stroke_width=4)
        gap_text = safe_text("Khoảng cách quá xa", font_size=16, color=RED_C, weight=BOLD).next_to(gap_arrow, UP)
        
        self.play(GrowFromCenter(gap_arrow), Write(gap_text), run_time=1.5)
        self.wait(1.5) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:13 - 0:22: "Chúng ta không thể dùng CNN decoder nhỏ để reconstruct 
        # từ slots về ảnh gốc, vì khoảng cách feature space quá lớn."
        # ══════════════════════════════════════════════════════════════════════
        # Slots
        slots = slot_stack(["s1", "s2", "s3"], radius=0.2).next_to(semantic_space, DOWN, buff=1.8)
        arr_sem_slot = Arrow(semantic_label.get_bottom(), slots.get_top(), color=GREY_B, buff=0.1)
        
        # Small CNN Decoder cố gắng khôi phục về RGB
        cnn_dec = labeled_box("Small CNN\nDecoder", width=1.5, height=0.8, color=GREY_C, font_size=14).move_to(slots.get_center() + RIGHT * 2.5)
        arr_slot_dec = Arrow(slots.get_right(), cnn_dec.get_left(), color=GREY_B)
        arr_dec_rgb = Arrow(cnn_dec, rgb_space, color=RED_C, buff=0.2)
        
        self.play(GrowArrow(arr_sem_slot), FadeIn(slots), run_time=1)
        self.play(GrowArrow(arr_slot_dec), FadeIn(cnn_dec), run_time=1)
        self.play(GrowArrow(arr_dec_rgb), run_time=1)
        
        # Đánh dấu X sập hệ thống
        cross = crossmark_vector(color=RED_C, size=0.5).move_to(cnn_dec)
        fail_text = safe_text("Không thể Reconstruct", font_size=16, color=RED_C).next_to(cnn_dec, DOWN)
        
        self.play(Create(cross), Write(fail_text), run_time=1.5)
        self.wait(1.5) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:22 - 0:31: "Giải pháp của DINOSAUR: reconstruct trong hidden 
        # feature space của teacher model thay vì pixel space."
        # ══════════════════════════════════════════════════════════════════════
        # Xóa đoạn lỗi
        fail_group = VGroup(gap_arrow, gap_text, rgb_space, rgb_label, arr_slot_dec, arr_dec_rgb, cnn_dec, cross, fail_text)
        self.play(FadeOut(fail_group), run_time=1.5)
        
        # Setup Teacher Target
        target_box = labeled_box("Target Features\n(Teacher Model)", width=2.0, height=1.0, color=YELLOW_C, font_size=16)
        target_box.move_to(RIGHT * 3 + UP * 1)
        
        # Decoder mới chĩa thẳng lên Target Box
        new_dec = labeled_box("Feature\nDecoder", width=1.5, height=0.8, color=GREEN_C, font_size=16).move_to(RIGHT * 3 + DOWN * 1.5)
        arr_slot_new = Arrow(slots.get_right(), new_dec.get_left(), color=GREY_B)
        arr_new_up = Arrow(new_dec.get_top(), target_box.get_bottom(), color=GREEN_C)
        
        self.play(FadeIn(target_box), run_time=1.5)
        self.play(GrowArrow(arr_slot_new), FadeIn(new_dec), run_time=1.5)
        self.play(GrowArrow(arr_new_up), run_time=1)
        
        recon_text = safe_text("Reconstruct trong\nFeature Space", font_size=16, color=GREEN_C).next_to(arr_new_up, RIGHT)
        self.play(Write(recon_text), run_time=1)
        self.wait(1.5) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:31 - 0:39: "Điều này cho phép giữ nguyên sức mạnh của encoder 
        # mà không cần thiết kế decoder phức tạp để convert từ feature space về RGB."
        # ══════════════════════════════════════════════════════════════════════
        # Nhấn mạnh sự đơn giản
        power_enc = SurroundingRectangle(vit_layers, color=YELLOW, buff=0.2)
        power_text = safe_text("Giữ sức mạnh", font_size=14, color=YELLOW).next_to(power_enc, UP)
        
        simple_dec = SurroundingRectangle(new_dec, color=GREEN_C, buff=0.2)
        simple_text = safe_text("Decoder đơn giản", font_size=14, color=GREEN_C).next_to(simple_dec, DOWN)
        
        self.play(Create(power_enc), Write(power_text), run_time=2)
        self.play(Create(simple_dec), Write(simple_text), run_time=2)
        self.wait(4) # Tổng 8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:39 - 0:49: "Pipeline trở thành: Image, Encoder ViT hoặc ResNet, 
        # Slot Attention, Decoder MLP hoặc Transformer, Reconstructed Features, 
        # với loss tính giữa reconstructed features và target features từ DINO ViT teacher."
        # ══════════════════════════════════════════════════════════════════════
        # Dọn dẹp để hiện Final Pipeline
        self.play(FadeOut(Group(*self.mobjects)), run_time=1)
        self.play(FadeIn(title), run_time=0.5) # Giữ lại title
        
        # Vẽ chuỗi 5 cục Pipeline
        nodes = ["Image", "Encoder\n(ViT / ResNet)", "Slot\nAttention", "Decoder\n(MLP / Trans)", "Reconstructed\nFeatures"]
        colors = [TEAL_C, SECONDARY_ACCENT, BLUE_COLOR, GREEN_E, PURPLE_C]
        boxes = VGroup(*[labeled_box(n, width=1.8, height=1.0, color=c, font_size=16) for n, c in zip(nodes, colors)])
        boxes.arrange(RIGHT, buff=0.5).shift(DOWN * 1)
        
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i+1].get_left(), color=GREY_B) for i in range(4)])
        
        # Teacher box
        teacher = labeled_box("Target Features\n(DINO Teacher)", width=2.5, height=0.8, color=YELLOW_D, font_size=16).next_to(boxes[4], UP, buff=1.5)
        
        # Animation xuất hiện tuần tự
        self.play(FadeIn(boxes[0]), run_time=0.5)
        for i in range(4):
            self.play(GrowArrow(arrows[i]), FadeIn(boxes[i+1]), run_time=0.7)
            
        # Loss tính toán
        self.play(FadeIn(teacher, shift=DOWN*0.5), run_time=1)
        mse_loss = DoubleArrow(boxes[4].get_top(), teacher.get_bottom(), color=RED_C)
        mse_text = safe_text("MSE Loss", font_size=16, color=RED_C, weight=BOLD).next_to(mse_loss, LEFT)
        
        self.play(GrowFromCenter(mse_loss), Write(mse_text), run_time=1.5)
        self.play(Wiggle(mse_text))
        
        self.wait(2.2) # Tổng ~10s

class S6_07_OpticalFlowDepth(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "Trước DINOSAUR, các nhà nghiên cứu đã cố khắc phục 
        # hạn chế pixel reconstruction bằng cách reconstruct các tín hiệu khác. 
        # SAVi mở rộng Slot Attention sang video bằng cách reconstruct optical flow."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Reconstruct Beyond RGB: SAVi & SAVi++")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # Panel 1: RGB (Đã bị loại bỏ)
        rgb_img = simple_image().scale(1.2)
        rgb_cross = crossmark_vector(color=RED_C, size=0.6).move_to(rgb_img)
        rgb_label = safe_text("RGB Pixels\n(Quá nhiễu)", font_size=16, color=RED_C).next_to(rgb_img, DOWN)
        panel_rgb = VGroup(rgb_img, rgb_cross, rgb_label).shift(LEFT * 4 + UP * 0.5)

        self.play(FadeIn(rgb_img), Write(rgb_label), run_time=1.5)
        self.play(Create(rgb_cross), run_time=1) # Đánh dấu X chối bỏ RGB
        self.wait(4)
        
        # Panel 2: SAVi (Optical Flow)
        flow_box = Rectangle(width=2.0, height=1.5, color=BLUE_C).set_fill(BLUE_E, opacity=0.28)
        # Tạo 1 chiếc xe đơn giản (đại diện Object)
        car_body = Rectangle(width=0.8, height=0.4, color=YELLOW_C).set_fill(YELLOW_C, opacity=0.8)
        car_wheels = VGroup(Circle(radius=0.1, color=WHITE).set_fill(GREY_E, opacity=1).shift(LEFT*0.25+DOWN*0.2),
                            Circle(radius=0.1, color=WHITE).set_fill(GREY_E, opacity=1).shift(RIGHT*0.25+DOWN*0.2))
        car = VGroup(car_body, car_wheels).move_to(flow_box).shift(LEFT*0.3)
        
        flow_label = safe_text("SAVi\n(Optical Flow)", font_size=18, color=BLUE_B, weight=BOLD).next_to(flow_box, DOWN)
        panel_flow = VGroup(flow_box, car, flow_label).shift(ORIGIN + UP * 0.5)
        
        arr_rgb_flow = Arrow(panel_rgb.get_right(), panel_flow.get_left(), color=GREY_B)
        self.play(GrowArrow(arr_rgb_flow), FadeIn(panel_flow), run_time=2)
        self.wait(2.5) # Tổng đoạn này ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:15: "Các pixel thuộc cùng một object thường chuyển động 
        # giống nhau, tạo signal mạnh cho object discovery."
        # ══════════════════════════════════════════════════════════════════════
        # Vector chuyển động đồng nhất
        flow_vectors = VGroup(*[
            Arrow(ORIGIN, RIGHT * 0.6, buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.2)
            .next_to(car, UP if i==0 else DOWN if i==1 else RIGHT, buff=0.1)
            for i in range(3)
        ])
        
        self.play(FadeIn(flow_vectors), run_time=1)
        
        # Di chuyển cả xe và vector cùng nhau (Motion Grouping)
        self.play(
            car.animate.shift(RIGHT * 0.5),
            flow_vectors.animate.shift(RIGHT * 0.5),
            rate_func=there_and_back,
            run_time=2
        )
        
        grouping_text = safe_text("Motion Grouping", font_size=14, color=YELLOW).next_to(flow_label, DOWN)
        self.play(Write(grouping_text), run_time=1)
        self.wait(4) # Tổng đoạn này ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:15 - 0:22: "SAVi++ mở rộng hơn nữa bằng cách reconstruct depth 
        # từ dữ liệu LiDAR. Depth mang thông tin hình học ổn định trước ánh sáng, texture, màu sắc."
        # ══════════════════════════════════════════════════════════════════════
        # Panel 3: SAVi++ (Depth)
        depth_box = Rectangle(width=2.0, height=1.5, color=TEAL_C).set_fill(TEAL_E, opacity=0.1)
        depth_layers = VGroup(*[
            Rectangle(width=1.2 - i * 0.2, height=0.8 - i * 0.1, color=TEAL_C)
            .set_fill(TEAL_C, opacity=0.3 + i * 0.2)
            .shift(UP * i * 0.1 + RIGHT * i * 0.1)
            for i in range(3)
        ]).move_to(depth_box)
        
        depth_label = safe_text("SAVi++\n(Depth LiDAR)", font_size=18, color=TEAL_B, weight=BOLD).next_to(depth_box, DOWN)
        panel_depth_bg = VGroup(depth_box, depth_label).shift(RIGHT * 4 + UP * 0.5)
        depth_layers.shift(RIGHT * 4 + UP * 0.5)
        
        arr_flow_depth = Arrow(panel_flow.get_right(), panel_depth_bg.get_left(), color=GREY_B)
        
        self.play(GrowArrow(arr_flow_depth), FadeIn(panel_depth_bg), run_time=1.5)
        for layer in depth_layers:
            self.play(FadeIn(layer, shift=DOWN*0.1), run_time=0.4)
        
        # Minh hoạ sự ổn định (Chống lại ánh sáng/Màu sắc)
        # Đã xóa shield, sun_icon, color_icon theo yêu cầu
        
        stable_text = safe_text("Ổn định hình học", font_size=14, color=GREEN_C).next_to(depth_label, DOWN)
        self.play(Write(stable_text), run_time=1)
        self.wait(4) # Tổng đoạn này ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:22 - 0:31: "Đặc biệt hữu ích cho autonomous driving và robotics. 
        # SAVi++ được đánh giá trên Waymo Open Dataset, cho phép phát hiện object 
        # mà không cần reconstruct RGB pixels."
        # ══════════════════════════════════════════════════════════════════════
        # Box ứng dụng bên dưới
        app_box = labeled_box("Autonomous Driving & Robotics", width=4.5, height=0.6, color=ACCENT_COLOR, font_size=18)
        waymo_box = labeled_box("Waymo Open Dataset", width=3.0, height=0.6, color=GREEN_C, font_size=18)
        app_group = VGroup(app_box, waymo_box).arrange(RIGHT, buff=0.5).to_edge(DOWN).shift(UP * 0.8)
        
        self.play(FadeIn(app_group, shift=UP*0.3), run_time=1.5)
        
        no_rgb_icon = Triangle(color=YELLOW).set_fill(YELLOW, opacity=1).scale(0.08).rotate(-PI/2)
        no_rgb_txt = safe_text("Không cần RGB Pixels", font_size=20, color=YELLOW, weight=BOLD)
        no_rgb_text = VGroup(no_rgb_icon, no_rgb_txt).arrange(RIGHT, buff=0.1).next_to(app_group, DOWN, buff=0.2)
        self.play(Write(no_rgb_text), run_time=1.5)
        self.wait(8) # Tổng đoạn này ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:31 - 0:40: "Hạn chế: đòi hỏi dữ liệu LiDAR, giới hạn ứng dụng."
        # ══════════════════════════════════════════════════════════════════════
        # Hộp cảnh báo đỏ chót
        warning_box = labeled_box("! Hạn chế: Bắt buộc có dữ liệu LiDAR đắt đỏ", width=6.0, height=0.7, color=RED_C, font_size=20)
        warning_box[0].set_fill(RED_E, opacity=0.8) # Làm nền hộp đỏ sậm
        warning_box.move_to(app_group) # Đè lên vị trí của app_group
        
        self.play(FadeOut(app_group), FadeOut(no_rgb_text), run_time=1)
        self.play(FadeIn(warning_box, shift=DOWN*0.2), run_time=1)
        
        # Nhấp nháy cảnh báo
        self.play(Wiggle(warning_box), run_time=2)
        self.wait(5) # Chờ kết thúc audio (Tổng đoạn này ~9s)

class S6_08_AdaSlot(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "Slot Attention gốc và DINOSAUR đều phải predefine 
        # số lượng slot K. K quá nhỏ thì bỏ sót object, K quá lớn thì phân tách 
        # object không cần thiết. Đặc biệt trên COCO, số object thay đổi rất nhiều."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Adaptive Slot Attention (AdaSlot)")
        self.play(FadeIn(title, shift=UP), run_time=1)

        # Minh hoạ vấn đề của K cố định (Fixed K Problem)
        k_problem_title = safe_text("Vấn đề: K (Số lượng slot) cố định", font_size=20, color=YELLOW_C).shift(UP * 2)
        
        # K quá nhỏ
        k_small = labeled_box("K quá nhỏ\n(Bỏ sót object)", width=2.5, height=1.0, color=RED_C, font_size=18).shift(LEFT * 3.5 + UP*0.5)
        cross_small = crossmark_vector(color=RED_C, size=0.3).next_to(k_small, RIGHT)
        
        # K quá lớn
        k_large = labeled_box("K quá lớn\n(Phân mảnh object)", width=2.5, height=1.0, color=RED_C, font_size=18).shift(RIGHT * 3.5 + UP*0.5)
        cross_large = crossmark_vector(color=RED_C, size=0.3).next_to(k_large, LEFT)

        self.play(Write(k_problem_title), run_time=1)
        self.play(FadeIn(k_small, shift=RIGHT*0.3), FadeIn(k_large, shift=LEFT*0.3), run_time=1.5)
        self.play(Create(cross_small), Create(cross_large), run_time=1)
        self.wait(4)
        
        coco_note = safe_text("Dataset COCO: Số lượng object thay đổi liên tục!", font_size=18, color=YELLOW).next_to(k_problem_title, DOWN, buff=2.8)
        self.play(Write(coco_note), run_time=1.5)
        self.wait(8) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:15: "AdaSlot giải quyết bằng cách frame dynamic slot 
        # selection như bài toán subset selection. Bắt đầu với nhiều slot, rồi dùng 
        # Gumbel Softmax chọn subset phù hợp."
        # ══════════════════════════════════════════════════════════════════════
        # Xoá màn hình để chuyển sang giải pháp
        self.play(FadeOut(k_problem_title), FadeOut(k_small), FadeOut(cross_small), FadeOut(k_large), FadeOut(cross_large), FadeOut(coco_note), run_time=1)

        # Bắt đầu pipeline AdaSlot
        candidates = slot_stack(["1", "2", "3", "4", "5"], [RED_C, GREEN_C, BLUE_C, YELLOW_C, PURPLE_C], radius=0.25)
        candidates_label = safe_text("Nhiều Slot\nỨng viên (N)", font_size=16, color=GREY_B).next_to(candidates, DOWN)
        group_cand = VGroup(candidates, candidates_label).shift(LEFT * 4 + UP * 0.5)

        selector = labeled_box("Gumbel Softmax\nSelector", width=2.0, height=1.5, color=YELLOW_D, font_size=18).move_to(UP * 0.5)
        
        # Chọn ra 3 slot (Subset), 2 slot bị tắt
        selected = slot_stack(["obj", "obj", "bg"], [RED_C, GREEN_C, BLUE_C], radius=0.25)
        dimmed = slot_stack(["off", "off"], [GREY_D, GREY_D], radius=0.2).set_opacity(0.3)
        outputs = VGroup(selected, dimmed).arrange(DOWN, buff=0.2)
        selected_label = safe_text("Subset Phù hợp\n(K tự thích ứng)", font_size=16, color=ACCENT_COLOR).next_to(outputs, DOWN)
        group_out = VGroup(outputs, selected_label).shift(RIGHT * 4 + UP * 0.5)

        arr1 = Arrow(group_cand.get_right(), selector.get_left(), color=GREY_B)
        arr2 = Arrow(selector.get_right(), group_out.get_left(), color=GREY_B)

        self.play(FadeIn(group_cand, shift=RIGHT*0.3), run_time=1.5)
        self.play(GrowArrow(arr1), FadeIn(selector), run_time=1.5)
        self.play(GrowArrow(arr2), FadeIn(group_out, shift=RIGHT*0.3), run_time=1.5)
        self.wait(4) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:15 - 0:25: "Gumbel Softmax cho phép chọn discrete mà vẫn 
        # differentiable, train end-to-end. AdaSlot dùng hai loss: reconstruction 
        # loss và regularization loss trên số slot được chọn."
        # ══════════════════════════════════════════════════════════════════════
        diff_text = safe_text("Discrete & Differentiable (Train End-to-End)", font_size=16, color=GREEN_C, weight=BOLD).next_to(selector, UP, buff=0.2)
        self.play(Write(diff_text), selector[0].animate.set_fill(YELLOW_D, opacity=0.5), run_time=1.5)

        # Vẽ 2 nhánh Loss
        loss_box = VGroup(
            labeled_box("1. L_Reconstruction", width=2.2, height=0.6, color=BLUE_C, font_size=14),
            labeled_box("2. L_Regularization\n(Ép giảm số slot)", width=2.2, height=0.6, color=RED_C, font_size=14)
        ).arrange(DOWN, buff=0.2).shift(DOWN * 2)

        arr_loss = Arrow(selector.get_bottom(), loss_box.get_top(), color=GREY_B)
        
        self.play(GrowArrow(arr_loss), FadeIn(loss_box, shift=UP*0.2), run_time=2)
        self.wait(3) # Tổng ~10s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:25 - 0:40: "Kết quả: out-perform DINOSAUR trên mọi metric 
        # trên COCO: ARI 75.59 so với 73.23, mBO 35.64 so với 33.85."
        # ══════════════════════════════════════════════════════════════════════
        # Xóa pipeline để hiện bảng kết quả COCO
        self.play(FadeOut(group_cand), FadeOut(arr1), FadeOut(selector), FadeOut(arr2), FadeOut(group_out), FadeOut(diff_text), FadeOut(arr_loss), FadeOut(loss_box), run_time=1)

        result_title = safe_text("Kết quả trên tập dữ liệu COCO", font_size=24, color=ACCENT_COLOR, weight=BOLD).shift(UP * 1.5)
        self.play(Write(result_title), run_time=1)

        # Bảng so sánh
        table_data = [
            ["Metric", "DINOSAUR", "AdaSlot"],
            ["ARI (^)", "73.23", "75.59"],
            ["mBO (^)", "33.85", "35.64"]
        ]
        
        # Dựng bảng bằng VGroup để dễ control màu sắc
        table = VGroup()
        for r, row in enumerate(table_data):
            row_group = VGroup()
            for c, text in enumerate(row):
                color = WHITE
                weight = NORMAL
                if r == 0: color = GREY_B; weight = BOLD
                elif c == 2: color = GREEN_C; weight = BOLD # Highlight cột AdaSlot
                elif c == 0: color = YELLOW_C
                
                cell = safe_text(text, font_size=20, color=color, weight=weight)
                cell.move_to(RIGHT * (c - 1) * 2.5 + DOWN * r * 0.8)
                row_group.add(cell)
            table.add(row_group)
        
        table.move_to(ORIGIN + DOWN*0.5)

        # Kẻ gạch chân Header
        line = Line(table.get_left() + UP*0.6, table.get_right() + UP*0.6, color=GREY_B)
        
        self.play(FadeIn(table[0]), Create(line), run_time=1.5) # Header
        self.play(FadeIn(table[1]), run_time=1.5) # ARI row
        self.play(FadeIn(table[2]), run_time=1.5) # mBO row

        # Bao quanh cột AdaSlot để nhấn mạnh "Out-perform"
        adaslot_col = VGroup(table[0][2], table[1][2], table[2][2])
        highlight_col = SurroundingRectangle(adaslot_col, color=GREEN_C, buff=0.3, stroke_width=3)
        win_text = safe_text("Out-perform!", font_size=18, color=GREEN_C, weight=BOLD).next_to(highlight_col, UP, buff=0.2)

        self.play(Create(highlight_col), Write(win_text), run_time=1.5)
        self.wait(7) # Tổng ~15s (đến hết audio)

class S6_09_VideoSaur(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:05: "VideoSaur là phương pháp khác biệt: thay vì 
        # reconstruct features, train slots dự đoán temporal feature similarity 
        # giữa các frame."
        # ══════════════════════════════════════════════════════════════════════
        # Tiêu đề
        title = title_mob("VideoSaur: Temporal Similarity")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # 1. Khai báo các đối tượng trong pipeline chính
        # Tạo 2 frame liên tiếp (Video)
        frame1 = simple_image().scale(0.85)
        frame2 = simple_image().scale(0.85)
        frames = VGroup(frame1, frame2).arrange(RIGHT, buff=0.1)
        frame_label = safe_text("Frame t & t+1", font_size=16, color=GREY_B).next_to(frames, DOWN)
        group_frames = VGroup(frames, frame_label)

        # Di chuyển object (vòng tròn đỏ) trong frame 2
        frame2[3].shift(RIGHT * 0.3 + UP * 0.1)

        # Hộp ViT + Slot Attention
        vit_box = labeled_box("SS-ViT\nEncoder", width=1.1, height=0.7, color=SECONDARY_ACCENT, font_size=14)
        slots_box = labeled_box("Slot\nAttention", width=1.1, height=0.7, color=BLUE_C, font_size=14)
        encoder_group = VGroup(vit_box, slots_box).arrange(RIGHT, buff=0.2)
        
        # Predicted Matrix
        pred_matrix = feature_grid(3, 3, cell=0.22, color=YELLOW)
        for i in range(3): pred_matrix[i*3 + i].set_fill(YELLOW_C, opacity=0.9)
        pred_label = safe_text("Predicted\nSimilarity", font_size=14, color=YELLOW).next_to(pred_matrix, DOWN)
        pred_group = VGroup(pred_matrix, pred_label)

        # Ground-truth Matrix
        gt_matrix = feature_grid(3, 3, cell=0.22, color=GREEN_C)
        for i in range(3): gt_matrix[i*3 + i].set_fill(GREEN_C, opacity=0.9)
        gt_label = safe_text("Ground-Truth\nCosine Distance", font_size=14, color=GREEN_C).next_to(gt_matrix, DOWN)
        gt_group = VGroup(gt_matrix, gt_label)

        # Sắp xếp toàn bộ pipeline
        pipeline = VGroup(group_frames, encoder_group, pred_group, gt_group).arrange(RIGHT, buff=0.9)
        gt_group.shift(RIGHT * 0.5) # Thêm khoảng trống cho mũi tên đỏ
        pipeline.move_to(UP * 0.8) # Căn giữa lại toàn bộ

        # Mũi tên kết nối pipeline (thêm stroke_width=5 để vừa phải)
        arr_to_model = Arrow(group_frames.get_right(), encoder_group.get_left(), buff=0.15, color=GREY_B, stroke_width=5)
        arr_to_matrix = Arrow(encoder_group.get_right(), pred_group.get_left(), buff=0.15, color=GREY_B, stroke_width=5)
        
        # Sửa lỗi mũi tên đè: tăng buff, giảm độ dày và giới hạn tip
        ce_loss = DoubleArrow(pred_matrix.get_right(), gt_matrix.get_left(), buff=0.25, color=RED_C, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        ce_label = safe_text("Cross-Entropy Loss", font_size=14, color=RED_C, weight=BOLD).next_to(ce_loss, UP, buff=0.15)

        # Heavy Decoder phía dưới
        heavy_dec = labeled_box("Heavy Decoder\n(MLP / Transformer)", width=2.4, height=0.9, color=GREY_C, font_size=16)
        heavy_dec.next_to(encoder_group, DOWN, buff=1.2)
        arr_down = Arrow(encoder_group.get_bottom(), heavy_dec.get_top(), buff=0.1, color=GREY_D, stroke_width=6)
        cross_dec = crossmark_vector(color=RED_C, size=0.4).move_to(heavy_dec)
        reduce_text = safe_text("Giảm tối đa độ phức tạp!", font_size=18, color=GREEN_C, weight=BOLD).next_to(heavy_dec, RIGHT, buff=0.5)

        # Dòng thông điệp "Thay vì Reconstruct"
        no_recon = safe_text("Thay vì Reconstruct", font_size=16, color=RED_C)
        cross_recon = crossmark_vector(color=RED_C, size=0.2).next_to(no_recon, LEFT, buff=0.1)
        no_recon_group = VGroup(cross_recon, no_recon).next_to(heavy_dec, LEFT, buff=0.8)

        # --- ANIMATION TRÌNH TỰ ---
        self.play(FadeIn(group_frames), run_time=1)
        self.play(FadeIn(no_recon_group), run_time=1)
        self.wait(3.5) # Tổng ~5s

        # [AUDIO] 0:05 - 0:13:
        self.play(GrowArrow(arr_to_model), FadeIn(encoder_group, shift=RIGHT*0.2), run_time=1.5)
        self.play(GrowArrow(arr_to_matrix), FadeIn(pred_group, shift=RIGHT*0.2), run_time=1.5)
        self.play(FadeIn(gt_group, shift=RIGHT*0.2), run_time=1)
        self.play(GrowFromCenter(ce_loss), Write(ce_label), run_time=1)
        self.wait(4) # Tổng ~13s

        # [AUDIO] 0:13 - 0:20:
        self.play(FadeIn(heavy_dec), GrowArrow(arr_down), run_time=1.5)
        self.play(Create(cross_dec), run_time=1)
        self.play(Write(reduce_text), run_time=1)
        self.play(Wiggle(reduce_text), run_time=0.5)
        self.wait(3) # Chờ đến hết audio (Tổng = 20s)

class S6_10_Part6Summary(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:18: "Phần 6 đã đi qua hành trình nâng cấp encoder: 
        # từ việc hiểu tại sao CNN với pixel reconstruction thất bại, đến feature 
        # reconstruction là key component, và sự ra đời của DINOSAUR. Chúng ta 
        # cũng khám phá reconstruct optical flow với SAVi, depth với SAVi++, 
        # dynamic slot number với AdaSlot, và temporal similarity với VideoSaur."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Tóm tắt Upgrading Encoder")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # Center Node
        center = labeled_box("Encoder\nUpgrade", width=2.0, height=1.1, color=HIGHLIGHT_COLOR, font_size=22)
        self.play(FadeIn(center, scale=1.2), run_time=1)
        
        # Nodes xung quanh (Sắp xếp lại theo flow thời gian của kịch bản)
        items = [
            labeled_box("1. CNN + Pixel RGB\n(Thất bại)", color=RED_C, font_size=16).shift(LEFT * 4 + UP * 1.5),
            labeled_box("2. DINO ViT Feature\n(DINOSAUR)", color=GREEN_C, font_size=16).shift(RIGHT * 4 + UP * 1.5),
            labeled_box("3. Flow / Depth\n(SAVi, SAVi++)", color=TEAL_C, font_size=16).shift(LEFT * 4 + DOWN * 1.4),
            labeled_box("4. Dynamic/Temporal\n(AdaSlot, VideoSaur)", color=BLUE_C, font_size=16).shift(RIGHT * 4 + DOWN * 1.4),
        ]
        
        arrows = VGroup(*[Arrow(center.get_center(), item.get_center(), buff=1.4, color=GREY_B) for item in items])
        
        # Lần lượt hiện ra khớp với audio đọc tên từng model
        self.play(GrowArrow(arrows[0]), FadeIn(items[0], shift=RIGHT*0.5), run_time=1) # CNN
        self.wait(2)
        self.play(GrowArrow(arrows[1]), FadeIn(items[1], shift=LEFT*0.5), run_time=1)  # DINOSAUR
        self.wait(4)
        self.play(GrowArrow(arrows[2]), FadeIn(items[2], shift=RIGHT*0.5), run_time=1) # SAVi, SAVi++
        self.wait(5)
        self.play(GrowArrow(arrows[3]), FadeIn(items[3], shift=LEFT*0.5), run_time=1)  # AdaSlot, VideoSaur
        self.wait(4) # Tổng ~18s
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:18 - 0:38: "Ba điểm chính: pixel reconstruction tạo signal quá 
        # yếu vì mô hình tập trung vào color statistics thay vì object structure. 
        # Self-supervised feature reconstruction từ DINO ViT tạo signal đủ mạnh 
        # cho object grouping. Và các giải pháp mới đang mở rộng giới hạn của 
        # object-centric learning."
        # ══════════════════════════════════════════════════════════════════════
        # Xóa sơ đồ mindmap khỏi màn hình
        mindmap_group = VGroup(center, *items, arrows)
        self.play(FadeOut(mindmap_group), run_time=1)
        
        takeaways_title = safe_text("3 ĐIỂM CHÍNH (KEY TAKEAWAYS):", font_size=24, color=YELLOW_C, weight=BOLD).to_edge(UP).shift(DOWN*1.2)
        self.play(Write(takeaways_title), run_time=1)
        
        # Danh sách 3 điểm
        t1 = VGroup(crossmark_vector(color=RED_C, size=0.2), safe_text("Pixel Recon: Quá yếu, chỉ focus vào màu sắc.", font_size=20)).arrange(RIGHT, buff=0.2)
        t2 = VGroup(checkmark_vector(color=GREEN_C, size=0.2), safe_text("SS-Feature Recon (DINO ViT): Đủ mạnh cho Object Grouping.", font_size=20)).arrange(RIGHT, buff=0.2)
        t3 = VGroup(Arrow(ORIGIN, RIGHT*0.3, color=BLUE_C, buff=0), safe_text("Biến thể mới (Flow, LiDAR, Dynamic, Video): Mở rộng OCL.", font_size=20)).arrange(RIGHT, buff=0.2)
        
        takeaways = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(takeaways_title, DOWN, buff=0.8)
        
        # Chạy khớp từng câu: Tách thời gian animation (run_time=1) và thời gian chờ (self.wait)
        self.play(FadeIn(t1, shift=UP*0.2), run_time=1) # Câu pixel
        self.wait(4)
        self.play(FadeIn(t2, shift=UP*0.2), run_time=1) # Câu feature
        self.wait(5)
        self.play(FadeIn(t3, shift=UP*0.2), run_time=1) # Câu biến thể
        self.wait(6) # Tổng ~38s
        
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:38 - 0:47: "PHẦN 7: UPGRADING DECODER — Nâng cấp Bộ giải mã"
        # ══════════════════════════════════════════════════════════════════════
        # Quét sạch màn hình
        self.play(FadeOut(title), FadeOut(takeaways_title), FadeOut(takeaways), run_time=1)
        
        # Tạo hiệu ứng vạch kẻ phân cách hoành tráng
        divider = Line(LEFT*6, RIGHT*6, color=ACCENT_COLOR, stroke_width=4)
        self.play(GrowFromCenter(divider), run_time=1)
        
        # Bật tiêu đề Phần 7
        part7_main = safe_text("UPGRADING DECODER", font_size=48, color=YELLOW, weight=BOLD).next_to(divider, UP, buff=0.4)
        part7_sub = safe_text("Nâng cấp Bộ giải mã", font_size=32, color=WHITE).next_to(divider, DOWN, buff=0.4)
        
        self.play(Write(part7_main), run_time=2)
        self.play(FadeIn(part7_sub, shift=UP*0.2), run_time=2)
        
        self.wait(2) # Tổng 47s kết thúc audio

class S7_01_SlotDecodingDilemma(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:07: "Decoder đóng vai trò tái tạo ảnh từ slot 
        # representations. Tuy nhiên tồn tại Slot-Decoding Dilemma, một trong 
        # những vấn đề cốt lõi nhất."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Slot-Decoding Dilemma (Nghịch lý Decoder)")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # Đặt trụ bập bênh (Pivot) và thanh xà (Beam) ngay từ đầu để set up context
        beam = Line(LEFT * 4.5, RIGHT * 4.5, color=YELLOW_C, stroke_width=8).shift(DOWN * 1.5)
        pivot = Triangle(color=YELLOW_C).scale(0.5).rotate(PI).next_to(beam, DOWN, buff=0)
        self.play(FadeIn(pivot), GrowFromCenter(beam), run_time=1.5)
        self.wait(4.5) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:07 - 0:17: "Decoder yếu như Spatial Broadcast Network có 
        # capacity hạn chế, buộc slot phải tập trung vào object riêng biệt, tạo 
        # object disentanglement tốt nhưng ảnh bị mờ và thiếu chi tiết."
        # ══════════════════════════════════════════════════════════════════════
        # Khối bên Trái (Decoder Yếu)
        left_slots = slot_stack(["obj 1", "obj 2", "bg"], [RED_C, GREEN_C, BLUE_C], radius=0.25)
        weak = labeled_box("Decoder Yếu\n(Ít Capacity)", width=1.8, height=1.0, color=GREY_B, font_size=16)
        blurry = simple_image().set_opacity(0.3) # Làm mờ ảnh
        
        left_group = VGroup(left_slots, weak, blurry).arrange(RIGHT, buff=0.6)
        left_label = safe_text("Slot tách tốt (v)\nẢnh mờ (x)", font_size=18, color=GREEN_C).next_to(left_group, DOWN, buff=0.2)
        
        arr1 = Arrow(left_slots.get_right(), weak.get_left(), buff=0.1, color=WHITE, stroke_width=5)
        arr2 = Arrow(weak.get_right(), blurry.get_left(), buff=0.1, color=WHITE, stroke_width=5)
        
        left_full = VGroup(left_group, left_label, arr1, arr2).next_to(beam.get_left(), UP, buff=0.1).shift(RIGHT*1.5)
        
        # Animation xuất hiện
        self.play(FadeIn(left_slots), run_time=1)
        self.play(GrowArrow(arr1), FadeIn(weak), run_time=1)
        self.play(GrowArrow(arr2), FadeIn(blurry), run_time=1.5)
        
        # Nhấn mạnh chữ Mờ
        self.play(Write(left_label), blurry.animate.set_color(GREY_E), run_time=1.5)
        
        # Bập bênh nghiêng nặng về bên trái
        self.play(
            Rotate(beam, angle=0.15, about_point=pivot.get_top()),
            Rotate(left_full, angle=0.15, about_point=pivot.get_top()),
            run_time=1.5
        )
        self.wait(3.5) # Tổng ~10s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:17 - 0:26: "Decoder mạnh như CNN decoder có thể tự tái tạo 
        # ảnh đẹp mà không cần thông tin cấu trúc từ slot, khiến slot mất tính 
        # object-centric."
        # ══════════════════════════════════════════════════════════════════════
        # Khối bên Phải (Decoder Mạnh)
        # Tạo mớ hỗn độn (Rối loạn)
        tangled = VGroup(
            Circle(radius=0.3, color=RED_C).set_fill(RED_C, opacity=0.4),
            Circle(radius=0.3, color=BLUE_C).set_fill(BLUE_C, opacity=0.4).shift(RIGHT*0.2 + UP*0.1),
            Circle(radius=0.3, color=GREEN_C).set_fill(GREEN_C, opacity=0.4).shift(RIGHT*0.1 + DOWN*0.2),
        )
        tangled_text = safe_text("Rối", font_size=14, color=WHITE).move_to(tangled)
        tangled_slots = VGroup(tangled, tangled_text)
        
        strong = labeled_box("Decoder Mạnh\n(Tự tái tạo)", width=1.8, height=1.0, color=MAROON_C, font_size=16)
        sharp = simple_image() # Ảnh sắc nét
        
        # Bập bênh trở lại cân bằng để đặt khối phải lên
        self.play(
            Rotate(beam, angle=-0.15, about_point=pivot.get_top()),
            Rotate(left_full, angle=-0.15, about_point=pivot.get_top()),
            run_time=0.5
        )
        
        right_group = VGroup(tangled_slots, strong, sharp).arrange(RIGHT, buff=0.6)
        right_label = safe_text("Slot rối (x)\nẢnh sắc nét (v)", font_size=18, color=RED_C).next_to(right_group, DOWN, buff=0.2)
        
        arr3 = Arrow(tangled_slots.get_right(), strong.get_left(), buff=0.1, color=WHITE, stroke_width=5)
        arr4 = Arrow(strong.get_right(), sharp.get_left(), buff=0.1, color=WHITE, stroke_width=5)
        
        right_full = VGroup(right_group, right_label, arr3, arr4).next_to(beam.get_right(), UP, buff=0.1).shift(LEFT*1.5)
        
        self.play(FadeIn(tangled_slots), run_time=1)
        self.play(GrowArrow(arr3), FadeIn(strong), run_time=1)
        self.play(GrowArrow(arr4), FadeIn(sharp), run_time=1.5)
        self.play(Write(right_label), run_time=1.5)
        
        # Nhấn mạnh sự tự tái tạo (Mũi tên cong che mặt slot)
        bypass = CurvedArrow(tangled_slots.get_top(), sharp.get_top(), angle=-PI/2, color=RED_C)
        bypass_text = safe_text("Bỏ qua cấu trúc", font_size=15, color=RED_C).next_to(bypass, UP, buff=0.1)
        self.play(Create(bypass), Write(bypass_text), run_time=1.5)
        self.wait(2) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:26 - 0:34: "Nghịch lý: decoder yếu thì slot tốt nhưng ảnh mờ, 
        # decoder mạnh thì ảnh đẹp nhưng slot mất object-centric."
        # ══════════════════════════════════════════════════════════════════════
        # Hiệu ứng bập bênh liên tục (Seesaw Effect)
        all_right = VGroup(right_full, bypass, bypass_text)
        
        self.play(
            Rotate(beam, angle=0.1, about_point=pivot.get_top()),
            Rotate(left_full, angle=0.1, about_point=pivot.get_top()),
            Rotate(all_right, angle=0.1, about_point=pivot.get_top()),
            run_time=1.5
        )
        self.play(
            Rotate(beam, angle=-0.2, about_point=pivot.get_top()),
            Rotate(left_full, angle=-0.2, about_point=pivot.get_top()),
            Rotate(all_right, angle=-0.2, about_point=pivot.get_top()),
            run_time=2
        )
        self.play(
            Rotate(beam, angle=0.1, about_point=pivot.get_top()),
            Rotate(left_full, angle=0.1, about_point=pivot.get_top()),
            Rotate(all_right, angle=0.1, about_point=pivot.get_top()),
            run_time=1.5
        )
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:34 - 0:39: "Giải pháp: phải thay đổi cách tiếp cận hoàn toàn."
        # ══════════════════════════════════════════════════════════════════════
        # Nổ tung/Dọn sạch bập bênh
        self.play(FadeOut(beam), FadeOut(pivot), FadeOut(left_full), FadeOut(all_right), FadeOut(arr1), FadeOut(arr2), FadeOut(arr3), FadeOut(arr4), run_time=1.5)
        
        solution = safe_text("=> Cần thay đổi kiến trúc Decoder hoàn toàn!", font_size=28, color=YELLOW, weight=BOLD)
        self.play(Write(solution), run_time=1.5)
        self.play(Wiggle(solution))
        self.wait(1) # Tổng ~5s

class S7_02_PixelIndependence(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "Pixel-mixture decoder còn gặp vấn đề Pixel 
        # Independence: mỗi pixel được tái tạo độc lập qua alpha compositing, 
        # không phụ thuộc pixel khác."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Vấn đề: Pixel Independence")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # Tạo lưới pixel độc lập
        pixel_grid = VGroup(*[
            Square(side_length=0.3, color=WHITE, stroke_width=1).set_fill([RED_C, BLUE_C, GREEN_C, YELLOW_C][(i + j) % 4], opacity=0.8)
            for i in range(5) for j in range(5)
        ]).arrange_in_grid(5, 5, buff=0.05).shift(LEFT * 4 + UP * 0.5)
        
        # Mọc lên rời rạc để nhấn mạnh tính "độc lập"
        import random
        random.seed(10)
        pixels_shuffled = list(pixel_grid)
        random.shuffle(pixels_shuffled)
        
        ind_label = safe_text("Tái tạo độc lập\n(Alpha Compositing)", font_size=22, color=RED_C).next_to(pixel_grid, DOWN, buff=0.3)
        
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pixels_shuffled], lag_ratio=0.05), run_time=1)
        self.play(Write(ind_label), run_time=1)
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:17: "Vấn đề trở nên nghiêm trọng khi muốn dùng slot 
        # như concept modules để tạo scene mới, giống word embedding trong DALL-E."
        # ══════════════════════════════════════════════════════════════════════
        # Các Concept Modules (Như các khối Lego / Word embeddings)
        concept_title = safe_text("Slot như Concept Modules (GenAI)", font_size=24, color=YELLOW_C).shift(RIGHT * 3 + UP * 2.2)
        
        slot_a = labeled_box("Slot A\n(Đầu tròn)", width=1.4, height=0.9, color=RED_C, font_size=16)
        slot_b = labeled_box("Slot B\n(Thân vuông)", width=1.4, height=0.9, color=BLUE_C, font_size=16)
        slot_c = labeled_box("Slot C\n(Chân tam giác)", width=1.6, height=0.9, color=GREEN_C, font_size=16)
        
        slots_group = VGroup(slot_a, slot_b, slot_c).arrange(RIGHT, buff=0.2).next_to(concept_title, DOWN, buff=0.5)
        
        self.play(Write(concept_title), run_time=1)
        self.play(FadeIn(slots_group, shift=DOWN*0.2), run_time=1)
        
        # Các mũi tên hội tụ để chuẩn bị mix
        mix_point = slot_b.get_bottom() + DOWN * 1.8
        dummy_circle = Circle(radius=0.9).move_to(mix_point)
        arrows_mix = VGroup(*[Arrow(s.get_bottom(), dummy_circle.get_boundary_point(s.get_bottom() - mix_point), buff=0.1, color=WHITE, stroke_width=4) for s in slots_group])
        self.play(GrowArrow(arrows_mix[0]), GrowArrow(arrows_mix[1]), GrowArrow(arrows_mix[2]), run_time=1)
        self.wait(4) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:17 - 0:25: "Khi decode slot từ các ảnh khác nhau, kết quả là 
        # superposition đơn giản không có global semantic consistency, tạo ra 
        # Frankenstein-like images."
        # ══════════════════════════════════════════════════════════════════════
        # Tạo quái vật Frankenstein do superposition lộn xộn
        head = Circle(radius=0.4, color=RED_C).set_fill(RED_E, opacity=0.8).shift(LEFT*0.2)
        body = Square(side_length=0.7, color=BLUE_C).set_fill(BLUE_E, opacity=0.8).shift(RIGHT*0.2 + DOWN*0.2)
        leg = Triangle(color=GREEN_C).set_fill(GREEN_E, opacity=0.8).rotate(PI/4).shift(LEFT*0.1 + DOWN*0.5)
        
        frankenstein = VGroup(body, leg, head).move_to(mix_point) # Đè lên nhau vô lý
        
        frank_label = safe_text("Frankenstein-like Image\n(Thiếu Global Consistency)", font_size=20, color=RED_C, weight=BOLD).next_to(frankenstein, DOWN, buff=0.3)
        cross_frank = crossmark_vector(color=RED_C, size=0.5).move_to(frankenstein)
        
        self.play(FadeIn(frankenstein, scale=1.5), run_time=1)
        self.play(Write(frank_label), Create(cross_frank), run_time=1)
        self.play(Wiggle(frankenstein), run_time=1)
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:25 - 0:33: "Autoregressive decoder như Image GPT tạo được 
        # global consistency nhưng đòi hỏi text supervision, trong khi mục tiêu 
        # là unsupervised."
        # ══════════════════════════════════════════════════════════════════════
        # Dọn sạch góc trái để minh hoạ Autoregressive
        self.play(FadeOut(pixel_grid), FadeOut(ind_label), run_time=1)
        
        auto_title = safe_text("Autoregressive (VD: Image GPT)", font_size=24, color=GREEN_C).shift(LEFT * 4 + UP * 2.2)
        
        # Mắt xích Autoregressive
        tokens = VGroup(*[Square(side_length=0.4, color=TEAL_C, stroke_width=2).set_fill(TEAL_C, opacity=0.3 + i*0.1) for i in range(5)]).arrange(RIGHT, buff=0.3)
        tokens.next_to(auto_title, DOWN, buff=1.0)
        
        chain = VGroup(*[Arrow(tokens[i].get_right(), tokens[i+1].get_left(), buff=0.05, color=YELLOW) for i in range(4)])
        
        auto_label = safe_text("Có Global Consistency (v)", font_size=20, color=GREEN_C).next_to(tokens, DOWN, buff=0.3)
        
        self.play(Write(auto_title), FadeIn(tokens, shift=RIGHT*0.2), FadeIn(chain), run_time=1)
        self.play(Write(auto_label), run_time=1)
        
        # Mâu thuẫn: Cần Text Supervision (Gạch chéo vì ta cần Unsupervised)
        text_sup = labeled_box("Cần Text Supervision", width=2.4, height=0.8, color=RED_C, font_size=18).next_to(auto_label, DOWN, buff=0.5)
        cross_sup = crossmark_vector(color=RED_C, size=0.4).next_to(text_sup, RIGHT)
        req_text = safe_text("Mục tiêu của OCL: Unsupervised", font_size=20, color=YELLOW, weight=BOLD).next_to(text_sup, DOWN, buff=0.2)
        
        self.play(FadeIn(text_sup, shift=UP*0.2), run_time=1)
        self.play(Create(cross_sup), Write(req_text), run_time=1)
        self.wait(2) # Tổng ~8s (Kết thúc 33s)
        
class S7_03_TwoDirections(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:07: "Slot-Decoding Dilemma có hai hướng giải quyết 
        # theo Tutorial CVPR 2024."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("2 Hướng giải quyết Slot-Decoding Dilemma")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        cvpr_badge = safe_text("(Theo CVPR 2024 Tutorial)", font_size=18, color=YELLOW_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(cvpr_badge), run_time=1)
        
        # Node gốc (Dilemma)
        root = labeled_box("Slot-Decoding\nDilemma", width=2.4, height=1.0, color=RED_C, font_size=20).shift(LEFT * 4.5)
        self.play(FadeIn(root, scale=1.2), run_time=1)
        self.wait(3.5) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:07 - 0:17: "Hướng 1: 3D Inductive Bias — giữ decoder vừa phải 
        # nhưng cung cấp thêm thông tin hình học 3D. Mô hình tiêu biểu: ObSuRF dùng 
        # NeRF-based decoder, OSRT dùng Slot Mixer Decoder."
        # ══════════════════════════════════════════════════════════════════════
        # Nhánh 1: 3D Inductive Bias (Trực quan 3D)
        branch_3d = labeled_box("Hướng 1:\n3D Inductive Bias", width=2.4, height=1.0, color=TEAL_C, font_size=18).shift(LEFT * 0.5 + UP * 1.8)
        arrow_3d = Arrow(root.get_right(), branch_3d.get_left(), buff=0.2, color=TEAL_C)
        
        self.play(GrowArrow(arrow_3d), FadeIn(branch_3d, shift=RIGHT*0.3), run_time=1)
        self.wait(4)

        # Các mô hình tiêu biểu
        models_3d = VGroup(
            safe_text("• ObSuRF (NeRF)", font_size=16, color=TEAL_C),
            safe_text("• OSRT (Slot Mixer)", font_size=16, color=TEAL_C)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(branch_3d, DOWN, buff=0.3)
        
        self.play(Write(models_3d), run_time=1)
        self.wait(6) # Tổng ~10s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:17 - 0:24: "Điểm chung: dùng camera pose và ray direction 
        # làm inductive bias."
        # ══════════════════════════════════════════════════════════════════════
        # Minh hoạ Camera và Tia sáng (Ray)
        cam_icon = VGroup(
            Rectangle(width=0.6, height=0.4, color=WHITE).set_fill(GREY_D, opacity=1),
            Polygon(RIGHT*0.3, RIGHT*0.6+UP*0.3, RIGHT*0.6+DOWN*0.3, color=WHITE).set_fill(GREY_D, opacity=1)
        ).shift(RIGHT * 3.5 + UP * 2.2)
        
        # Vẽ một khối lập phương 3D (Cube)
        cube = Square(side_length=0.8, color=TEAL_C).set_fill(TEAL_E, opacity=0.3).shift(RIGHT * 5.5 + UP * 1.5)
        cube_back = Square(side_length=0.8, color=TEAL_C).shift(RIGHT * 5.7 + UP * 1.7)
        lines = VGroup(*[Line(cube.get_vertices()[i], cube_back.get_vertices()[i], color=TEAL_C) for i in range(4)])
        cube_3d = VGroup(cube_back, lines, cube)
        
        # Tia sáng từ Camera chiếu vào vật thể
        ray = DashedLine(cam_icon.get_right(), cube_3d.get_left(), color=YELLOW_C)
        ray_text = safe_text("Camera Pose &\nRay Direction", font_size=14, color=YELLOW_C).next_to(ray, DOWN, buff=0.1).shift(LEFT * 0.6)
        
        self.play(FadeIn(cam_icon, shift=RIGHT*0.2), FadeIn(cube_3d), run_time=1)
        self.play(Create(ray), Write(ray_text), run_time=1)
        self.wait(4) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:24 - 0:36: "Hướng 2: Decoupling Decoding — tách decoding 
        # thành nhiều giai đoạn, decode qua ngôn ngữ trung gian. Mô hình tiêu biểu: 
        # SLATE dùng VQ tokens và Transformer, LSD dùng latent diffusion, DORSAL 
        # dùng multiview diffusion."
        # ══════════════════════════════════════════════════════════════════════
        # Nhánh 2: Decoupling Decoding (Tách giai đoạn)
        branch_decouple = labeled_box("Hướng 2:\nDecoupling Decoding", width=2.4, height=1.0, color=BLUE_C, font_size=18).shift(LEFT * 0.5 + DOWN * 1.2)
        arrow_decouple = Arrow(root.get_right(), branch_decouple.get_left(), buff=0.2, color=BLUE_C)
        
        self.play(GrowArrow(arrow_decouple), FadeIn(branch_decouple, shift=RIGHT*0.3), run_time=1)
        
        # Decode qua "ngôn ngữ trung gian" (Token)
        tokens = feature_grid(2, 5, cell=0.25, color=BLUE_C).next_to(branch_decouple, RIGHT, buff=0.8)
        arr_token = Arrow(branch_decouple.get_right(), tokens.get_left(), color=GREY_B)
        token_label = safe_text("Ngôn ngữ trung gian\n(VD: Discrete Tokens)", font_size=14, color=BLUE_B).next_to(tokens, UP, buff=0.1)
        
        self.play(GrowArrow(arr_token), FadeIn(tokens, shift=RIGHT*0.2), Write(token_label), run_time=1)
        self.wait(3)

        # Các mô hình tiêu biểu
        models_dec = VGroup(
            safe_text("• SLATE (Transformer)", font_size=16, color=BLUE_C),
            safe_text("• LSD (Diffusion)", font_size=16, color=BLUE_C),
            safe_text("• DORSAL (Multiview Diff)", font_size=16, color=BLUE_C)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(branch_decouple, DOWN, buff=0.3)
        
        self.play(Write(models_dec), run_time=1)
        self.wait(5.5) # Tổng ~12s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:36 - 0:45: "Điểm chung: tách riêng slot learning và image 
        # generation để giảm độ phức tạp."
        # ══════════════════════════════════════════════════════════════════════
        # Khối Generation
        gen_box = labeled_box("Image\nGeneration", width=1.5, height=0.8, color=PURPLE_C, font_size=16).next_to(tokens, RIGHT, buff=0.8)
        arr_gen = Arrow(tokens.get_right(), gen_box.get_left(), color=GREY_B)
        
        self.play(GrowArrow(arr_gen), FadeIn(gen_box, shift=RIGHT*0.2), run_time=1)
        
        # Nét đứt phân tách 2 mảng rõ ràng (Slot Learning | Image Generation)
        separator = DashedLine(gen_box.get_top() + UP*1.0 + LEFT*1.2, gen_box.get_bottom() + DOWN*1.0 + LEFT*1.2, color=RED_C)
        sep_text_left = safe_text("Slot Learning", font_size=14, color=BLUE_C, weight=BOLD).next_to(separator, LEFT, buff=0.2).shift(DOWN*0.5)
        sep_text_right = safe_text("Generation", font_size=14, color=PURPLE_C, weight=BOLD).next_to(separator, RIGHT, buff=0.2).shift(DOWN*0.5)
        
        self.play(Create(separator), Write(sep_text_left), Write(sep_text_right), run_time=1)
        
        # Chốt: Giảm độ phức tạp
        reduce_badge = safe_text("-> Giảm độ phức tạp", font_size=18, color=YELLOW, weight=BOLD).next_to(gen_box, DOWN, buff=0.5)
        self.play(Write(reduce_badge), run_time=1)
        self.wait(4.5) # Tổng ~9s

class S7_04_MLPvsTransformer(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:04: "DINOSAUR đề xuất hai loại decoder."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("DINOSAUR: Hai loại Decoder")
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        self.wait(2.5) # Tổng 4s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:04 - 0:13: "MLP Decoder xử lý từng slot độc lập: broadcast 
        # slot ra N tokens, cộng learned positional encoding, dùng shared MLP 
        # tạo reconstruction và alpha map, rồi weighted sum."
        # ══════════════════════════════════════════════════════════════════════
        # 1. Pipeline của MLP Decoder (Nửa trên màn hình)
        mlp_title = safe_text("1. MLP Decoder (Độc lập, Song song)", font_size=20, color=GREEN_C, weight=BOLD).to_edge(LEFT).shift(UP * 2.5 + RIGHT*0.5)
        self.play(Write(mlp_title), run_time=1)

        # Các thành phần MLP
        slots_mlp = slot_stack(["s1", "s2"], [RED_C, GREEN_C], radius=0.25).next_to(mlp_title, DOWN, buff=0.3).align_to(mlp_title, LEFT)
        
        # Broadcast & PE
        bc_pe = labeled_box("Broadcast\n+ P.E.", width=1.5, height=0.8, color=TEAL_C, font_size=16).next_to(slots_mlp, RIGHT, buff=0.4)
        arr1 = Arrow(slots_mlp.get_right(), bc_pe.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        # Shared MLP
        shared_mlp = labeled_box("Shared MLP", width=1.5, height=0.8, color=GREEN_C, font_size=16).next_to(bc_pe, RIGHT, buff=0.4)
        arr2 = Arrow(bc_pe.get_right(), shared_mlp.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        # Recon & Alpha -> Weighted Sum
        out_group = VGroup(
            safe_text("Recon", font_size=14, color=WHITE),
            safe_text("Alpha Map", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.2).next_to(shared_mlp, RIGHT, buff=0.4)
        arr3 = Arrow(shared_mlp.get_right(), out_group.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        sum_box = labeled_box("Weighted\nSum", width=1.2, height=0.8, color=YELLOW_D, font_size=16).next_to(out_group, RIGHT, buff=0.4)
        arr4 = Arrow(out_group.get_right(), sum_box.get_left(), buff=0.1, color=WHITE, stroke_width=4)

        self.play(FadeIn(slots_mlp), GrowArrow(arr1), FadeIn(bc_pe), run_time=2)
        self.play(GrowArrow(arr2), FadeIn(shared_mlp), run_time=2)
        self.play(GrowArrow(arr3), FadeIn(out_group), GrowArrow(arr4), FadeIn(sum_box), run_time=2)
        self.wait(2) # Tổng 9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:13 - 0:21: "Ưu điểm: tính toán cực kỳ hiệu quả nhờ chia sẻ 
        # weights, tốt cho instance-level separation với ARI scores cao hơn."
        # ══════════════════════════════════════════════════════════════════════
        # Highlight chữ Shared MLP
        self.play(shared_mlp[0].animate.set_fill(GREEN_E, opacity=0.8), run_time=1)
        
        mlp_pros = VGroup(
            VGroup(checkmark_vector(color=GREEN_C, size=0.2), safe_text("Tính toán cực kỳ hiệu quả", font_size=16)).arrange(RIGHT, buff=0.1),
            VGroup(checkmark_vector(color=GREEN_C, size=0.2), safe_text("Instance-level separation (ARI cao)", font_size=16)).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(sum_box, RIGHT, buff=0.5)

        self.play(FadeIn(mlp_pros[0], shift=LEFT*0.2), run_time=2)
        self.play(FadeIn(mlp_pros[1], shift=LEFT*0.2), run_time=2)
        self.wait(3) # Tổng 8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:21 - 0:28: "Transformer Decoder reconstruct autoregressive: 
        # feature tại vị trí n điều kiện trên tất cả features trước đó và toàn bộ slots."
        # ══════════════════════════════════════════════════════════════════════
        # 2. Pipeline của Transformer Decoder (Nửa dưới màn hình)
        trans_title = safe_text("2. Transformer Decoder (Autoregressive)", font_size=20, color=PURPLE_C, weight=BOLD).to_edge(LEFT).shift(UP * 0.5 + RIGHT*0.5)
        self.play(Write(trans_title), run_time=1)

        slots_trans = slot_stack(["s1", "s2", "s3"], [RED_C, GREEN_C, BLUE_C], radius=0.2).next_to(trans_title, DOWN, buff=0.3).align_to(trans_title, LEFT)
        
        trans_box = labeled_box("Transformer", width=2.0, height=0.8, color=PURPLE_C, font_size=16).next_to(slots_trans, RIGHT, buff=0.4)
        arr5 = Arrow(slots_trans.get_right(), trans_box.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        # Mô phỏng Autoregressive (Pixel n phụ thuộc pixel trước)
        tokens = VGroup(*[Square(side_length=0.3, color=PURPLE_C).set_fill(PURPLE_C, opacity=0.5) for _ in range(5)]).arrange(RIGHT, buff=0.2).next_to(trans_box, RIGHT, buff=0.5)
        
        self.play(FadeIn(slots_trans), GrowArrow(arr5), FadeIn(trans_box), run_time=2)
        
        # Mọc ra từng token và mũi tên vòng vèo (điều kiện)
        self.play(FadeIn(tokens[0]), run_time=0.5)
        arr_conds = VGroup()
        for i in range(4):
            arr_cond = CurvedArrow(tokens[i].get_top(), tokens[i+1].get_top(), angle=-PI/2, color=YELLOW, tip_length=0.15)
            arr_conds.add(arr_cond)
            self.play(Create(arr_cond), FadeIn(tokens[i+1]), run_time=0.5)
        
        self.wait(1.5) # Tổng 7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:28 - 0:37: "Ưu điểm: mask chặt hơn, background separation 
        # sạch hơn, cải thiện 9-10 class mBO trên PASCAL và COCO."
        # ══════════════════════════════════════════════════════════════════════
        trans_pros = VGroup(
            VGroup(checkmark_vector(color=GREEN_C, size=0.2), safe_text("Mask chặt, sạch Background", font_size=16)).arrange(RIGHT, buff=0.1),
            VGroup(checkmark_vector(color=GREEN_C, size=0.2), safe_text("Cải thiện mBO (PASCAL/COCO)", font_size=16)).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tokens, RIGHT, buff=0.5).align_to(mlp_pros, LEFT)

        self.play(FadeIn(trans_pros[0], shift=LEFT*0.2), run_time=2)
        self.play(FadeIn(trans_pros[1], shift=LEFT*0.2), run_time=2)
        self.wait(5) # Tổng 9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:37 - 0:43: "Tuy nhiên có xu hướng dùng excess slots tách 
        # object thành nhiều phần."
        # ══════════════════════════════════════════════════════════════════════
        # Minh hoạ phân mảnh object
        con_group = VGroup()
        cross = crossmark_vector(color=RED_C, size=0.2)
        con_text = safe_text("Nhược điểm: Tách vụn object (Excess slots)", font_size=16, color=RED_C)
        con_label = VGroup(cross, con_text).arrange(RIGHT, buff=0.1)
        
        # Hình tròn bị nứt làm 3 mảnh
        frag_obj = VGroup(
            Arc(radius=0.3, start_angle=0, angle=PI*0.6, color=RED_C).set_fill(RED_C, opacity=0.8),
            Arc(radius=0.3, start_angle=PI*0.6, angle=PI*0.8, color=RED_C).set_fill(RED_C, opacity=0.8),
            Arc(radius=0.3, start_angle=PI*1.4, angle=PI*0.6, color=RED_C).set_fill(RED_C, opacity=0.8)
        ).arrange(RIGHT, buff=0.05).scale(0.8)
        
        con_group.add(con_label, frag_obj).arrange(DOWN, buff=0.1).next_to(trans_pros, DOWN, buff=0.2).align_to(trans_pros, LEFT)

        self.play(FadeIn(con_label), run_time=1.5)
        # Nổ tung object ra xíu
        self.play(FadeIn(frag_obj), frag_obj[0].animate.shift(UR*0.1), frag_obj[1].animate.shift(LEFT*0.1), frag_obj[2].animate.shift(DR*0.1), run_time=2.5)
        self.wait(2) # Tổng 6s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:43 - 0:51: "Khuyến nghị: MLP decoder làm first choice vì 
        # đơn giản và ổn định, Transformer decoder khi cần semantic grouping."
        # ══════════════════════════════════════════════════════════════════════
        # Hiển thị luôn Khuyến nghị mà không làm mờ Transformer
        
        recommend_box = labeled_box("Khuyến nghị (First Choice):\nMLP Decoder (Đơn giản, Ổn định)", width=5.5, height=0.8, color=YELLOW, font_size=20)
        recommend_box.to_edge(DOWN).shift(UP * 0.3)
        
        trans_note = safe_text("(*Dùng Transformer khi cần Semantic Grouping mạnh)", font_size=14, color=PURPLE_B).next_to(recommend_box, UP, buff=0.1)

        self.play(FadeIn(recommend_box, shift=UP*0.2), FadeIn(trans_note), run_time=2)
        self.play(Wiggle(recommend_box), run_time=1)
        self.wait(3.5) # Chờ kết thúc (Tổng 8s)

class S7_05_SLATEDecoder(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:06: "SLATE giải quyết cả Slot-Decoding Dilemma lẫn 
        # Pixel Independence bằng ngôn ngữ trung gian."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("SLATE Decoder: Trạm trung chuyển Token")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        intro_text = safe_text("Giải pháp: Decode qua ngôn ngữ trung gian", font_size=20, color=YELLOW_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(intro_text), run_time=1.5)
        self.wait(3.5) # Tổng ~6s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:06 - 0:14: "Bước 1: DVAE Tokenization chia ảnh thành patch, 
        # gán mỗi patch một discrete token qua Gumbel-Softmax."
        # ══════════════════════════════════════════════════════════════════════
        # Pipeline sắp xếp phía trên màn hình
        image = simple_image(width=1.0, height=0.7).shift(LEFT * 5.5 + UP * 1)
        
        dvae = labeled_box("DVAE", width=1.2, height=0.7, color=TEAL_C, font_size=16).next_to(image, RIGHT, buff=0.6)
        arr1 = Arrow(image.get_right(), dvae.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        # Discrete Tokens (Các ô màu rõ rệt, không bị hòa trộn)
        tokens = feature_grid(2, 4, cell=0.25, color=YELLOW_D).next_to(dvae, RIGHT, buff=0.6)
        tokens[0].set_fill(RED_C); tokens[1].set_fill(BLUE_C); tokens[2].set_fill(GREEN_C) # Tô màu khác nhau để thành Discrete
        arr2 = Arrow(dvae.get_right(), tokens.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        token_label = safe_text("Discrete Tokens\n(Gumbel-Softmax)", font_size=14, color=YELLOW).next_to(tokens, UP, buff=0.2)
        
        self.play(FadeIn(image), run_time=1)
        self.play(GrowArrow(arr1), FadeIn(dvae), run_time=2)
        self.play(GrowArrow(arr2), FadeIn(tokens), Write(token_label), run_time=3)
        self.wait(2) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:14 - 0:21: "Bước 2: Slot Attention trên token space, mỗi 
        # token map qua learned dictionary thành embedding, tạo ra object slots 
        # và attention maps."
        # ══════════════════════════════════════════════════════════════════════
        sa_box = labeled_box("Slot\nAttention", width=1.2, height=0.7, color=BLUE_C, font_size=16).next_to(tokens, RIGHT, buff=0.6)
        arr3 = Arrow(tokens.get_right(), sa_box.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        slots = slot_stack(["s1", "s2", "s3"], [RED_C, BLUE_C, GREEN_C], radius=0.2).next_to(sa_box, RIGHT, buff=0.6)
        arr4 = Arrow(sa_box.get_right(), slots.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        self.play(GrowArrow(arr3), FadeIn(sa_box), run_time=2.5)
        self.play(GrowArrow(arr4), FadeIn(slots), run_time=2.5)
        self.wait(2) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:21 - 0:28: "Bước 3: Transformer decoder reconstruct lại sequence 
        # tokens theo cách autoregressive, với cross-entropy loss."
        # ══════════════════════════════════════════════════════════════════════
        transformer = labeled_box("Transformer\nDecoder", width=1.5, height=0.7, color=PURPLE_C, font_size=14).next_to(slots, RIGHT, buff=0.6)
        arr5 = Arrow(slots.get_right(), transformer.get_left(), buff=0.1, color=WHITE, stroke_width=4)
        
        # Mũi tên cong biểu diễn Autoregressive sinh ngược ra token
        recon_arr = CurvedArrow(transformer.get_bottom(), tokens.get_bottom(), angle=-PI/2, color=PURPLE_C, tip_length=0.15)
        ce_loss = safe_text("Cross-Entropy Loss\n(Autoregressive)", font_size=14, color=PURPLE_B).next_to(recon_arr, DOWN, buff=0.1)
        
        self.play(GrowArrow(arr5), FadeIn(transformer), run_time=2)
        self.play(Create(recon_arr), Write(ce_loss), run_time=3)
        self.wait(2) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:28 - 0:38: "Thành tựu quan trọng nhất: Visual Concept Library. 
        # Sau khi train, dùng K-means clustering nhóm slots từ toàn bộ dataset 
        # thành visual concepts như tóc, mặt, object nền."
        # ══════════════════════════════════════════════════════════════════════
        # Dọn dẹp Pipeline nhường chỗ cho Phase 2 (Concept Library)
        self.play(FadeOut(VGroup(image, dvae, tokens, token_label, sa_box, slots, transformer, arr1, arr2, arr3, arr4, arr5, recon_arr, ce_loss)), run_time=1)
        
        library_title = safe_text("Visual Concept Library (Qua K-Means Clustering)", font_size=24, color=GREEN_C, weight=BOLD).shift(UP * 1.5)
        self.play(Write(library_title), run_time=1.5)
        
        # Tung các slot bay lộn xộn
        import random
        random.seed(42)
        random_slots = VGroup(*[Circle(radius=0.15, fill_color=random.choice([RED_C, BLUE_C, YELLOW_D]), fill_opacity=0.8, stroke_width=0).shift(LEFT*random.uniform(-4,4) + DOWN*random.uniform(0, 1.5)) for _ in range(15)])
        self.play(FadeIn(random_slots), run_time=1.5)
        
        # Tạo 3 cái hộp chứa (Clusters)
        cluster_hair = labeled_box("Tóc", width=1.5, height=1.0, color=YELLOW_D, fill_opacity=0.1, font_size=16).shift(LEFT * 3 + DOWN * 1)
        cluster_face = labeled_box("Mặt", width=1.5, height=1.0, color=RED_C, fill_opacity=0.1, font_size=16).shift(ORIGIN + DOWN * 1)
        cluster_bg = labeled_box("Nền", width=1.5, height=1.0, color=BLUE_C, fill_opacity=0.1, font_size=16).shift(RIGHT * 3 + DOWN * 1)
        
        for cluster in [cluster_hair, cluster_face, cluster_bg]:
            cluster[1].next_to(cluster[0].get_top(), DOWN, buff=0.1)
        
        self.play(FadeIn(cluster_hair), FadeIn(cluster_face), FadeIn(cluster_bg), run_time=2)
        
        # K-Means: Hút các slot vào đúng chuồng màu của nó
        animations = []
        for slot in random_slots:
            if slot.get_fill_color() == YELLOW_D: animations.append(slot.animate.move_to(cluster_hair.get_center() + DOWN*0.2))
            elif slot.get_fill_color() == RED_C: animations.append(slot.animate.move_to(cluster_face.get_center() + DOWN*0.2))
            else: animations.append(slot.animate.move_to(cluster_bg.get_center() + DOWN*0.2))
            
        self.play(*animations, run_time=2)
        self.wait(2) # Tổng ~10s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:38 - 0:48: "Để tạo ảnh mới, chọn slots từ các clusters khác 
        # nhau giống như chọn từ để tạo câu, cho phép zero-shot generation với 
        # global semantic consistency."
        # ══════════════════════════════════════════════════════════════════════
        # Rút từ mỗi ô 1 slot ra ghép thành "câu"
        pick_hair = Circle(radius=0.25, fill_color=YELLOW_D, fill_opacity=1, stroke_width=0)
        pick_face = Circle(radius=0.25, fill_color=RED_C, fill_opacity=1, stroke_width=0)
        pick_bg = Circle(radius=0.25, fill_color=BLUE_C, fill_opacity=1, stroke_width=0)
        
        plus1 = safe_text("+", font_size=24)
        plus2 = safe_text("+", font_size=24)
        equal = safe_text("=", font_size=24)
        
        # Create placeholders cho equation
        ph_hair = Circle(radius=0.25).set_opacity(0)
        ph_face = Circle(radius=0.25).set_opacity(0)
        ph_bg = Circle(radius=0.25).set_opacity(0)
        
        equation = VGroup(ph_hair, plus1, ph_face, plus2, ph_bg, equal).arrange(RIGHT, buff=0.3).shift(DOWN * 2.8 + LEFT * 1.5)
        
        pick_hair.move_to(cluster_hair.get_center() + DOWN*0.2)
        pick_face.move_to(cluster_face.get_center() + DOWN*0.2)
        pick_bg.move_to(cluster_bg.get_center() + DOWN*0.2)
        
        self.play(FadeIn(pick_hair), FadeIn(pick_face), FadeIn(pick_bg), run_time=0.5)
        
        # Mũi tên từ các hộp bay xuống phương trình
        self.play(
            pick_hair.animate.move_to(ph_hair.get_center()),
            pick_face.animate.move_to(ph_face.get_center()),
            pick_bg.animate.move_to(ph_bg.get_center()),
            FadeIn(plus1), FadeIn(plus2), FadeIn(equal),
            run_time=2.5
        )
        
        # Generation: Biến thành cái mặt (Face)
        gen_face = mini_face(scale=1.5).next_to(equal, RIGHT, buff=0.3)
        zero_shot_text = safe_text("Zero-shot Generation\n(Global Consistency)", font_size=16, color=GREEN_C, weight=BOLD).next_to(gen_face, RIGHT, buff=0.5)
        
        self.play(FadeIn(gen_face, shift=LEFT*0.5), run_time=2.5)
        self.play(Write(zero_shot_text), run_time=2)
        self.play(Wiggle(zero_shot_text), run_time=1)
        self.wait(2) # Tổng ~10s (Kết thúc ~48s)

class S7_06_DiffusionLSD(Scene):
    def construct(self):
        # Hàm hỗ trợ vẽ mũi tên chuẩn
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(
                start, end, 
                buff=0.1, 
                color=color, 
                stroke_width=4 # Nét vẽ to và đậm
            )

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "Latent Slot Diffusion (LSD) kết hợp Latent Diffusion 
        # Models với slot representations, đại diện thế hệ decoder mới nhất."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Latent Slot Diffusion (LSD)")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        subtitle = safe_text("Thế hệ Decoder mới nhất (LDM + Slots)", font_size=20, color=YELLOW_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(subtitle), run_time=1.5)
        self.wait(5.5) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:16: "Pre-trained Auto-Encoder nén ảnh thành latent 
        # representation ở không gian thấp hơn, giảm computational burden."
        # ══════════════════════════════════════════════════════════════════════
        # Bắt đầu luồng Pipeline
        image = simple_image(width=1.2, height=0.9)
        img_label = safe_text("Image", font_size=14, color=WHITE).next_to(image, DOWN)
        img_group = VGroup(image, img_label).shift(LEFT * 5.5 + DOWN * 0.5)
        
        encoder = labeled_box("Auto\nEncoder", width=1.4, height=0.9, color=TEAL_C, font_size=16)
        encoder.next_to(img_group, RIGHT, buff=0.6) # Khoảng cách rộng để mũi tên rõ
        arr1 = solid_arrow(img_group.get_right(), encoder.get_left())
        
        # Latent Representation (Vẽ nhỏ đi để thể hiện sự "Nén")
        latent = labeled_box("Latent\n(z0)", width=0.8, height=0.6, color=BLUE_C, font_size=14)
        latent.next_to(encoder, RIGHT, buff=0.6)
        arr2 = solid_arrow(encoder.get_right(), latent.get_left())
        
        compress_text = safe_text("Nén không gian\n(Giảm tính toán)", font_size=12, color=GREEN_C).next_to(latent, DOWN)

        self.play(FadeIn(img_group), run_time=1)
        self.play(GrowArrow(arr1), FadeIn(encoder), run_time=2)
        # Hiệu ứng thu nhỏ khi ra khỏi AE
        self.play(GrowArrow(arr2), FadeIn(latent, scale=0.5), Write(compress_text), run_time=2)
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:16 - 0:25: "Slot-Conditioned Diffusion denoise từ Gaussian 
        # noise thành latent có điều kiện trên slots, thay vì text embedding như LDM."
        # ══════════════════════════════════════════════════════════════════════
        # Thêm nhiễu
        import random
        noise_box = Rectangle(width=0.8, height=0.6, color=GREY_B).next_to(latent, RIGHT, buff=0.6)
        noise_dots = VGroup(*[Dot(radius=0.03, color=GREY_C).move_to(noise_box.get_center() + RIGHT*random.uniform(-0.3,0.3) + UP*random.uniform(-0.2,0.2)) for _ in range(15)])
        noisy_latent = VGroup(noise_box, noise_dots)
        
        noise_label = safe_text("Noisy\nLatent", font_size=14, color=GREY_B).next_to(noisy_latent, DOWN)
        arr3 = solid_arrow(latent.get_right(), noisy_latent.get_left())
        
        self.play(GrowArrow(arr3), FadeIn(noisy_latent), Write(noise_label), run_time=1.5)

        # Điều kiện (Conditioning): Text vs Slots
        text_cond = labeled_box("Text Embedding", width=1.6, height=0.5, color=GREY_C, font_size=14).shift(UP * 1.2 + RIGHT * 0.5)
        cross_text = crossmark_vector(color=RED_C, size=0.3).move_to(text_cond)
        
        slots = slot_stack(["obj", "face", "bg"], [RED_C, YELLOW_C, BLUE_C], radius=0.15).next_to(text_cond, RIGHT, buff=0.5)
        slot_label = safe_text("Object Slots", font_size=14, color=YELLOW_C, weight=BOLD).next_to(slots, UP, buff=0.1)

        self.play(FadeIn(text_cond), run_time=1.5)
        self.play(Create(cross_text), run_time=1) # Gạch bỏ text prompt
        self.play(FadeIn(slots, shift=LEFT*0.3), Write(slot_label), run_time=2)
        self.wait(3) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:25 - 0:30: "Denoising Network là biến thể UNet với 
        # slot-conditioned transformer."
        # ══════════════════════════════════════════════════════════════════════
        unet = labeled_box("LDM U-Net\n(Denoise)", width=1.6, height=1.0, color=PURPLE_C, font_size=16)
        unet.next_to(noisy_latent, RIGHT, buff=0.6)
        arr4 = solid_arrow(noisy_latent.get_right(), unet.get_left())
        
        # Mũi tên Cross-Attention từ Slots cắm xuống U-Net
        cond_arrow = solid_arrow(slots.get_bottom(), unet.get_top(), color=YELLOW_D)
        cross_attn = safe_text("Cross-Attention\n(Slot-Conditioned)", font_size=12, color=YELLOW_C).next_to(cond_arrow, RIGHT, buff=0.1)
        
        self.play(GrowArrow(arr4), FadeIn(unet), run_time=1.5)
        self.play(GrowArrow(cond_arrow), Write(cross_attn), run_time=2)
        self.wait(1.5) # Tổng ~5s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:30 - 0:38: "LSD kế thừa Visual Concept Library từ SLATE 
        # và mở ra khả năng editing: object removal, insertion, background swapping."
        # ══════════════════════════════════════════════════════════════════════
        output_img = simple_image(width=1.2, height=0.9)
        output_img.next_to(unet, RIGHT, buff=0.6)
        arr5 = solid_arrow(unet.get_right(), output_img.get_left())
        
        self.play(GrowArrow(arr5), FadeIn(output_img), run_time=1)
        
        # Bật lên các tính năng Editing
        edits = VGroup(
            safe_text("[-] Removal", font_size=14, color=RED_C),
            safe_text("[+] Insertion", font_size=14, color=GREEN_C),
            safe_text("[<->] BG Swap", font_size=14, color=BLUE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(output_img, DOWN, buff=0.2)
        
        self.play(LaggedStart(*[FadeIn(e, shift=UP*0.1) for e in edits], lag_ratio=0.3), run_time=3)
        self.wait(4) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:38 - 0:43: "Đặc biệt, LSD lần đầu cho phép face editing 
        # trên ảnh thực tế."
        # ══════════════════════════════════════════════════════════════════════
        # Nổi bật Face Editing
        face = mini_face(scale=1.2).next_to(output_img, RIGHT, buff=0.8)
        face_glow = Circle(radius=0.8, color=YELLOW_C).set_fill(YELLOW_E, opacity=0.3).move_to(face)
        
        face_text = safe_text("Đột phá:\nFace Editing\ntrên ảnh thực", font_size=16, color=YELLOW_D, weight=BOLD).next_to(face, DOWN, buff=0.2)
        
        self.play(FadeIn(face_glow, scale=0.5), FadeIn(face), run_time=1.5)
        self.play(Write(face_text), run_time=1)
        self.play(Wiggle(face_text), run_time=1)
        self.wait(1.5) # Tổng ~5s

class S7_07_DORSAL3D(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(
                start, end, 
                buff=0.1, 
                color=color, 
                stroke_width=4
            )

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "DORSAL đưa diffusion-based decoder lên 3D scene 
        # rendering. Thay vì tạo 2D image, DORSAL sinh multiple views của 3D scene 
        # có consistency không gian."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("DORSAL: 3D Scene Diffusion")
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(2)
        
        # So sánh 2D vs 3D ở ngay đầu video
        old_2d = labeled_box("2D Image", width=2.0, height=0.8, color=GREY_B, font_size=18).shift(LEFT*2.5 + UP*1.5)
        cross_2d = crossmark_vector(color=RED_C, size=0.3).next_to(old_2d, RIGHT)
        
        new_3d = labeled_box("3D Scene\n(Multiple Views, Consistency)", width=3.5, height=0.8, color=TEAL_C, font_size=18).shift(RIGHT*1.5 + UP*1.5)
        check_3d = checkmark_vector(color=GREEN_C, size=0.3).next_to(new_3d, RIGHT)
        
        intro_group = VGroup(old_2d, cross_2d, new_3d, check_3d)
        
        self.play(FadeIn(old_2d), FadeIn(new_3d), run_time=1)
        self.play(Create(cross_2d), Create(check_3d), run_time=1.5)
        self.wait(5) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:17: "Kiến trúc kết hợp OSRT encoder với Multiview U-Net 
        # diffusion model. Context views được encode thành scene representation, 
        # Slot Attention tạo Object Slots..."
        # ══════════════════════════════════════════════════════════════════════
        # Dọn dẹp phần Intro để vẽ Pipeline
        self.play(FadeOut(intro_group), run_time=1)
        
        # Context Views (Xếp chồng lệch nhau để tạo hiệu ứng nhiều ảnh)
        views = VGroup(*[simple_image(width=1.0, height=0.7).shift(RIGHT * i * 0.15 + UP * i * 0.1) for i in range(3)])
        views_label = safe_text("Context Views", font_size=14, color=GREY_B).next_to(views, DOWN)
        views_group = VGroup(views, views_label).shift(LEFT * 4.0 + DOWN * 0.5)
        
        self.play(FadeIn(views_group, shift=RIGHT*0.2), run_time=1)
        
        # OSRT Encoder
        osrt = labeled_box("OSRT Encoder\n(Scene Rep.)", width=1.6, height=0.9, color=TEAL_C, font_size=14)
        osrt.next_to(views_group, RIGHT, buff=0.8)
        arr1 = solid_arrow(views_group.get_right(), osrt.get_left())
        
        self.play(GrowArrow(arr1), FadeIn(osrt), run_time=1.5)
        
        # Nhảy lên tạo Object Slots
        slots = slot_stack(["obj1", "obj2", "bg"], [RED_C, GREEN_C, BLUE_C], radius=0.2)
        slots.next_to(osrt, UP, buff=0.8)
        slot_label = safe_text("Object Slots", font_size=14, color=YELLOW).next_to(slots, UP, buff=0.1)
        
        arr_up = solid_arrow(osrt.get_top(), slots.get_bottom(), color=YELLOW_D)
        
        self.play(GrowArrow(arr_up), FadeIn(slots), Write(slot_label), run_time=1.5)
        self.wait(2) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:17 - 0:25: "...rồi slots làm conditioning cho diffusion 
        # qua FiLM modulation và cross-attention."
        # ══════════════════════════════════════════════════════════════════════
        # U-Net Diffusion Model
        unet = labeled_box("Multiview\nU-Net Diffusion", width=1.8, height=1.0, color=PURPLE_C, font_size=14)
        unet.next_to(osrt, RIGHT, buff=1.0)
        
        arr2 = solid_arrow(osrt.get_right(), unet.get_left())
        self.play(GrowArrow(arr2), FadeIn(unet), run_time=1)
        
        # Conditioning: Slots bắn tín hiệu xuống U-Net
        cond_arrow = CurvedArrow(slots.get_right(), unet.get_top(), angle=-PI/3, color=YELLOW_C, stroke_width=4)
        cond_texts = VGroup(
            safe_text("FiLM Modulation", font_size=14, color=YELLOW_C),
            safe_text("& Cross-Attention", font_size=14, color=YELLOW_C)
        ).arrange(DOWN, buff=0.05).next_to(cond_arrow, UP, buff=0.1)
        
        self.play(Create(cond_arrow), run_time=1)
        self.play(Write(cond_texts), run_time=1.5)
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:25 - 0:35: "Trên cả MultiShapeNet và Street View thực tế, 
        # FID score tốt hơn OSRT rất nhiều, tạo ra ảnh sắc nét và realistic hơn."
        # ══════════════════════════════════════════════════════════════════════
        # Sinh ra nhiều views nhất quán
        outputs = VGroup(*[simple_image(width=0.85, height=0.55).rotate((i - 1) * 0.15) for i in range(3)]).arrange(DOWN, buff=0.05)
        outputs.next_to(unet, RIGHT, buff=0.8)
        out_label = safe_text("Consistent\nMultiple Views", font_size=14, color=GREEN_C).next_to(outputs, DOWN, buff=0.1)
        
        arr3 = solid_arrow(unet.get_right(), outputs.get_left())
        
        self.play(GrowArrow(arr3), FadeIn(outputs), Write(out_label), run_time=1.5)
        
        # Khung Đánh giá (FID Score)
        eval_box = Rectangle(width=6.0, height=0.9, color=ACCENT_COLOR).set_fill(BG_COLOR, opacity=1).to_edge(DOWN, buff=0.4)
        dataset_text = safe_text("Datasets: MultiShapeNet & Real Street View", font_size=14, color=GREY_B).move_to(eval_box.get_top() + DOWN*0.3)
        fid_text = safe_text("FID Score (Giảm: Sắc nét & Realistic hơn OSRT)", font_size=18, color=YELLOW_D, weight=BOLD).next_to(dataset_text, DOWN, buff=0.2)
        
        self.play(FadeIn(eval_box), Write(dataset_text), run_time=1.5)
        self.play(Write(fid_text), run_time=1)
        self.play(Wiggle(fid_text), run_time=1)
        self.wait(2) # Tổng ~10s

class S7_08_ObSuRF(Scene):
    def construct(self):
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:06: "ObSuRF là một trong những mô hình đầu tiên thay 
        # CNN decoder 2D bằng NeRF decoder 3D."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("ObSuRF: NeRF-based 3D Decoder")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # Mô tả ngắn quá trình thay đổi 2D -> 3D
        cnn_2d = safe_text("CNN Decoder 2D", font_size=24, color=RED_C).shift(LEFT * 3 + UP * 2.5)
        cross = crossmark_vector(color=RED_C, size=0.3).next_to(cnn_2d, RIGHT)
        nerf_3d = safe_text("NeRF Decoder 3D", font_size=24, color=TEAL_C, weight=BOLD).shift(RIGHT * 3 + UP * 2.5)
        check = checkmark_vector(color=GREEN_C, size=0.3).next_to(nerf_3d, RIGHT)
        
        self.play(FadeIn(cnn_2d), FadeIn(nerf_3d), run_time=1)
        self.play(Create(cross), Create(check), run_time=1.5)
        self.wait(2.5) # Tổng ~6s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:06 - 0:13: "Mỗi slot được map sang một NeRF độc lập, ánh xạ 
        # tọa độ 3D và viewing direction thành volume density và radiance."
        # ══════════════════════════════════════════════════════════════════════
        # Xóa dòng giải thích nhường chỗ cho Pipeline
        self.play(FadeOut(cnn_2d), FadeOut(cross), FadeOut(nerf_3d), FadeOut(check), run_time=0.5)

        # 1. Các Slots đầu vào
        slots = slot_stack(["s1", "s2", "s3"], [RED_C, GREEN_C, BLUE_C], radius=0.25).shift(LEFT * 4.5 + UP * 0.3)
        slot_label = safe_text("Object Slots", font_size=18, color=WHITE).next_to(slots, UP, buff=0.2)
        
        self.play(FadeIn(slots, shift=RIGHT*0.2), Write(slot_label), run_time=1)

        # 2. Map sang 3 khối NeRF 3D
        nerfs = VGroup()
        for color in [RED_C, GREEN_C, BLUE_C]:
            # Đoạn code tự vẽ một hình hộp chữ nhật (Box) 3D cho mỗi màu
            volume = VGroup(
                Rectangle(width=0.8, height=0.55, color=color).set_fill(color, opacity=0.2),
                Rectangle(width=0.8, height=0.55, color=color).set_fill(color, opacity=0.1).shift(RIGHT * 0.16 + UP * 0.14),
                Line(LEFT * 0.4 + DOWN * 0.275, LEFT * 0.24 + DOWN * 0.135, color=color),
                Line(RIGHT * 0.4 + DOWN * 0.275, RIGHT * 0.56 + DOWN * 0.135, color=color),
                Line(LEFT * 0.4 + UP * 0.275, LEFT * 0.24 + UP * 0.415, color=color),
                Line(RIGHT * 0.4 + UP * 0.275, RIGHT * 0.56 + UP * 0.415, color=color),
            )
            nerfs.add(volume)
            
        nerfs.arrange(DOWN, buff=0.3).next_to(slots, RIGHT, buff=1.2).align_to(slots, DOWN)
        
        arr1 = solid_arrow(slots.get_right(), nerfs.get_left() + LEFT * 0.2)
        self.play(GrowArrow(arr1), FadeIn(nerfs), run_time=1.5)
        
        # Chữ Density & Radiance hiện kế bên NeRF
        nerf_label = safe_text("NeRF Độc Lập\n(Tọa độ 3D + View Dir)", font_size=16, color=TEAL_C, weight=BOLD).next_to(nerfs, UP, buff=0.2)
        math_text = safe_text("- Density (σ)\n- Radiance (c)", font_size=16, color=YELLOW).next_to(nerfs, DOWN, buff=0.2)
        
        self.play(Write(nerf_label), Write(math_text), run_time=2.5)
        self.wait(1.5) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:13 - 0:21: "Khi render novel view, các ray được sample từ 
        # từng NeRF slot rồi composite thành ảnh cuối cùng. 3D inductive bias 
        # giúp model hiểu cấu trúc không gian, tạo ảnh chất lượng từ nhiều góc nhìn."
        # ══════════════════════════════════════════════════════════════════════
        # Bộ Volumetric Rendering
        render_box = labeled_box("Volumetric\nRendering\n(Composite)", width=2.0, height=1.2, color=PURPLE_C, font_size=16).next_to(nerfs, RIGHT, buff=1.2)
        
        # Vẽ các tia sáng đứt nét chiếu từ 3 NeRF hội tụ vào bộ Render
        rays = VGroup(*[DashedLine(nerfs[i].get_right(), render_box.get_left() + UP*(0.3-i*0.3), color=YELLOW_D) for i in range(3)])
        
        self.play(FadeIn(render_box), Create(rays), run_time=2)
        
        # Ảnh Novel Views đầu ra
        novel_views = VGroup(
            simple_image(width=1.0, height=0.7), 
            simple_image(width=1.0, height=0.7).rotate(0.2)
        ).arrange(DOWN, buff=0.2).next_to(render_box, RIGHT, buff=1.0)
        
        arr2 = solid_arrow(render_box.get_right(), novel_views.get_left())
        novel_label = safe_text("Novel Views\n(Hiểu không gian 3D)", font_size=16, color=GREEN_C).next_to(novel_views, DOWN)
        
        self.play(GrowArrow(arr2), FadeIn(novel_views), Write(novel_label), run_time=2)
        self.wait(4) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:21 - 0:33: "Hạn chế: yêu cầu multi-view data, chi phí tính 
        # toán cao, chỉ hoạt động tốt trên CLEVR-3D synthetic."
        # ══════════════════════════════════════════════════════════════════════
        # Khung cảnh báo hạn chế ở phần dưới
        warn_box = Rectangle(width=8.5, height=1.8, color=RED_C).set_fill(RED_E, opacity=0.3).to_edge(DOWN).shift(UP*0.2)
        warn_title = safe_text("Hạn chế của ObSuRF:", font_size=20, color=RED_C, weight=BOLD).next_to(warn_box.get_top(), DOWN, buff=0.1)
        
        warn_list = VGroup(
            safe_text("• Bắt buộc có Multi-view Data", font_size=16, color=WHITE),
            safe_text("• Chi phí tính toán cực kỳ lớn (Render 3D)", font_size=16, color=WHITE),
            safe_text("• Khó Scale: Chỉ tốt trên Synthetic (CLEVR-3D)", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(warn_title, DOWN, buff=0.15)
        
        self.play(FadeIn(warn_box), Write(warn_title), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.1) for t in warn_list], lag_ratio=0.3), run_time=3.5)
        self.play(Wiggle(warn_box), run_time=1)
        self.wait(6) # Tổng ~12s (Kết thúc 33s)

class S7_09_OSRT(Scene):
    def construct(self):
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "OSRT cải tiến hướng 3D với kiến trúc Slot Mixer 
        # Decoder sáng tạo. Thay vì decode mỗi slot riêng rồi overlay, OSRT trộn 
        # các slots trước rồi map sang ảnh."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("OSRT: Slot Mixer Decoder & Light-field")
        self.play(FadeIn(title, shift=UP), run_time=1)

        # Sơ đồ ban đầu (Đầu vào)
        context = VGroup(*[simple_image(width=1.0, height=0.7).shift(RIGHT * i * 0.15 + UP * i * 0.1) for i in range(3)])
        context_label = safe_text("Street View\nContext", font_size=16, color=GREY_B).next_to(context, DOWN)
        group_ctx = VGroup(context, context_label).move_to(LEFT * 5.0 + UP * 0.7)
        
        # Mũi tên và Slots
        arr1 = solid_arrow(group_ctx.get_right(), group_ctx.get_right() + RIGHT*0.8)
        slots = slot_stack(["s1", "s2", "s3"], [RED_C, GREEN_C, BLUE_C], radius=0.25).next_to(arr1, RIGHT, buff=0.1)
        
        self.play(FadeIn(group_ctx, shift=RIGHT*0.2), run_time=1.5)
        self.play(GrowArrow(arr1), FadeIn(slots), run_time=1.5)
        
        # Tương phản: Overlay vs Trộn Slot
        mix_title = safe_text("Trộn Slot trước khi tạo ảnh", font_size=20, color=YELLOW).next_to(title, DOWN, buff=0.2)
        self.play(Write(mix_title), run_time=1)
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:17: "Slot Mixer gồm: Allocation Transformer predict 
        # allocation weight, Mixing Block tính weighted mean, và Render MLP kết 
        # hợp features map sang RGB."
        # ══════════════════════════════════════════════════════════════════════
        # Cấu trúc của Slot Mixer
        mixer_rect = Rectangle(width=2.4, height=1.6, color=YELLOW_D).next_to(slots, RIGHT, buff=0.8)
        mixer_title = safe_text("Slot Mixer", font_size=22, color=YELLOW_D, weight=BOLD).next_to(mixer_rect.get_top(), DOWN, buff=0.1)
        mixer_box_bg = VGroup(mixer_rect, mixer_title)
        
        arr2 = solid_arrow(slots.get_right(), mixer_rect.get_left())
        self.play(GrowArrow(arr2), FadeIn(mixer_box_bg), run_time=1)
        
        # Phân rã 3 thành phần của Slot Mixer ở ngay bên dưới
        mixer_details = VGroup(
            safe_text("1. Allocation Transformer (Predict weights)", font_size=16, color=YELLOW_C),
            safe_text("2. Mixing Block (Weighted Mean)", font_size=16, color=YELLOW_C),
            safe_text("3. Render MLP (Features -> RGB)", font_size=16, color=YELLOW_C)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(mixer_rect, DOWN, buff=0.3)
        
        # Hiệu ứng trộn slot (Các vòng tròn lồng vào nhau bên trong hộp Mixer)
        mixed_circles = VGroup(
            Circle(radius=0.25, color=RED_C).set_fill(RED_C, opacity=0.4).shift(LEFT*0.15 + UP*0.1),
            Circle(radius=0.25, color=GREEN_C).set_fill(GREEN_C, opacity=0.4).shift(RIGHT*0.15 + UP*0.1),
            Circle(radius=0.25, color=BLUE_C).set_fill(BLUE_C, opacity=0.4).shift(DOWN*0.15)
        ).move_to(mixer_rect).shift(DOWN*0.2)
        
        self.play(LaggedStart(*[FadeIn(d, shift=UP*0.1) for d in mixer_details], lag_ratio=0.3), FadeIn(mixed_circles), run_time=3)
        self.play(Rotate(mixed_circles, angle=PI, run_time=2)) # Vòng xoáy trộn
        self.wait(3) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:17 - 0:28: "OSRT dùng light-field rendering thay vì volumetric 
        # rendering, giảm chi phí gần 100 lần so với NeRF. Scale được đến Street 
        # View thực tế."
        # ══════════════════════════════════════════════════════════════════════
        # Khối Light-field Renderer
        lightfield = labeled_box("Light-field\nRenderer", width=1.8, height=1.0, color=TEAL_C, font_size=18).next_to(mixer_rect, RIGHT, buff=0.8)
        arr3 = solid_arrow(mixer_rect.get_right(), lightfield.get_left())
        
        # Badge Giảm 100x Chi phí (Đưa lên trên Light-field để tránh đè)
        badge_100x = labeled_box("⚡ ~100x Nhanh Hơn NeRF", width=2.8, height=0.5, color=GREEN_C, fill_opacity=0.3, font_size=18).next_to(lightfield, UP, buff=0.3)
        
        self.play(GrowArrow(arr3), FadeIn(lightfield), run_time=1.5)
        self.play(FadeIn(badge_100x, scale=1.2), run_time=1.5)
        
        # Ảnh RGB xuất ra (Scale đến dữ liệu thực)
        output_rgb = simple_image(width=1.2, height=0.9).next_to(lightfield, RIGHT, buff=0.8)
        arr4 = solid_arrow(lightfield.get_right(), output_rgb.get_left())
        real_label = safe_text("Real Street View", font_size=16, color=WHITE).next_to(output_rgb, DOWN, buff=0.1)
        
        self.play(GrowArrow(arr4), FadeIn(output_rgb), Write(real_label), run_time=2.5)
        self.wait(5.5) # Tổng ~11s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:28 - 0:39: "OSRT cũng là backbone cho DORSAL, slot representations 
        # được freeze làm conditioning cho diffusion decoder."
        # ══════════════════════════════════════════════════════════════════════
        # Dấu hiệu nhắc nhớ về DORSAL ở Scene trước
        dorsal_link = Rectangle(width=6.0, height=1.6, color=PURPLE_C, stroke_width=2).set_fill(PURPLE_E, opacity=0.1).to_edge(DOWN, buff=0.2)
        
        dorsal_title = safe_text("Dùng làm Backbone cho DORSAL", font_size=20, color=PURPLE_C, weight=BOLD).next_to(dorsal_link.get_top(), DOWN, buff=0.1)
        
        cond_text = safe_text("Slots Frozen (Cấp Condition cho Diffusion)", font_size=18, color=WHITE).next_to(dorsal_title, DOWN, buff=0.2)
        
        self.play(FadeIn(dorsal_link), Write(dorsal_title), run_time=2)
        self.play(Write(cond_text), run_time=2)
        self.wait(7) # Tổng ~11s (Kết thúc 39s)

class S7_10_SysBinder(Scene):
    def construct(self):
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "SysBinder giải quyết vấn đề disentangle thuộc 
        # tính của slot. Một slot được biểu diễn bằng nhiều blocks, mỗi block 
        # mã hóa thuộc tính cụ thể: block shape, block color, block position."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("SysBinder: Neural Systematic Binder")
        self.play(FadeIn(title, shift=UP), run_time=1)

        # Object Slot gốc
        slot = labeled_box("Object Slot\n(Tổng thể)", width=1.8, height=1.0, color=BLUE_C, font_size=16)
        slot.shift(LEFT * 4.5 + UP * 0.2)
        
        # Disentangle thành 3 Blocks
        blocks = VGroup(
            labeled_box("1. Shape Block", width=1.6, height=0.7, color=TEAL_C, font_size=14),
            labeled_box("2. Color Block", width=1.6, height=0.7, color=RED_C, font_size=14),
            labeled_box("3. Position Block", width=1.6, height=0.7, color=YELLOW_D, font_size=14)
        ).arrange(DOWN, buff=0.3).next_to(slot, RIGHT, buff=1.8)
        
        arr_split = solid_arrow(slot.get_right(), blocks.get_left())
        disentangle_text = safe_text("Disentangle", font_size=16, color=YELLOW_C).next_to(arr_split, UP, buff=0.1)

        self.play(FadeIn(slot, shift=RIGHT*0.2), run_time=1)
        self.play(GrowArrow(arr_split), Write(disentangle_text), run_time=1)
        # Hiện 3 block bay từ trong Slot ra để minh họa sự phân tách
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT*0.5) for b in blocks], lag_ratio=0.3), run_time=1)
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:17: "Điều này cho phép không chỉ thay thế object toàn 
        # bộ như SLATE, mà chỉnh sửa từng thuộc tính riêng biệt."
        # ══════════════════════════════════════════════════════════════════════
        # Bắt đầu với 1 Object Gốc (Hình vuông, màu xanh dương, ở giữa)
        demo_box = Rectangle(width=4.0, height=3.0, color=GREY_B, stroke_width=2).set_fill(BG_COLOR, opacity=1).shift(RIGHT * 3.5 + UP*0.2)
        demo_title = safe_text("Editing Độc Lập", font_size=16, color=WHITE, weight=BOLD).next_to(demo_box.get_top(), DOWN, buff=0.1)
        
        obj = Square(side_length=0.8, color=BLUE_C).set_fill(BLUE_C, opacity=0.8).move_to(demo_box.get_center())
        
        arr_to_demo = solid_arrow(blocks.get_right(), demo_box.get_left())
        self.play(GrowArrow(arr_to_demo), FadeIn(demo_box), Write(demo_title), FadeIn(obj, scale=0.5), run_time=2)

        # 1. Chỉnh sửa Shape (Hình vuông -> Hình tam giác)
        new_shape = Triangle(color=BLUE_C).set_fill(BLUE_C, opacity=0.8).scale(0.8).move_to(obj)
        self.play(
            blocks[0][0].animate.set_fill(TEAL_E, opacity=0.8), # Làm sáng Shape block
            Transform(obj, new_shape), # Biến hình
            run_time=1
        )
        
        # 2. Chỉnh sửa Color (Xanh -> Đỏ)
        self.play(
            blocks[0][0].animate.set_fill(TEAL_C, opacity=0.2), # Trả Shape block về cũ
            blocks[1][0].animate.set_fill(RED_E, opacity=0.8),   # Làm sáng Color block
            obj.animate.set_color(RED_C).set_fill(RED_C, opacity=0.8), # Đổi màu
            run_time=1
        )
        
        # 3. Chỉnh sửa Position (Di chuyển sang trái)
        self.play(
            blocks[1][0].animate.set_fill(RED_C, opacity=0.2),  # Trả Color block về cũ
            blocks[2][0].animate.set_fill(YELLOW_E, opacity=0.8),# Làm sáng Position block
            obj.animate.shift(RIGHT * 1.2), # Di chuyển
            run_time=1
        )
        self.play(blocks[2][0].animate.set_fill(YELLOW_D, opacity=0.2), run_time=0.5)
        self.wait(2) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:17 - 0:25: "Tạo khả năng systematic generalization mạnh hơn, 
        # vì AI hiểu các thuộc tính độc lập và kết hợp tự do."
        # ══════════════════════════════════════════════════════════════════════
        # Bảng tổng kết chốt hạ nằm phía dưới màn hình
        conclusion_box = labeled_box("Systematic Generalization", width=6.5, height=0.6, color=ACCENT_COLOR, font_size=20).to_edge(DOWN).shift(UP*0.5)
        
        explain_arrow = MathTex(r"\Rightarrow", color=YELLOW_C).scale(0.7)
        explain_str = safe_text("Hiểu độc lập & Kết hợp tự do (Mix & Match)", font_size=16, color=YELLOW_C)
        explain_text = VGroup(explain_arrow, explain_str).arrange(RIGHT, buff=0.15).next_to(conclusion_box, DOWN, buff=0.15)
        
        self.play(FadeIn(conclusion_box, shift=UP*0.3), run_time=1.5)
        self.play(Write(explain_text), run_time=2)
        
        # Vẽ vài vật thể ngẫu nhiên lấp ló để minh họa chữ "kết hợp tự do"
        mix_group = VGroup(
            Circle(radius=0.2, color=TEAL_C).set_fill(TEAL_C, opacity=0.8),
            Star(color=YELLOW_C).scale(0.3).set_fill(YELLOW_C, opacity=0.8),
            Square(side_length=0.4, color=PURPLE_C).set_fill(PURPLE_C, opacity=0.8)
        ).arrange(RIGHT, buff=0.3).next_to(conclusion_box, UP, buff=0.2)
        
        self.play(FadeIn(mix_group, shift=DOWN*0.2), run_time=1.5)
        self.play(Wiggle(conclusion_box), run_time=1)
        self.wait(2) # Tổng ~8s (Đúng 25s)
class S7_11_MoToK(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn nét to không bị bẹp
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "MoToK đặt câu hỏi: tại sao không reconstruct nhiều 
        # modalities cùng lúc? MoToK dùng pseudo segmentation masks từ motion segmentation..."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("MoToK: Multi-Modal Reconstruction")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # Câu hỏi mở đầu
        question = safe_text("Tại sao không reconstruct tất cả cùng lúc?", font_size=22, color=YELLOW_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(question), run_time=1.5)

        # 1. Đầu vào (Inputs)
        inputs_box = labeled_box("Inputs\n(Video Frames)", width=1.5, height=1.0, color=GREY_C, font_size=18).shift(LEFT * 4.0 + UP * 0.5)
        self.play(FadeIn(inputs_box), run_time=1)

        # 2. Pseudo Masks từ Motion
        mask_bg = Rectangle(width=1.5, height=1.2, color=WHITE).set_fill(GREY_E, opacity=0.4)
        mask_obj1 = Circle(radius=0.25, color=RED_C).set_fill(RED_C, opacity=0.8).shift(LEFT * 0.25 + DOWN*0.1)
        mask_obj2 = Square(side_length=0.4, color=GREEN_C).set_fill(GREEN_C, opacity=0.8).shift(RIGHT * 0.3 + UP*0.1)
        
        mask_group = VGroup(mask_bg, mask_obj1, mask_obj2).next_to(inputs_box, RIGHT, buff=0.8)
        mask_label = safe_text("Pseudo Masks\n(Từ Motion)", font_size=16, color=YELLOW).next_to(mask_group, UP, buff=0.2)
        
        arr_input_mask = solid_arrow(inputs_box.get_right(), mask_group.get_left())
        
        self.play(GrowArrow(arr_input_mask), FadeIn(mask_group), Write(mask_label), run_time=2.5)
        self.wait(1.5) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:15: "...train slots reconstruct đồng thời RGB, Optical Flow, 
        # Depth, và Token. Slot Decoder gồm Linear layer, CNN, Transformer, Perceiver 
        # cho phép reconstruct nhiều output types."
        # ══════════════════════════════════════════════════════════════════════
        self.play(FadeOut(question), run_time=0.5) # Dọn dẹp câu hỏi để rộng chỗ
        
        # 3. Rich Slots
        slots = slot_stack(["Rich", "Slots"], [PURPLE_C, PURPLE_D], radius=0.35).next_to(mask_group, RIGHT, buff=0.8)
        arr_mask_slot = solid_arrow(mask_group.get_right(), slots.get_left(), color=PURPLE_C)
        
        # 4. Tập hợp Decoders
        decoders = VGroup(
            labeled_box("Linear", width=1.4, height=0.5, color=GREY_C, font_size=16),
            labeled_box("CNN", width=1.4, height=0.5, color=TEAL_C, font_size=16),
            labeled_box("Transformer", width=1.4, height=0.5, color=BLUE_C, font_size=16),
            labeled_box("Perceiver", width=1.4, height=0.5, color=MAROON_C, font_size=16)
        ).arrange(DOWN, buff=0.1).next_to(slots, RIGHT, buff=0.8)
        
        arr_slot_dec = solid_arrow(slots.get_right(), decoders.get_left())
        
        # 5. Các Modalities đầu ra
        outputs = VGroup(
            labeled_box("1. RGB", width=1.2, height=0.5, color=RED_C, font_size=16),
            labeled_box("2. Flow", width=1.2, height=0.5, color=BLUE_C, font_size=16),
            labeled_box("3. Depth", width=1.2, height=0.5, color=TEAL_C, font_size=16),
            labeled_box("4. Token", width=1.2, height=0.5, color=YELLOW_D, font_size=16),
        ).arrange(DOWN, buff=0.1).next_to(decoders, RIGHT, buff=0.8)
        
        arr_dec_out = solid_arrow(decoders.get_right(), outputs.get_left(), color=YELLOW_D)
        
        # Animation xuất hiện hàng loạt
        self.play(GrowArrow(arr_mask_slot), FadeIn(slots), run_time=1)
        self.play(GrowArrow(arr_slot_dec), FadeIn(decoders, shift=RIGHT*0.2), run_time=2)
        self.play(GrowArrow(arr_dec_out), LaggedStart(*[FadeIn(o, shift=LEFT*0.2) for o in outputs], lag_ratio=0.2), run_time=3)
        self.wait(0.5) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:15 - 0:24: "Slots học representation phong phú hơn khi phải 
        # tạo nhiều loại output, và pseudo labels hướng dẫn mà không cần ground-truth 
        # segmentation."
        # ══════════════════════════════════════════════════════════════════════
        # Hiệu ứng lan toả ngược từ Output về Slot để biểu thị "Học Representation phong phú"
        self.play(
            slots.animate.scale(1.2),
            slots[0][0].animate.set_color(YELLOW_C), # Làm vòng ngoài của slot sáng lên
            slots[1][0].animate.set_color(YELLOW_C),
            run_time=1
        )
        
        rich_text = safe_text("Representation\nPhong Phú", font_size=16, color=YELLOW_C, weight=BOLD).next_to(slots, UP, buff=0.2)
        self.play(Write(rich_text), run_time=1.5)
        
        # Nhấn mạnh Pseudo Labels (Mũi tên vòng lên chỉ dẫn)
        guide_arrow = CurvedArrow(mask_group.get_bottom() + DOWN*0.1, slots.get_bottom() + DOWN*0.1, angle=PI/2, color=GREEN_C)
        guide_text = safe_text("Hướng dẫn\n(Không cần GT)", font_size=14, color=GREEN_C).next_to(guide_arrow, DOWN, buff=0.1)
        
        self.play(Create(guide_arrow), Write(guide_text), run_time=2.5)
        self.wait(3) # Tổng ~9s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:24 - 0:30: Chờ hình ảnh lưu lại trong tâm trí người xem vài giây
        # cuối theo audio
        # ══════════════════════════════════════════════════════════════════════
        # Thêm một viền tổng kết (Conclusion box) bao quanh cả hệ thống
        conclusion = labeled_box("Ép slot học sâu hơn thông qua Multi-Modal & Pseudo Labels", width=6.5, height=0.6, color=ACCENT_COLOR, font_size=20).to_edge(DOWN).shift(UP*0.3)
        
        self.play(FadeIn(conclusion, shift=UP*0.2), run_time=2)
        self.play(Wiggle(conclusion), run_time=1.5)
        self.wait(2.5) # Tổng 6s (Đạt mốc 30s)

class S7_12_CoSA(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn nét to không bị bẹp
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "CoSA đề xuất Grounded Slot Dictionary. Khác với 
        # Visual Concept Library của SLATE dùng K-means clustering..."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("CoSA: Grounded Slot Dictionary (GSD)")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        # Nhắc lại SLATE K-Means và gạch bỏ (Vì không rõ nghĩa)
        slate_box = labeled_box("SLATE: K-Means Clustering\n(Không rõ Semantic)", width=3.5, height=0.8, color=GREY_C, font_size=18).shift(UP * 1.5)
        cross_slate = crossmark_vector(color=RED_C, size=0.4).next_to(slate_box, RIGHT)
        
        self.play(FadeIn(slate_box, shift=DOWN*0.2), run_time=1.5)
        self.play(Create(cross_slate), run_time=1)
        self.wait(3) # Tổng ~5s
        
        # Dọn đi nhường chỗ cho CoSA
        self.play(FadeOut(slate_box), FadeOut(cross_slate), run_time=1)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:15: "...CoSA dùng GSD Binding map slot elements vào 
        # loại object cụ thể. Ví dụ: bind riêng eyes, facial hair, cheeks, forehead."
        # ══════════════════════════════════════════════════════════════════════
        # Mặt gốc
        face = mini_face(scale=1.5).shift(LEFT * 5.0 + DOWN * 0.5)
        face_label = safe_text("Image", font_size=16, color=WHITE).next_to(face, DOWN)
        self.play(FadeIn(face), Write(face_label), run_time=1)
        self.wait(1)
        
        # Các parts cụ thể (Eyes, Forehead, Cheeks, Mouth)
        parts = VGroup(
            labeled_box("eyes (mắt)", width=1.5, height=0.5, color=BLUE_C, font_size=16),
            labeled_box("forehead (trán)", width=1.5, height=0.5, color=YELLOW_D, font_size=16),
            labeled_box("cheeks (má)", width=1.5, height=0.5, color=RED_C, font_size=16),
            labeled_box("mouth (miệng)", width=1.5, height=0.5, color=GREEN_C, font_size=16),
        ).arrange(DOWN, buff=0.15).next_to(face, RIGHT, buff=1.2)
        
        # Nối dây từ mặt sang từng part (GSD Binding)
        lines = VGroup(*[Line(face.get_right(), parts[i].get_left(), color=GREY_C) for i in range(len(parts))])
        bind_text = safe_text("GSD Binding", font_size=16, color=YELLOW_C, weight=BOLD).next_to(lines, UP, buff=0.2)
        
        self.play(LaggedStart(
            *[AnimationGroup(Create(lines[i]), FadeIn(parts[i], shift=RIGHT*0.2)) for i in range(len(parts))],
            lag_ratio=0.3
        ), run_time=3.5)
        self.play(Write(bind_text), run_time=1)
        self.wait(2) # Tổng ~12s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:15 - 0:22: "GSD giải quyết vấn đề của SLATE: K-means clusters 
        # có thể không mang ý nghĩa semantic rõ ràng. GSD Binding cung cấp 
        # ground truth semantic..."
        # ══════════════════════════════════════════════════════════════════════
        # Gom vào Dictionary
        dictionary = labeled_box("Grounded Slot\nDictionary", width=2.0, height=1.2, color=HIGHLIGHT_COLOR, font_size=20)
        dictionary.next_to(parts, RIGHT, buff=1.0)
        
        arr1 = solid_arrow(parts.get_right(), dictionary.get_left(), color=YELLOW_C)
        
        self.play(GrowArrow(arr1), FadeIn(dictionary, scale=1.2), run_time=2)
        
        # Nhấn mạnh Ground Truth Semantic
        gt_box = SurroundingRectangle(dictionary, color=GREEN_C, buff=0.1)
        gt_text = safe_text("Ground-Truth Semantic (Rõ ràng)", font_size=16, color=GREEN_C).next_to(gt_box, UP, buff=0.1)
        
        self.play(Create(gt_box), Write(gt_text), run_time=2)
        self.wait(3) # Tổng ~19s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:22 - 0:30: "...giúp compose image chính xác và có kiểm soát hơn."
        # ══════════════════════════════════════════════════════════════════════
        # Đầu ra (Compose)
        out_face = mini_face(scale=1.5).next_to(dictionary, RIGHT, buff=1.2)
        arr2 = solid_arrow(dictionary.get_right(), out_face.get_left(), color=GREEN_C)
        
        # Vòng tròn sweep quanh mặt để hiện "Có kiểm soát"
        control_ring = Circle(radius=1.0, color=GREEN_C).set_fill(GREEN_E, opacity=0.2).move_to(out_face)
        compose_text = safe_text("Compose Chính xác\n& Có kiểm soát", font_size=18, color=GREEN_C, weight=BOLD).next_to(out_face, DOWN, buff=0.2)
        check_out = checkmark_vector(color=GREEN_C, size=0.3).next_to(compose_text, RIGHT)
        
        self.play(GrowArrow(arr2), run_time=1)
        # Mặt mọc lên từ từ từng bộ phận (để thể hiện việc Compose)
        self.play(FadeIn(control_ring), FadeIn(out_face), run_time=2)
        
        self.play(Write(compose_text), Create(check_out), run_time=2)
        self.play(Wiggle(compose_text), run_time=1)
        self.wait(5) # Tổng ~30s

class S7_13_ISA(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn nét to không bị bẹp
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "Invariant Slot Attention giải quyết vấn đề nhận diện 
        # object có đối xứng không gian. Nhiều object như bàn, bình, cổng có spatial symmetry."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("ISA: Invariant Slot Attention")
        self.play(FadeIn(title, shift=UP), run_time=1)

        # Minh hoạ 1 vật thể có tính đối xứng (Cái bình / Vase)
        # Dùng 2 nửa (Sector) ghép lại để lát nữa dễ làm hiệu ứng tách rời
        left_half = Sector(radius=0.8, angle=PI, start_angle=PI/2, color=GREY_C).set_fill(WHITE, opacity=0.8)
        right_half = Sector(radius=0.8, angle=PI, start_angle=-PI/2, color=GREY_C).set_fill(WHITE, opacity=0.8)
        vase = VGroup(left_half, right_half).shift(LEFT * 4 + UP * 0.5)

        # Trục đối xứng
        sym_axis = DashedLine(vase.get_top() + UP*0.5, vase.get_bottom() + DOWN*0.5, color=YELLOW_C)
        sym_text = safe_text("Spatial Symmetry\n(Đối xứng không gian)", font_size=18, color=YELLOW_C).next_to(sym_axis, UP, buff=0.2)

        self.play(FadeIn(vase, shift=UP*0.2), run_time=1.5)
        self.play(Create(sym_axis), Write(sym_text), run_time=2.5)
        self.wait(3) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:13: "Slot Attention gốc có thể tách object đối xứng 
        # thành nhiều slot."
        # ══════════════════════════════════════════════════════════════════════
        # Lỗi của Slot Attention gốc: Cắt vật thể làm 2 slot vì tưởng là 2 vật khác nhau
        self.play(
            left_half.animate.shift(LEFT * 0.5).set_color(RED_C),
            right_half.animate.shift(RIGHT * 0.5).set_color(BLUE_C),
            run_time=1.5
        )
        
        fail_text = safe_text("Vanilla OCL:\nPhân mảnh Object", font_size=20, color=RED_C, weight=BOLD).next_to(vase, DOWN, buff=0.5)
        cross = crossmark_vector(color=RED_C, size=0.3).next_to(fail_text, LEFT)
        
        self.play(Write(fail_text), Create(cross), run_time=1.5)
        self.wait(2) # Tổng ~13s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:13 - 0:21: "ISA dùng slot-centric reference frames control 
        # position, scale, orientation."
        # ══════════════════════════════════════════════════════════════════════
        # Mũi tên chuyển tiếp
        arr = solid_arrow(LEFT*1.5 + UP*0.5, RIGHT*1.5 + UP*0.5, color=GREEN_C)
        self.play(GrowArrow(arr), run_time=1)

        # Giải pháp ISA: Hàn gắn lại vật thể
        isa_vase_left = Sector(radius=0.8, angle=PI, start_angle=PI/2, color=GREEN_E).set_fill(GREEN_C, opacity=0.8)
        isa_vase_right = Sector(radius=0.8, angle=PI, start_angle=-PI/2, color=GREEN_E).set_fill(GREEN_C, opacity=0.8)
        isa_vase = VGroup(isa_vase_left, isa_vase_right).shift(RIGHT * 4 + UP * 0.5)
        
        self.play(FadeIn(isa_vase_left, shift=RIGHT*0.5), FadeIn(isa_vase_right, shift=LEFT*0.5), run_time=1.5)

        # Vẽ Reference Frame (Hệ trục toạ độ bọc lấy vật thể)
        ref_box = SurroundingRectangle(isa_vase, color=YELLOW_D, buff=0.2, stroke_width=2).set_fill(YELLOW_E, opacity=0.1)
        ref_x = Arrow(ref_box.get_center(), ref_box.get_right() + RIGHT*0.3, color=YELLOW_D, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        ref_y = Arrow(ref_box.get_center(), ref_box.get_top() + UP*0.3, color=YELLOW_D, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        ref_arc = Arc(radius=0.5, start_angle=0, angle=PI/2, color=YELLOW_D).move_to(ref_box.get_center())
        
        ref_frame = VGroup(ref_box, ref_x, ref_y, ref_arc)
        
        ref_text = safe_text("Reference Frame\n(Pos, Scale, Ori)", font_size=18, color=YELLOW_D).next_to(ref_box, UP, buff=0.3)
        
        self.play(Create(ref_frame), Write(ref_text), run_time=2)
        self.wait(3.5) # Tổng ~21s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:21 - 0:30: "Cho phép nhận diện toàn bộ object có đối xứng và 
        # thao tác di chuyển, thay đổi kích thước mà không phá hủy cấu trúc. 
        # Đặc biệt hữu ích cho robotics."
        # ══════════════════════════════════════════════════════════════════════
        success_text = safe_text("Nhận diện trọn vẹn & Thao tác an toàn", font_size=20, color=GREEN_C, weight=BOLD).next_to(ref_box, DOWN, buff=0.5)
        check = checkmark_vector(color=GREEN_C, size=0.3).next_to(success_text, LEFT)
        
        self.play(Write(success_text), Create(check), run_time=1)
        
        # Gom object và reference frame lại thành 1 khối để thao tác (Manipulation)
        holistic_obj = VGroup(isa_vase, ref_frame)
        
        # Di chuyển (Shift) + Thay đổi kích thước (Scale) + Xoay (Orientation)
        self.play(
            holistic_obj.animate.scale(1.2).shift(RIGHT*0.5 + UP*0.5).rotate(-PI/6),
            run_time=2
        )
        self.play(
            holistic_obj.animate.scale(0.8).shift(LEFT*0.5 + DOWN*0.5).rotate(PI/4),
            run_time=2
        )
        
        # Nhấn mạnh ứng dụng Robotics
        robotics_badge = labeled_box("Ứng dụng đắc lực cho Robotics 🤖", width=4.0, height=0.6, color=ACCENT_COLOR, font_size=20)
        robotics_badge.to_edge(DOWN).shift(UP*0.2)
        
        self.play(FadeIn(robotics_badge, shift=UP*0.2), run_time=1)
        self.play(Wiggle(robotics_badge), run_time=1)
        self.wait(2) # Tổng 30s

class S7_14_DiffFAE(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn nét to không bị bẹp
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:06: "DiffFAE ứng dụng slot-based decoder cho facial 
        # editing. Stage 1 dùng Slot Attention trích xuất semantic tokens..."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("DiffFAE: Facial Appearance Editing")
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(3)

        # Đóng khung Stage 1
        stage1_label = safe_text("Stage 1: Extract Semantic Tokens", font_size=18, color=YELLOW_C, weight=BOLD).shift(LEFT * 4.0 + UP * 1.5)
        self.play(Write(stage1_label), run_time=1)
        
        # Mặt mẫu
        face = mini_face(scale=1.5).shift(LEFT * 4.8)
        face_label = safe_text("Input Face", font_size=16, color=WHITE).next_to(face, DOWN)
        self.play(FadeIn(face, shift=RIGHT*0.2), Write(face_label), run_time=1)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:06 - 0:13: "...chia khuôn mặt thành 4 region. Stage 2 finetune 
        # Latent Diffusion Model, dùng Cross-Attention và AdaIN integrate slot 
        # features vào denoising process."
        # ══════════════════════════════════════════════════════════════════════
        # Cắt mặt thành 4 vùng (Trán, Mắt, Má, Miệng)
        regions = VGroup(*[
            Rectangle(width=1.5, height=0.3, color=color).set_fill(color, opacity=0.3).move_to(face.get_center() + UP * y)
            for y, color in [(0.45, BLUE_C), (0.15, YELLOW_D), (-0.15, RED_C), (-0.45, GREEN_C)]
        ])
        
        # Mũi tên từ Mặt sang Semantic Tokens
        tokens = feature_grid(1, 4, cell=0.4, color=YELLOW_C).next_to(face, RIGHT, buff=0.8)
        tokens[0].set_fill(BLUE_C); tokens[1].set_fill(YELLOW_D); tokens[2].set_fill(RED_C); tokens[3].set_fill(GREEN_C)
        
        arr1 = solid_arrow(face.get_right(), tokens.get_left())
        token_label = safe_text("4 Semantic\nTokens", font_size=16, color=YELLOW).next_to(tokens, DOWN)
        
        self.play(FadeIn(regions), run_time=1)
        self.play(GrowArrow(arr1), FadeIn(tokens), Write(token_label), run_time=1.5)
        self.wait(2)

        # Đóng khung Stage 2
        stage2_label = safe_text("Stage 2: LDM Finetuning", font_size=18, color=PURPLE_C, weight=BOLD).shift(RIGHT * 2.0 + UP * 1.5)
        self.play(Write(stage2_label), run_time=1)
        
        # Latent Diffusion Model
        ldm = labeled_box("Latent Diffusion", width=2.0, height=1.2, color=PURPLE_C, font_size=18).next_to(tokens, RIGHT, buff=1.8)
        arr2 = solid_arrow(tokens.get_right(), ldm.get_left())
        
        # Integrate bằng Cross-Attn và AdaIN
        integrate_cond = safe_text("Cross-Attention\n& AdaIN", font_size=18, color=YELLOW_C).next_to(arr2, UP, buff=0.15)
        
        self.play(GrowArrow(arr2), Write(integrate_cond), run_time=1.5)
        self.play(FadeIn(ldm, shift=RIGHT*0.2), run_time=1)
        self.wait(1) # Tổng ~13s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:13 - 0:24: "Kết quả: chỉnh sửa facial compositionally, thay đổi 
        # pose, expression, lighting mà giữ nguyên identity."
        # ══════════════════════════════════════════════════════════════════════
        # Mặt Edit (Nghiêng đi chút xíu để tạo cảm giác "Thay đổi Pose/Expression")
        edited_face = mini_face(scale=1.5).next_to(ldm, RIGHT, buff=1.0).rotate(-0.15)
        
        arr3 = solid_arrow(ldm.get_right(), edited_face.get_left(), color=GREEN_C)
        
        # Bảng tính năng Editing
        edit_features = VGroup(
            VGroup(checkmark_vector(color=GREEN_C, size=0.25), safe_text("Pose", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.15),
            VGroup(checkmark_vector(color=GREEN_C, size=0.25), safe_text("Expression", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.15),
            VGroup(checkmark_vector(color=GREEN_C, size=0.25), safe_text("Lighting", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.15)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(edited_face, DOWN, buff=0.3).align_to(edited_face, LEFT).shift(RIGHT*0.5)
        
        self.play(GrowArrow(arr3), FadeIn(edited_face), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(f, shift=UP*0.1) for f in edit_features], lag_ratio=0.3), run_time=2.5)

        # Vòng khóa bảo vệ Identity (Giữ nguyên nhận dạng)
        lock_glow = Circle(radius=1.0, color=GREEN_C).set_fill(GREEN_E, opacity=0.2).move_to(edited_face)
        lock_icon = safe_text("Giữ nguyên Identity", font_size=16, color=GREEN_C, weight=BOLD).next_to(lock_glow, UP, buff=0.1)
        
        self.play(FadeIn(lock_glow), Write(lock_icon), run_time=2)
        self.play(Wiggle(lock_icon), run_time=1.5)
        self.wait(2) # Tổng ~24s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:24 - 0:32: "Semantic tokens từ slot attention out-perform 
        # features từ MAE và CLIP."
        # ══════════════════════════════════════════════════════════════════════
        # Tạo bảng so sánh ở dưới đáy màn hình
        compare_box = Rectangle(width=7.0, height=0.9, color=ACCENT_COLOR).set_fill(BG_COLOR, opacity=1).to_edge(DOWN).shift(UP*0.2)
        
        compare_text = VGroup(
            safe_text("Slot Attention Tokens ", font_size=20, color=YELLOW_C, weight=BOLD),
            safe_text(" > ", font_size=24, color=GREEN_C, weight=BOLD),
            safe_text(" MAE & CLIP Features", font_size=20, color=GREY_B)
        ).arrange(RIGHT, buff=0.1).move_to(compare_box)
        
        self.play(FadeIn(compare_box), run_time=1.5)
        self.play(Write(compare_text), run_time=2)
        self.play(Wiggle(compare_text[1]), run_time=1.5) # Rung dấu lớn hơn
        self.wait(2) # Tổng ~32s

class S7_15_PaLME(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn nét to không bị bẹp
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:06: "PaLM-E kết hợp object-centric representation 
        # với Large Language Model. Object slots từ OSRT được đưa vào PaLM LLM."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("PaLM-E: LLM cho Robotics")
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(5)
        
        # Bắt đầu luồng Pipeline: CV -> Slots -> LLM
        # 1. Hình ảnh & OSRT
        image = simple_image(width=1.2, height=0.8).shift(LEFT * 5.0 + UP * 1.5)
        osrt = labeled_box("OSRT\nEncoder", width=1.8, height=1.0, color=TEAL_C, font_size=18).next_to(image, RIGHT, buff=0.6)
        arr1 = solid_arrow(image.get_right(), osrt.get_left())
        
        # 2. Object Slots
        slots = slot_stack(["cup", "table", "goal"], [RED_C, GREEN_C, BLUE_C], radius=0.25).next_to(osrt, RIGHT, buff=0.6)
        arr2 = solid_arrow(osrt.get_right(), slots.get_left(), color=YELLOW_C)
        
        # 3. LLM Model
        llm = labeled_box("PaLM-E\n(Language Model)", width=2.5, height=1.2, color=YELLOW_D, font_size=20).next_to(slots, RIGHT, buff=0.8)
        arr3 = solid_arrow(slots.get_right(), llm.get_left(), color=YELLOW_D)
        
        self.play(FadeIn(image), run_time=1)
        self.play(GrowArrow(arr1), FadeIn(osrt), run_time=1)
        self.play(GrowArrow(arr2), FadeIn(slots), run_time=1)
        self.play(GrowArrow(arr3), FadeIn(llm), run_time=2)
        self.wait(1) # Tổng ~7s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:06 - 0:13: "Kiến trúc: Image, OSRT Encoder, Object Slots, 
        # ViT, PaLM, Control."
        # ══════════════════════════════════════════════════════════════════════
        # Nối tiếp nhánh LLM ra Control / Robotics
        plan = VGroup(
            labeled_box("1. Nhìn (Vision)", width=2.4, height=0.5, color=GREY_B, font_size=16),
            labeled_box("2. Kế hoạch (Reasoning)", width=2.4, height=0.5, color=GREY_B, font_size=16),
            labeled_box("3. Hành động (Control)", width=2.4, height=0.5, color=ACCENT_COLOR, font_size=16),
        ).arrange(DOWN, buff=0.15).next_to(llm, RIGHT, buff=0.8)
        
        arr4 = solid_arrow(llm.get_right(), plan.get_left(), color=ACCENT_COLOR)
        
        # Vẽ cánh tay Robot
        arm = VGroup(
            Line(ORIGIN, RIGHT * 0.65 + UP * 0.35, color=BLUE_C, stroke_width=7),
            Line(RIGHT * 0.65 + UP * 0.35, RIGHT * 1.12 + DOWN * 0.05, color=BLUE_C, stroke_width=7),
            Circle(radius=0.1, color=YELLOW_D).set_fill(YELLOW_D, opacity=1),
            VGroup(Line(ORIGIN, RIGHT * 0.18 + UP * 0.18, color=WHITE, stroke_width=4), Line(ORIGIN, RIGHT * 0.18 + DOWN * 0.18, color=WHITE, stroke_width=4)).shift(RIGHT * 1.12 + DOWN * 0.05),
        ).next_to(plan, DOWN, buff=0.3)
        robot_label = safe_text("Robot Action", font_size=18, color=BLUE_C, weight=BOLD).next_to(arm, DOWN)
        
        self.play(GrowArrow(arr4), FadeIn(plan), run_time=2)
        self.play(FadeIn(arm, shift=UP*0.2), Write(robot_label), run_time=2)
        self.wait(2) # Tổng ~13s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:13 - 0:21: "PaLM-E demo trên nhiều task embodied AI: robot 
        # đi lấy đồ vật, suy nghĩ cách grab block, sắp xếp đồ vật theo màu."
        # ══════════════════════════════════════════════════════════════════════
        # Hộp liệt kê Tasks (Embodied AI)
        tasks_box = Rectangle(width=5.5, height=2.5, color=BLUE_E).set_fill(BG_COLOR, opacity=0.9).shift(LEFT * 3.5 + DOWN * 1.2)
        tasks_title = safe_text("Embodied AI Tasks", font_size=20, color=YELLOW, weight=BOLD).next_to(tasks_box.get_top(), DOWN, buff=0.2)
        
        task_list = VGroup(
            safe_text("• Tìm & Lấy đồ vật", font_size=18, color=WHITE),
            safe_text("• Suy nghĩ cách gắp khối (Grab)", font_size=18, color=WHITE),
            safe_text("• Sắp xếp đồ vật theo màu", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tasks_title, DOWN, buff=0.3).align_to(tasks_box.get_left(), LEFT).shift(RIGHT*0.5)
        
        self.play(FadeIn(tasks_box), Write(tasks_title), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT*0.2) for t in task_list], lag_ratio=0.3), run_time=3.5)
        self.wait(0.5) # Tổng ~21s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:21 - 0:31: "Cho thấy object-centric representation có thể 
        # làm bridge giữa visual understanding và language-based reasoning."
        # ══════════════════════════════════════════════════════════════════════
        # Cây cầu kết nối (Bridge)
        bridge_box = labeled_box("Object Slots = Cây cầu kết nối (Bridge)", width=6.5, height=0.7, color=GREEN_C, font_size=22).to_edge(DOWN).shift(UP*0.2 + RIGHT*3)
        
        visual_txt = safe_text("Visual\nUnderstanding", font_size=18, color=TEAL_C).next_to(bridge_box, UP, buff=0.3).align_to(bridge_box, LEFT).shift(RIGHT*0.5)
        reason_txt = safe_text("Language\nReasoning", font_size=18, color=YELLOW_D).next_to(bridge_box, UP, buff=0.3).align_to(bridge_box, RIGHT).shift(LEFT*0.5)
        
        # Mũi tên uốn cong tạo thành cái cầu
        bridge_curve = CurvedArrow(visual_txt.get_right(), reason_txt.get_left(), angle=-PI/2, color=GREEN_C)
        
        self.play(FadeIn(bridge_box, shift=UP*0.2), run_time=2)
        self.play(Write(visual_txt), Write(reason_txt), Create(bridge_curve), run_time=3.5)
        
        self.play(Wiggle(bridge_box), run_time=1.5)
        self.wait(3) # Tổng ~31s

class S7_16_ThreeParadigms(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn nét to không bị bẹp
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:08: "Object-centric representation mở ra 3 mô thức thao 
        # tác (paradigms) chính để chỉnh sửa hình ảnh một cách có kiểm soát."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("3 Paradigms of Manipulation")
        self.play(FadeIn(title, shift=UP), run_time=1)
        
        intro_text = safe_text("Thao tác với Slot để sinh ảnh mới", font_size=20, color=YELLOW_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(intro_text), run_time=1.5)
        self.wait(4) # Tổng ~8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:08 - 0:15: "Mô thức thứ nhất là Substituting: Thay thế hoàn 
        # toàn một slot object này bằng một slot object khác."
        # ══════════════════════════════════════════════════════════════════════
        # Panel 1: Substituting (Thay thế)
        box_sub = labeled_box("1. Substituting\n(Thay thế)", width=2.5, height=0.8, color=RED_C, font_size=18).shift(LEFT * 4 + UP * 0.5)
        
        # Object A (Hình tròn Đỏ) -> Object B (Hình vuông Xanh)
        obj_a = Circle(radius=0.4, color=RED_C).set_fill(RED_E, opacity=0.8).next_to(box_sub, DOWN, buff=0.6).shift(LEFT*0.8)
        obj_b = Square(side_length=0.7, color=BLUE_C).set_fill(BLUE_E, opacity=0.8).next_to(box_sub, DOWN, buff=0.6).shift(RIGHT*0.8)
        arr_sub = solid_arrow(obj_a.get_right(), obj_b.get_left())

        self.play(FadeIn(box_sub, shift=DOWN*0.2), run_time=1)
        self.play(FadeIn(obj_a), run_time=1)
        
        # Animation Thay thế: Hình tròn nhảy lên và biến thành Hình vuông
        moving_obj = obj_a.copy()
        self.play(GrowArrow(arr_sub), run_time=1)
        self.play(Transform(moving_obj, obj_b), run_time=2)
        self.wait(1.5) # Tổng ~15s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:15 - 0:23: "Thứ hai là Manipulating: Giữ nguyên object nhưng 
        # thay đổi các thuộc tính bên trong như màu sắc, hình dáng."
        # ══════════════════════════════════════════════════════════════════════
        # Panel 2: Manipulating (Đổi thuộc tính)
        box_manip = labeled_box("2. Manipulating\n(Đổi thuộc tính)", width=2.5, height=0.8, color=YELLOW_D, font_size=18).shift(UP * 0.5)
        
        obj_green = Circle(radius=0.4, color=GREEN_C).set_fill(GREEN_E, opacity=0.8).next_to(box_manip, DOWN, buff=0.6).shift(LEFT*0.8)
        obj_yellow = Circle(radius=0.4, color=YELLOW_C).set_fill(YELLOW_E, opacity=0.8).next_to(box_manip, DOWN, buff=0.6).shift(RIGHT*0.8)
        arr_manip = solid_arrow(obj_green.get_right(), obj_yellow.get_left())

        self.play(FadeIn(box_manip, shift=DOWN*0.2), run_time=1)
        self.play(FadeIn(obj_green), run_time=1)
        
        # Animation Đổi thuộc tính: Vẫn là nó nhưng đổi màu
        changing_obj = obj_green.copy()
        self.play(GrowArrow(arr_manip), run_time=1)
        self.play(
            changing_obj.animate.move_to(obj_yellow.get_center()).set_color(YELLOW_C).set_fill(YELLOW_E, opacity=0.8), 
            run_time=2
        )
        self.wait(2) # Tổng ~23s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:23 - 0:31: "Cuối cùng là Moving: Di chuyển vị trí không gian 
        # của object trong scene mà không làm ảnh hưởng đến nền."
        # ══════════════════════════════════════════════════════════════════════
        # Panel 3: Moving (Di chuyển)
        box_move = labeled_box("3. Moving\n(Di chuyển)", width=2.5, height=0.8, color=BLUE_C, font_size=18).shift(RIGHT * 4 + UP * 0.5)
        
        # Trục đường đi mờ
        track_line = DashedLine(box_move.get_bottom() + DOWN*1.0 + LEFT*0.8, box_move.get_bottom() + DOWN*1.0 + RIGHT*0.8, color=GREY_C)
        
        obj_move = Circle(radius=0.4, color=PURPLE_C).set_fill(PURPLE_E, opacity=0.8).move_to(track_line.get_start())

        self.play(FadeIn(box_move, shift=DOWN*0.2), run_time=1)
        self.play(Create(track_line), FadeIn(obj_move), run_time=1.5)
        
        # Animation Di chuyển: Trượt dọc theo đường line
        self.play(obj_move.animate.move_to(track_line.get_end()), run_time=2.5)
        
        # Dòng chốt cuối cùng dưới màn hình
        caption = safe_text("Object-Centric Learning cho phép kiểm soát AI sinh ảnh hoàn toàn", font_size=20, color=GREEN_C, weight=BOLD).to_edge(DOWN).shift(UP*0.5)
        self.play(Write(caption), run_time=2)
        self.wait(1) # Tổng ~31s

class S7_17_Part7Summary(Scene):
    def construct(self):
        # Hàm vẽ mũi tên chuẩn nét to không bị bẹp
        def solid_arrow(start, end, color=GREY_B):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=4)

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:00 - 0:10: "Phần 7 đã đi qua nhiều hướng nâng cấp decoder. 
        # Xu hướng rõ ràng: từ decoder đơn giản MLP đến generative model mạnh 
        # hơn như Transformer và Diffusion."
        # ══════════════════════════════════════════════════════════════════════
        title = title_mob("Tóm tắt Upgrading Decoder")
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.wait(1)
        
        # Timeline sự tiến hóa của Decoder
        mlp_box = labeled_box("MLP\n(Đơn giản)", width=1.8, height=0.8, color=GREEN_C, font_size=16)
        trans_box = labeled_box("Transformer\n(Autoregressive)", width=2.0, height=0.8, color=BLUE_C, font_size=16)
        diff_box = labeled_box("Diffusion\n(Generative AI)", width=1.8, height=0.8, color=PURPLE_C, font_size=16)
        
        timeline = VGroup(mlp_box, trans_box, diff_box).arrange(RIGHT, buff=1.2).shift(UP * 1.5)
        
        arr1 = solid_arrow(mlp_box.get_right(), trans_box.get_left())
        arr2 = solid_arrow(trans_box.get_right(), diff_box.get_left())
        
        # Hiện dần theo thứ tự tiến hóa
        self.play(FadeIn(mlp_box, shift=RIGHT*0.2), run_time=1.5)
        self.play(GrowArrow(arr1), FadeIn(trans_box, shift=RIGHT*0.2), run_time=1.5)
        self.play(GrowArrow(arr2), FadeIn(diff_box, shift=RIGHT*0.2), run_time=1.5)
        self.wait(4.5) # Tổng ~10s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:10 - 0:21: "Triết lý thay đổi: thay vì ép decoder yếu để slot 
        # học object, hãy xây decoder đủ mạnh tái tạo ảnh chất lượng cao và thiết 
        # kế kiến trúc giữ slot object-centric."
        # ══════════════════════════════════════════════════════════════════════
        # Nhấn mạnh Triết lý cốt lõi
        philosophy_title = safe_text("⭐ Triết lý thay đổi hoàn toàn:", font_size=18, color=YELLOW_C, weight=BOLD).shift(DOWN * 0.2)
        
        principle_text = safe_text("Xây Decoder ĐỦ MẠNH + Thiết kế kiến trúc khéo léo\nVừa có ảnh đẹp, vừa giữ Slot Object-centric", font_size=20, color=WHITE).next_to(philosophy_title, DOWN, buff=0.3)
        principle_box = SurroundingRectangle(principle_text, color=HIGHLIGHT_COLOR, buff=0.3, stroke_width=3).set_fill(HIGHLIGHT_COLOR, opacity=0.1)
        
        self.play(Write(philosophy_title), run_time=1.5)
        self.play(Write(principle_text), run_time=2)
        self.play(Create(principle_box), run_time=1.5)
        self.play(Wiggle(principle_box), run_time=1.5)
        self.wait(2.5) # Tổng ~11s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:21 - 0:25: "Ba điểm chính:"
        # ══════════════════════════════════════════════════════════════════════
        # Dọn sạch Phase 1 để hiển thị Check-list 3 điểm
        phase1_group = VGroup(timeline, arr1, arr2, philosophy_title, principle_text, principle_box)
        self.play(FadeOut(phase1_group), run_time=1)
        
        takeaways_title = safe_text("3 ĐIỂM CHÍNH CẦN NHỚ:", font_size=26, color=YELLOW, weight=BOLD).to_edge(UP).shift(DOWN*1.2)
        self.play(Write(takeaways_title), run_time=1)
        self.wait(0.5) # Tổng 4s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:25 - 0:30: "Slot-Decoding Dilemma và Pixel Independence 
        # là hai vấn đề cốt lõi."
        # ══════════════════════════════════════════════════════════════════════
        t1_icon = crossmark_vector(color=RED_C, size=0.25)
        t1_text = safe_text("1. Hai vấn đề cốt lõi: Slot-Decoding Dilemma & Pixel Independence", font_size=20, color=WHITE)
        point1 = VGroup(t1_icon, t1_text).arrange(RIGHT, buff=0.2).next_to(takeaways_title, DOWN, buff=0.8).align_to(takeaways_title, LEFT).shift(LEFT*2.5)

        self.play(FadeIn(point1, shift=UP*0.2), run_time=1)
        self.wait(1.5) # Tổng 5s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:30 - 0:38: "Hai hướng giải quyết: 3D Inductive Bias với ObSuRF 
        # và OSRT, và Decoupling Decoding với SLATE, LSD, DORSAL."
        # ══════════════════════════════════════════════════════════════════════
        t2_icon = checkmark_vector(color=GREEN_C, size=0.25)
        t2_text = safe_text("2. Hai hướng giải quyết:\n    • 3D Inductive Bias (ObSuRF, OSRT)\n    • Decoupling Decoding (SLATE, LSD, DORSAL)", font_size=20, color=WHITE)
        point2 = VGroup(t2_icon, t2_text).arrange(RIGHT, buff=0.2).next_to(point1, DOWN, buff=0.5).align_to(point1, LEFT)

        self.play(FadeIn(point2, shift=UP*0.2), run_time=1)
        self.wait(8) # Tổng 8s

        # ══════════════════════════════════════════════════════════════════════
        # [AUDIO] 0:38 - 0:47: "Các ứng dụng thực tế như DiffFAE cho facial editing 
        # và PaLM-E cho robotics cho thấy object-centric representation đang mở rộng 
        # vào generative AI và embodied AI."
        # ══════════════════════════════════════════════════════════════════════
        t3_icon = Arrow(ORIGIN, RIGHT*0.3, color=BLUE_C, buff=0)
        t3_text = safe_text("3. Ứng dụng thực tế: Mở rộng sang Generative AI & Embodied AI", font_size=20, color=YELLOW_C)
        point3 = VGroup(t3_icon, t3_text).arrange(RIGHT, buff=0.2).next_to(point2, DOWN, buff=0.6).align_to(point2, LEFT)

        # Min minh họa bằng 2 icon sinh động
        app_icons = VGroup(
            VGroup(mini_face(scale=0.8), safe_text("DiffFAE\n(Facial Edit)", font_size=14, color=GREY_B)).arrange(DOWN, buff=0.1),
            VGroup(slot_stack(["LLM"], [YELLOW_D], radius=0.3), safe_text("PaLM-E\n(Robotics)", font_size=14, color=GREY_B)).arrange(DOWN, buff=0.1)
        ).arrange(RIGHT, buff=1.5).next_to(point3, DOWN, buff=0.5).align_to(t3_text, LEFT).shift(RIGHT * 1.5)

        self.play(FadeIn(point3, shift=UP*0.2), run_time=2)
        self.play(FadeIn(app_icons, shift=UP*0.2), run_time=2)
        self.play(Wiggle(app_icons), run_time=1.5)
        self.wait(3.5) # Tổng 9s (Kết thúc đúng 47s)