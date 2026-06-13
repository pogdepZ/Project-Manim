from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='Sự kết hợp giữa Mô phỏng cổ điển và Neural Networks',
            voice='Engine mô phỏng vật lý cộng mô phỏng khả vi. Thay vì bắt mạng nơ ron tự học lại vật lý từ đầu, một hướng là cấy trực tiếp các Physics Engine vào mạng nơ ron sâu. Chúng ta gọi nó là mô phỏng khả vi. Lực ma sát, trọng lực được tính toán bằng phương trình toán học và truyền ngược gradient lại mạng nơ ron. Mô hình A I nhận dạng cấu trúc điểm ảnh, sau đó giao phần tính toán cơ học lại cho bộ máy vật lý cổ điển. Sự kết hợp này vừa đảm bảo chính xác định luật Newton, vừa giữ được tính linh hoạt học tập vô hạn của Deep Learning.',
            formula='Physics Engine + Differentiable Simulation',
            visual_hints=['Phần mềm mô phỏng vật lý Unity 3D dung hợp với một mạng nơ ron sâu.', 'Các véc tơ lực F chạy ngược chiều trên các sợi dây thần kinh của mô hình mạng.', 'A I phân tích khối hộp, Physics Engine tính toán chính xác quỹ đạo rơi xuống đất.'],
            pattern='Pixel to Object',
            duration=33.144,
        )
