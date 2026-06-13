#!/usr/bin/env powershell
# Automatic Full Pipeline: Render (Docker) + Narration + Combine
# Run: .\auto_all.ps1

Write-Host "===========================================" -ForegroundColor Green
Write-Host "  AUTOMATIC VIDEO PRODUCTION PIPELINE" -ForegroundColor Green
Write-Host "  Render (Docker) -> Narration -> Combine" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

$ErrorActionPreference = 'Stop'

# Scenes to render
$scenes = @(
    'SlotAttentionIntro',
    'PixelsToObjects',
    'SlotAttentionMechanism',
    'AlphaChannelBlending',
    'CausalIntervention',
    'EndingScene'
)

# ====== STEP 1: RENDER ALL SCENES WITH DOCKER ======
Write-Host "`n[1/3] RENDERING 6 VIDEO SCENES WITH DOCKER..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

foreach ($i in 0..($scenes.Count - 1)) {
    $scene = $scenes[$i]
    $current = $i + 1
    $total = $scenes.Count
    
    Write-Host "`n[$current/$total] Rendering: $scene" -ForegroundColor Yellow
    
    $cmd = "docker run --rm -it -v `"${PWD}:/manim`" manimcommunity/manim manim -ql scene.py $scene"
    
    try {
        Invoke-Expression $cmd
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to render $scene" -ForegroundColor Red
            exit 1
        }
        Write-Host "[OK] $scene rendered successfully" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Exception rendering $scene" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n[SUCCESS] All 6 scenes rendered!" -ForegroundColor Green

# ====== STEP 2: GENERATE VIETNAMESE NARRATION ======
Write-Host "`n[2/3] GENERATING VIETNAMESE NARRATION (TTS)..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`nThis will create 6 MP3 files with TTS narration..."
python generate_narration.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to generate narration" -ForegroundColor Red
    exit 1
}

Write-Host "[SUCCESS] Narration generated!" -ForegroundColor Green

# ====== STEP 3: COMBINE VIDEO + AUDIO ======
Write-Host "`n[3/3] COMBINING VIDEO + AUDIO..." -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

Write-Host "`nThis will merge all videos and audio into one file..."
python combine_video_audio.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to combine video and audio" -ForegroundColor Red
    exit 1
}

Write-Host "[SUCCESS] Video + audio combined!" -ForegroundColor Green

# ====== VERIFY OUTPUT ======
Write-Host "`n[4/4] VERIFYING OUTPUT..." -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

if (Test-Path "final_video_with_narration.mp4") {
    $fileSize = (Get-Item "final_video_with_narration.mp4").Length / 1MB
    Write-Host "`n[SUCCESS] Output file created!" -ForegroundColor Green
    Write-Host "  File: final_video_with_narration.mp4" -ForegroundColor White
    Write-Host "  Size: $($fileSize.ToString('F2')) MB" -ForegroundColor White
} else {
    Write-Host "[ERROR] Output file not found!" -ForegroundColor Red
    exit 1
}

# ====== FINAL SUMMARY ======
Write-Host "`n===========================================" -ForegroundColor Green
Write-Host "  PIPELINE COMPLETE!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

Write-Host "`nGenerated video:" -ForegroundColor Cyan
Write-Host "  -> final_video_with_narration.mp4" -ForegroundColor Yellow

Write-Host "`nVideo contains:" -ForegroundColor Cyan
Write-Host "  * 6 animated scenes (2-3 minutes)" -ForegroundColor White
Write-Host "  * Vietnamese narration (TTS)" -ForegroundColor White
Write-Host "  * Mathematical formulas" -ForegroundColor White
Write-Host "  * Ready for YouTube/TikTok" -ForegroundColor White

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Watch the video" -ForegroundColor White
Write-Host "  2. Share on social media" -ForegroundColor White

Write-Host "`n" -ForegroundColor White
