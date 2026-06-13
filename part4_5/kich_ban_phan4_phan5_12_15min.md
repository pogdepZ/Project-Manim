# KỊCH BẢN PHẦN 4 & PHẦN 5 – BẢN CHUẨN 12–15 PHÚT

**Topic:** Synthetic-to-Real Gap & Reconstruct Beyond RGB  
**Target duration:** 12–15 phút  
**Recommended target:** khoảng 13 phút 30 giây  
**Vị trí trong video nhóm:** `SLOT ATTENTION → Synthetic-to-Real Gap & Reconstruct Beyond RGB → UPGRADING ENCODER`

## 0. Nguyên tắc chất lượng

- Không kéo dài video bằng `self.wait()` một cách cơ học.
- Mỗi scene phải có narration riêng, visual riêng, và 3–6 visual beats.
- Text trên màn hình phải ngắn, không chép nguyên voice-over.
- Mỗi frame chỉ nên truyền tải một ý chính.
- Không để text, card, arrow, object chồng lên nhau.
- Mọi visual optical flow, LiDAR, point cloud, feature map đều là **conceptual illustration**.
- Không thêm claim khoa học ngoài source map. Nếu cần claim mới, ghi `TODO_SOURCE_REQUIRED`.

## 1. Tổng cấu trúc thời lượng mới

| Scene ID | Scene title | Vai trò | Target |
|---|---|---|---:|
| P4_00 | Bridge from Slot Attention | Nối từ phần trước | 0:45 |
| P4_01 | Synthetic vs Real-world Gap | Đặt vấn đề chính | 1:20 |
| P4_02 | Why Real-world Data Is Hard | Texture/lighting/occlusion/clutter/motion | 1:25 |
| P4_03 | RGB Reconstruction Pipeline | Giải thích pipeline RGB reconstruction | 1:15 |
| P4_04 | Why Raw RGB Can Distract | Raw RGB kéo model về low-level details | 1:30 |
| P4_05 | Core Question: Beyond RGB | Chuyển sang câu hỏi nghiên cứu | 0:55 |
| P5_01 | Optical Flow as Motion Cue | Optical flow là motion cue | 1:20 |
| P5_02 | Motion Helps, But Has Limits | Lợi ích và giới hạn của motion cue | 1:15 |
| P5_03 | Depth, LiDAR, and Waymo | Geometry cue + Waymo context | 1:35 |
| P5_04 | DINOSAUR Feature Reconstruction | Feature reconstruction beyond RGB | 1:35 |
| P5_05 | Final Synthesis + Bridge to Upgrading Encoder | Tổng hợp và nối sang phần sau | 1:00 |

**Tổng target:** khoảng 13 phút 35 giây.  
**Khoảng chấp nhận:** 12–15 phút.

---

# P4_00 – Bridge from Slot Attention

**Duration target:** 0:45

## Purpose
Nối từ phần trước: **Slot Attention**. Nhắc lại rằng slot-based object-centric learning đã giúp model phân rã scene, nhưng đặt câu hỏi: nếu dùng slots, ta nên huấn luyện chúng bằng target nào?

## Visual goal
Pixels/Image → Slot Attention → Slots → Reconstruction Target? → hai nhánh `Synthetic-to-Real Gap` và `Beyond RGB`.

## On-screen text
```text
From Slot Attention...
to reconstruction targets
```
```text
Question:
What should the slots reconstruct?
```

## Voice-over
Ở phần trước, chúng ta đã nói về Slot Attention. Ý tưởng chính là thay vì xem cả ảnh như một khối đặc, model cố gắng phân rã scene thành nhiều biểu diễn nhỏ hơn, gọi là slots.

Các slots này giống như những vector đại diện cho các thành phần khác nhau trong scene. Một slot có thể tập trung vào một object, một vùng background, hoặc một phần có cấu trúc nào đó. Đây là một bước quan trọng của object-centric learning.

