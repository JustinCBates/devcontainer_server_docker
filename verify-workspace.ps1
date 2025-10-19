# Workspace Repository Verification Script
# This script verifies that all repositories are properly accessible from the workspace

Write-Information "🔍 Multi-Repository Workspace Verification" -Tags Title

Write-Information "`n📍 Current Location: $(Get-Location)" -Tags Info

function Show-RepoInfo {
    param(
        [string]$Path,
        [string]$Label
    )

    if (Test-Path $Path) {
        Write-Information "  ✅ $Label: accessible" -Tags Success
        $count = (Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Information "    📂 Files: $count" -Tags Info
        if (Test-Path (Join-Path $Path '.git')) {
            Write-Information "    🔧 Git repository: present" -Tags Info
        } else {
            Write-Information "    � Git repository: not present" -Tags Info
        }
    } else {
        Write-Warning "  ❌ $Label: not accessible"
    }
}

Write-Information "`n🐳 VPS Testing Environment (main repo):" -Tags Info
Show-RepoInfo -Path '.' -Label 'VPS Testing Environment'

Write-Information "`n🔧 WSL & Docker Manager:" -Tags Info
Show-RepoInfo -Path '..\wsl-and-docker-desktop-manager' -Label 'WSL & Docker Manager'

Write-Information "`n🎨 TUI Form Designer:" -Tags Info
Show-RepoInfo -Path '..\TUI_Form_Designer' -Label 'TUI Form Designer'

Write-Information "`n🎛️ Workspace Configuration:" -Tags Info
if (Test-Path 'multi-repo-workspace.code-workspace') {
    Write-Information "  ✅ Workspace file found" -Tags Success
    Write-Information "  📄 File: multi-repo-workspace.code-workspace" -Tags Info
} else {
    Write-Warning "  ❌ Workspace file missing"
}

Write-Information "`n🚀 To open the workspace:" -Tags Info
Write-Information "   1. Open VS Code" -Tags Info
Write-Information "   2. File → Open Workspace from File..." -Tags Info
Write-Information "   3. Select: multi-repo-workspace.code-workspace" -Tags Info
Write-Information "   4. All three repositories should appear in Explorer" -Tags Info

Write-Information "`n✅ Verification completed!" -Tags Success