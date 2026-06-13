import json
data = json.load(open('output/final/manifest.json'))
indices = [e['scene_index'] for e in data]
print(indices)
