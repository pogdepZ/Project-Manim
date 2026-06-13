from __future__ import annotations

from manim import *
from visual_beats import VisualBeatScene


class GeneratedVideo(VisualBeatScene):
    def construct(self):
        self.show_scene(
            title='Ngẫu nhiên hóa miền (Domain Randomization)',
            voice='Huấn luyện trên vật lý ngẫu nhiên để tổng quát hóa ra thực tế. Một kỹ thuật phổ biến để hỗ trợ Sim to Real là Ngẫu nhiên hóa miền. Trong giả lập, ta thay đổi liên tục mọi thông số vật lý một cách ngẫu nhiên. Hôm nay sàn nhà trơn như băng, ngày mai trọng lực nặng gấp đôi. Quả bóng bay lúc màu đỏ, lúc màu xanh lá cây chớp nháy loạn xạ. Bằng cách ép A I sinh tồn trong sự hỗn loạn, nó bị ép phải tìm ra các quy luật nhân quả lõi ẩn bên dưới sự nhiễu loạn bề mặt đó. Khi đưa ra môi trường thật, A I chỉ xem thế giới thực là một trong muôn vàn các thông số ngẫu nhiên mà nó đã từng vượt qua.',
            formula='Train on random physics \\to Generalize to reality',
            visual_hints=['Màn hình mô phỏng tự động đổi màu tường, đổi khối lượng đồ vật, đổi mức trọng lực.', 'Các đồ vật thay đổi hình dáng và vật liệu liên tục theo tần số chớp mắt.', 'Robot vẫn đi vững vàng tiến về phía trước mặc cho môi trường xung quanh thay đổi bão táp.'],
            pattern='Distribution Shift',
            duration=37.272,
        )
