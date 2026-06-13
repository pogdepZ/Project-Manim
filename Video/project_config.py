"""Central registry for independently owned Manim video projects."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PROJECTS = {
    "part123": {
        "title": "Part 1-2-3",
        "scene_file": BASE_DIR / "projects" / "part123" / "part123.py",
        "scenes": ["Scene1", "Scene2", "Scene3"],
        "narration_keys": ["scene1", "scene2", "scene3"],
        "manim_output_name": "part123",
        "final_output": BASE_DIR / "output" / "part123.mp4",
    },
    "part45": {
        "title": "Part 4-5",
        "scene_file": BASE_DIR / "projects" / "part45" / "part45.py",
        "scenes": ["Scene4", "Scene5"],
        "narration_keys": ["scene4", "scene5"],
        "manim_output_name": "part45",
        "final_output": BASE_DIR / "output" / "part45.mp4",
    },
    "part67": {
        "title": "Part 6-7",
        "scene_file": BASE_DIR / "projects" / "part67" / "part67.py",
        "scenes": ["Scene6", "Scene7"],
        "narration_keys": ["scene6", "scene7"],
        "manim_output_name": "part67",
        "final_output": BASE_DIR / "output" / "part67.mp4",
    },
    "part8910": {
        "title": "Part 8-9-10",
        "scene_file": BASE_DIR / "projects" / "part8910" / "part8910.py",
        "scenes": ["Scene8", "Scene9", "Scene10"],
        "narration_keys": ["scene8", "scene9", "scene10"],
        "manim_output_name": "part8910",
        "final_output": BASE_DIR / "output" / "part8910.mp4",
    },
    "object_centric_learning": {
        "title": "Object-Centric Learning",
        "scene_file": BASE_DIR
        / "projects"
        / "object_centric_learning"
        / "object_centric_learning.py",
        "scenes": [f"Scene{i}" for i in range(1, 14)],
        "narration_keys": [f"scene{i}" for i in range(1, 14)],
        "manim_output_name": "object_centric_learning",
        "final_output": BASE_DIR / "output" / "object_centric_learning.mp4",
    },
    "autonomous_driving": {
        "title": "Autonomous Driving Scene",
        "scene_file": BASE_DIR
        / "projects"
        / "autonomous_driving"
        / "autonomous_driving.py",
        "scenes": ["AutonomousDrivingScene"],
        "narration_keys": [],
        "manim_output_name": "autonomous_driving",
        "final_output": BASE_DIR / "output" / "autonomous_driving.mp4",
    },
}


def get_project(name):
    try:
        return PROJECTS[name]
    except KeyError as exc:
        available = ", ".join(sorted(PROJECTS))
        raise SystemExit(f"Unknown project '{name}'. Available projects: {available}") from exc
