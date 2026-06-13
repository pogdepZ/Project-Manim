#!/bin/bash

echo "======================================"
echo "MERGING ALL BATCHES INTO FINAL VIDEO"
echo "======================================"

cd /home/pognova/SkillManim/manim-video-builder

rm -f concat_all.txt

for i in {1..6}; do
    batch_file="output_batch_${i}.mp4"
    if [ -f "$batch_file" ]; then
        echo "file '$batch_file'" >> concat_all.txt
    else
        echo "WARNING: $batch_file not found!"
    fi
done

ffmpeg -y -f concat -safe 0 -i concat_all.txt -c copy final_full_video_v5.mp4

echo "======================================"
echo "DONE! final_full_video_v5.mp4 has been created."
echo "======================================"
