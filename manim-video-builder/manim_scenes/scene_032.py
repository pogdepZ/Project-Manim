from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='Offline Reinforcement Learning và World Models',
            voice='Tập dữ liệu tĩnh, dẫn tới mô hình thế giới, dẫn tới tối ưu hóa chính sách hành động. Trong học tăng cường thông thường, robot phải liên tục thử sai trong môi trường thực. Việc này tốn kém và cực kỳ nguy hiểm nếu áp dụng cho xe tự lái. Học tăng cường ngoại tuyến, hay Offline RL, giải quyết vấn đề này. Hệ thống được cung cấp một tập dữ liệu lớn ghi lại các chuyến đi trước đó của con người. Từ dữ liệu tĩnh này, A I xây dựng một mô hình thế giới toàn diện. Sau đó nó dùng mô hình này để ảo hóa các chuyến đi mới và học cách tự lái. Chúng ta loại bỏ hoàn toàn rủi ro hỏng hóc thiết bị vật lý trong quá trình thu thập kinh nghiệm.',
            formula='Static Dataset \\to World Model \\to Policy Optimization',
            visual_hints=['Xe tự lái đâm liên tục vào tường để thử nghiệm cách rẽ phải.', 'Hàng đống ổ cứng chứa video hành trình đổ dữ liệu vào máy chủ A I.', 'Chiếc xe ảo chạy hàng ngàn lần bên trong môi trường mô phỏng do mô hình thế giới tạo ra.'],
            pattern='World Model Rollout',
            duration=40.872,
        )
