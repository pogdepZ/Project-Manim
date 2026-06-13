from manim import *
import sys
import os

sys.path.append(os.path.dirname(__file__))
from design_system_v3 import *

class Scene013(Scene):
    def construct(self):
        self.camera.background_color = NAVY_BG
        
        audio_path = "/home/pognova/SkillManim/manim-video-builder/output/scenes/scene_013/narration.mp3"
        if os.path.exists(audio_path):
            self.add_sound(audio_path)

        def sync_to(target_time):
            wait_time = target_time - self.renderer.time
            if wait_time > 0:
                self.wait(wait_time)

        # TITLE
        title = create_title("Học quan hệ giữa các đối tượng")
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)

        # FORMULA
        formula = create_formula_panel("r_{ij} = g(z_i, z_j)")
        self.play(FadeIn(formula, shift=UP*0.2), run_time=1.0)
        
        # ---------------------------------------------------------
        # SEGMENT 1 (0s - 9.5s)
        # Voice: "Sau khi tách được các đối tượng đơn lẻ, chúng ta cần học mối quan hệ. Thế giới không phải là những vật thể nằm tách biệt vô nghĩa."
        # ---------------------------------------------------------
        objects = VGroup(
            create_real_entity_box('ball', 'Quả bóng', scene_name="scene_013", color=COLOR_USER),
            create_real_entity_box('box', 'Chiếc hộp', scene_name="scene_013", color=COLOR_USER),
            create_real_entity_box('table', 'Mặt bàn', scene_name="scene_013", color=COLOR_USER)
        ).arrange(RIGHT, buff=1.0).center()
        
        self.play(LaggedStart(*[FadeIn(obj, shift=UP*0.3) for obj in objects], lag_ratio=0.3), run_time=2.0)
        
        sync_to(11.76)

        # ---------------------------------------------------------
        # SEGMENT 2 (9.5s - 19.0s)
        # Voice: "Chúng ta học hàm rê nhận đầu vào là biểu diễn của hai vật thể. Kết quả cho biết mối quan hệ không gian hoặc động học giữa chúng."
        # ---------------------------------------------------------
        line1 = Line(objects[0].get_right(), objects[1].get_left(), color=COLOR_RESULT, stroke_width=4)
        line2 = Line(objects[1].get_right(), objects[2].get_left(), color=COLOR_RESULT, stroke_width=4)
        
        self.play(Create(line1), Create(line2), run_time=1.5)
        
        sync_to(20.00)

        # ---------------------------------------------------------
        # SEGMENT 3 (19.0s - 28.5s)
        # Voice: "Ví dụ, quả bóng đang nằm trên chiếc hộp, chiếc hộp đặt trên bàn. Các mối quan hệ này tạo nên cấu trúc ngữ nghĩa cho toàn cảnh."
        # ---------------------------------------------------------
        label1 = create_text_box("Nằm trên", color=COLOR_WARNING).scale(0.6).next_to(line1, UP, buff=0.1)
        label2 = create_text_box("Đặt trên", color=COLOR_WARNING).scale(0.6).next_to(line2, UP, buff=0.1)
        
        self.play(FadeIn(label1, shift=UP*0.1), FadeIn(label2, shift=UP*0.1), run_time=1.0)
        
        sync_to(28.42)

        # ---------------------------------------------------------
        # SEGMENT 4 (28.5s - 38.0s)
        # Voice: "Việc xây dựng một đồ thị quan hệ giữa các biểu diễn này cung cấp một cấu trúc dồi dào cho các mạng nơ ron đồ thị G N N hoạt động."
        # ---------------------------------------------------------
        gnn_text = create_text_box("Mạng Neural Đồ thị (GNN)", color=COLOR_AI).to_edge(UP, buff=1.2)
        self.play(FadeIn(gnn_text, shift=DOWN*0.2), run_time=1.0)
        self.play(Indicate(gnn_text, color=COLOR_AI), run_time=1.5)
        
        total_dur = 37.344
        sync_to(total_dur)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
