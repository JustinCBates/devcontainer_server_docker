@echo off
REM VPS Docker Images Rebuild Script (Batch Version)
REM Rebuilds all 5 VPS images with time estimates
REM Author: Generated for VPS Testing Environment
REM Date: October 19, 2025

echo.
echo ================================
echo  VPS Docker Images Rebuild
echo ================================
echo.

REM Change to project directory
cd /d "%~dp0"

echo [INFO] Working Directory: %CD%
echo [INFO] Estimated Total Time: 15-20 minutes
echo.

REM List planned builds
echo [QUEUE] Build Order:
echo   1. Alpine Linux 3.18 (2-3 min)
echo   2. Rocky Linux 9 (1.5-2 min)  
echo   3. CentOS Stream 9 (4-5 min)
echo   4. Ubuntu 22.04 LTS (3-4 min)
echo   5. Debian 12 Bookworm (3-4 min)
echo.

REM Confirmation
set /p "confirm=Continue with rebuild? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo [CANCELLED] Rebuild cancelled by user
    pause
    exit /b 0
)

echo.
echo [START] Beginning VPS rebuild at %TIME%
echo ========================================

REM Initialize counters
set success_count=0
set failure_count=0
set start_time=%TIME%

REM Build 1: Alpine Linux (fastest first)
echo.
echo [1/5] Building Alpine Linux VPS (ETA: 2-3 minutes)...
echo Time Started: %TIME%
docker build -t alpine-vps:latest -f distros/alpine/Dockerfile distros/alpine/
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Alpine Linux build completed
    set /a success_count+=1
) else (
    echo [FAILED] Alpine Linux build failed
    set /a failure_count+=1
)

REM Build 2: Rocky Linux  
echo.
echo [2/5] Building Rocky Linux VPS (ETA: 1.5-2 minutes)...
echo Time Started: %TIME%
docker build -t rocky-vps:latest -f distros/rocky/Dockerfile distros/rocky/
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Rocky Linux build completed
    set /a success_count+=1
) else (
    echo [FAILED] Rocky Linux build failed
    set /a failure_count+=1
)

REM Build 3: CentOS Stream
echo.
echo [3/5] Building CentOS Stream VPS (ETA: 4-5 minutes)...
echo Time Started: %TIME%
docker build -t centos-vps:latest -f distros/centos/Dockerfile distros/centos/
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] CentOS Stream build completed
    set /a success_count+=1
) else (
    echo [FAILED] CentOS Stream build failed
    set /a failure_count+=1
)

REM Build 4: Ubuntu
echo.
echo [4/5] Building Ubuntu VPS (ETA: 3-4 minutes)...
echo Time Started: %TIME%
docker build -t ubuntu-vps:latest -f distros/ubuntu/Dockerfile distros/ubuntu/
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Ubuntu build completed
    set /a success_count+=1
) else (
    echo [FAILED] Ubuntu build failed  
    set /a failure_count+=1
)

REM Build 5: Debian
echo.
echo [5/5] Building Debian VPS (ETA: 3-4 minutes)...
echo Time Started: %TIME%
docker build -t debian-vps:latest -f distros/debian/Dockerfile distros/debian/
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Debian build completed
    set /a success_count+=1
) else (
    echo [FAILED] Debian build failed
    set /a failure_count+=1
)

REM Final Summary
echo.
echo ========================================
echo            REBUILD SUMMARY
echo ========================================
echo Start Time: %start_time%
echo End Time:   %TIME%
echo.
echo Successful Builds: %success_count%
echo Failed Builds:     %failure_count%
echo.

REM Show built images
echo Built VPS Images:
docker images --filter reference="*-vps:latest" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo.
if %failure_count% EQU 0 (
    echo [SUCCESS] All VPS images rebuilt successfully!
    echo.
    echo Next Steps:
    echo - Test VPS connectivity with: ssh -p 2202 vpsuser@localhost
    echo - Run containers with: docker run -d --name test-vps -p 2202:22 debian-vps:latest
    echo - Check documentation: docs\VPS-TESTING-COMMANDS.md
) else (
    echo [WARNING] Some builds failed. Check the output above for details.
    echo.
    echo Troubleshooting:
    echo - Ensure Docker Desktop is running
    echo - Check available disk space
    echo - Try rebuilding individual images manually
)

echo.
pause