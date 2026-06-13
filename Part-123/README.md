# SkillManim Video Workspace

Folder nay duoc chia lai de nhieu nguoi lam Manim song song ma it conflict.

## Cau truc

```text
Video/
├── project_config.py
├── render_all.py
├── generate_narration.py
├── combine_video_audio.py
├── full_production.py
├── shared/
│   └── manim_defaults.py
├── projects/
│   ├── part123/
│   │   └── part123.py
│   ├── part45/
│   │   └── part45.py
│   ├── part67/
│   │   └── part67.py
│   ├── part8910/
│   │   └── part8910.py
│   ├── object_centric_learning/
│   │   └── object_centric_learning.py
│   └── autonomous_driving/
│       └── autonomous_driving.py
├── assets/
├── narration/      # output local, khong push
├── media/          # output Manim, khong push
└── output/         # final mp4, khong push
```

## Nguyen tac lam 4 nguoi

4 folder chinh de chia viec:

```text
Video/projects/part123/    # nguoi 1 lam Scene1, Scene2, Scene3
Video/projects/part45/     # nguoi 2 lam Scene4, Scene5
Video/projects/part67/     # nguoi 3 lam Scene6, Scene7
Video/projects/part8910/   # nguoi 4 lam Scene8, Scene9, Scene10
```

Moi nguoi chi sua folder part cua minh trong `Video/projects/<ten_part>/`.

Vi du:

```text
Video/projects/part123/part123.py
Video/projects/part45/part45.py
Video/projects/part67/part67.py
Video/projects/part8910/part8910.py
```

Chi sua file cua project minh. Neu can helper dung chung thi them vao `Video/shared/`.
Khong sua output trong `media/`, `narration/`, `output/` vi cac folder nay la file sinh ra tu may tung nguoi.

Sau khi them project moi, dang ky trong `Video/project_config.py`:

```python
"alice_topic": {
    "title": "Alice Topic",
    "scene_file": BASE_DIR / "projects" / "alice_topic" / "alice_topic.py",
    "scenes": ["Scene1", "Scene2"],
    "narration_keys": ["scene1", "scene2"],
    "manim_output_name": "alice_topic",
    "final_output": BASE_DIR / "output" / "alice_topic.mp4",
},
```

`manim_output_name` nen trung voi ten file `.py` de dung voi output mac dinh cua Manim.

## Cai dat

```bash
cd Video
python3 -m pip install -r requirements.txt
```

May cung can co FFmpeg trong PATH.

## Render

Render project mac dinh:

```bash
cd Video
python3 render_all.py --project object_centric_learning
```

Render nhanh de test:

```bash
python3 render_all.py --project object_centric_learning --quality l
```

Render theo part:

```bash
../.venv/bin/python render_all.py --project part123 --quality l
../.venv/bin/python render_all.py --project part45 --quality l
../.venv/bin/python render_all.py --project part67 --quality l
../.venv/bin/python render_all.py --project part8910 --quality l
```

Render mot scene:

```bash
python3 render_all.py --project object_centric_learning --scene Scene1
```

## Tao narration

```bash
python3 generate_narration.py --project object_centric_learning
```

Audio se nam trong:

```text
Video/narration/object_centric_learning/
```

## Ghep video voi audio

```bash
python3 combine_video_audio.py --project object_centric_learning
```

Final video se nam trong:

```text
Video/output/object_centric_learning.mp4
```

## Chay full pipeline

```bash
python3 full_production.py --project object_centric_learning
```

Neu da co narration san:

```bash
python3 full_production.py --project object_centric_learning --skip-tts
```

## Luu y push chung

Nen push source:

- `Video/projects/...`
- `Video/shared/...`
- `Video/project_config.py`
- script `.py`
- `Video/assets/...` neu asset do la source can thiet

Khong push:

- `Video/media/`
- `Video/narration/`
- `Video/output/`
- file `*.mp4`, `*.mp3`
- file `*:Zone.Identifier`
