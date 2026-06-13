from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='AI Đạo đức: Mô phỏng hệ quả',
            voice='Mô hình thế giới mô phỏng hệ quả của hành động, sau đó kiểm tra đạo đức. Trí tuệ nhân tạo tương lai không chỉ thông minh mà phải có đạo đức. Khi giao quyền điều khiển xe tự lái, chúng ta trao cho máy móc quyền sinh sát. Mô hình thế giới cho phép A I lập kế hoạch phản thực tế. Nếu rẽ trái, hệ quả là gì? Nếu đi thẳng, bao nhiêu người bị thương? Bằng việc giả lập trước các chuỗi hệ quả vật lý, A I có thể áp dụng các bộ luật Asimov để chặn đứng các hành vi tồi tệ. Mô hình thế giới chính là không gian nội tâm để A I hình thành lương tâm trước khi xuất tay hành động.',
            formula='World Model \\to Action Consequence \\to Ethical Check',
            visual_hints=['Hình ảnh ngã tư nguy hiểm, một bên là người già, một bên là rào chắn bê tông.', 'Hai màn hình ảo hiện ra, phân tích mức độ thiệt hại của mỗi quyết định trong tương lai gần.', 'Vòng tròn bảo vệ màu xanh lam hiện lên ngăn cản chiếc xe lao về phía người đi bộ.'],
            pattern='World Model Rollout',
            duration=37.032,
        )
