# NARRATION SCRIPT – PHẦN 4 & PHẦN 5 BẢN 12–15 PHÚT

**Target duration:** 12–15 phút  
**Recommended target:** khoảng 13 phút 30 giây  
**Use case:** nguồn trực tiếp cho `generate_narration_part4_part5.py`.

## Scene mapping

| Key | Scene class đề xuất | MP3 output |
|---|---|---|
| p4_00_bridge_slot_attention | Part04BridgeSlotAttention | p4_00_bridge_slot_attention.mp3 |
| p4_01_synthetic_real_gap | Part04SyntheticRealGap | p4_01_synthetic_real_gap.mp3 |
| p4_02_real_world_hard | Part04RealWorldHard | p4_02_real_world_hard.mp3 |
| p4_03_rgb_reconstruction | Part04RGBReconstructionPipeline | p4_03_rgb_reconstruction.mp3 |
| p4_04_rgb_distracts | Part04RGBDistracts | p4_04_rgb_distracts.mp3 |
| p4_05_core_question | Part04CoreQuestion | p4_05_core_question.mp3 |
| p5_01_optical_flow | Part05OpticalFlowCue | p5_01_optical_flow.mp3 |
| p5_02_motion_limits | Part05MotionLimits | p5_02_motion_limits.mp3 |
| p5_03_depth_lidar_waymo | Part05DepthLidarWaymo | p5_03_depth_lidar_waymo.mp3 |
| p5_04_dinosaur_features | Part05DinosaurFeatures | p5_04_dinosaur_features.mp3 |
| p5_05_synthesis_encoder_bridge | Part05SynthesisEncoderBridge | p5_05_synthesis_encoder_bridge.mp3 |

## Pronunciation notes for Vietnamese TTS

Only apply these replacements for audio generation, not on-screen text.

```python
PRONUNCIATION_MAP = {
    "raw RGB": "raw a gi bi",
    "RGB frame": "a gi bi frame",
    "RGB": "a gi bi",
    "LiDAR": "lai đa",
    "SAVi++": "sa vi plus plus",
    "SAVi": "sa vi",
    "DINOSAUR": "đai nô so",
    "Waymo": "quây mô",
    "SSL": "ét ét eo",
    "object-centric": "óp-dzèct sen-tric",
    "Slot Attention": "slot attention",
    "self-supervised": "seo sù pờ vai",
    "optical flow": "óp-ti-cồ flow",
    "synthetic-to-real gap": "sin-the-tic tu real gap",
    "Upgrading Encoder": "upgrading encoder",
}
```

Sort replacements by key length descending.

---

# p4_00_bridge_slot_attention

Ở phần trước, chúng ta đã nói về Slot Attention. Ý tưởng chính là thay vì xem cả ảnh như một khối đặc, model cố gắng phân rã scene thành nhiều biểu diễn nhỏ hơn, gọi là slots.

Các slots này giống như những vector đại diện cho các thành phần khác nhau trong scene. Một slot có thể tập trung vào một object, một vùng background, hoặc một phần có cấu trúc nào đó. Đây là một bước quan trọng của object-centric learning.

Nhưng sau khi có slots, câu hỏi tiếp theo là: ta sẽ huấn luyện chúng bằng cách nào? Nhiều phương pháp dùng reconstruction: model nhận input, tạo slots, rồi decoder cố dựng lại một target nào đó.

Vậy target đó nên là gì? Có phải lúc nào cũng là raw RGB pixels không? Đây chính là điểm nối sang phần của chúng ta: synthetic-to-real gap và reconstruct beyond RGB.

---

# p4_01_synthetic_real_gap

Trước hết, hãy nhìn vào sự khác biệt giữa synthetic data và real-world data.

Trong synthetic data, scene thường được kiểm soát tốt hơn. Ta có thể tạo vài object hình học đơn giản, đặt chúng trên một background sạch, giữ ánh sáng ổn định, và kiểm soát số lượng object trong scene. Điều này rất hữu ích cho nghiên cứu, vì nó giúp kiểm tra xem model có học được cấu trúc cơ bản hay không.

Nhưng khi chuyển sang real-world data, mọi thứ phức tạp hơn nhiều. Object ngoài đời thật có texture, vật liệu, shadow, reflection và có thể bị che khuất một phần. Background cũng không còn sạch nữa; nó có thể chứa đường phố, cây cối, biển báo, người, xe, và rất nhiều chi tiết gây nhiễu.

Vì vậy, synthetic-to-real gap không chỉ là chuyện ảnh thật “rối hơn”. Nó là khoảng cách giữa một môi trường được kiểm soát và một môi trường mở, nơi model phải xử lý nhiều biến thể mà nó không thể dự đoán trước.

---

# p4_02_real_world_hard

