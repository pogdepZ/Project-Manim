# CODEX PROMPT – REBUILD PART 4 & 5 FROM SCRATCH, 12–15 MINUTES

You are a senior Manim engineer, Python engineer, and scientific video production assistant.

We are rebuilding Part 4 & Part 5 from scratch because prior iterations became visually messy: overlapping text, misaligned arrows, duplicated visual beats, and poor layout discipline.

This time, prioritize product quality over speed. Take time to design clean scenes, stable layout helpers, accurate narration mapping, and reliable audio/video sync.

## 0. Files to read first

Read these files before editing code:

1. `kich_ban_phan4_phan5_12_15min.md`  
   Primary storyboard. Target duration: 12–15 minutes. Includes scene goals, on-screen text, voice-over, visual beats, and transitions.

2. `NARRATION_SCRIPT_12_15min.md`  
   Primary narration source. Use this for `generate_narration_part4_part5.py`.

3. `object_centric_part4_part5_video_content_12_15min.md`  
   Scientific accuracy and production rules.

Also inspect current project files:
- `scene_part4_part5.py`
- `render_part4_part5.py`
- `generate_narration_part4_part5.py`
- `combine_part4_part5.py`
- README / requirements files if present.

## 1. Hard goals

Build a polished Manim educational video for:

```text
Synthetic-to-Real Gap & Reconstruct Beyond RGB
```

Final video requirements:
- Duration: 12–15 minutes.
- Target: about 13–14 minutes.
- Clear bridge from previous section: `SLOT ATTENTION`.
- Clear bridge to next section: `UPGRADING ENCODER`.
- Clean visuals, not crowded slides.
- Stable layout and no overlapping objects.
- Per-scene audio/video sync.
- Scientific claims must be cautious and source-aligned.

## 2. Do not do these

Do not:
- stretch scenes by only adding `self.wait()`;
- create long static slides with no visual changes;
- add too many objects to one frame;
- leave old visual beats on screen when new beats appear;
- hard-code random coordinates everywhere;
- connect arrows using manual coordinates when object anchors are available;
- allow cards/text/arrows to overlap;
- invent scientific claims;
- create fake paper diagrams or fake benchmark results;
- call Waymo “only a LiDAR dataset”;
- imply RGB is useless;
- imply optical flow perfectly detects objects;
- imply LiDAR/depth gives semantic labels automatically;
- imply DINOSAUR uses optical flow or LiDAR;
- imply real-world object-centric learning is solved.

## 3. Required scene structure

Implement these scene classes in `scene_part4_part5.py`:

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

Update `render_part4_part5.py` and `combine_part4_part5.py` to use this exact order.

## 4. Scene order and target durations

| Scene class | Target |
|---|---:|
| Part04BridgeSlotAttention | 0:45 |
| Part04SyntheticRealGap | 1:20 |
| Part04RealWorldHard | 1:25 |
| Part04RGBReconstructionPipeline | 1:15 |
| Part04RGBDistracts | 1:30 |
| Part04CoreQuestion | 0:55 |
| Part05OpticalFlowCue | 1:20 |
| Part05MotionLimits | 1:15 |
| Part05DepthLidarWaymo | 1:35 |
| Part05DinosaurFeatures | 1:35 |
| Part05SynthesisEncoderBridge | 1:00 |

Final total must be 12–15 minutes.

If narration duration differs from planned duration, sync video to audio per scene rather than cutting narration.

## 5. Layout architecture

Before building scenes, create a reusable layout system in `scene_part4_part5.py`.

Use constants:

```python
TITLE_Y = 3.25
SUBTITLE_Y = 2.82
CONTENT_TOP = 2.25
CONTENT_BOTTOM = -2.25
FOOTER_Y = -3.25
LEFT_X = -3.4
CENTER_X = 0
RIGHT_X = 3.4
SAFE_LEFT = -6.15
SAFE_RIGHT = 6.15
SAFE_TOP = 3.35
SAFE_BOTTOM = -3.35
```

Create helpers:
- `add_background(scene)`
- `make_title(text)`
- `make_subtitle(text)`
- `make_section_label(number, title)`
- `make_footer_takeaway(text)`
- `make_card(width, height, stroke_color, fill_color=None)`
- `make_pill(text, color)`
- `make_pipeline(labels, colors=None, max_width=11.0)`
- `make_routed_arrow(start_mob, end_mob, color)`
- `fit_to_width(mob, max_width)`
- `keep_inside_frame(mob, margin=0.25)`
- `replace_beat(scene, old_group, new_group, run_time=0.8)`

Rules:
- Title, subtitle, section label, and footer are persistent.
- Main content must stay inside the content area.
- Use `VGroup.arrange()` and object anchors.
- Avoid arbitrary `.shift()` except at final group level.
- Set z-index: background 0, panels/cards 1, arrows 2, icons/objects 3, text 4, title/footer 5.

## 6. Visual beat discipline

Each scene must be made of visual beats.

Rules:
- Each beat is a `VGroup`.
- Replace or dim the previous beat before showing the next.
- Do not keep all beats visible at once.
- Each beat should match a segment of the voice-over.
- On-screen text must be short.
- Use diagrams and animation, not paragraphs.

