from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='Giới hạn của việc nén dữ liệu',
            voice='Việc nén thông tin không phải là sự thấu hiểu thực sự. Tuy nhiên, có một phe chỉ trích cho rằng nén dữ liệu video hoàn hảo chưa chắc tạo ra một World Model thực thụ. Ilya Sutskever từng nói dự đoán từ tiếp theo tốt chính là một dạng mô hình thế giới. Nhưng Yann LeCun cho rằng sinh tạo điểm ảnh là sự lãng phí. Tranh cãi này vẫn chưa ngã ngũ. Dù vậy, chúng ta đều đồng ý rằng mô phỏng các mối quan hệ động học ở mức biểu diễn cấp cao là tiết kiệm nhất. Tương lai sẽ thuộc về hệ thống biết khi nào nên bỏ qua tiểu tiết để nắm bắt bức tranh toàn cảnh.',
            formula='Compression != True Understanding',
            visual_hints=['Cái máy ép ép chặt hàng ngàn video thành một khối lập phương dữ liệu siêu đặc.', 'Cuộc đối thoại ảo giữa hai triết lý: một bên tạo ra điểm ảnh, một bên dự đoán không gian ẩn.', 'Khối xử lý không gian ẩn chạy mượt mà tiêu thụ ít năng lượng hơn hẳn cỗ máy tạo ảnh.'],
            pattern='Pixel to Object',
            duration=34.728,
        )
