@echo off
REM ==============================================================================
REM              VPS ENVIRONMENT LAUNCHER FOR WINDOWS
REM ==============================================================================
REM This is THE script to run from Windows PowerShell to start the VPS environment
REM Usage: .\START-WINDOWS.bat
REM ==============================================================================

title VPS Environment Launcher
color 0A

echo.
echo ================================================================
echo                VPS ENVIRONMENT LAUNCHER
echo                     Windows Version
echo ================================================================
echo.
echo Starting the interactive VPS environment launcher...
echo.

REM Check Python in standard user installation path first (avoids MS Store redirect)
set PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
if exist "%PYTHON_PATH%" (
    echo Found Python 3.12 installation
    "%PYTHON_PATH%" project\advanced-launcher.py %*
    goto :end
)

REM Try Python launcher
where py >nul 2>&1
if not errorlevel 1 (
    echo Using Python launcher (py)
    py project\advanced-launcher.py %*
    goto :end
)

REM Try system Python (last resort - may trigger MS Store)
where python >nul 2>&1
if not errorlevel 1 (
    echo Using system Python
    python project\advanced-launcher.py %*
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