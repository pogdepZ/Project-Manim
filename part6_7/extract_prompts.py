import re
import os

with open('merged_script_content.txt', 'r', encoding='utf-8') as f:
    script_text = f.read()

with open('scene_part6_7.py', 'r', encoding='utf-8') as f:
    code_text = f.read()

# Extract scripts
scripts = {}
matches = re.finditer(r'### SCENE (\d+):[^\n]+\n[^\n]+\n\n\"([^\"]+)\"', script_text)
for m in matches:
    scene_num = int(m.group(1))
    content = m.group(2).strip()
    scripts[scene_num] = content

# Extract code classes
classes = {}
lines = code_text.split('\n')
current_class = None
current_code = []

scene_mapping = {
    8: 'S6_08_AdaSlot',
    9: 'S6_09_VideoSaur',
    10: 'S6_10_Part6Summary',
    11: 'S7_01_SlotDecodingDilemma',
    12: 'S7_02_PixelIndependence',
    13: 'S7_03_TwoDirections',
    14: 'S7_04_MLPvsTransformer',
    15: 'S7_05_SLATEDecoder',
    16: 'S7_06_DiffusionLSD',
    17: 'S7_07_DORSAL3D',
    18: 'S7_08_ObSuRF',
    19: 'S7_09_OSRT',
    20: 'S7_10_SysBinder',
    21: 'S7_11_MoToK',
    22: 'S7_12_CoSA',
    23: 'S7_13_ISA',
    24: 'S7_14_DiffFAE',
    25: 'S7_15_PaLME',
    26: 'S7_16_ThreeParadigms',
    27: 'S7_17_Part7Summary'
}

reverse_mapping = {v: k for k, v in scene_mapping.items()}

for line in lines:
    if line.startswith('class S'):
        if current_class is not None:
            if current_class in reverse_mapping:
                classes[reverse_mapping[current_class]] = '\n'.join(current_code)
        m = re.match(r'class ([A-Za-z0-9_]+)\(Scene\):', line)
        if m:
            current_class = m.group(1)
            current_code = [line]
    elif current_class is not None:
        current_code.append(line)

if current_class in reverse_mapping:
    classes[reverse_mapping[current_class]] = '\n'.join(current_code)

output = []
for i in range(8, 28):
    if i in scripts and i in classes:
        prompt = f'\"{scripts[i]}\"\n\nđây là script của scene {i} hãy thêm object, animation mô tả thêm vì có nhiều nội\\ndung giải thích không có mô tả cho nội dung đó\n\n[thay code theo scene từ scene_part6_7.py vào đây]\n{classes[i]}\n\nchỉnh thời gian xuất hiện của các object sao cho fit với audio dài xx:xxp \\ncomment từng ọbject và chuyển động vào code luôn\n\n------------------------------------------------------------\n'
        output.append(prompt)

with open(r'C:\Users\minpr\.gemini\antigravity-ide\brain\1d91e16b-3110-4bb4-9a38-2427afb908c9\prompts_scene_8_to_27.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('Done')
