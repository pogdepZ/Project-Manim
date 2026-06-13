#!/usr/bin/env python3
"""
Generate Vietnamese narration using Microsoft Edge TTS.
Run: python generate_narration.py

Requires: pip install edge-tts pydub
"""

import asyncio
import argparse
import re
import subprocess
import sys
from pathlib import Path

from project_config import BASE_DIR, PROJECTS, get_project

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts
REPLACEMENTS = {
    # Full phrases first (longest matches first to avoid partial replacements)
    "Out-of-Distribution Generalization": "ao ốp đít-tri-biu-sơn gien-nơ-ra-lai-zei-sơn",
    "Out-of-Distribution": "ao ốp đít-tri-biu-sơn",
    "Object-Centric Learning": "Ób-jếct Xen-tríc Lơ-ning",
    "Object-centric representation": "Ób-jếct xen-tríc rép-ri-zen-tei-sơn",
    "Object-Centric": "Ób-jếct Xen-tríc",
    "Object-centric": "Ób-jếct xen-tríc",
    "object-centric": "ób-jếct xen-tríc",
    "Structured Representation": "Strắc-chờ Rép-ri-zen-tei-sơn",
    "structured representation": "strắc-chờ rép-ri-zen-tei-sơn",
    "Machine Learning": "Ma-shin Lơ-ning",
    "machine learning": "ma-shin lơ-ning",
    "Slot Attention": "Slót A-ten-sơn",
    "slot attention": "slót a-ten-sơn",
    "Computer Vision": "Côm-piu-tơ Vi-sơn",
    "computer vision": "côm-piu-tơ vi-sơn",
    "embodied AI": "em-bô-điết A I",
    "AI": "A I",
    "systematic generalization": "xít-te-ma-tic gien-nơ-ra-lai-zei-sơn",
    "grid representation": "grít rép-ri-zen-tei-sơn",
    "set representation": "sét rép-ri-zen-tei-sơn",
    "scene understanding": "xin ăn-dơ-stăn-đing",
    "feature map": "phi-chờ máp",
    "synthetic data": "sin-the-tic đa-ta",
    "real-world data": "rin-ruôn đa-ta",
    
    # Capitalized Words (for start of sentence)
    "Object": "Ób-jếct",
    "Objects": "Ób-jếct",
    "Pixel": "Píc-xơ",
    "Pixels": "Píc-xơ",
    "Scene": "Xin",
    "Scenes": "Xin",
    "Slot": "Slót",
    "Slots": "Slót",
    "Vector": "Véc-tơ",
    "Vectors": "Véc-tơ",
    "Feature": "Phi-chờ",
    "Features": "Phi-chờ",
    "Dataset": "Đa-ta-sét",
    "Datasets": "Đa-ta-sét",
    "Pattern": "Pát-tờn",
    "Patterns": "Pát-tờn",
    "Texture": "Tếch-chờ",
    "Background": "Bách-grao",
    "LEGO": "Le-go",

    # Lowercase Words
    "CLEVR": "cle-vơ",
    "Multi-dSprites": "mơ-ti đi-xơ-pờ-rai",
    "compositionuality": "côm-pơ-zi-sơ-na-li-ti",
    "representation": "rép-ri-zen-tei-sơn",
    "representations": "rép-ri-zen-tei-sơn",
    "generalization": "gien-nơ-ra-lai-zei-sơn",
    "background": "bách-grao",
    "pattern": "pát-tờn",
    "patterns": "pát-tờn",
    "pixel": "píc-xơ",
    "pixels": "píc-xơ",
    "object": "ób-jếct",
    "objects": "ób-jếct",
    "scene": "xin",
    "scenes": "xin",
    "tutorial": "tu-to-ri-ân",
    "vector": "véc-tơ",
    "vectors": "véc-tơ",
    "dataset": "đa-ta-sét",
    "datasets": "đa-ta-sét",
    "synthetic": "sin-the-tic",
    "texture": "tếch-chờ",
    "encoder": "en-cô-dơ",
    "feature": "phi-chờ",
    "features": "phi-chờ",
    "slot": "slót",
    "slots": "slót",
    "grid": "grít",
    "set": "sét",
    "test": "tét",
    "attention": "a-ten-sơn",
    "reasoning": "ri-zơ-ning",
    "planning": "pờ-lan-ning",
    "robotics": "rô-bốt-tíc",
    "robot": "rô-bốt",
}

