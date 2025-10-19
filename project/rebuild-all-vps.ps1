# VPS Docker Images Rebuild Script
# Rebuilds all 5 VPS images with progress tracking and time estimates
# Author: Generated for VPS Testing Environment
# Date: October 19, 2025

param(
    [switch]$Force,           # Force rebuild without confirmation
    [switch]$CleanFirst,      # Remove existing images before rebuild
    [switch]$SkipTests,       # Skip post-build testing
    [string[]]$Only = @()     # Build only specific distributions
)

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Progress { param($Message) Write-Host $Message -ForegroundColor Magenta }

# VPS Build Configuration
$VPSBuilds = @(
    @{
        Name = "Alpine Linux 3.18"
        Tag = "alpine-vps:latest"
        Directory = "distros/alpine"
        Port = 2205
        EstimatedTime = "2-3 minutes"
        TimeoutMinutes = 5
        Priority = 1  # Build fastest first
    },
    @{
        Name = "Rocky Linux 9"
        Tag = "rocky-vps:latest" 
        Directory = "distros/rocky"
        Port = 2206
        EstimatedTime = "1.5-2 minutes"
        TimeoutMinutes = 4
        Priority = 2
    },
    @{
        Name = "CentOS Stream 9"
        Tag = "centos-vps:latest"
        Directory = "distros/centos" 
        Port = 2204
        EstimatedTime = "4-5 minutes"
        TimeoutMinutes = 8
        Priority = 3
    },
    @{
        Name = "Ubuntu 22.04 LTS"
        Tag = "ubuntu-vps:latest"
        Directory = "distros/ubuntu"
        Port = 2203
        EstimatedTime = "3-4 minutes" 
        TimeoutMinutes = 7
        Priority = 4
    },
    @{
        Name = "Debian 12 Bookworm"
        Tag = "debian-vps:latest"
        Directory = "distros/debian"
        Port = 2202
        EstimatedTime = "3-4 minutes"
        TimeoutMinutes = 7
        Priority = 5
    }
)

# Sort by priority (fastest first)
$VPSBuilds = $VPSBuilds | Sort-Object Priority

# Filter builds if specific distributions requested
if ($Only.Count -gt 0) {
    $VPSBuilds = $VPSBuilds | Where-Object { 
        $_.Name -match ($Only -join '|') -or 
        $_.Tag -match ($Only -join '|') -or
        $_.Directory -match ($Only -join '|')
    }
    Write-Info "🎯 Building only selected distributions: $($Only -join ', ')"
}

# Display build summary
Write-Host "`n🚀 VPS Docker Images Rebuild Script" -ForegroundColor Blue -BackgroundColor White
Write-Host "=" * 50
Write-Info "📋 Planned Builds: $($VPSBuilds.Count) distributions"
Write-Info "⏱️  Total Estimated Time: $(($VPSBuilds | Measure-Object -Property TimeoutMinutes -Sum).Sum) minutes maximum"
Write-Info "📁 Working Directory: $(Get-Location)"

# Show build queue
Write-Host "`n📋 Build Queue:" -ForegroundColor Yellow
foreach ($build in $VPSBuilds) {
    Write-Host "  $($build.Priority). $($build.Name) ($($build.EstimatedTime))" -ForegroundColor White
}

# Confirmation unless -Force is used
if (-not $Force) {
    Write-Host "`n❓ Continue with rebuild? (y/N): " -NoNewline -ForegroundColor Yellow
    $confirm = Read-Host
    if ($confirm -notmatch '^[Yy]') {
        Write-Warning "❌ Rebuild cancelled by user"
        exit 0
    }
}

# Initialize tracking variables
$StartTime = Get-Date
$BuildResults = @()
$SuccessCount = 0
$FailureCount = 0

Write-Success "`n🏁 Starting VPS rebuild process..."
Write-Info "Start Time: $($StartTime.ToString('HH:mm:ss'))"