Ta có thể chia độ phức tạp của real-world data thành vài nhóm.

Nhóm đầu tiên là appearance. Một object ngoài đời không chỉ là một khối màu đơn giản. Một chiếc xe có kính, kim loại, bánh xe, logo, phản chiếu ánh sáng và các chi tiết nhỏ.

Nhóm thứ hai là lighting. Cùng một object có thể trông khác nhau dưới nắng, trong bóng râm, ban đêm, hoặc khi có reflection từ môi trường.

Nhóm thứ ba là occlusion. Object thường bị che một phần. Model chỉ thấy một phần của object, nhưng vẫn cần hiểu rằng nó thuộc về một entity hoàn chỉnh.

Nhóm thứ tư là clutter. Background ngoài đời chứa nhiều object và pattern không liên quan. Điều này khiến ranh giới giữa object chính và background khó rõ ràng.

Cuối cùng là motion. Trong video, object có thể chuyển động rigid hoặc non-rigid, và camera cũng có thể di chuyển. Những yếu tố này làm real-world object-centric learning khó hơn rất nhiều so với synthetic scenes đơn giản.

---

# p4_03_rgb_reconstruction

Trong nhiều mô hình object-centric, một cách huấn luyện phổ biến là RGB reconstruction.

Pipeline cơ bản như sau. Model nhận vào một RGB frame. Encoder biến ảnh thành feature representation. Sau đó, một cơ chế object-centric như slots cố gắng chia representation này thành nhiều phần nhỏ hơn. Cuối cùng, decoder dùng các slots để reconstruct lại ảnh RGB.

Trực giác ban đầu nghe khá hợp lý. Nếu model có thể dựng lại cả scene từ slots, ta hy vọng mỗi slot đã học được một phần có ý nghĩa trong scene.

Nhưng điểm quan trọng là reconstruction loss không trực tiếp nói với model: “hãy hiểu object”. Nó chỉ nói: “hãy làm output pixel giống input pixel”. Vì vậy, nếu cách dễ nhất để giảm loss là học màu sắc, texture hoặc background pattern, model có thể dành nhiều năng lực cho các chi tiết cấp thấp đó.

---

# p4_04_rgb_distracts

Với ảnh thực tế, raw RGB chứa rất nhiều chi tiết cấp thấp.

Ví dụ, một chiếc xe không chỉ là một object đơn giản. Kính xe có thể phản chiếu bầu trời. Thân xe có thể bị shadow che một phần. Bánh xe có texture khác với thân xe. Background phía sau cũng có nhiều pattern khác nhau.

Tất cả những thứ này đều xuất hiện trong pixel, nên nếu target là reconstruct RGB thật giống, model phải giải thích chúng. Điều đó không sai. Nhưng không phải chi tiết nào cũng quan trọng cho object-centric representation.

Ta muốn model hiểu entity-level structure: đâu là xe, đâu là người, đâu là background, các object liên hệ với nhau như thế nào. Trong khi đó, raw RGB reconstruction có thể kéo model về câu hỏi cấp thấp hơn: pixel này màu gì, texture này trông ra sao, shadow này nằm ở đâu.

Vì vậy, RGB reconstruction vẫn hữu ích, nhưng không phải lúc nào cũng là target phù hợp nhất khi muốn scale object-centric learning sang real-world data.

---

# p4_05_core_question

Từ đây, câu hỏi nghiên cứu chính xuất hiện: nếu mục tiêu là học object-centric representation, liệu raw RGB pixel có luôn là reconstruction target tốt nhất không?

Câu trả lời thận trọng là: không phải lúc nào cũng vậy.

Thay vì chỉ reconstruct RGB, researchers bắt đầu khai thác các tín hiệu có cấu trúc hơn. Motion cho biết scene thay đổi như thế nào qua thời gian. Geometry cho biết quan hệ gần xa và cấu trúc 3D. Self-supervised features có thể cung cấp representation trừu tượng hơn raw pixels.

Đây là tinh thần của reconstruct beyond RGB: không phải bỏ RGB, mà là chọn training signal phù hợp hơn với cấu trúc ta muốn model học.

---

# p5_01_optical_flow

Một hướng beyond RGB quan trọng là optical flow.

Optical flow mô tả chuyển động biểu kiến giữa hai frame liên tiếp. Ta có thể hình dung nó như một trường vector hai chiều. Mỗi vector mô tả một điểm ảnh hoặc vùng ảnh đã dịch chuyển từ frame trước sang frame sau như thế nào.

Điểm thú vị là optical flow đổi câu hỏi huấn luyện. RGB hỏi: pixel này màu gì? Flow hỏi: pixel này đã di chuyển như thế nào?

Trong video, motion là một cue rất hữu ích. Object thường tồn tại qua nhiều frame, và các vùng thuộc cùng một object thường có xu hướng motion liên quan với nhau. Vì vậy, optical flow có thể hỗ trợ model trong việc grouping và tracking.

