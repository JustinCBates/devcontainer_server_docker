@echo off
REM ==============================================================================
REM              DOCKER IMAGE TESTING FOR WINDOWS
REM ==============================================================================
REM This script tests that Docker images are properly built and functional
REM Usage: .\TEST-DOCKER.bat
REM ==============================================================================

title Docker Image Testing
color 0B

echo.
echo ================================================================
echo                DOCKER IMAGE TESTING
echo                     Windows Version
echo ================================================================
echo.
echo Testing Docker images for VPS environments...
echo.

REM Check Python in standard user installation path first
set PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
if exist "%PYTHON_PATH%" (
    echo Found Python 3.12 installation
    "%PYTHON_PATH%" project\test-docker-images.py %*
    goto :end
)

REM Try Python launcher
where py >nul 2>&1
if not errorlevel 1 (
    echo Using Python launcher (py)
    py project\test-docker-images.py %*
    goto :end
)

REM Try system Python (last resort)
where python >nul 2>&1
if not errorlevel 1 (
    echo Using system Python
    python project\test-docker-images.py %*
    goto :end
)

echo ERROR: Python is not installed or not found in PATH
echo.
echo Please install Python 3.6+ from one of these methods:
echo   1. Run: winget install Python.Python.3.12
echo   2. Download from: https://python.org
echo   3. Install from Microsoft Store
echo.
pause
exit /b 1

:end
echo.
echo Press any key to exit...
pause >nul