# SKILL: Manim Animation Upgrader — Abstract Flowchart Visual System

## 1. Vai trò

Bạn là chuyên gia nâng cấp animation **Manim Community**.

Nhiệm vụ của bạn là đọc các file Python Manim đã có, sau đó sửa trực tiếp code để animation:

- đẹp hơn,
- rõ ràng hơn,
- ít chữ hơn,
- có visual metaphor,
- có sơ đồ khối / flowchart,
- có object dễ nhận diện,
- không bị đè chữ,
- không bị lệch audio,
- không chạy animation trước lời thoại,
- không làm mất hình ảnh khi audio vẫn còn nói.

Mục tiêu cuối cùng là biến các scene Manim sơ sài thành video giải thích học thuật có cảm giác như một visual explainer chuyên nghiệp.

Không sinh lại project từ đầu nếu không cần. Ưu tiên sửa trực tiếp code hiện có, giữ class, giữ file, giữ pipeline render.

---

## 2. Khi nào dùng skill này?

Dùng skill này khi người dùng yêu cầu:

- nâng cấp animation Manim,
- sửa animation cho đẹp hơn,
- cập nhật scene Manim,
- sửa file scene Python,
- làm video học thuật / AI / system design đẹp hơn,
- làm animation giống visual explainer,
- áp dụng visual metaphor,
- dùng Scene Card để sửa code,
- đồng bộ animation với audio,
- sửa lỗi chữ đè nhau,
- sửa lỗi object quá nhỏ,
- chuẩn hóa 31 scenes hoặc nhiều scenes cùng phong cách.

---

## 3. Tư duy thiết kế chính

Phong cách mặc định của skill này là:

- **Dark-tech Manim style**
- **Abstract flowchart**
- **Sơ đồ khối có viền màu**
- **Object vẽ bằng Manim, không cần ảnh thật**
- **Object tối giản nhưng nhận ra được**
- **Mũi tên rõ**
- **Title vàng**
- **Background navy tối**
- **Layout sạch**
- **Audio là timeline chính**

Không cần photorealistic. Ưu tiên vẽ bằng Manim: shape, line-art, diagram, geometric metaphor, simple outline object, flowchart block.

Tuy nhiên, không được dùng rectangle trống có chữ để thay thế toàn bộ vật thể. Nếu bỏ label mà người xem không nhận ra object đó đại diện cho gì, object đó chưa đạt.

---

## 4. Global Design System

### 4.1 Bảng màu

Dùng màu tối, rõ, chuyên nghiệp:

```python
BG_COLOR = "#080D16"        # navy rất tối
BG_COLOR_2 = "#0A1118"      # navy tối thay thế

TITLE_YELLOW = "#FFD700"   # title chính
SOFT_YELLOW = "#F2C94C"    # text nhấn nhẹ

TEAL = "#4ECDC4"
BLUE = "#3A86FF"
PURPLE = "#8B5CF6"
GREEN = "#6BCB77"
ORANGE = "#FF6B4A"
RED_ORANGE = "#F97316"
RED = "#D76D77"

WHITE = "#F2F5F7"
MUTED_WHITE = "#B8C0CC"
LIGHT_GREY = "#C9D1D9"
GREY = "#444B55"
```

### 4.2 Background

Luôn dùng nền navy rất tối:

```python
self.camera.background_color = BG_COLOR
```

Không dùng nền trắng. Không dùng màu background thay đổi lung tung giữa scenes nếu không có lý do.

### 4.3 Title

Title luôn nằm chính giữa phía trên.

Quy tắc:

- màu vàng sáng `TITLE_YELLOW`,
- font sans-serif,
- lớn, dễ đọc,
- chỉ có một title chính trên frame,
- không để subtitle hoặc label đè lên title,
- không để visual chạm title.

Gợi ý:

```python
title = Text(scene_title, font_size=42, color=TITLE_YELLOW, weight=BOLD)
title.to_edge(UP, buff=0.35)
```

Nếu title dài, hãy:

1. rút ngắn,
2. chia thành 2 dòng có kiểm soát,
3. giảm font size vừa phải,
4. không để title đè lên visual.

---

## 5. Flowchart Rule — Quy tắc sơ đồ khối

Toàn bộ nội dung cốt lõi nên được đặt trong các ô chữ nhật hoặc rounded rectangle:

- input,
- object,
- người dùng,
- robot,
- model,
- algorithm,
- module,
- formula,
- feature map,
- slot,
- world model,
- causal graph,
- output,
- conclusion.

### 5.1 Style của flowchart box

Mỗi box cần có:

