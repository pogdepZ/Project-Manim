#!/bin/bash
source venv/bin/activate

# Fix merge for Batch 2
echo "MERGING BATCH 2"
rm -f concat_batch2.txt
for i in {6..10}; do
    scene_num=$(printf "%03d" $i)
    mp4_file="media/videos/scene_${scene_num}_v5/480p15/Scene${scene_num}.mp4"
    if [ -f "$mp4_file" ]; then
        echo "file '$mp4_file'" >> concat_batch2.txt
    fi
done
ffmpeg -y -f concat -safe 0 -i concat_batch2.txt -c copy output_batch_2.mp4

# Fix merge for Batch 3
echo "MERGING BATCH 3"
rm -f concat_batch3.txt
for i in {11..15}; do
    scene_num=$(printf "%03d" $i)
    mp4_file="media/videos/scene_${scene_num}_v5/480p15/Scene${scene_num}.mp4"
    if [ -f "$mp4_file" ]; then
        echo "file '$mp4_file'" >> concat_batch3.txt
    fi
done
ffmpeg -y -f concat -safe 0 -i concat_batch3.txt -c copy output_batch_3.mp4

# Render Batch 4 (016 - 020)
echo "RENDERING BATCH 4"
for i in {16..20}; do
    scene_num=$(printf "%03d" $i)
    echo "Rendering Scene ${scene_num}_v5..."
    manim -ql manim_scenes/scene_${scene_num}_v5.py Scene${scene_num}
done

rm -f concat_batch4.txt
for i in {16..20}; do
    scene_num=$(printf "%03d" $i)
    mp4_file="media/videos/scene_${scene_num}_v5/480p15/Scene${scene_num}.mp4"
    if [ -f "$mp4_file" ]; then
        echo "file '$mp4_file'" >> concat_batch4.txt
    fi
done
ffmpeg -y -f concat -safe 0 -i concat_batch4.txt -c copy output_batch_4.mp4

# Render Batch 5 (021 - 025)
echo "RENDERING BATCH 5"
for i in {21..25}; do
    scene_num=$(printf "%03d" $i)
    echo "Rendering Scene ${scene_num}_v5..."
    manim -ql manim_scenes/scene_${scene_num}_v5.py Scene${scene_num}
done

rm -f concat_batch5.txt
for i in {21..25}; do
    scene_num=$(printf "%03d" $i)
    mp4_file="media/videos/scene_${scene_num}_v5/480p15/Scene${scene_num}.mp4"
    if [ -f "$mp4_file" ]; then
        echo "file '$mp4_file'" >> concat_batch5.txt
    fi
done
ffmpeg -y -f concat -safe 0 -i concat_batch5.txt -c copy output_batch_5.mp4

# Render Batch 6 (026 - 030)
echo "RENDERING BATCH 6"
for i in {26..31}; do
    scene_num=$(printf "%03d" $i)
    echo "Rendering Scene ${scene_num}_v5..."
    manim -ql manim_scenes/scene_${scene_num}_v5.py Scene${scene_num}
done

rm -f concat_batch6.txt
for i in {26..31}; do
    scene_num=$(printf "%03d" $i)
    mp4_file="media/videos/scene_${scene_num}_v5/480p15/Scene${scene_num}.mp4"
    if [ -f "$mp4_file" ]; then
        echo "file '$mp4_file'" >> concat_batch6.txt
    fi
done
ffmpeg -y -f concat -safe 0 -i concat_batch6.txt -c copy output_batch_6.mp4

echo "ALL BATCHES RENDERED AND MERGED!"