def preprocess_text(text):
    # Sort keys by length in descending order
    sorted_keys = sorted(REPLACEMENTS.keys(), key=len, reverse=True)
    
    for key in sorted_keys:
        val = REPLACEMENTS[key]
        pattern = r''
        if key[0].isalnum():
            pattern += r'\b'
        pattern += re.escape(key)
        if key[-1].isalnum():
            pattern += r'\b'
            
        text = re.sub(pattern, val, text)
    return text


narrations = {
    "scene1": (
        "Hãy nhìn vào bức ảnh này. Chỉ trong một phần giây, chúng ta có thể nhận ra rất nhiều thứ cùng lúc. "
        "Một chiếc xe đang ở phía trước. Một người đi bộ đang đứng bên đường. Một cái cây nằm ở phía sau. "
        "Có thể còn có biển báo, mặt đường, bóng đổ, và nhiều chi tiết nhỏ khác. Điều thú vị là chúng ta "
        "không cần phải đếm từng điểm ảnh để hiểu bức ảnh này. Không ai trong chúng ta nhìn vào ảnh và nghĩ "
        "rằng: đây là một ma trận gồm hàng triệu giá trị màu sắc. Chúng ta nhìn thấy các đối tượng. "
        "Chúng ta nhìn thấy ý nghĩa. Chúng ta hiểu được một phần cấu trúc của scene. Hãy tưởng tượng bạn "
        "đang lái xe ngoài đời thực. Chỉ trong vài giây, bộ não của bạn phải nhận ra xe phía trước, "
        "người đi bộ bên lề đường, tín hiệu giao thông, và những vật thể có thể gây nguy hiểm. Điều đáng "
        "kinh ngạc là con người làm điều này gần như tự động. Không cần tính toán thủ công từng pixel. "
        "Không cần phân tích từng giá trị màu. Bộ não con người trực tiếp nhận ra các object và mối quan hệ "
        "giữa chúng. Nhưng đối với máy tính, mọi thứ bắt đầu theo một cách rất khác."
    ),
    "scene2": (
        "Khi phóng to một bức ảnh đủ nhiều lần, thứ còn lại chỉ là các pixel. Mỗi pixel đơn giản chỉ là "
        "những con số biểu diễn màu sắc. Không có khái niệm xe. Không có khái niệm người. Không có khái niệm cây. "
        "Chỉ có dữ liệu. Đối với máy tính, một bức ảnh ban đầu không phải là một cảnh có ý nghĩa. Nó là một tập "
        "hợp rất lớn các con số. Và điều này dẫn đến một câu hỏi quan trọng. Nếu máy tính chỉ nhìn thấy các con số, "
        "làm thế nào nó có thể hiểu được thế giới?"
    ),
    "scene3": (
        "Trong Machine Learning hiện đại, mô hình được huấn luyện bằng cách quan sát rất nhiều ví dụ. Ví dụ, "
        "nếu muốn nhận diện mèo, chúng ta cung cấp cho mô hình hàng nghìn bức ảnh mèo. Sau quá trình huấn luyện, "
        "mô hình dần học được các pattern xuất hiện thường xuyên trong dữ liệu. Kết quả là nó có thể dự đoán "
        "khá chính xác liệu một bức ảnh có chứa mèo hay không. Trên tập kiểm tra, mô hình thậm chí có thể đạt "
        "độ chính xác rất cao. Tuy nhiên, độ chính xác cao không đồng nghĩa với việc mô hình thực sự hiểu được "
        "khái niệm mèo giống như con người. Nó có thể đang dựa vào những pattern trong dữ liệu, thay vì hiểu "
        "object theo nghĩa sâu hơn."
    ),
    "scene4": (
        "Hãy tưởng tượng một mô hình hoạt động rất tốt trên dữ liệu huấn luyện. Nó nhận diện ảnh mèo rất chính xác "
        "khi ảnh có ánh sáng tốt, góc chụp quen thuộc, và background tương tự dữ liệu đã học. Nhưng sau đó, "
        "chúng ta đưa cho nó một bức ảnh khác. Con mèo nằm trong tuyết. Hoặc con mèo bị che khuất một phần. "
        "Hoặc ảnh được chụp trong điều kiện ánh sáng yếu. Đối với con người, đó vẫn là một con mèo. Nhưng đối "
        "với mô hình, rất nhiều thứ đã thay đổi. Màu nền thay đổi. Texture thay đổi. Ánh sáng thay đổi. "
        "Một phần object có thể bị che mất. Những pattern mà mô hình từng dựa vào trước đó có thể không còn "
        "xuất hiện rõ ràng nữa. Đây là một trong những thách thức lớn của Machine Learning hiện đại. Mô hình có "
        "thể học rất tốt trên dữ liệu quen thuộc. Nhưng khi dữ liệu test khác với dữ liệu huấn luyện, hiệu năng "
        "có thể suy giảm đáng kể. Các nhà nghiên cứu gọi đây là vấn đề Out-of-Distribution Generalization. "
        "Nói đơn giản hơn, AI có thể hoạt động tốt trong môi trường quen thuộc, nhưng gặp khó khăn khi bước ra "
        "thế giới thực. Điều này khiến các nhà nghiên cứu đặt ra một câu hỏi mới. Liệu có cách nào để mô hình "
        "hiểu thế giới theo cách gần với con người hơn hay không?"
    ),
    "scene5": (
        "Một ý tưởng quan trọng trong tutorial là Structured Representation, hay biểu diễn có cấu trúc. Thay "
        "vì xem toàn bộ bức ảnh như một khối dữ liệu duy nhất, chúng ta cố gắng chia nó thành các thành phần "
        "có ý nghĩa. Ví dụ: một chiếc xe, một người đi bộ, một biển báo, và mặt đường. Những "
        "thành phần này không tồn tại riêng lẻ. Chúng còn có mối quan hệ với nhau. Người đi bộ có thể đang đứng "
        "cạnh đường. Xe có thể đang di chuyển về phía trước. Biển báo có thể nằm gần làn đường. Đó không chỉ là "
        "một tập hợp pixel. Đó là một scene có cấu trúc. Hãy tưởng tượng có hai bức ảnh khác nhau. Trong bức "
        "ảnh thứ nhất, một người đứng cạnh chiếc xe. Trong bức ảnh thứ hai, chiếc xe xuất hiện ở vị trí khác, "
        "người đứng ở góc nhìn khác, background cũng thay đổi. Về mặt pixel, hai bức ảnh này có thể rất khác "
        "nhau. Nhưng về mặt ý nghĩa, chúng vẫn chứa những thành phần quen thuộc: người, xe, đường. Điều đó cho "
        "thấy, khi hiểu được các object và quan hệ giữa chúng, mô hình có thể có một cách biểu diễn ổn định hơn "
        "so với chỉ dựa vào pixel. Cách biểu diễn này gần hơn với cách con người quan sát và suy nghĩ về thế giới."
    ),
    "scene6": (
        "Hãy tưởng tượng bạn có một hộp LEGO. Bạn không học thuộc từng mô hình LEGO hoàn chỉnh. Bạn học từng "
        "mảnh ghép. Sau đó, từ những mảnh ghép đó, bạn có thể tạo ra rất nhiều cấu trúc mới. Object-centric "
        "representation cũng có trực giác tương tự. Nếu mô hình hiểu các thành phần cơ bản của thế giới, nó có "
        "thể sử dụng lại kiến thức đó trong những tình huống mới. Ví dụ, nếu mô hình đã hiểu thế nào là một chiếc "
        "xe, một người, và một con đường, thì khi gặp một scene mới có cách sắp xếp khác, nó vẫn có thể suy luận "
        "dựa trên những thành phần quen thuộc đó. Đây là ý tưởng liên quan đến compositionality. Tức là khả năng "
        "kết hợp các thành phần đã học để hiểu những tình huống mới. Và từ đó dẫn đến systematic generalization. "
        "Tức là khả năng tổng quát hóa có hệ thống sang các trường hợp chưa từng xuất hiện trong dữ liệu huấn luyện. "
        "Đây là một trong những lý do khiến structured representation trở thành một hướng nghiên cứu quan trọng "
        "trong Computer Vision."
    ),
    "scene7": (
        "Từ những ý tưởng đó, một hướng nghiên cứu được hình thành. Đó là Object-Centric Learning. Mục tiêu của "
        "hướng nghiên cứu này là học representation ở mức object thay vì chỉ ở mức pixel. Thay vì hỏi: 'Bức ảnh "
        "này trông như thế nào?' Mô hình bắt đầu hỏi: 'Có những object nào đang tồn tại trong scene?' Mỗi object "
        "có thể được biểu diễn bằng một vector riêng. Những vector này có thể được sử dụng cho các tác vụ khác "
        "nhau như scene understanding, reasoning, planning hoặc robotics. Đây là lý do Object-Centric Learning "
        "được quan tâm trong nhiều hướng nghiên cứu hiện đại. Đặc biệt là trong các hệ thống cần tương tác với "
        "môi trường thật như robot, xe tự hành, hoặc embodied AI. Những hệ thống này không chỉ cần nhận diện ảnh. "
        "Chúng cần hiểu môi trường xung quanh gồm những object nào, object nào đang di chuyển, object nào có thể "
        "tương tác, và điều gì có thể thay đổi trong scene."
    ),
    "scene8": (
        "Nhưng làm thế nào để máy tính tự tìm ra các object? Đây là lúc Slot Attention xuất hiện. Sau khi encoder "
        "trích xuất feature từ ảnh, mô hình tạo ra một tập các slot. Có thể hình dung slot giống như những chiếc "
        "hộp trống. Ban đầu, chúng chưa biết mình sẽ chứa thông tin gì. Nhiệm vụ của chúng là tìm cách giải thích "
        "những gì đang xuất hiện trong scene. Mỗi slot là một representation được học trong quá trình huấn luyện. "
        "Nó không phải là nhãn object được con người gán sẵn. Đó là lý do Slot Attention đặc biệt thú vị trong "
        "Object-Centric Learning."
    ),
    "scene9": (
        "Hãy tưởng tượng có năm người cùng nhìn vào một bức tranh. Mỗi người cố gắng mô tả một phần khác nhau "
        "của bức tranh đó. Nếu hai người cùng mô tả một vùng, sẽ có sự cạnh tranh. Dần dần, mỗi người sẽ chuyên "
        "môn hóa vào một khu vực riêng. Slot Attention hoạt động theo trực giác tương tự. Mỗi slot sẽ cạnh tranh "
        "với các slot khác để nhận trách nhiệm giải thích một phần dữ liệu. Thông qua cơ chế attention, các slot "
        "dần tập trung vào những vùng khác nhau của ảnh. Một slot có thể học về chiếc xe. Một slot khác có thể "
        "học về người đi bộ. Một slot khác nữa có thể tập trung vào background. Quá trình này diễn ra tự động "
        "trong quá trình huấn luyện. Tuy nhiên, cần nói chính xác rằng một slot không phải lúc nào cũng tương ứng "
        "hoàn hảo với một object trong mọi trường hợp. Ta nên hiểu slot là một representation được mô hình học "
        "để giải thích cấu trúc trong dữ liệu."
    ),
    "scene10": (
        "Thông thường, feature map của ảnh được biểu diễn dưới dạng lưới hai chiều. Giống như một bản đồ các "
        "đặc trưng trải đều trên không gian ảnh. Slot Attention chuyển representation này thành một tập các vector "
        "độc lập. Ta có thể hình dung quá trình này là chuyển từ grid representation sang set representation. "
        "Thay vì chỉ giữ thông tin theo vị trí pixel, mô hình học một tập các biểu diễn trừu tượng hơn. Mỗi vector "
        "có thể mang thông tin về một phần khác nhau của scene. Điều này giúp mô hình tiến gần hơn tới cách "
        "biểu diễn thế giới theo từng object riêng biệt."
    ),
    "scene11": (
        "Slot Attention đã đạt được những kết quả rất ấn tượng trên các dataset synthetic như CLEVR hay Multi-dSprites. "
        "Trong những môi trường được kiểm soát tốt, object thường rõ ràng hơn. Background đơn giản hơn. Và các "
        "yếu tố gây nhiễu thường ít phức tạp hơn so với dữ liệu thực tế. Điều đáng chú ý là mô hình không cần "
        "được cung cấp nhãn object thủ công. Không ai nói trước với mô hình: đây là xe, đây là người, đây là hình "
        "cầu, đây là background. Tuy nhiên, trong nhiều trường hợp, các slot vẫn có thể học được những cấu trúc "
        "có ý nghĩa. Đó là lý do Slot Attention trở thành một cột mốc quan trọng trong Object-Centric Learning."
    ),
    "scene12": (
        "Tuy nhiên, thế giới thực không giống các dataset synthetic đơn giản. Object có texture phức tạp hơn. "
        "Ánh sáng thay đổi liên tục. Các vật thể có thể che khuất lẫn nhau. Background chứa rất nhiều nhiễu. "
        "Một chiếc xe ngoài đời không chỉ là một khối hình đơn giản. Nó có kính, kim loại, bóng đổ, phản chiếu, "
        "logo, vết bẩn, và có thể bị che bởi những object khác. Khi chuyển sang dữ liệu thực tế, Slot Attention "
        "và các phương pháp object-centric ban đầu bắt đầu gặp nhiều thách thức hơn."
    ),
    "scene13": (
        "Vậy câu hỏi đặt ra là: Làm thế nào để đưa Object-Centric Learning từ những thế giới đơn giản trong "
        "phòng thí nghiệm bước ra dữ liệu thực tế? Trong phần tiếp theo, chúng ta sẽ khám phá khoảng cách "
        "giữa synthetic data và real-world data, cũng như những hướng nghiên cứu được đề xuất để thu hẹp khoảng cách đó."
    ),
}

