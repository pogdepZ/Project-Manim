#!/bin/bash
set -e

echo "======================================"
echo "RENDERING SCENES 001 - 005 (v5)"
echo "======================================"

# Run manim for each scene
manim -pqm manim_scenes/scene_001_v5.py Scene001
manim -pqm manim_scenes/scene_002_v5.py Scene002
manim -pqm manim_scenes/scene_003_v5.py Scene003
manim -pqm manim_scenes/scene_004_v5.py Scene004
manim -pqm manim_scenes/scene_005_v5.py Scene005

echo "======================================"
echo "CREATING FFMPEG CONCAT FILE"
echo "======================================"

# Create the concat list
cat <<EOF > concat_list.txt
file 'media/videos/scene_001_v5/720p30/Scene001.mp4'
file 'media/videos/scene_002_v5/720p30/Scene002.mp4'
file 'media/videos/scene_003_v5/720p30/Scene003.mp4'
file 'media/videos/scene_004_v5/720p30/Scene004.mp4'
file 'media/videos/scene_005_v5/720p30/Scene005.mp4'
EOF

# Note: The resolution is 720p30 because of the -qm flag (medium quality).
# If you used -qh (high quality), it would be 1080p60.

echo "======================================"
echo "MERGING VIDEOS WITH FFMPEG"
echo "======================================"

# Concatenate using ffmpeg
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy output_batch_1.mp4

echo "======================================"
echo "DONE! output_batch_1.mp4 created."
echo "======================================"
