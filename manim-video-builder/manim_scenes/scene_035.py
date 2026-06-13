from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='Hạn chế của thuật toán P C',
            voice='Lớp tương đương Markov. Thuật toán P C là một trong những phương pháp cổ điển nhất để khám phá nhân quả. Tuy nhiên, nó bị giới hạn bởi lớp tương đương Markov. Nghĩa là nếu hai đồ thị khác nhau nhưng tạo ra cùng một phân phối dữ liệu quan sát, thuật toán sẽ chịu thua, không biết mũi tên nên hướng về bên nào. Xác suất thống kê đơn thuần là không đủ để phá vỡ sự đối xứng này. Trí tuệ nhân tạo cần phải có thêm kiến thức nền hoặc động lực học thời gian. Đây là rào cản lý thuyết lớn khiến học sâu và nhân quả chưa thể dung hợp một cách hoàn hảo.',
            formula='Markov Equivalence Classes',
            visual_hints=['Thuật toán P C được minh họa bằng một cái rây lọc, đang cố gắng rây dữ liệu.', 'Hai đồ thị A suy ra B và B suy ra A cùng nhấp nháy, một dấu chấm hỏi lớn xuất hiện.', 'Một chiếc đồng hồ bấm giờ xuất hiện, cung cấp chiều không gian thời gian để phá vỡ bế tắc.'],
            pattern='Causal Graph',
            duration=33.816,
        )
