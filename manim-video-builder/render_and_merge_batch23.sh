#!/bin/bash
source venv/bin/activate

# Render Batch 2 (006 - 010)
for i in {6..10}; do
    scene_num=$(printf "%03d" $i)
    echo "Rendering Scene ${scene_num}_v5..."
    manim -pqL manim_scenes/scene_${scene_num}_v5.py Scene${scene_num}
done

echo "======================================"
echo "CREATING FFMPEG CONCAT FILE FOR BATCH 2"
echo "======================================"
rm -f concat_batch2.txt
for i in {6..10}; do
    scene_num=$(printf "%03d" $i)
    # Get the generated mp4 path
    mp4_file="media/videos/scene_${scene_num}_v5/720p30/Scene${scene_num}.mp4"
    if [ -f "$mp4_file" ]; then
        echo "file '$mp4_file'" >> concat_batch2.txt
    else
        echo "WARNING: $mp4_file not found!"
    fi
done

echo "======================================"
echo "MERGING BATCH 2 WITH FFMPEG"
echo "======================================"
ffmpeg -y -f concat -safe 0 -i concat_batch2.txt -c copy output_batch_2.mp4

# Render Batch 3 (011 - 015)
for i in {11..15}; do
    scene_num=$(printf "%03d" $i)
    echo "Rendering Scene ${scene_num}_v5..."
    manim -pqL manim_scenes/scene_${scene_num}_v5.py Scene${scene_num}
done

echo "======================================"
echo "CREATING FFMPEG CONCAT FILE FOR BATCH 3"
echo "======================================"
rm -f concat_batch3.txt
for i in {11..15}; do
    scene_num=$(printf "%03d" $i)
    # Get the generated mp4 path
    mp4_file="media/videos/scene_${scene_num}_v5/720p30/Scene${scene_num}.mp4"
    if [ -f "$mp4_file" ]; then
        echo "file '$mp4_file'" >> concat_batch3.txt
    else
        echo "WARNING: $mp4_file not found!"
    fi
done

echo "======================================"
echo "MERGING BATCH 3 WITH FFMPEG"
echo "======================================"
ffmpeg -y -f concat -safe 0 -i concat_batch3.txt -c copy output_batch_3.mp4

echo "======================================"
echo "DONE! output_batch_2.mp4 and output_batch_3.mp4 created."
echo "======================================"
