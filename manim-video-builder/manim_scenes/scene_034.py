from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='Causal Discovery (Khám phá nhân quả)',
            voice='Dữ liệu quan sát dẫn tới đồ thị có hướng không chu trình. Làm sao A I biết được đồ thị nhân quả ban đầu? Quá trình tự động tìm ra mối quan hệ nguyên nhân - kết quả từ dữ liệu thô được gọi là Khám phá Nhân quả. Từ một tập dữ liệu về giá nhà, thời tiết và dân số, hệ thống sử dụng các phép kiểm định tính độc lập có điều kiện để nối các mũi tên có hướng. Nó xác định được rằng dân số tăng làm giá nhà tăng, chứ không phải giá nhà tăng làm người ta đẻ nhiều hơn. Đây là bài toán nghịch đảo cực khó trong toán học, đóng vai trò xây dựng hệ khung xương vững chắc cho World Models.',
            formula='Observational Data \\to DAG (Directed Acyclic Graph)',
            visual_hints=['Hình ảnh hàng núi dữ liệu đang bay lượn và tự động tự sắp xếp thành một sơ đồ mạng lưới.', 'Các điểm dữ liệu được nối lại bằng các đường thẳng, rồi biến thành các mũi tên một chiều.', 'Mũi tên kết nối từ khối Dân số hướng thẳng vào khối Giá nhà.'],
            pattern='Correlation vs Causation',
            duration=35.328,
        )
