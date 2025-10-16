# Workspace Repository Verification Script
# This script verifies that all repositories are properly accessible from the workspace

Write-Host "🔍 Multi-Repository Workspace Verification" -ForegroundColor Green

# Check current location
Write-Host "`n📍 Current Location: $(Get-Location)" -ForegroundColor Yellow

# Check main repository
Write-Host "`n🐳 VPS Testing Environment (main repo):" -ForegroundColor Cyan
if (Test-Path ".git") {
    Write-Host "  ✅ Git repository detected" -ForegroundColor Green
    Write-Host "  📂 Files: $(((Get-ChildItem -File).Count)) files, $(((Get-ChildItem -Directory).Count)) directories" -ForegroundColor White
} else {
    Write-Host "  ❌ No git repository found" -ForegroundColor Red
}

# Check WSL & Docker Manager
Write-Host "`n🔧 WSL & Docker Manager:" -ForegroundColor Cyan
if (Test-Path "../wsl-and-docker-desktop-manager") {
    Write-Host "  ✅ Repository accessible" -ForegroundColor Green
    $wslFiles = Get-ChildItem "../wsl-and-docker-desktop-manager" -File | Measure-Object
    Write-Host "  📂 Files: $($wslFiles.Count) files" -ForegroundColor White
    if (Test-Path "../wsl-and-docker-desktop-manager/.git") {
        Write-Host "  ✅ Git repository detected" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ Repository not accessible" -ForegroundColor Red
}

# Check TUI Form Designer  
Write-Host "`n🎨 TUI Form Designer:" -ForegroundColor Cyan
if (Test-Path "../TUI_Form_Designer") {
    Write-Host "  ✅ Repository accessible" -ForegroundColor Green
    $tuiFiles = Get-ChildItem "../TUI_Form_Designer" -File | Measure-Object
    Write-Host "  📂 Files: $($tuiFiles.Count) files" -ForegroundColor White
    if (Test-Path "../TUI_Form_Designer/.git") {
        Write-Host "  ✅ Git repository detected" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ Repository not accessible" -ForegroundColor Red
}

# Check workspace file
Write-Host "`n🎛️ Workspace Configuration:" -ForegroundColor Cyan
if (Test-Path "multi-repo-workspace.code-workspace") {
    Write-Host "  ✅ Workspace file found" -ForegroundColor Green
    Write-Host "  📄 File: multi-repo-workspace.code-workspace" -ForegroundColor White
} else {
    Write-Host "  ❌ Workspace file missing" -ForegroundColor Red
}

Write-Host "`n🚀 To open the workspace:" -ForegroundColor Green
Write-Host "   1. Open VS Code" -ForegroundColor White
Write-Host "   2. File → Open Workspace from File..." -ForegroundColor White
Write-Host "   3. Select: multi-repo-workspace.code-workspace" -ForegroundColor White
Write-Host "   4. All three repositories should appear in Explorer" -ForegroundColor White

Write-Host "`n✅ Verification completed!" -ForegroundColor Green