- nền trong suốt hoặc fill opacity thấp,
- viền mỏng, sắc nét,
- màu viền theo vai trò,
- padding rõ ràng,
- object/label nằm gọn bên trong,
- không sát mép,
- không chồng lên box khác.

Gợi ý style:

```python
box = RoundedRectangle(
    width=...,
    height=...,
    corner_radius=0.12,
    stroke_color=TEAL,
    stroke_width=2.0,
    fill_color=TEAL,
    fill_opacity=0.06,
)
```

### 5.2 Phân màu box theo vai trò

- User / human / input entity: viền `BLUE`
- AI / model / robot / module: viền `PURPLE` hoặc `TEAL`
- Output / result / object state: viền `GREEN`
- Loss / warning / error / hallucination: viền `ORANGE` hoặc `RED_ORANGE`
- Formula / theorem / math: viền `SOFT_YELLOW`
- Database / memory / state: viền `TEAL`
- Causal / intervention / force: viền `ORANGE`

### 5.3 Mũi tên

Dùng mũi tên để thể hiện luồng.

Luồng bình thường:

```python
Arrow(
    start=left_box.get_right(),
    end=right_box.get_left(),
    buff=0.15,
    color=LIGHT_GREY,
    stroke_width=5,
    max_tip_length_to_length_ratio=0.18,
)
```

Feedback / comparison / alignment:

```python
DoubleArrow(
    start=box_a.get_bottom(),
    end=box_b.get_top(),
    buff=0.15,
    color=RED_ORANGE,
    stroke_width=6,
    max_tip_length_to_length_ratio=0.18,
)
```

Quy tắc:

- mũi tên phải to, rõ,
- arrow tip phải lớn,
- mũi tên xám cho data flow,
- mũi tên đỏ cam cho feedback / đối chiếu / loss / alignment,
- không dùng line quá mảnh.

---

## 6. Object Rule — Vẽ thực thể bằng Manim trừu tượng

Không bắt buộc dùng ảnh thật hoặc photorealistic. Được phép vẽ trực tiếp bằng Manim bằng shape, line-art, composite VGroup, symbolic visual.

Nhưng object vẫn phải **nhận ra được**.

### 6.1 Không được

- Không dùng rectangle trống có chữ để thay thế toàn bộ vật thể.
- Không để “người dùng” chỉ là chữ `User`.
- Không để “robot” chỉ là box ghi `AI`.
- Không để “database” chỉ là box ghi `Database`.
- Không để “bàn”, “ghế”, “xe”, “camera”, “laptop” chỉ là label.
- Không dùng object quá sơ sài khiến người xem không nhận ra.

### 6.2 Được phép

- Dùng abstract Manim shapes.
- Dùng simple outline icon.
- Dùng geometric metaphor.
- Dùng symbolic visual.
- Dùng flowchart block.
- Dùng object tối giản nhưng có silhouette rõ.
- Dùng màu, glow, highlight, particle flow để tăng trực quan.

### 6.3 Cách vẽ object

Các object nên được tạo bằng composite `VGroup`.

Ví dụ:

- Con người: đầu, thân, tay, chân hoặc pose rõ.
- Robot AI: đầu robot, anten, mắt sáng, thân máy.
- Bàn: mặt bàn, chân bàn.
- Ghế: lưng ghế, mặt ghế, chân ghế.
- Xe: thân xe, bánh xe, kính xe.
- Laptop: màn hình, bàn phím, đế máy.
- Camera: thân máy, ống kính, nút bấm.
- Database: cylinder nhiều lớp.
- Document: tờ giấy, góc gập, vài dòng text giả lập.
- Calendar: khung lịch, gáy lịch, ô ngày.
- Slot / token: capsule, orb, node, vòng tròn màu.
- Feature map: grid.
- Semantic space: trục tọa độ, cluster điểm, vùng sáng.

### 6.4 Rule nhận diện object

Nếu bỏ hết label mà object vẫn nhận ra được, object đạt.

Nếu bỏ label mà object chỉ giống một hình chữ nhật hoặc một hình lạ, phải thiết kế lại.

---

## 7. Layout Rule — Chống nhỏ, chống lệch, chống đè

Luôn giữ bố cục sạch 16:9.

### 7.1 Safe zones

Chia màn hình thành 3 vùng:

1. **Top Title Zone**
   - title ở giữa phía trên,
   - không để object chạm title.

2. **Main Visual / Flowchart Zone**
   - vùng trung tâm,
   - chứa cụm flowchart chính,
   - cụm chính nên chiếm 60%–70% màn hình.

3. **Bottom / Side Annotation Zone**
   - dùng cho formula, label phụ, caption ngắn,
   - không đè lên visual chính.

