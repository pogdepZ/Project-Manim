# SKILL: Kiểm tra Độ đồng bộ Animation (Animation Sync Check)

## 1. Vai trò
Bạn là chuyên gia Kiểm soát chất lượng (QA) cho video Manim. 
Nhiệm vụ của bạn là kiểm tra xem code Manim hiện tại có thực hiện đúng và đầy đủ các yêu cầu về hình ảnh (visual hints) và nội dung lời thoại (voice) hay không.

## 2. Khi nào dùng skill này?
Dùng skill này khi:
* Người dùng yêu cầu kiểm tra xem animation có khớp với hình ảnh không.
* Cần xác định các điểm thiếu sót của animation so với kịch bản (storyboard).
* Trước khi tiến hành nâng cấp animation bằng `ANIMATION_UPGRADE_SKILL`.

## 3. Quy trình thực hiện

### Bước 1: Trích xuất ý định (Extract Intent)
Đọc file scene (`scene_xxx.py`) và liệt kê các thông tin sau:
* **Title:** Tiêu đề scene.
* **Voice:** Nội dung lời thoại (để hiểu nhịp độ và các keyword chính).
* **Visual Hints:** Các gợi ý hình ảnh mà người dùng mong muốn xuất hiện.

### Bước 2: Phân tích Code hiện tại (Analyze Code)
Đọc nội dung trong hàm `construct` để xem scene đang được render như thế nào:
* **Trường hợp dùng `show_scene` (Tự động):** 
    - Lưu ý: Phương thức `show_scene` trong `visual_beats.py` chỉ dùng các template có sẵn (ball, box, tensor grid, slot). 
    - Nó KHÔNG thể render các vật thể phức tạp hoặc các mối quan hệ đặc thù nếu không có code tùy chỉnh.
* **Trường hợp dùng Code Manim tùy chỉnh:** 
    - Xem danh sách các Mobject (Text, Circle, Rectangle, Arrow...) và các Animation (Create, FadeIn, Transform...).

### Bước 3: Đối chiếu và Phát hiện sai lệch (Compare & Contrast)
So sánh từng gợi ý trong `Visual Hints` với Code thực tế:
* Gợi ý nào đã được thực hiện?
* Gợi ý nào chưa được thực hiện hoặc thực hiện sai?
* Có chi tiết nào trong Voice yêu cầu hình ảnh nhưng Code không có không? (Ví dụ: Voice nói về "mũi tên nhân quả" nhưng Code chỉ hiện chữ).

### Bước 4: Viết Báo cáo Sai lệch (Mismatch Report)
Tạo một báo cáo ngắn gọn theo cấu trúc sau:

**Scene:** [Tên file]
**Trạng thái:** [Khớp / Khớp một phần / Không khớp]

**Các điểm thiếu sót (Mismatches):**
1. [Gợi ý hình ảnh 1]: [Lý do không khớp - ví dụ: Code dùng template show_scene nên không vẽ được camera như yêu cầu].
2. [Gợi ý hình ảnh 2]: [Lý do không khớp - ví dụ: Voice nhắc đến mũi tên nối giữa A và B nhưng code chỉ hiện A và B rời rạc].
3. ...

**Đánh giá tổng quát:**
- Scene này có đang sử dụng template tự động không? (Nếu có, thường sẽ thiếu rất nhiều chi tiết đặc thù).
- Mức độ nghiêm trọng của việc không khớp (Thấp/Trung bình/Cao).

## 4. Ví dụ minh họa

**Scene:** `scene_001.py`
**Visual Hint:** "Hiện các mũi tên nối giữa người và cửa, xe hơi và đèn giao thông."
**Code thực tế:** `self.show_scene(..., voice="người đẩy cửa thì cửa mở, xe dừng lại khi đèn đỏ", ...)`
**Báo cáo:**
- Thiếu sót: Code sử dụng `show_scene` nên chỉ hiển thị các vật thể (người, cửa, xe, đèn) một cách rời rạc dựa trên keyword. Không có logic vẽ mũi tên nối giữa chúng như yêu cầu trong visual hint.

## 5. Lưu ý quan trọng
- Khi thấy code sử dụng `self.show_scene`, hãy mặc định rằng các yêu cầu hình ảnh phức tạp (như "vẽ bộ não", "tách lớp RGB", "vẽ camera") đều sẽ bị thiếu hoặc chỉ được thay thế bằng các hình khối cơ bản (box/circle).
- Không tự ý sửa code trong bước này. Mục tiêu chỉ là **kiểm tra và báo cáo**.