# Clean existing images if requested
if ($CleanFirst) {
    Write-Progress "`n🧹 Cleaning existing VPS images..."
    foreach ($build in $VPSBuilds) {
        $existingImage = docker images -q $build.Tag
        if ($existingImage) {
            Write-Info "  Removing $($build.Tag)..."
            docker rmi $build.Tag -f 2>$null
        }
    }
    Write-Success "✅ Cleanup complete"
}

# Build each VPS image
foreach ($build in $VPSBuilds) {
    $buildStart = Get-Date
    $buildNumber = $VPSBuilds.IndexOf($build) + 1
    
    Write-Host "`n" + ("=" * 60) -ForegroundColor Blue
    Write-Progress "🔨 Building $buildNumber/$($VPSBuilds.Count): $($build.Name)"
    Write-Info "📁 Directory: $($build.Directory)"  
    Write-Info "🏷️  Tag: $($build.Tag)"
    Write-Info "⏱️  Estimated Time: $($build.EstimatedTime)"
    Write-Info "⏰ Build Started: $($buildStart.ToString('HH:mm:ss'))"
    Write-Host ("-" * 40) -ForegroundColor Gray

    # Check if Dockerfile exists
    $dockerfilePath = Join-Path $build.Directory "Dockerfile"
    if (-not (Test-Path $dockerfilePath)) {
        Write-Error "❌ Dockerfile not found: $dockerfilePath"
        $BuildResults += @{
            Name = $build.Name
            Status = "FAILED"
            Error = "Dockerfile not found"
            Duration = "0s"
        }
        $FailureCount++
        continue
    }

    # Build with timeout
    try {
        Write-Progress "Building Docker image (timeout: $($build.TimeoutMinutes) minutes)..."
        
        # Start build process
        $buildJob = Start-Job -ScriptBlock {
            param($tag, $directory)
            docker build -t $tag -f "$directory/Dockerfile" $directory
            return $LASTEXITCODE
        } -ArgumentList $build.Tag, $build.Directory

        # Wait for completion or timeout
        $completed = $buildJob | Wait-Job -Timeout ($build.TimeoutMinutes * 60)
        
        if ($completed) {
            $exitCode = Receive-Job $buildJob
            Remove-Job $buildJob
            
            if ($exitCode -eq 0) {
                $buildEnd = Get-Date
                $duration = $buildEnd - $buildStart
                Write-Success "✅ Build completed successfully!"
                Write-Info "⏱️  Actual Time: $($duration.ToString('mm\:ss'))"
                
                # Get image size
                $imageSize = (docker images $build.Tag --format "{{.Size}}") 2>$null
                if ($imageSize) {
                    Write-Info "📦 Image Size: $imageSize"
                }
                
                $BuildResults += @{
                    Name = $build.Name
                    Status = "SUCCESS" 
                    Duration = $duration.ToString('mm\:ss')
                    Size = $imageSize
                }
                $SuccessCount++
            } else {
                Write-Error "❌ Build failed with exit code: $exitCode"
                $BuildResults += @{
                    Name = $build.Name
                    Status = "FAILED"
                    Error = "Build exit code: $exitCode"
                    Duration = (Get-Date) - $buildStart | ForEach-Object { $_.ToString('mm\:ss') }
                }
                $FailureCount++
            }
        } else {
            Write-Error "⏰ Build timed out after $($build.TimeoutMinutes) minutes"
            $buildJob | Stop-Job
            Remove-Job $buildJob
            $BuildResults += @{
                Name = $build.Name
                Status = "TIMEOUT"
                Error = "Build exceeded $($build.TimeoutMinutes) minute timeout"
                Duration = "$($build.TimeoutMinutes):00"
            }
            $FailureCount++
        }
    }
    catch {
        Write-Error "❌ Build error: $($_.Exception.Message)"
        $BuildResults += @{
            Name = $build.Name
            Status = "ERROR"
            Error = $_.Exception.Message
            Duration = (Get-Date) - $buildStart | ForEach-Object { $_.ToString('mm\:ss') }
        }
        $FailureCount++
    }

    # Show progress
    $elapsed = (Get-Date) - $StartTime
    Write-Info "📊 Progress: $buildNumber/$($VPSBuilds.Count) complete (Elapsed: $($elapsed.ToString('mm\:ss')))"
}