Nhưng sau khi có slots, câu hỏi tiếp theo là: ta sẽ huấn luyện chúng bằng cách nào? Nhiều phương pháp dùng reconstruction: model nhận input, tạo slots, rồi decoder cố dựng lại một target nào đó.

Vậy target đó nên là gì? Có phải lúc nào cũng là raw RGB pixels không? Đây chính là điểm nối sang phần của chúng ta: synthetic-to-real gap và reconstruct beyond RGB.

## Visual beats
1. Pixels/Image → Slot Attention.
2. Slot Attention → multiple slots.
3. Slots → Reconstruction Target?
4. Branch to “Synthetic-to-Real Gap” and “Beyond RGB”.

---

# P4_01 – Synthetic vs Real-world Gap

**Duration target:** 1:20

## Purpose
Đặt vấn đề chính: synthetic data giúp nghiên cứu dễ kiểm soát, nhưng real-world data phức tạp hơn rất nhiều.

## Visual goal
Split-screen:
- Left: Synthetic Data – clean, controlled, simple.
- Right: Real-world Data – texture, lighting, occlusion, clutter.

## On-screen text
```text
Synthetic Data
Clean • Controlled • Simple
```
```text
Real-world Data
Texture • Lighting • Occlusion • Clutter
```

## Voice-over
Trước hết, hãy nhìn vào sự khác biệt giữa synthetic data và real-world data.

Trong synthetic data, scene thường được kiểm soát tốt hơn. Ta có thể tạo vài object hình học đơn giản, đặt chúng trên một background sạch, giữ ánh sáng ổn định, và kiểm soát số lượng object trong scene. Điều này rất hữu ích cho nghiên cứu, vì nó giúp kiểm tra xem model có học được cấu trúc cơ bản hay không.

Nhưng khi chuyển sang real-world data, mọi thứ phức tạp hơn nhiều. Object ngoài đời thật có texture, vật liệu, shadow, reflection và có thể bị che khuất một phần. Background cũng không còn sạch nữa; nó có thể chứa đường phố, cây cối, biển báo, người, xe, và rất nhiều chi tiết gây nhiễu.

Vì vậy, synthetic-to-real gap không chỉ là chuyện ảnh thật “rối hơn”. Nó là khoảng cách giữa một môi trường được kiểm soát và một môi trường mở, nơi model phải xử lý nhiều biến thể mà nó không thể dự đoán trước.

## Visual beats
1. Build synthetic side.
2. Add clean labels: controlled, simple, stable.
3. Build real-world side.
4. Add clutter/occlusion/lighting tags.
5. Final contrast line: “Controlled world → Open world”.

---

# P4_02 – Why Real-world Data Is Hard

**Duration target:** 1:25

## Purpose
Phân tích các nguồn khó khăn trong real-world data: appearance, lighting, occlusion, clutter, motion.

## Visual goal
Một object trung tâm, ví dụ car/person, được thêm từng lớp khó khăn: texture → lighting/shadow → occlusion → clutter → motion.

## On-screen text
```text
Real-world complexity
Appearance • Lighting • Occlusion • Clutter • Motion
```

## Voice-over
Ta có thể chia độ phức tạp của real-world data thành vài nhóm.

Nhóm đầu tiên là appearance. Một object ngoài đời không chỉ là một khối màu đơn giản. Một chiếc xe có kính, kim loại, bánh xe, logo, phản chiếu ánh sáng và các chi tiết nhỏ.

Nhóm thứ hai là lighting. Cùng một object có thể trông khác nhau dưới nắng, trong bóng râm, ban đêm, hoặc khi có reflection từ môi trường.

Nhóm thứ ba là occlusion. Object thường bị che một phần. Model chỉ thấy một phần của object, nhưng vẫn cần hiểu rằng nó thuộc về một entity hoàn chỉnh.

