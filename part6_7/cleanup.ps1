#!/usr/bin/env powershell
# Cleanup Script - Remove all installed packages
# Created: May 19, 2026

Write-Host "===========================================" -ForegroundColor Yellow
Write-Host "  CLEANUP: Remove Installed Packages" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Yellow

$removedItems = @()

# 1. FFmpeg
Write-Host "`n[1/2] Removing FFmpeg..." -ForegroundColor Cyan
try {
    winget uninstall --id Gyan.FFmpeg -e --force 2>&1 | Out-Null
    $removedItems += "✓ FFmpeg 8.1.1"
    Write-Host "  ✓ FFmpeg removed" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ FFmpeg not found or already removed" -ForegroundColor Yellow
}

# 2. Python Packages
Write-Host "`n[2/2] Removing Python packages..." -ForegroundColor Cyan
$packages = @("edge-tts", "pydub", "manim")

foreach ($pkg in $packages) {
    try {
        $output = pip uninstall $pkg -y 2>&1
        if ($output -like "*Successfully uninstalled*") {
            $removedItems += "✓ $pkg"
            Write-Host "  ✓ $pkg removed" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ $pkg not found or already removed" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ⚠ Error with $pkg" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "`n===========================================" -ForegroundColor Green
Write-Host "  CLEANUP COMPLETE" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

Write-Host "`nRemoved items:" -ForegroundColor Cyan
foreach ($item in $removedItems) {
    Write-Host "  $item" -ForegroundColor White
}

Write-Host "`n📁 Kept files:" -ForegroundColor Cyan
Write-Host "  - d:\manim-object-video\ (all source files)" -ForegroundColor White
Write-Host "  - final_video_with_narration.mp4 (your video)" -ForegroundColor White
Write-Host "  - media/ folder (all video scenes)" -ForegroundColor White
Write-Host "  - narration/ folder (all MP3 files)" -ForegroundColor White

Write-Host "`n✅ System cleaned up!" -ForegroundColor Green
