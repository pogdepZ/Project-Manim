# OBJECT-CENTRIC PART 4–5 CONTENT SPEC – BẢN 12–15 PHÚT

**Topic:** Synthetic-to-Real Gap & Reconstruct Beyond RGB  
**Target duration:** 12–15 phút  
**Primary storyboard:** `kich_ban_phan4_phan5_12_15min.md`  
**Primary narration:** `NARRATION_SCRIPT_12_15min.md`

## 1. Vị trí trong video nhóm

```text
SLOT ATTENTION  →  SYNTHETIC-TO-REAL GAP & BEYOND RGB  →  UPGRADING ENCODER
```

Video bắt buộc có:
- opening bridge từ Slot Attention;
- closing bridge sang Upgrading Encoder.

## 2. Core message

Real-world data phức tạp hơn synthetic data vì có nhiều yếu tố appearance, lighting, occlusion, clutter và motion.

Vì raw RGB reconstruction có thể khiến model dành nhiều năng lực cho low-level visual details, researchers xem xét các reconstruction targets hoặc signals khác ngoài RGB:
- optical flow cho motion;
- depth/LiDAR cho geometry;
- self-supervised features cho structured visual representation.

Ý chính không phải là RGB vô dụng. Ý đúng là reconstruction target nên phù hợp với cấu trúc mà ta muốn model học.

## 3. Source map

### [S1] Slot Attention — NeurIPS 2020
Use for transition from prior content, slots, competitive attention.
Safe claim: Slot Attention produces abstract slots/object-like representations.
Do not say slots always perfectly correspond to real objects.

### [S2] SAVi
Use for optical flow prediction, motion cue, video object-centric learning.
Safe claim: Optical flow can be used as a prediction target and can support segmentation/tracking.
Do not say optical flow detects objects perfectly.

### [S3] SAVi++
Use for depth prediction, sparse LiDAR depth, real-world video and Waymo.
Safe claim: Sparse depth signals from LiDAR can be used as self-supervision target.
Do not say LiDAR/depth gives semantic object labels automatically.

### [S4] DINOSAUR
Use for self-supervised feature reconstruction.
Safe claim: DINOSAUR reconstructs self-supervised features, not raw RGB pixels.
Do not say DINOSAUR uses optical flow or LiDAR.

### [S5] CVPR 2024 Object-centric Representations Tutorial
Use for high-level framing only.

### [S6] OpenCV Optical Flow Documentation
Use for definition of optical flow as apparent motion between consecutive frames.

### [S7] NOAA LiDAR Explanation
Use for definition of LiDAR as laser-based distance measurement / 3D surface information.

### [S8] Waymo Open Dataset
Use for autonomous driving perception dataset and camera + LiDAR-related data.

## 4. Required wording

Use:
- “có thể hỗ trợ”
- “là một cue”
- “thường có xu hướng”
- “không phải lời giải hoàn chỉnh”
- “conceptual illustration”
- “training signal”
- “self-supervision target”
- “structured visual representation”

Avoid:
- “RGB vô dụng”
- “Optical flow phát hiện object”
- “Depth giải quyết segmentation”
- “LiDAR hiểu object”
- “Waymo chỉ là LiDAR dataset”
- “Real-world object-centric learning đã được solved hoàn toàn”

## 5. Visual quality requirements

Every scene must use a stable layout system:
- title area;
- content area;
- footer/takeaway area;
- optional small progress label.

Required helpers:
- `make_title`
- `make_subtitle`
- `make_caption`
- `make_card`
- `make_pill`
- `make_pipeline`
- `make_table_row`
- `fit_to_width`
- `keep_inside_frame`
- `replace_beat`

Avoid:
- random hard-coded shifts;
- arrows with manual coordinates when object anchors can be used;
- retaining all visual beats on screen at once;
- text paragraphs on screen;
- arrow through text;
- overlapping cards.

## 6. Required scene classes

Recommended class names:

```python
class Part04BridgeSlotAttention(Scene): ...
class Part04SyntheticRealGap(Scene): ...
class Part04RealWorldHard(Scene): ...
class Part04RGBReconstructionPipeline(Scene): ...
class Part04RGBDistracts(Scene): ...
class Part04CoreQuestion(Scene): ...
class Part05OpticalFlowCue(Scene): ...
class Part05MotionLimits(Scene): ...
class Part05DepthLidarWaymo(Scene): ...
class Part05DinosaurFeatures(Scene): ...
class Part05SynthesisEncoderBridge(Scene): ...
```

## 7. Audio/video sync

For each scene:
1. render scene video;
2. generate matching MP3;
3. measure video duration and audio duration;
4. pad video or audio per scene if needed;
5. merge per scene;
6. concatenate synced clips.

Do not concatenate all video and all audio separately before merging.

## 8. Final acceptance criteria

- Final duration is 12–15 minutes.
- Visuals are clean and readable.
- No layout overlap.
- No arrow misalignment.
- No fake scientific diagrams from papers.
- No unsupported claims.
- Audio and video are synced per scene.
- Intro bridge from Slot Attention exists.
- Outro bridge to Upgrading Encoder exists.