Nhóm thứ tư là clutter. Background ngoài đời chứa nhiều object và pattern không liên quan. Điều này khiến ranh giới giữa object chính và background khó rõ ràng.

Cuối cùng là motion. Trong video, object có thể chuyển động rigid hoặc non-rigid, và camera cũng có thể di chuyển. Những yếu tố này làm real-world object-centric learning khó hơn rất nhiều so với synthetic scenes đơn giản.

## Visual beats
1. Show central object.
2. Add texture/material.
3. Add lighting/shadow.
4. Add occluder.
5. Add cluttered background.
6. Add motion arrows.

---

# P4_03 – RGB Reconstruction Pipeline

**Duration target:** 1:15

## Purpose
Giải thích RGB reconstruction pipeline trước khi chỉ ra giới hạn.

## Visual goal
Pipeline: `RGB Frame → Encoder → Slots → Decoder → Reconstructed RGB`. Sau đó thêm pixel-level loss nối input/output.

## On-screen text
```text
RGB Reconstruction
Input RGB → Encoder → Slots → Decoder → RGB Output
```
```text
Loss asks:
“Make pixels similar”
```

## Voice-over
Trong nhiều mô hình object-centric, một cách huấn luyện phổ biến là RGB reconstruction.

Pipeline cơ bản như sau. Model nhận vào một RGB frame. Encoder biến ảnh thành feature representation. Sau đó, một cơ chế object-centric như slots cố gắng chia representation này thành nhiều phần nhỏ hơn. Cuối cùng, decoder dùng các slots để reconstruct lại ảnh RGB.

Trực giác ban đầu nghe khá hợp lý. Nếu model có thể dựng lại cả scene từ slots, ta hy vọng mỗi slot đã học được một phần có ý nghĩa trong scene.

Nhưng điểm quan trọng là reconstruction loss không trực tiếp nói với model: “hãy hiểu object”. Nó chỉ nói: “hãy làm output pixel giống input pixel”. Vì vậy, nếu cách dễ nhất để giảm loss là học màu sắc, texture hoặc background pattern, model có thể dành nhiều năng lực cho các chi tiết cấp thấp đó.

## Visual beats
1. Show RGB frame card.
2. Add encoder.
3. Add slots one by one.
4. Add decoder.
5. Add reconstructed RGB.
6. Add pixel-level loss connection.

---

# P4_04 – Why Raw RGB Can Distract

**Duration target:** 1:30

## Purpose
Giải thích vì sao reconstruct raw RGB có thể không tối ưu cho real-world object-centric learning.

## Visual goal
Minh họa object real-world với tags: color, texture, shadow, reflection, background, occlusion. Sau đó tách thành hai câu hỏi: pixel question và object question.

## On-screen text
```text
Raw RGB contains low-level details
Color • Texture • Shadow • Reflection • Background
```
```text
Object understanding asks:
What entities exist?
```

## Voice-over
Với ảnh thực tế, raw RGB chứa rất nhiều chi tiết cấp thấp.

Ví dụ, một chiếc xe không chỉ là một object đơn giản. Kính xe có thể phản chiếu bầu trời. Thân xe có thể bị shadow che một phần. Bánh xe có texture khác với thân xe. Background phía sau cũng có nhiều pattern khác nhau.

Tất cả những thứ này đều xuất hiện trong pixel, nên nếu target là reconstruct RGB thật giống, model phải giải thích chúng. Điều đó không sai. Nhưng không phải chi tiết nào cũng quan trọng cho object-centric representation.

Ta muốn model hiểu entity-level structure: đâu là xe, đâu là người, đâu là background, các object liên hệ với nhau như thế nào. Trong khi đó, raw RGB reconstruction có thể kéo model về câu hỏi cấp thấp hơn: pixel này màu gì, texture này trông ra sao, shadow này nằm ở đâu.

Vì vậy, RGB reconstruction vẫn hữu ích, nhưng không phải lúc nào cũng là target phù hợp nhất khi muốn scale object-centric learning sang real-world data.