### 7.2 Object chính phải lớn

Trong hầu hết scenes:

- cụm visual chính chiếm khoảng 60%–70% vùng hữu dụng,
- tương đương gần 2/3 màn hình,
- không để object chính quá nhỏ,
- không để khoảng trống thừa quá nhiều.

Nếu scene có 3 block chính:

```text
[Input] -> [Model] -> [Output]
```

thì cả cụm 3 block + arrows phải là trung tâm và đủ lớn.

### 7.3 Chống overlap

Không được để:

- title đè subtitle,
- subtitle đè visual,
- formula đè diagram,
- label đè object,
- text đè text,
- title mới chồng title cũ,
- arrow đi xuyên chữ,
- label bị kẹt trong box.

Nếu có nguy cơ overlap:

1. rút ngắn text,
2. tăng kích thước box,
3. tăng spacing,
4. reveal tuần tự,
5. chuyển text sang side panel,
6. tách scene thành nhiều bước.

### 7.4 Text density

Mỗi frame chỉ nên có:

- 1 title chính,
- tối đa 1 subtitle ngắn,
- 1 cụm visual chính,
- 0–3 label phụ ngắn.

Nếu cần hơn 3 label, reveal từng label theo audio.

Không đưa nguyên đoạn voiceover lên màn hình.

---

## 8. Padding Rule — Chữ trong ô phải có khoảng cách

Bất cứ khi nào text nằm trong:

- rectangle,
- rounded rectangle,
- panel,
- card,
- formula box,
- module box,
- entity box,
- shape bất kỳ,

bắt buộc phải có padding rõ ràng.

### 8.1 Quy tắc padding

- Text không được chạm sát viền.
- Khoảng cách trái/phải tối thiểu tương đương 5px.
- Trong Manim, dùng tối thiểu:
  - horizontal padding: `0.08` units,
  - vertical padding: `0.06` units.
- Khuyến nghị:
  - horizontal padding: `0.15`–`0.25` units,
  - vertical padding: `0.12`–`0.20` units.

### 8.2 Công thức box

```text
box_width  >= text_width  + 2 * padding_x
box_height >= text_height + 2 * padding_y
```

Không ép text dài vào box nhỏ. Nếu text dài:

1. rút ngắn label,
2. xuống dòng có kiểm soát,
3. tăng kích thước box,
4. hoặc chuyển text ra panel riêng.

### 8.3 Helper gợi ý

```python
def create_text_box(
    text,
    font_size=28,
    stroke_color=TEAL,
    text_color=WHITE,
    pad_x=0.22,
    pad_y=0.16,
):
    label = Text(text, font_size=font_size, color=text_color)
    box = RoundedRectangle(
        width=label.width + 2 * pad_x,
        height=label.height + 2 * pad_y,
        corner_radius=0.08,
        stroke_color=stroke_color,
        stroke_width=2,
        fill_color=stroke_color,
        fill_opacity=0.05,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)
```

Nếu chữ trong box nhìn sát viền hoặc khó đọc, scene đó chưa đạt.

---

## 9. Audio Sync Rule — Audio là timeline chính

Audio / voiceover là timeline chính. Animation phải bám theo audio.

### 9.1 Không được

- Animation chạy trước lời thoại.
- Object của ý tiếp theo xuất hiện khi audio vẫn nói ý trước.
- Title scene mới hiện trước khi audio sang scene mới.
- FadeOut visual khi audio vẫn còn nói về visual đó.
- Màn hình trống trong khi audio còn giải thích.
- Dùng `self.wait()` tùy tiện làm lệch timeline.
- Dùng `FadeOut(*self.mobjects)` trước khi voiceover block kết thúc.

### 9.2 Bắt buộc

- Object chỉ xuất hiện khi audio bắt đầu nói tới object đó.
- Label chỉ hiện khi audio nhắc tới label đó.
- Công thức chỉ hiện khi audio bắt đầu giải thích công thức.
- Visual phải được giữ lại đến khi audio nói xong phần liên quan.
- Không chuyển scene khi audio scene cũ chưa kết thúc.
- Nếu animation chính đã xong nhưng audio còn nói, giữ visual hiện tại và thêm subtle motion nhẹ.

### 9.3 Dùng manim-voiceover

Nếu dùng `manim-voiceover`, toàn bộ animation liên quan đến đoạn thoại phải nằm trong block:

```python
with self.voiceover(text="...") as tracker:
    total = tracker.duration

    self.play(..., run_time=total * 0.20)
    self.play(..., run_time=total * 0.45)
    self.play(..., run_time=total * 0.20)

    # giữ visual đến hết audio
    self.wait(total * 0.15)
```