Trong SAVi, optical flow được nghiên cứu như một prediction target cho video object-centric learning. Nhưng cần nhớ: optical flow là cue hỗ trợ, không phải cơ chế tự động phát hiện object hoàn hảo.

---

# p5_02_motion_limits

Motion cue rất hữu ích, nhưng không phải lời giải hoàn chỉnh.

Trong trường hợp đơn giản, một object di chuyển trên background tĩnh có thể tạo ra flow khá rõ. Điều này giúp model có thêm tín hiệu để grouping vùng object.

Nhưng real-world video phức tạp hơn. Nếu object đứng yên, motion cue có thể rất yếu. Nếu camera di chuyển, background cũng sinh ra optical flow. Nếu nhiều object cùng chuyển động theo một hướng, flow có thể gây nhầm lẫn. Và với non-rigid object như người đi bộ, các phần khác nhau của cùng một object có thể có local motion khác nhau.

Vì vậy, motion nên được hiểu là một tín hiệu hỗ trợ object-centric learning, không phải ground-truth segmentation.

---

# p5_03_depth_lidar_waymo

Ngoài motion, một tín hiệu beyond RGB quan trọng khác là geometry, đặc biệt thông qua depth và LiDAR.

Depth cho biết điểm nào gần, điểm nào xa, bề mặt nào đứng trước, bề mặt nào nằm sau. Trong robotics và autonomous driving, thông tin này rất quan trọng, vì hệ thống không chỉ cần biết object trông như thế nào, mà còn cần biết object nằm ở đâu trong không gian.

LiDAR là một cảm biến dùng xung laser để đo khoảng cách và tạo thông tin ba chiều về bề mặt. Trong thực tế, LiDAR thường tạo ra point cloud hoặc depth signal dạng thưa. Nó cung cấp geometry cue, nhưng không tự động cung cấp semantic object labels.

Trong SAVi++, sparse depth signals từ LiDAR được dùng như một self-supervision target cho slot-based video representation.

Bối cảnh thường được nhắc đến ở đây là Waymo Open Dataset. Cần nói chính xác: Waymo không chỉ là một dataset LiDAR. Nó là dataset perception cho autonomous driving, bao gồm dữ liệu camera và LiDAR-related data trong các real-world driving scenes.

---

# p5_04_dinosaur_features

Beyond RGB không chỉ có optical flow và depth. Một hướng quan trọng khác là reconstruct self-supervised features.

Trong DINOSAUR, thay vì yêu cầu model reconstruct raw RGB pixels, model reconstruct features từ các self-supervised vision models. Đây là một thay đổi quan trọng về training target.

Raw RGB pixels chứa rất nhiều chi tiết cấp thấp như màu sắc, texture, lighting và background. Trong khi đó, self-supervised features có thể mang thông tin thị giác có cấu trúc hơn, hữu ích hơn cho object grouping trên real-world images.

Điểm cần nói rõ là DINOSAUR thuộc nhánh feature reconstruction. Nó không dùng optical flow, cũng không dùng LiDAR depth. DINOSAUR cho thấy reconstruct self-supervised features có thể là một training signal đủ mạnh để object-centric representations xuất hiện theo cách fully unsupervised.

Vì vậy, reconstruct beyond RGB không chỉ là đổi sang sensor mới. Nó còn có thể là đổi từ pixel-level target sang feature-level target.

---

# p5_05_synthesis_encoder_bridge

Tóm lại, synthetic-to-real gap cho thấy rằng real-world data không chỉ phức tạp hơn về mặt hình ảnh. Nó còn khiến reconstruction target trở nên quan trọng hơn.

Nếu target là RGB, model học nhiều về appearance. Nếu target là optical flow, model học motion. Nếu target là depth hoặc LiDAR signal, model học geometry. Nếu target là self-supervised features, model học từ một representation có cấu trúc hơn raw pixels.

Thông điệp chính là: reconstruct beyond RGB không có nghĩa RGB vô dụng. Nó có nghĩa là training signal nên phù hợp với cấu trúc mà ta muốn model học.

Đến đây, ta đã nói về việc thay đổi reconstruction target. Nhưng target chỉ là một nửa câu chuyện. Phần tiếp theo sẽ đi vào một hướng cải thiện khác: nâng cấp encoder. Nếu encoder tạo ra feature tốt hơn ngay từ đầu, thì các slots và reconstruction target phía sau cũng có cơ hội học representation tốt hơn.

Vì vậy, từ câu hỏi “model nên reconstruct cái gì?”, chúng ta chuyển sang câu hỏi tiếp theo: “model nên encode input như thế nào?” Đó là phần Upgrading Encoder.