## Visual beats
1. Show object.
2. Add tags: color/texture/shadow/reflection/background.
3. Dim tags and show “pixel question”.
4. Replace with “object question”.
5. Final takeaway: RGB useful, but not always optimal.

---

# P4_05 – Core Question: Beyond RGB

**Duration target:** 0:55

## Purpose
Chuyển từ problem sang hướng “beyond RGB”.

## Visual goal
Câu hỏi trung tâm và ba nhánh: Motion, Geometry, Features.

## On-screen text
```text
Do we always need to reconstruct raw RGB pixels?
```
```text
Beyond RGB:
Motion • Geometry • Features
```

## Voice-over
Từ đây, câu hỏi nghiên cứu chính xuất hiện: nếu mục tiêu là học object-centric representation, liệu raw RGB pixel có luôn là reconstruction target tốt nhất không?

Câu trả lời thận trọng là: không phải lúc nào cũng vậy.

Thay vì chỉ reconstruct RGB, researchers bắt đầu khai thác các tín hiệu có cấu trúc hơn. Motion cho biết scene thay đổi như thế nào qua thời gian. Geometry cho biết quan hệ gần xa và cấu trúc 3D. Self-supervised features có thể cung cấp representation trừu tượng hơn raw pixels.

Đây là tinh thần của reconstruct beyond RGB: không phải bỏ RGB, mà là chọn training signal phù hợp hơn với cấu trúc ta muốn model học.

## Visual beats
1. Show RGB target.
2. Show question “Always RGB?”.
3. Branch to Motion.
4. Branch to Geometry.
5. Branch to Features.

---

# P5_01 – Optical Flow as Motion Cue

**Duration target:** 1:20

## Purpose
Giải thích optical flow và vì sao nó là motion cue.

## Visual goal
Hai frame `t` và `t+1`, object di chuyển, vector arrows.

## On-screen text
```text
Optical Flow
Apparent motion between consecutive frames
```
```text
RGB asks: What color?
Flow asks: How did it move?
```

## Voice-over
Một hướng beyond RGB quan trọng là optical flow.

Optical flow mô tả chuyển động biểu kiến giữa hai frame liên tiếp. Ta có thể hình dung nó như một trường vector hai chiều. Mỗi vector mô tả một điểm ảnh hoặc vùng ảnh đã dịch chuyển từ frame trước sang frame sau như thế nào.

Điểm thú vị là optical flow đổi câu hỏi huấn luyện. RGB hỏi: pixel này màu gì? Flow hỏi: pixel này đã di chuyển như thế nào?

Trong video, motion là một cue rất hữu ích. Object thường tồn tại qua nhiều frame, và các vùng thuộc cùng một object thường có xu hướng motion liên quan với nhau. Vì vậy, optical flow có thể hỗ trợ model trong việc grouping và tracking.

Trong SAVi, optical flow được nghiên cứu như một prediction target cho video object-centric learning. Nhưng cần nhớ: optical flow là cue hỗ trợ, không phải cơ chế tự động phát hiện object hoàn hảo.

## Visual beats
1. Show frame t.
2. Show frame t+1.
3. Move object position.
4. Draw main displacement arrow.
5. Add vector field.
6. Show RGB question vs Flow question.

---

# P5_02 – Motion Helps, But Has Limits

**Duration target:** 1:15

## Purpose
Giải thích motion cue hữu ích nhưng không hoàn chỉnh.

## Visual goal
4 mini cases: simple moving object, static object, moving camera, shared/non-rigid motion.

## On-screen text
```text
Motion helps...
but motion alone is not enough.
```
```text
Useful cue ≠ complete solution
```

## Voice-over
Motion cue rất hữu ích, nhưng không phải lời giải hoàn chỉnh.

Trong trường hợp đơn giản, một object di chuyển trên background tĩnh có thể tạo ra flow khá rõ. Điều này giúp model có thêm tín hiệu để grouping vùng object.

