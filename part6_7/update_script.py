import re

SCENE_TITLES = [
    "SCENE 1: CNN Failure",
    "SCENE 2: Feature Reconstruction",
    "SCENE 3: ViT Architecture",
    "SCENE 4: DINOSAUR Model",
    "SCENE 5: SSL Comparison",
    "SCENE 6: Encoder Upgrade Challenge",
    "SCENE 7: Optical Flow & Depth",
    "SCENE 8: Dynamic Slots (AdaSlot)",
    "SCENE 9: Temporal Similarity (VideoSaur)",
    "SCENE 10: Part 6 Summary",
    "SCENE 11: Slot-Decoding Dilemma",
    "SCENE 12: Pixel Independence",
    "SCENE 13: 3D Bias & Decoupling",
    "SCENE 14: MLP vs Transformer",
    "SCENE 15: SLATE",
    "SCENE 16: Latent Slot Diffusion",
    "SCENE 17: DORSAL",
    "SCENE 18: ObSuRF",
    "SCENE 19: OSRT",
    "SCENE 20: SysBinder",
    "SCENE 21: MoToK",
    "SCENE 22: CoSA",
    "SCENE 23: ISA",
    "SCENE 24: DiffFAE",
    "SCENE 25: PaLM-E",
    "SCENE 26: Three Paradigms",
    "SCENE 27: Part 7 Summary"
]

SCENE_MAPPING = {
    1: r"^6\.1\.",
    2: r"^6\.2\.",
    3: r"^6\.3\.",
    4: r"^6\.4\.",
    5: r"^6\.5\.",
    6: r"^6\.6\.",
    7: r"^6\.7\.",
    8: r"^6\.8\.",
    9: r"^6\.9\.",
    10: r"^6\.10\.",
    11: r"^7\.1\.",
    12: r"^7\.2\.",
    13: r"^7\.3\.",
    14: r"^7\.4\.",
    15: r"^7\.5\.",
    16: r"^7\.6\.",
    17: r"^7\.7\.",
    18: r"^7\.8\.",
    19: r"^7\.9\.",
    20: r"^7\.10\.",
    21: r"^7\.11\.",
    22: r"^7\.12\.",
    23: r"^7\.13\.",
    24: r"^7\.14\.",
    25: r"^7\.15\.",
    26: r"^7\.16\.",
    27: r"^7\.17\.",
}

with open("extracted_docx.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

# Parse into sections
sections = {}
current_section_idx = 0

for line in lines:
    line = line.strip()
    if not line or line.startswith("[Visual]") or line.startswith("TÀI LIỆU THAM KHẢO") or line.startswith("[1]"):
        continue
    
    match = re.match(r"^([67]\.\d+(\.\d+)?)\.", line)
    if match:
        # Check if it matches a scene starting section
        sec_prefix = match.group(1) + "."
        # find matching scene
        matched_scene = None
        for scene_idx, pat in SCENE_MAPPING.items():
            if re.match(pat, sec_prefix):
                matched_scene = scene_idx
                break
        
        if matched_scene:
            current_section_idx = matched_scene
            # Ignore the title line for narration or we can include it but maybe without the "6.1. Title"
            # It's better to ignore the heading line for TTS narration
            sections[current_section_idx] = []
            continue
        elif current_section_idx == 7 and sec_prefix.startswith("6.7."):
            # subsections 6.7.1, 6.7.2 belong to scene 7
            continue
        
    if current_section_idx > 0:
        sections[current_section_idx].append(line)

# Now build the script
with open("merged_script_content.txt", "w", encoding="utf-8") as f:
    for i in range(1, 28):
        title = SCENE_TITLES[i-1]
        narration = " ".join(sections.get(i, []))
        # Ensure narration is wrapped in quotes
        f.write(f"### {title}\n")
        f.write(f"**Thời gian video: TBD**\n\n")
        f.write(f'"{narration}"\n\n---\n\n')

print("Update completed.")
