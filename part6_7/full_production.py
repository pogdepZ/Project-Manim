#!/usr/bin/env python3
"""
Master Script: Full Video Production Pipeline
Run: python full_production.py

This script automates the entire workflow:
1. Check dependencies
2. Render all Manim scenes
3. Generate Vietnamese narration
4. Combine video + audio
5. Validate output
"""

import subprocess
import sys
import os
from pathlib import Path

os.environ["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"

class VideoProducer:
    def __init__(self):
        self.step = 0
        self.total_steps = 5
    
    def print_header(self, title):
        print(f"\n{'='*70}")
        self.step += 1
        print(f"STEP {self.step}/{self.total_steps}: {title}")
        print(f"{'='*70}\n")
    
    def run_command(self, cmd, description=""):
        """Run shell command"""
        if description:
            print(f"▶ {description}...")
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e}")
            return False
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        self.print_header("Checking Dependencies")
        
        result = self.run_command(
            [sys.executable, "check_dependencies.py"],
            "Checking dependencies"
        )
        
        if not result:
            print("\n❌ Missing dependencies. Install with:")
            print("   pip install -r requirements.txt")
            return False
        
        print("✅ All dependencies ready!")
        return True
    
    def render_scenes(self):
        """Render all Manim scenes"""
        self.print_header("Rendering Manim Scenes")
        
        print("This may take 30-45 minutes depending on your computer...")
        print("Quality: 1080p60 (high)\n")
        
        result = self.run_command(
            [sys.executable, "render_all.py"],
            "Rendering 6 scenes"
        )
        
        if not result:
            print("\n❌ Render failed")
            return False
        
        print("\n✅ All scenes rendered!")
        return True
    
    def generate_narration(self):
        """Generate Vietnamese narration"""
        self.print_header("Generating Vietnamese Narration (TTS)")
        
        print("Creating 6 MP3 files with Microsoft Edge TTS...\n")
        
        result = self.run_command(
            [sys.executable, "generate_narration.py"],
            "Generating narration"
        )
        
        if not result:
            print("\n❌ Narration generation failed")
            return False
        
        print("\n✅ Narration ready!")
        return True
    
    def combine_video_audio(self):
        """Combine video and audio"""
        self.print_header("Combining Video + Audio")
        
        print("Merging 6 video scenes and 6 audio files...\n")
        
        result = self.run_command(
            [sys.executable, "combine_video_audio.py"],
            "Combining video and audio"
        )
        
        if not result:
            print("\n❌ Combination failed")
            return False
        
        print("\n✅ Video + audio combined!")
        return True
    
    def validate_output(self):
        """Validate final output"""
        self.print_header("Validating Output")
        
        output_file = "final_video_with_narration.mp4"
        
        if not os.path.exists(output_file):
            print(f"❌ Output file not found: {output_file}")
            return False
        
        file_size = os.path.getsize(output_file) / (1024 * 1024)
        
        print(f"✅ Output file exists")
        print(f"📁 File: {output_file}")
        print(f"📊 Size: {file_size:.2f} MB")
        print(f"⏱️  Duration: ~2-3 minutes")
        
        return True
    
    def run_full_pipeline(self):
        """Execute full production pipeline"""
        print("\n" + "🎬 " * 20)
        print("   Object-Centric Learning - Full Video Production")
        print("🎬 " * 20)
        
        steps = [
            ("dependencies", self.check_dependencies),
            ("render", self.render_scenes),
            ("narration", self.generate_narration),
            ("combine", self.combine_video_audio),
            ("validate", self.validate_output),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n❌ Pipeline failed at step: {step_name}")
                    return False
            except Exception as e:
                print(f"\n❌ Error in {step_name}: {e}")
                return False
        
        return True
    
    def print_final_summary(self):
        """Print final summary and next steps"""
        print("\n" + "="*70)
        print("✅ VIDEO PRODUCTION COMPLETE!")
        print("="*70)
        
        print("\n📹 Output Video:")
        print("   final_video_with_narration.mp4")
        
        print("\n📊 Video Specifications:")
        print("   • Duration: ~2-3 minutes")
        print("   • Resolution: 1080p @ 60 fps")
        print("   • Audio: Vietnamese (TTS)")
        print("   • Contains: 6 animated scenes + 5 formulas")
        
        print("\n🚀 Next Steps:")
        print("   1. Watch: Open final_video_with_narration.mp4")
        print("   2. Share: Upload to YouTube, TikTok, Instagram")
        print("   3. Customize: Edit scene.py for variations")
        
        print("\n📚 Reference Files:")
        print("   • NARRATION_SCRIPT.md - Full narration text")
        print("   • README.md - Detailed documentation")
        print("   • QUICK_START.md - Quick reference")
        
        print("\n" + "="*70)

def main():
    try:
        producer = VideoProducer()
        
        success = producer.run_full_pipeline()
        
        if success:
            producer.print_final_summary()
            print("\n🎉 Ready to share your video!")
            return 0
        else:
            print("\n❌ Production pipeline failed")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏸️  Production cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