VOICE = "vi-VN-HoaiMyNeural"
RATE = "+0%"


def parse_args():
    parser = argparse.ArgumentParser(description="Generate narration for a project.")
    parser.add_argument(
        "--project",
        default="object_centric_learning",
        choices=sorted(PROJECTS),
        help="Project key from project_config.py.",
    )
    return parser.parse_args()


async def generate_narration(key, text, output_file):
    processed_text = preprocess_text(text)
    if processed_text != text:
        print(f"🔄  Preprocessed English words for {key}")
    for attempt in range(1, 4):
        print(f"🎙️  Generating: {output_file}... attempt {attempt}/3")
        try:
            communicate = edge_tts.Communicate(text=processed_text, voice=VOICE, rate=RATE)
            await communicate.save(output_file)
            if Path(output_file).stat().st_size == 0:
                raise RuntimeError("TTS returned an empty file")
            print(f"✓ {output_file} created ({len(processed_text)} chars)")
            return
        except Exception as exc:
            if attempt == 3:
                raise
            print(f"  retrying after TTS error: {exc}")
            await asyncio.sleep(2)


async def main():
    args = parse_args()
    project = get_project(args.project)
    narration_keys = project.get("narration_keys", [])
    if not narration_keys:
        raise SystemExit(f"Project '{args.project}' has no narration_keys configured.")

    missing = [key for key in narration_keys if key not in narrations]
    if missing:
        raise SystemExit(
            f"Missing narration text for project '{args.project}': {', '.join(missing)}"
        )

    print("=" * 60)
    print("Vietnamese Narration Generator (Edge TTS)")
    print("=" * 60)

    output_dir = BASE_DIR / "narration" / args.project
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Output directory: {output_dir}")
    print(f"🎞️  Project: {project['title']}")
    print(f"🎤 Voice: {VOICE}\n")

    for key in narration_keys:
        text = narrations[key]
        output_file = output_dir / f"{key}.mp3"
        await generate_narration(key, text, str(output_file))

    print("\n" + "=" * 60)
    print("✓ All narration files generated!")
    print("=" * 60)
    print(f"\nNext step: python combine_video_audio.py --project {args.project}")


if __name__ == "__main__":
    asyncio.run(main())
