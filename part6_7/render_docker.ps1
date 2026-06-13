#!/usr/bin/env powershell
<#
Docker Manim Renderer - Render all scenes using Docker
Run: .\render_docker.ps1
#>

param(
    [ValidateSet('l', 'm', 'h')]
    [string]$Quality = 'l',
    
    [switch]$NoPreview,
    [switch]$OnlyOneScene,
    [string]$SceneName = 'SlotAttentionIntro'
)

$ErrorActionPreference = 'Stop'

$scenes = @(
    'SlotAttentionIntro',
    'PixelsToObjects',
    'SlotAttentionMechanism',
    'AlphaChannelBlending',
    'CausalIntervention',
    'EndingScene'
)

# Translate quality flag
$qualityName = @{'l'='Low (480p15)'; 'm'='Medium (720p30)'; 'h'='High (1080p60)'}[$Quality]

# Build flags (no preview in Docker - no GUI environment)
$flags = "q$Quality"

Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Docker Manim Renderer - Object-Centric Learning  ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host "`n⚙️  Settings:" -ForegroundColor Yellow
Write-Host "  Quality: $qualityName"
Write-Host "  Preview: Disabled (Docker has no GUI)"
Write-Host "  Flags: -$flags`n"

# Check if Docker is installed
Write-Host "🐳 Checking Docker..." -ForegroundColor Cyan
try {
    docker --version | Out-Null
    Write-Host "✓ Docker is available`n"
} catch {
    Write-Host "❌ Docker not found. Install from https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# Pull latest image
Write-Host "📥 Pulling latest Manim Docker image..." -ForegroundColor Cyan
docker pull manimcommunity/manim
Write-Host ""

# Render scenes
if ($OnlyOneScene) {
    $scenes = @($SceneName)
}

$successCount = 0
$failCount = 0

foreach ($i in 0..($scenes.Count - 1)) {
    $scene = $scenes[$i]
    $current = $i + 1
    $total = $scenes.Count
    
    Write-Host "┌─────────────────────────────────────────────────────┐" -ForegroundColor Green
    Write-Host "│ [$current/$total] Rendering: $scene" -ForegroundColor Green
    Write-Host "└─────────────────────────────────────────────────────┘" -ForegroundColor Green
    Write-Host ""
    
    $cmd = "docker run --rm -it `
      -v `"${PWD}:/manim`" `
      manimcommunity/manim `
      manim -$flags scene.py $scene"
    
    try {
        Invoke-Expression $cmd
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ $scene rendered successfully`n" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "✗ Error rendering $scene (exit code: $LASTEXITCODE)`n" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host "✗ Exception rendering $scene: $_`n" -ForegroundColor Red
        $failCount++
    }
}

# Summary
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    Render Complete                   ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host "`n📊 Results:" -ForegroundColor Yellow
Write-Host "  ✓ Success: $successCount" -ForegroundColor Green
Write-Host "  ✗ Failed:  $failCount" -ForegroundColor Red

if ($failCount -eq 0) {
    Write-Host "`n✅ All scenes rendered successfully!" -ForegroundColor Green
    Write-Host "`n📂 Output location:"
    Write-Host "   media/videos/480p15/ObjectCentricLearning/"
    Write-Host "`n🎬 Next steps:"
    Write-Host "   1. python generate_narration.py"
    Write-Host "   2. python combine_video_audio.py"
    exit 0
} else {
    Write-Host "`n❌ Some renders failed" -ForegroundColor Red
    exit 1
}
