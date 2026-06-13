#!/bin/bash
echo "Waiting for rendering process (PID 140349) to finish..."
while kill -0 140349 2>/dev/null; do
    sleep 5
done
echo "Rendering complete. Starting merge..."
cd /home/pognova/SkillManim/manim-video-builder
../.venv/bin/python merge_final_v3.py > merge_v3.log 2>&1
echo "Merge complete."