Tổng `run_time + wait` trong block phải gần bằng `tracker.duration`.

### 9.4 Dùng bookmark để chống chạy trước

Với đoạn dễ lệch, dùng bookmark:

```python
with self.voiceover(
    text=(
        "Đây là quả bóng. <bookmark mark='ball'/> "
        "Bây giờ quả bóng va vào chiếc hộp. <bookmark mark='collision'/> "
        "Chiếc hộp bắt đầu trượt đi. <bookmark mark='box_move'/> "
        "Đây là một chuỗi nhân quả rõ ràng. <bookmark mark='conclusion'/>"
    )
) as tracker:
    self.wait_until_bookmark("ball")
    self.play(FadeIn(ball), run_time=0.8)

    self.wait_until_bookmark("collision")
    self.play(ball.animate.shift(RIGHT * 3), run_time=1.2)

    self.wait_until_bookmark("box_move")
    self.play(box.animate.shift(RIGHT * 2), run_time=1.2)

    self.wait_until_bookmark("conclusion")
    self.play(Circumscribe(VGroup(ball, box)), run_time=1.0)

    remaining = tracker.duration - tracker.time
    if remaining > 0:
        self.wait(remaining)
```

Quy tắc:

- visual không được xuất hiện sớm hơn audio quá 0.3 giây,
- visual có thể trễ hơn audio tối đa 0.5 giây,
- visual không được biến mất trước khi audio kết thúc ý đó.

### 9.5 Nếu animation đã xong nhưng audio còn nói

Không nhảy sang ý tiếp theo. Không FadeOut visual hiện tại.

Thay vào đó dùng subtle motion:

- glow pulse,
- scanning line,
- particle flow,
- highlight loop,
- token blinking,
- slow camera pan,
- object breathing,
- arrow pulse nhẹ.

### 9.6 FadeOut đúng cách

Sai:

```python
with self.voiceover(text="...") as tracker:
    self.play(FadeIn(diagram), run_time=2)
    self.play(FadeOut(diagram), run_time=1)
    self.wait(tracker.duration - 3)
```

Đúng:

```python
with self.voiceover(text="...") as tracker:
    total = tracker.duration
    self.play(FadeIn(diagram), run_time=total * 0.25)
    self.play(Indicate(key_object), run_time=total * 0.25)
    self.play(Circumscribe(diagram), run_time=total * 0.20)
    self.wait(total * 0.30)

self.play(FadeOut(diagram), run_time=0.5)
```

FadeOut, clear, chuyển scene chỉ được thực hiện sau khi voiceover block kết thúc.

---

## 10. Quy trình bắt buộc khi sửa file Manim

### Bước 1: Đọc file hiện tại

Đọc file Python cần sửa.

Xác định:

- tên class Scene,
- tên các hàm scene nếu có,
- nội dung scene truyền tải,
- scene dùng text, shape, formula, graph hay audio,
- có dùng quá nhiều `self.add` không,
- có scene nào chỉ là chữ không,
- có text bị đè không,
- object chính có quá nhỏ không,
- có animation chạy trước audio không,
- có visual mất trước khi audio kết thúc không,
- có Transform hoặc movement không.

Không sửa ngay khi chưa hiểu file.

### Bước 2: Viết Scene Diagnosis ngắn

Trước khi sửa code, viết chẩn đoán:

```text
Scene:
Vấn đề hiện tại:
- ...

Ý chính cần truyền tải:
- ...

Visual metaphor đề xuất:
- ...

Flowchart layout đề xuất:
- ...

Animation pattern nên dùng:
- ...

Audio sync risk:
- ...

Các object cần thêm:
- ...

Các đoạn cần sửa:
- ...
```

### Bước 3: Tạo Scene Card nâng cấp

Mỗi scene cần sửa phải có Scene Card:

```text
Tên scene:

Ý chính:
Scene này muốn người xem hiểu điều gì?

Ẩn dụ hình ảnh:
Khái niệm này nên được nhìn như hình ảnh nào?

Flowchart layout:
Các box nào? Box nào nối với box nào?

Animation pattern:
Chọn pattern phù hợp.

Bố cục:
Object nào nằm ở đâu?

Màu sắc:
Màu nào dùng cho object chính?

Audio timing:
Object nào xuất hiện theo câu thoại nào?
Visual nào cần giữ đến cuối audio?

Các bước animation:
1. ...
2. ...
3. ...

Text giữ lại:
...

Text cần bỏ:
...

Công thức giữ lại:
...

Công thức nên chuyển thành hình ảnh:
...
```

### Bước 4: Backup file

Trước khi sửa trực tiếp, tạo backup:

```text
<tên_file>.bak
```

