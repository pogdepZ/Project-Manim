import re

extensions = [
    "Sự chuyển đổi từ không gian vật lý sang ma trận điểm ảnh là bước đầu tiên để hệ thống thị giác máy tính bắt đầu quy trình nhận thức.",
    "Bằng cách chia tách không gian màu RGB, hệ thống máy học có thể phân tích cường độ sáng một cách độc lập trước khi tái tạo lại vật thể.",
    "Quá trình nén thông qua các tầng nơ ron chập giúp trích xuất các đặc trưng bất biến, giảm thiểu đáng kể chi phí tính toán.",
    "Không gian biểu diễn ẩn bị rối khiến các thuật toán phân lớp truyền thống không thể vạch ra ranh giới quyết định chính xác.",
    "Phương pháp học không giám sát này mở ra kỷ nguyên mới, nơi máy móc tự khám phá cấu trúc tự nhiên mà không phụ thuộc vào nhãn thủ công.",
    "Đặc tính bất biến với hoán vị của các slot đảm bảo rằng kiến trúc mạng nơ ron không bị phụ thuộc vào thứ tự ngẫu nhiên của các đối tượng.",
    "Bằng việc sử dụng kỹ thuật Softmax có chuẩn hóa, mỗi điểm ảnh bị bắt buộc phải cạnh tranh để thuộc về một vùng chú ý duy nhất.",
    "Sự cạnh tranh này dựa trên nguyên lý thắt nút cổ chai thông tin, ép buộc mô hình phải loại bỏ sự dư thừa.",
    "Hàm suy hao tái tạo đóng vai trò như một tín hiệu giám sát mạnh mẽ, tối ưu hóa các trọng số của bộ mã hóa và giải mã.",
    "Sự chênh lệch miền dữ liệu này chính là bài toán chuyển giao học máy cốt lõi mà các kỹ sư A I đang nỗ lực giải quyết.",
    "Kiến trúc Transformer với cơ chế tự chú ý toàn cục cho phép mô hình nhìn bao quát toàn bộ bức ảnh ngay từ những tầng xử lý đầu tiên.",
    "Sự tinh cất tri thức từ Đi nô giúp duy trì tính nhất quán về mặt hình học, đảm bảo quá trình chia slot hội tụ nhanh hơn.",
    "Việc xây dựng một đồ thị quan hệ giữa các biểu diễn này cung cấp một cấu trúc dồi dào cho các mạng nơ ron đồ thị G N N hoạt động.",
    "Những tương quan rác này là nguyên nhân chính khiến các mô hình học sâu hiện đại sụp đổ khi được triển khai trong thực tế.",
    "Việc mô phỏng toán tử do cho phép chúng ta phá vỡ các liên kết nhân quả giả tạo, hướng tới sự hiểu biết cốt lõi về hệ thống.",
    "Sự khác biệt giữa phân phối có điều kiện và phân phối can thiệp chính là chìa khóa để A I đạt được khả năng suy luận phi nghịch đảo.",
    "Khi xác định được đồ thị nhân quả cấu trúc, chúng ta có thể phân tích được sự can thiệp và dự đoán chính xác trong các kịch bản giả định.",
    "Đây là nền tảng để xây dựng các mô hình vật lý trực quan, giúp robot tương tác an toàn với thế giới xung quanh.",
    "Bảo toàn các đại lượng vật lý như động lượng trong không gian biểu diễn ẩn giúp tăng cường tính bền vững của mô hình.",
    "Bằng cách neo các biến số nhân quả vào các slot đối tượng, chúng ta giải quyết được bài toán khó nhất trong việc khám phá nhân quả.",
    "Sự bền vững đối với các biến thể ngoài phân phối chứng minh rằng mô hình đã thực sự học được các cơ chế vật lý nền tảng.",
    "Khả năng theo dõi đối tượng ẩn đòi hỏi bộ nhớ tuần tự tinh vi, thường được xử lý qua mạng nơ ron hồi quy hoặc Transformer.",
    "Việc triển khai các chuỗi tự hồi quy bên trong không gian ẩn cho phép dự báo các kịch bản dài hạn mà không tốn kém chi phí render đồ họa.",
    "Khả năng học tăng cường dựa trên mô hình này giảm đáng kể số lượng mẫu thử nghiệm cần thiết để robot thành thạo một kỹ năng.",
    "Hệ thống tránh va chạm tích cực sử dụng mô hình nhân quả để lọc bỏ nhiễu từ các phương tiện không ảnh hưởng đến quỹ đạo của chúng ta.",
    "Bằng cách mô phỏng các chính sách khác nhau bên trong mô hình thế giới, tác nhân có thể đạt được phần thưởng tối đa mà không tốn chi phí rủi ro thực tế.",
    "Kỹ thuật giải thích mô hình A I như thế này đặc biệt cấp thiết để đáp ứng các tiêu chuẩn khắt khe về đạo đức và pháp lý trong y khoa.",
    "Hệ thống ra quyết định phân tán dựa trên bản sao số có thể tối ưu hóa lưu lượng giao thông toàn thành phố theo thời gian thực.",
    "Khả năng liên kết ngôn ngữ tự nhiên với các đối tượng hình học tạo nên các mô hình nền tảng đa phương thức mạnh mẽ.",
    "Vượt qua sự bùng nổ tổ hợp trong không gian trạng thái thực sự là một rào cản lớn về mặt tính toán và thuật toán học sâu hiện nay.",
    "Đây chính là bình minh của trí tuệ nhân tạo tổng quát, nơi máy móc không chỉ nhận diện mà thực sự thấu hiểu sự vận hành của vũ trụ."
]

def main():
    with open("input/script.txt", "r", encoding="utf-8") as f:
        text = f.read()

    sections = re.split(r'(## \d+\. .*?\n)', text)
    if not sections[0].strip():
        sections = sections[1:]

    new_text = ""
    ext_index = 0

    for i in range(0, len(sections), 2):
        heading = sections[i]
        body = sections[i+1] if i+1 < len(sections) else ""
        
        if ext_index < len(extensions):
            # Append the extension to the end of the voiceover section
            body = body.rstrip() + "\n" + extensions[ext_index] + "\n\n"
            ext_index += 1
            
        new_text += heading + body

    with open("input/script.txt", "w", encoding="utf-8") as f:
        f.write(new_text)
        
    print(f"Expanded {ext_index} scenes with deep AI context.")

if __name__ == "__main__":
    main()