In code, mark beats clearly:

```python
# Beat 1: bridge from Slot Attention
# Beat 2: ask reconstruction target question
# Beat 3: branch into this section
```

## 7. Scene-specific requirements

### Part04BridgeSlotAttention
Visual: Pixels/Image → Slot Attention → Slots → Reconstruction Target? → Synthetic-to-Real Gap + Beyond RGB.  
Takeaway: `After slots, the next question is the training target.`

### Part04SyntheticRealGap
Visual: clean split-screen: Synthetic Data vs Real-world Data.  
Takeaway: `Controlled scenes do not capture all real-world complexity.`

### Part04RealWorldHard
Visual beats: appearance/texture, lighting/shadow, occlusion, clutter, motion.  
Rule: at most 3 active tags visible at once. Dim older tags.

### Part04RGBReconstructionPipeline
Visual: pipeline `RGB Frame → Encoder → Slots → Decoder → RGB Output`, then pixel-level loss.  
Caution: `The loss asks for similar pixels, not direct object understanding.`

### Part04RGBDistracts
Visual: real-world object illustration, tags, pixel question vs object question.  
Takeaway: `RGB is useful, but not always the best object-centric target.`

### Part04CoreQuestion
Visual: central question, branches to Motion, Geometry, Features.

### Part05OpticalFlowCue
Visual: frame t, frame t+1, moving object, displacement arrows.  
Caption: `Conceptual vector field, not computed optical flow.`

### Part05MotionLimits
Visual: four mini-cards: helpful motion, static object, moving camera, shared/non-rigid motion.  
Warning: `Useful cue ≠ complete solution`.

### Part05DepthLidarWaymo
Visual: driving scene, LiDAR rays, sparse point cloud, Waymo dataset card.  
Caption: `Sparse depth signals, not semantic labels.`

### Part05DinosaurFeatures
Visual: pixel target vs feature target, feature map grid.  
Warning: `DINOSAUR: feature reconstruction, not flow or LiDAR.`

### Part05SynthesisEncoderBridge
Visual: summary table, then `Better target + Better encoder`, highlight Encoder block.  
Final card: `Next: Upgrading Encoder`.

## 8. Narration generation

Update `generate_narration_part4_part5.py` from `NARRATION_SCRIPT_12_15min.md`.

Requirements:
- One MP3 per scene.
- Output folder: `narration_part4_part5/`.
- Keep a `PRONUNCIATION_MAP`.
- Apply TTS normalization only to narration text, not on-screen text.
- Sort pronunciation replacements by descending key length.

## 9. Audio/video sync

Update `combine_part4_part5.py`.

Do not concatenate video-only and audio-only streams separately first.

Required pipeline:
1. For each scene, locate rendered video and matching MP3.
2. Use `ffprobe` to measure video_duration, audio_duration, delta.
3. Print table: `Scene | video duration | audio duration | delta | action`.
4. If audio is longer than video, pad video using freeze last frame / `tpad`.
5. If video is longer than audio, pad audio with silence.
6. Merge each scene into a synced temporary clip.
7. Concatenate synced clips.
8. Output: `final_part4_part5_with_narration.mp4`.

Encoding:
- video: `libx264`
- audio: `aac`
- pix_fmt: `yuv420p`
- fps: `30`

Do not use `-shortest` in a way that cuts narration.

## 10. Quality control process

Do the work in phases:

1. Read and plan.
2. Implement stable layout helpers.
3. Implement scenes one by one.
4. Render test each scene after implementation.
5. Validate layout visually.
6. Generate narration.
7. Combine per scene.
8. Confirm final duration is 12–15 minutes.

For every rendered scene, check:
- no text overlap;
- no card overlap;
- no arrow through text;
- no object outside safe frame;
- no visual beat remains accidentally visible;
- footer and title are readable.

## 11. Required test commands

Syntax check:

```bash
python -m py_compile scene_part4_part5.py render_part4_part5.py generate_narration_part4_part5.py combine_part4_part5.py
```

Render representative scenes first:

```bash
manim -qm scene_part4_part5.py Part04BridgeSlotAttention
manim -qm scene_part4_part5.py Part04RGBReconstructionPipeline
manim -qm scene_part4_part5.py Part05OpticalFlowCue
manim -qm scene_part4_part5.py Part05DepthLidarWaymo
manim -qm scene_part4_part5.py Part05DinosaurFeatures
manim -qm scene_part4_part5.py Part05SynthesisEncoderBridge
```

Full pipeline:

```bash
python render_part4_part5.py
python generate_narration_part4_part5.py
python combine_part4_part5.py
```

## 12. Final report requirements

At the end, report:
- files changed;
- scene class list;
- actual narration durations if available;
- final video duration;
- layout helpers added;
- how overlap/arrow alignment was prevented;
- how audio/video sync was handled;
- whether intro bridge from Slot Attention is present;
- whether outro bridge to Upgrading Encoder is present;
- any scientific claim adjusted for accuracy;
- commands to rerun.

Focus on quality. Do not rush.