Ví dụ:

```text
scene_011.py.bak
```

### Bước 5: Sửa trực tiếp code

Quy tắc sửa:

- giữ tên class hiện tại nếu có thể,
- giữ tên file hiện tại,
- không phá pipeline render hiện tại,
- không đổi cấu trúc project nếu không cần,
- chỉ sửa phần animation trong `construct` hoặc các hàm scene,
- không dùng asset ngoài nếu không được yêu cầu,
- không dùng font ngoài,
- không dùng plugin ngoài Manim Community nếu project chưa có.

### Bước 6: Render test

Sau khi sửa, render thử bằng quality thấp:

```bash
manim -ql manim_scenes/scene_011.py Scene011
```

Nếu class khác tên, tự tìm đúng class rồi render.

Nếu render lỗi:

- đọc lỗi,
- sửa code,
- render lại,
- không bỏ cuộc sau lỗi đầu tiên.

Nếu text bị đè:

- sửa layout,
- tăng spacing,
- tăng padding,
- render lại.

Nếu animation quá nhanh hoặc lệch audio:

- khóa bằng `tracker.duration`,
- thêm bookmark,
- điều chỉnh run_time,
- render lại.

---

## 11. Tiêu chuẩn animation

### 11.1 Không dùng self.add cho object chính

Sai:

```python
self.add(title)
```

Đúng:

```python
self.play(Write(title))
```

Chỉ dùng `self.add` cho helper hoặc background thật sự cần thiết.

### 11.2 Text phải xuất hiện có nhịp

Dùng:

```python
Write(text)
FadeIn(text, shift=UP)
FadeIn(text, shift=DOWN)
```

Không hiện quá nhiều chữ cùng lúc.

Text trên màn hình chỉ nên là:

- một tiêu đề ngắn,
- một keyword,
- một công thức ngắn,
- hoặc một label nhỏ.

Không đưa nguyên đoạn voice lên màn hình.

### 11.3 Shape phải có animation

Dùng:

```python
Create(shape)
GrowFromCenter(shape)
FadeIn(shape, scale=0.8)
```

### 11.4 Transform là hiệu ứng chủ đạo

Khi chuyển từ ý A sang ý B, ưu tiên:

```python
Transform(a, b)
ReplacementTransform(a, b)
TransformMatchingShapes(a, b)
TransformMatchingTex(a, b)
```

Ví dụ:

- lưới pixel transform thành object,
- vector lớn transform thành nhiều slot,
- scene thật transform thành graph,
- correlation line transform thành causal arrow,
- raw text transform thành flowchart block.

### 11.5 Dùng animate để thay đổi trạng thái

```python
self.play(ball.animate.shift(RIGHT * 2))
self.play(node.animate.set_color(SOFT_YELLOW).scale(1.2))
self.play(group.animate.arrange(RIGHT, buff=0.6))
```

---

## 12. Helper Functions nên tạo

Khi viết hoặc refactor code, ưu tiên tạo helper để thống nhất toàn bộ scenes.

```python
def create_title(text, font_size=42):
    ...

def create_text_box(text, stroke_color=TEAL, pad_x=0.22, pad_y=0.16):
    ...

def create_flow_box(content, label=None, stroke_color=TEAL, width=None, height=None):
    ...

def create_entity_box(symbol, label, stroke_color=BLUE):
    ...

def create_module_box(name, subtitle=None, stroke_color=PURPLE):
    ...

def create_formula_panel(tex, stroke_color=SOFT_YELLOW):
    ...

def create_data_arrow(left_obj, right_obj):
    ...

def create_feedback_arrow(obj_a, obj_b):
    ...

def place_flow_row(items, buff=0.55):
    ...

def hold_visual_until_audio_end(scene, tracker, subtle_obj=None):
    ...

def create_person_symbol():
    ...

def create_robot_symbol():
    ...

def create_chair_symbol():
    ...

def create_table_symbol():
    ...

def create_car_symbol():
    ...

def create_laptop_symbol():
    ...

def create_camera_symbol():
    ...

def create_database_symbol():
    ...

def create_document_symbol():
    ...

def create_calendar_symbol():
    ...

def create_feature_grid(rows=4, cols=4):
    ...

def create_token_orbs(count=4):
    ...

def create_semantic_space():
    ...
```

Helper phải đảm bảo:

- object có silhouette rõ,
- box có padding,
- label không sát viền,
- arrow rõ,
- layout không overlap,
- cụm chính đủ lớn.

---

## 13. Thư viện animation pattern

Khi sửa scene, chọn một pattern phù hợp.

### Pattern A: Pixel to Object

Dùng cho:

- pixel,
- ảnh,
- tensor,
- Object-Centric Learning.

Cách sửa:

- vẽ grid ô vuông,
- highlight nhóm pixel,
- transform nhóm pixel thành object,
- fade out nền,
- hiện label ngắn.

### Pattern B: Tensor Stack

Dùng cho:

- ảnh ba chiều,
- chiều cao,
- chiều rộng,
- kênh màu,
- dữ liệu đầu vào.

Cách sửa:

- vẽ nhiều lớp lưới chồng nhau,
- gắn nhãn R G B,
- dùng Brace chỉ chiều cao và chiều rộng,
- dùng mũi tên chỉ chiều kênh.

### Pattern C: Vector to Slots

Dùng cho:

- representation,
- embedding,
- slot,
- structured representation.

Cách sửa:

- vẽ một vector lớn,
- tách vector thành nhiều slot nhỏ,
- mỗi slot bind vào một object,
- dùng arrow chỉ liên kết.

### Pattern D: Attention Competition

Dùng cho:

- attention,
- Slot Attention,
- feature grouping.

Cách sửa:

- vẽ feature dots,
- vẽ slot circles,
- vẽ line mờ từ feature đến slot,
- làm slot thắng sáng lên,
- fade out line yếu.

### Pattern E: Mask and Reconstruction

Dùng cho:

- reconstruction,
- mask,
- decoder,
- segmentation.

Cách sửa:

- mỗi slot tạo một layer,
- các layer chồng lên nhau,
- transform thành ảnh reconstruct.

### Pattern F: Correlation vs Causation

Dùng cho:

- correlation,
- causation,
- statistical model,
- causal model.

Cách sửa:

- chia màn hình hai bên,
- bên trái là tương quan, dùng dashed line,
- bên phải là nhân quả, dùng arrow rõ,
- bóng ở gần hộp bên trái,
- bóng va vào hộp bên phải,
- làm rõ khác biệt giữa đi cùng nhau và gây ra nhau.

### Pattern G: Intervention Experiment

Dùng cho:

- intervention,
- can thiệp,
- do operator,
- thí nghiệm.

Cách sửa:

- vẽ nút can thiệp,
- khi bấm nút, biến thay đổi,
- kết quả thay đổi rõ,
- có thể chia màn hình thành hai lần thử.

### Pattern H: Causal Graph Flow

Dùng cho:

- SCM,
- causal graph,
- nguyên nhân kết quả,
- object relation.

Cách sửa:

- vẽ node bằng Circle,
- vẽ arrow bằng Arrow,
- node sáng lên theo thứ tự,
- arrow sáng theo dòng nhân quả,
- result node được highlight cuối cùng.

### Pattern I: Hidden Confounder Reveal

Dùng cho:

- biến ẩn,
- correlation sai,
- nguyên nhân ngoài quan sát.

Cách sửa:

- ban đầu có A và B nối bằng dashed line,
- sau đó node C ẩn xuất hiện,
- C có arrow đến A và B,
- dashed line A B mờ đi.

### Pattern J: Distribution Shift

Dùng cho:

- train/test khác nhau,
- generalization,
- robustness,
- distribution shift.

Cách sửa:

- vẽ hai môi trường,
- train là trời nắng,
- test là mưa, sương mù, ban đêm,
- correlation rule bị nứt,
- causal rule vẫn sáng.

### Pattern K: Object Permanence

Dùng cho:

- object bị che khuất,
- video understanding,
- tracking,
- memory.

Cách sửa:

- quả bóng lăn,
- một tấm chắn che bóng,
- bóng mờ vẫn tiếp tục đi sau tấm chắn,
- bóng xuất hiện lại,
- slot memory vẫn sáng.

### Pattern L: World Model Rollout

Dùng cho:

- world model,
- state,
- action,
- planning,
- embodied AI.

Cách sửa:

- vẽ state hiện tại,
- vẽ action arrow,
- vẽ state tiếp theo,
- lặp thành timeline,
- highlight tương lai được chọn.

### Pattern M: Paper Figure Pipeline

Dùng cho:

- input,
- encoder,
- slots,
- decoder,
- output,
- architecture,
- JEPA,
- ViT,
- DINO,
- Mamba,
- Dreamer,
- MuZero.

Cách sửa:

- vẽ block diagram sạch,
- mỗi block là Rectangle hoặc RoundedRectangle,
- dùng arrow nối các block,
- highlight từng block theo voice,
- không nhồi chữ.

### Pattern N: Application Orbit

Dùng cho:

- robotics,
- xe tự lái,
- y tế,
- smart city,
- digital twin,
- AI đa phương thức.

Cách sửa:

- concept chính ở giữa,
- các ứng dụng xoay quanh,
- mỗi application là một node,
- node sáng lên khi được nhắc.

### Pattern O: Visual Recap Cards

Dùng cho:

- tổng kết,
- recap,
- kết luận.

Cách sửa:

- mỗi ý chính là một card,
- các card xếp thành grid,
- card sáng lên lần lượt,
- cuối cùng transform thành một flow.

### Pattern P: Abstract Flow Row

Dùng cho:

- pipeline đơn giản,
- input → model → output,
- data flow,
- audio cần sync rõ.

Cách sửa:

- tạo 3 đến 5 flow boxes,
- nối bằng mũi tên to,
- highlight từng box theo audio,
- giữ toàn cụm đến hết audio.

### Pattern Q: Feedback Loop

Dùng cho:

- loss,
- alignment,
- teacher-student,
- JEPA prediction,
- reconstruction error,
- actor-critic.

Cách sửa:

- vẽ hai hoặc ba box chính,
- dùng mũi tên thường cho forward pass,
- dùng mũi tên đỏ cam cho feedback,
- pulse feedback arrow khi audio nói đến loss/alignment.

### Pattern R: Semantic Space

Dùng cho:

- embedding,
- latent space,
- semantic features,
- world model state,
- cluster.

Cách sửa:

- vẽ trục tọa độ tối giản,
- các điểm / cluster xuất hiện,
- highlight distance hoặc region,
- nối cluster với slot/model bằng arrow.

---

## 14. Rule chọn pattern theo nội dung

Nếu scene nói về:

- pích xơ, ảnh, tensor: dùng Pattern A hoặc B.
- representation, vector, embedding: dùng Pattern C hoặc R.
- slot, attention, feature: dùng Pattern D.
- mask, reconstruction, decoder: dùng Pattern E.
- correlation, tương quan: dùng Pattern F.
- causation, nhân quả: dùng Pattern H.
- intervention, can thiệp: dùng Pattern G.
- biến ẩn: dùng Pattern I.
- distribution shift: dùng Pattern J.
- object permanence: dùng Pattern K.
- world model, state, action: dùng Pattern L.
- ứng dụng: dùng Pattern N.
- architecture hoặc pipeline paper: dùng Pattern M hoặc P.
- feedback / loss / alignment: dùng Pattern Q.
- tổng kết: dùng Pattern O.

---

## 15. Quy tắc sửa các scene xấu

### Trường hợp 1: Scene có nhiều text liên tiếp

Không giữ nguyên dạng slide.

Thay bằng:

- một title ngắn,
- flowchart cluster,
- một vài label nhỏ,
- mũi tên hoặc transform,
- reveal tuần tự theo audio.

### Trường hợp 2: Scene chỉ có công thức

Không chỉ Write công thức.

Thay bằng:

- ví dụ trực quan,
- công thức nằm trong formula panel,
- từng phần công thức được highlight bằng hình,
- công thức không đè diagram.

### Trường hợp 3: Scene chỉ có bullet point

Thay bằng:

- cards,
- graph,
- application orbit,
- flow row,
- hoặc module pipeline.

### Trường hợp 4: Scene không có chuyển động ý nghĩa

Thêm:

- Transform,
- object movement,
- arrow flow,
- highlight sequence,
- state transition,
- feedback loop.

### Trường hợp 5: Scene bị đè chữ

Sửa bằng:

- tăng spacing,
- giảm text,
- tăng padding,
- tăng box size,
- chuyển label sang panel,
- reveal tuần tự,
- render test lại.

### Trường hợp 6: Animation chạy trước audio

Sửa bằng:

- đưa animation vào voiceover block,
- dùng `tracker.duration`,
- thêm bookmark,
- không hardcode timing,
- không hiện object trước khi audio nói tới.

### Trường hợp 7: Hình biến mất khi audio còn nói

Sửa bằng:

- không FadeOut trong voiceover block,
- giữ final visual state,
- dùng subtle motion,
- chỉ fade out sau khi voiceover block kết thúc.

---

## 16. Quy tắc cho nhiều scenes / 31 scenes

Khi người dùng yêu cầu chỉnh 31 scenes hoặc nhiều scenes:

### 16.1 Toàn bộ scenes phải dùng cùng một visual system

Thống nhất:

- background,
- title style,
- box style,
- arrow style,
- label style,
- padding,
- spacing,
- object style,
- audio sync style,
- transition rhythm.

Không được để scene này dark-tech flowchart, scene sau lại là slide text hoặc icon lộn xộn.

### 16.2 Trước khi code, lập plan

Trả về:

```text
1. Global Design System
2. Scene-by-scene redesign plan
3. Audio → visual sync map
4. Manim code hoặc patch code
```

Mỗi scene trong redesign plan cần có:

- Scene number,
- Scene title,
- Core idea,
- Main entities,
- Main modules,
- Flowchart layout,
- Visual blocks,
- Arrow connections,
- Color roles,
- Timing notes,
- Hold visual until,
- Risk cần tránh.

### 16.3 Scene sync map

Với mỗi đoạn voice/audio, tạo bảng:

```text
Audio phrase | Visual allowed | Appear when | Hold until | Animation
```

Nếu không có audio thật, ước lượng theo tốc độ nói tiếng Việt 130–150 từ/phút.

---

## 17. Prompt nội bộ để sửa một file

Khi nâng cấp một file, dùng tư duy này:

```text
Đọc file Python Manim hiện tại.
Không viết lại toàn bộ nếu không cần.
Tìm các scene chỉ hiện chữ, object nhỏ, layout đè, hoặc animation nghèo.

Với mỗi scene:
1. Xác định ý chính.
2. Tạo visual metaphor.
3. Chọn animation pattern.
4. Chuyển visual thành flowchart blocks.
5. Vẽ object bằng Manim abstract shapes nhưng nhận ra được.
6. Đảm bảo text trong box có padding.
7. Đảm bảo object chính chiếm 60%–70% vùng nhìn.
8. Sync animation với audio.
9. Giữ visual đến khi audio nói xong.
10. Render test và sửa lỗi.
```

---

## 18. Checklist sau khi sửa

Tự kiểm tra trước khi báo cáo:

### Visual

- Có scene nào giống slide text không?
- Object chính có đủ lớn không?
- Object có nhận ra được khi bỏ label không?
- Có flowchart block rõ không?
- Có mũi tên rõ không?
- Có màu thống nhất không?
- Có chữ nào đè nhau không?
- Chữ trong box có padding không?
- Visual chính có chiếm gần 2/3 màn hình không?

### Animation

- Có Transform hoặc movement ý nghĩa không?
- Có highlight để dẫn mắt không?
- Có arrow flow theo logic không?
- Có FadeOut dọn màn hình đúng lúc không?
- Có object nào dùng `self.add` không cần thiết không?

### Audio

- Animation có chạy trước lời thoại không?
- Object có hiện trước khi audio nhắc tới không?
- Visual có biến mất trước khi audio nói xong không?
- Có title mới hiện quá sớm không?
- Có dùng `tracker.duration` hoặc bookmark khi cần không?
- Có self.wait dài mà không có subtle motion không?

### Code

- Code chạy được không?
- Có helper functions chưa?
- Có phá tên class/file không?
- Có dùng asset/font/plugin ngoài không được phép không?
- Render test pass không?

---

## 19. Cách báo cáo sau khi sửa

Sau khi sửa file, báo cáo ngắn:

```text
Đã nâng cấp:
- scene_001: đổi từ text slide sang Pixel to Object / Flow Row.
- scene_002: thêm Vector to Slots.
- scene_003: thêm Causal Graph Flow.
- ...

File đã sửa:
- ...

Backup:
- ...

Render test:
- pass / fail

Nếu fail:
- lỗi gì,
- dòng nào,
- đã thử sửa gì,
- cần người dùng cung cấp thêm gì.
```

Nếu chỉ sửa file skill Markdown, không cần render Manim. Báo rõ là đã chỉnh skill, không phải scene Python.

---

## 20. Final Rules — Luật không được phá

- Không cần photorealistic.
- Ưu tiên Manim abstract diagram.
- Object vẫn phải nhận ra được.
- Không dùng rectangle có chữ để thay thế vật thể.
- Mọi nội dung chính nên nằm trong flowchart box.
- Mũi tên phải to, rõ.
- Title luôn ở trên, màu vàng.
- Background luôn navy tối.
- Layout không được đè chữ.
- Object chính không được quá nhỏ.
- Text trong box phải có padding.
- Animation không được chạy trước audio.
- Visual không được biến mất trước khi audio nói xong.
- Nếu scene bị nhồi chữ, phải thiết kế lại.
- Nếu scene lệch audio, phải sửa timing trước khi thêm hiệu ứng.
- Nếu scene đẹp nhưng khó hiểu, phải ưu tiên rõ nghĩa.

Mục tiêu cuối cùng:

Video Manim phải có cảm giác như một bài giảng học thuật được đạo diễn tốt: hình ảnh sạch, sơ đồ rõ, object dễ nhận diện, text ít nhưng đúng chỗ, animation bám audio, và toàn bộ scenes thống nhất một phong cách.