# Final summary
$EndTime = Get-Date
$TotalDuration = $EndTime - $StartTime

Write-Host "`n" + ("=" * 60) -ForegroundColor Blue
Write-Host "📊 REBUILD SUMMARY" -ForegroundColor Blue -BackgroundColor White
Write-Host ("=" * 60) -ForegroundColor Blue

Write-Info "⏱️  Total Duration: $($TotalDuration.ToString('mm\:ss'))"
Write-Info "🏁 Completed: $($StartTime.ToString('HH:mm:ss')) - $($EndTime.ToString('HH:mm:ss'))"
Write-Success "✅ Successful Builds: $SuccessCount"
if ($FailureCount -gt 0) {
    Write-Error "❌ Failed Builds: $FailureCount"
}

# Detailed results table
Write-Host "`n📋 Detailed Results:" -ForegroundColor Yellow
Write-Host ("-" * 80) -ForegroundColor Gray
Write-Host ("{0,-25} {1,-10} {2,-10} {3,-15}" -f "Distribution", "Status", "Duration", "Size") -ForegroundColor White
Write-Host ("-" * 80) -ForegroundColor Gray

foreach ($result in $BuildResults) {
    $statusColor = switch ($result.Status) {
        "SUCCESS" { "Green" }
        "FAILED" { "Red" }
        "TIMEOUT" { "Yellow" }
        "ERROR" { "Magenta" }
        default { "White" }
    }
    
    $line = "{0,-25} {1,-10} {2,-10} {3,-15}" -f $result.Name, $result.Status, $result.Duration, $result.Size
    Write-Host $line -ForegroundColor $statusColor
}

# Post-build testing if not skipped
if (-not $SkipTests -and $SuccessCount -gt 0) {
    Write-Host "`n🧪 Running post-build tests..." -ForegroundColor Yellow
    
    Write-Info "Checking built images..."
    docker images --filter reference="*-vps:latest" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    Write-Info "`nTesting image functionality..."
    foreach ($result in $BuildResults | Where-Object { $_.Status -eq "SUCCESS" }) {
        $build = $VPSBuilds | Where-Object { $_.Name -eq $result.Name }
        Write-Host "  Testing $($build.Tag)..." -NoNewline
        
        # Quick container test
        $testContainer = "test-$($build.Tag -replace ':.*')-$(Get-Random)"
        try {
            docker run -d --name $testContainer $build.Tag > $null
            Start-Sleep 2
            $containerStatus = docker inspect $testContainer --format "{{.State.Status}}" 2>$null
            docker rm -f $testContainer > $null 2>&1
            
            if ($containerStatus -eq "running") {
                Write-Host " ✅" -ForegroundColor Green
            } else {
                Write-Host " ❌" -ForegroundColor Red
            }
        }
        catch {
            Write-Host " ❌" -ForegroundColor Red
        }
    }
}

# Recommendations
if ($FailureCount -gt 0) {
    Write-Host "`n💡 Recommendations:" -ForegroundColor Yellow
    Write-Info "• Check failed build logs above for specific errors"
    Write-Info "• Try rebuilding individual distributions with: .\rebuild-all-vps.ps1 -Only 'DistributionName'"
    Write-Info "• Use -CleanFirst flag to remove cached layers"
    Write-Info "• Check Docker Desktop has sufficient resources allocated"
}

# Exit with appropriate code
if ($FailureCount -eq 0) {
    Write-Success "`n🎉 All VPS images rebuilt successfully!"
    exit 0
} else {
    Write-Warning "`n⚠️  Some builds failed. Check logs above for details."
    exit 1
}