import sys
import os

sys.path.append(os.path.abspath('manim_scenes'))

from design_system_v3 import *
print('Design system loaded successfully!')

try:
    from scene_001_v5 import Scene001
    print('Scene001 loaded successfully!')
except Exception as e:
    print(f'Error loading Scene001: {e}')

try:
    from scene_005_v5 import Scene005
    print('Scene005 loaded successfully!')
except Exception as e:
    print(f'Error loading Scene005: {e}')
