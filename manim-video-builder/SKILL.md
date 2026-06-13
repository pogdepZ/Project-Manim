---
name: manim-video-builder
description: >-
  Turn a long explanation script into a narrated Manim video with visual math
  animations, Vietnamese edge-tts narration, subtitles, timing files, and a final MP4.
  Supports Auto and Manual modes.
---

# manim-video-builder

Use this skill when the user wants to turn a long explanation script into a narrated Manim video. It supports automatic templates or manual editing of individual scenes before rendering.

---

## Modes of Operation

The tool supports two primary workflows depending on the complexity of the animations:

### 1. Auto Mode
Use this mode to quickly generate and render a video using preset animation templates based on keywords detected in the script.

```bash
python src/main.py --input input/script.txt --voice vi-VN-HoaiMyNeural --max-chars 800 --quality medium
```

*Note: If `python` is not available, use `python3` instead.*

---

### 2. Manual Mode (Recommended for Premium 3Blue1Brown Aesthetics)
Since beautiful, 100% automated animations are difficult, use Manual Mode to generate the code, customize key scenes, and render the final video without losing your edits.

#### Step 1: Generate Scene Code & Manifest (Dry Run)
Generate all voice narration files, subtitles, and draft Manim python code without running the renderer.
```bash
python src/main.py --input input/script.txt --no-render
```

#### Step 2: Customize Scene Animations
Edit the generated python scripts located in `manim_scenes/` (e.g. [scene_001.py](file:///Ubuntu/home/pognova/SkillManim/manim-video-builder/manim_scenes/scene_001.py)). Add custom equations, graphs, vectors, or visual logic.

#### Step 3: Render and Assemble
Compile and render the final video using the `--keep-code` flag to prevent overwriting your modified files:
```bash
python src/main.py --keep-code
```

---

## Recommended Script Structure for Long Documents
For long documents, structure the inputs into clear, logical segments so the initial layout represents a complete storyboard:

1. **Scene 1 (Title & Main Ideas)**: Displays the title of the topic and key high-level concepts.
2. **Scene 2 (Formulas & Equations)**: Visualizes the math formulas, variables, and theoretical foundation.
3. **Scene 3 (Graph / Visual Logic)**: Renders coordinate systems, function plots, or custom diagrams.
4. **Scene 4 (Illustrative Examples)**: Demonstrates concrete applications, object transitions, or step-by-step logic.
5. **Scene 5 (Recap / Conclusion)**: Summarizes the takeaways and provides a visual wrap-up.

---

## Key Command Line Options

- `--input <path>`: Path to the source text file containing the video script.
- `--voice <voice_name>`: Specify edge-tts voice (e.g. `vi-VN-HoaiMyNeural`, `vi-VN-NamMinhNeural`).
- `--keep-code`: Keep existing `.py` scene files in `manim_scenes/` instead of regenerating/overwriting them.
- `--no-render`: Only generate scene assets, voice, and Manim code without rendering.
- `--no-tts`: Skip voice synthesis; use text-length estimated timings.
- `--resume`: Skip scenes that already have completed outputs (`video_with_audio.mp4`).
- `--force`: Force rebuild/re-render of selected scenes.
- `--clean`: Clear previous outputs in `output/` and `manim_scenes/`.
- `--quality low|medium|high`: Set rendering quality (low: 480p, medium: 720p, high: 1080p).

---

## File and Output Artifacts

- **Scene Code**: [manim_scenes/](file:///Ubuntu/home/pognova/SkillManim/manim-video-builder/manim_scenes/) - contains individual python files for each scene (e.g. `scene_001.py`).
- **Scene Assets**: [output/scenes/](file:///Ubuntu/home/pognova/SkillManim/manim-video-builder/output/scenes/) - subdirectory per scene containing temporary voice tracks, partial renders, and subtitles.
- **Final Output**: [output/final/](file:///Ubuntu/home/pognova/SkillManim/manim-video-builder/output/final/)
  - `manifest.json`: JSON structure describing all scene timings.
  - `subtitles.srt`: Subtitle track for the full video.
  - `narration.mp3`: Unified narration audio track.
  - `final_video.mp4`: The final narrated MP4 video.