Nhưng real-world video phức tạp hơn. Nếu object đứng yên, motion cue có thể rất yếu. Nếu camera di chuyển, background cũng sinh ra optical flow. Nếu nhiều object cùng chuyển động theo một hướng, flow có thể gây nhầm lẫn. Và với non-rigid object như người đi bộ, các phần khác nhau của cùng một object có thể có local motion khác nhau.

Vì vậy, motion nên được hiểu là một tín hiệu hỗ trợ object-centric learning, không phải ground-truth segmentation.

## Visual beats
1. Helpful case: object moves, clear arrows.
2. Static object: no/weak arrow.
3. Moving camera: whole background flow.
4. Shared/non-rigid motion.
5. Final warning card.

---

# P5_03 – Depth, LiDAR, and Waymo

**Duration target:** 1:35

## Purpose
Giải thích geometry cue thông qua depth/LiDAR và giới thiệu Waymo context.

## Visual goal
Driving scene → LiDAR rays → sparse point cloud → dataset card.

## On-screen text
```text
Depth / LiDAR
Geometry cue
Near • Far • Front • Behind
```
```text
Waymo Open Dataset
Autonomous driving perception
Camera + LiDAR-related data
```

## Voice-over
Ngoài motion, một tín hiệu beyond RGB quan trọng khác là geometry, đặc biệt thông qua depth và LiDAR.

Depth cho biết điểm nào gần, điểm nào xa, bề mặt nào đứng trước, bề mặt nào nằm sau. Trong robotics và autonomous driving, thông tin này rất quan trọng, vì hệ thống không chỉ cần biết object trông như thế nào, mà còn cần biết object nằm ở đâu trong không gian.

LiDAR là một cảm biến dùng xung laser để đo khoảng cách và tạo thông tin ba chiều về bề mặt. Trong thực tế, LiDAR thường tạo ra point cloud hoặc depth signal dạng thưa. Nó cung cấp geometry cue, nhưng không tự động cung cấp semantic object labels.

Trong SAVi++, sparse depth signals từ LiDAR được dùng như một self-supervision target cho slot-based video representation.

Bối cảnh thường được nhắc đến ở đây là Waymo Open Dataset. Cần nói chính xác: Waymo không chỉ là một dataset LiDAR. Nó là dataset perception cho autonomous driving, bao gồm dữ liệu camera và LiDAR-related data trong các real-world driving scenes.

## Visual beats
1. Show driving scene.
2. Add near/far labels.
3. Add LiDAR rays.
4. Transform to sparse point cloud.
5. Show “not semantic labels” caution.
6. Transition to Waymo dataset card.

---

# P5_04 – DINOSAUR Feature Reconstruction

**Duration target:** 1:35

## Purpose
Giải thích self-supervised feature reconstruction như một hướng beyond RGB khác.

## Visual goal
So sánh hai pipelines:
- Pixel target: Image → Slots → Decoder → RGB pixels
- Feature target: Image → SSL Backbone → Feature Map; Slots → Decoder → Feature Map

## On-screen text
```text
DINOSAUR
Reconstruct self-supervised features
not raw RGB pixels
```
```text
Target changes:
pixels → features
```

## Voice-over
Beyond RGB không chỉ có optical flow và depth. Một hướng quan trọng khác là reconstruct self-supervised features.

Trong DINOSAUR, thay vì yêu cầu model reconstruct raw RGB pixels, model reconstruct features từ các self-supervised vision models. Đây là một thay đổi quan trọng về training target.

Raw RGB pixels chứa rất nhiều chi tiết cấp thấp như màu sắc, texture, lighting và background. Trong khi đó, self-supervised features có thể mang thông tin thị giác có cấu trúc hơn, hữu ích hơn cho object grouping trên real-world images.

