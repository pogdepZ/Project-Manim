from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='Sim-to-Real Transfer (Chuyển giao Thực tế)',
            voice='Mô phỏng chi phí thấp dẫn tới thế giới thực đắt đỏ. Khái niệm Sim to Real chỉ quá trình huấn luyện não bộ robot trong máy tính, sau đó tải não bộ đó vào một con robot vật lý. Môi trường giả lập rất rẻ và an toàn, nhưng nó hoàn hảo quá mức. Ma sát trong thực tế hay gió thổi là những thứ rất khó mô phỏng chuẩn. Khoảng cách thực tế này là cơn ác mộng của dân làm robot. Mô hình thế giới mạnh có thể khắc phục bằng cách học các tính chất bất biến của vật lý. Nó dễ dàng chuyển đổi bộ luật tương tác sang môi trường mới mà không bị sai lệch quá lớn.',
            formula='Simulation (Cheap) \\to Real World (Expensive)',
            visual_hints=['Sợi cáp truyền luồng ánh sáng dữ liệu từ máy trạm 3D sang đầu một chú robot chó thật.', 'Robot trong máy tính nhảy mượt mà, nhưng robot ngoài đời thực bị trượt chân trên sàn bóng.', 'Khối đặc trưng nhân quả tự động loại bỏ các yếu tố nhiễu bề mặt, giữ lại quy luật động lực học.'],
            pattern='Correlation vs Causation',
            duration=34.512,
        )