Điểm cần nói rõ là DINOSAUR thuộc nhánh feature reconstruction. Nó không dùng optical flow, cũng không dùng LiDAR depth. DINOSAUR cho thấy reconstruct self-supervised features có thể là một training signal đủ mạnh để object-centric representations xuất hiện theo cách fully unsupervised.

Vì vậy, reconstruct beyond RGB không chỉ là đổi sang sensor mới. Nó còn có thể là đổi từ pixel-level target sang feature-level target.

## Visual beats
1. Show pixel reconstruction path.
2. Highlight low-level RGB details.
3. Replace with SSL backbone.
4. Show feature map grid.
5. Show slot decoder reconstructing feature map.
6. Add caution: “not flow, not LiDAR”.

---

# P5_05 – Final Synthesis + Bridge to Upgrading Encoder

**Duration target:** 1:00

## Purpose
Tổng hợp toàn bộ phần này và chuyển sang phần sau: **Upgrading Encoder**.

## Visual goal
Summary table:
- RGB → Appearance
- Optical Flow → Motion
- Depth/LiDAR → Geometry
- SSL Features → Structured representation

Sau đó transform sang: `Better target + Better encoder → stronger object-centric learning`.

## On-screen text
```text
Reconstruction targets shape what the model learns
```
```text
RGB → Appearance
Flow → Motion
Depth/LiDAR → Geometry
SSL Features → Structured representation
```
```text
Next:
Upgrading Encoder
```

## Voice-over
Tóm lại, synthetic-to-real gap cho thấy rằng real-world data không chỉ phức tạp hơn về mặt hình ảnh. Nó còn khiến reconstruction target trở nên quan trọng hơn.

Nếu target là RGB, model học nhiều về appearance. Nếu target là optical flow, model học motion. Nếu target là depth hoặc LiDAR signal, model học geometry. Nếu target là self-supervised features, model học từ một representation có cấu trúc hơn raw pixels.

Thông điệp chính là: reconstruct beyond RGB không có nghĩa RGB vô dụng. Nó có nghĩa là training signal nên phù hợp với cấu trúc mà ta muốn model học.

Đến đây, ta đã nói về việc thay đổi reconstruction target. Nhưng target chỉ là một nửa câu chuyện. Phần tiếp theo sẽ đi vào một hướng cải thiện khác: nâng cấp encoder. Nếu encoder tạo ra feature tốt hơn ngay từ đầu, thì các slots và reconstruction target phía sau cũng có cơ hội học representation tốt hơn.

Vì vậy, từ câu hỏi “model nên reconstruct cái gì?”, chúng ta chuyển sang câu hỏi tiếp theo: “model nên encode input như thế nào?” Đó là phần Upgrading Encoder.

## Visual beats
1. Build summary rows.
2. Highlight “target shapes learning”.
3. Show Slot Attention pipeline again.
4. Highlight encoder block.
5. Transition card: “Next: Upgrading Encoder”.

---

# 2. Final accuracy checklist

- [ ] Có đoạn nối từ Slot Attention sang phần này.
- [ ] Có đoạn chuyển từ phần này sang Upgrading Encoder.
- [ ] Tổng duration nằm trong 12–15 phút.
- [ ] Không nói RGB vô dụng.
- [ ] Không nói optical flow phát hiện object hoàn hảo.
- [ ] Không nói depth/LiDAR tự động tạo semantic labels.
- [ ] Không nói DINOSAUR dùng optical flow hoặc LiDAR.
- [ ] Không nói Waymo chỉ là LiDAR dataset.
- [ ] Không nói SAVi++ hoặc DINOSAUR giải quyết hoàn toàn real-world object-centric learning.
- [ ] Mọi visual phức tạp đều có comment `SIMPLIFIED_VISUAL`.
- [ ] Mọi claim chính đều map về source map.
- [ ] Audio/video được sync theo từng scene.
- [ ] Không có layout overlap, text chồng, arrow lệch, object sát mép.
