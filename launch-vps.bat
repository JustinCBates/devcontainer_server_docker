@echo off
REM Advanced VPS Environment Launcher (Python version)
REM This batch file runs the Python-based advanced launcher

echo Starting Advanced VPS Environment Launcher (Python)...
echo.

REM Check if Python is available (try different common locations)
where python >nul 2>&1
if not errorlevel 1 (
    python advanced-launcher.py %*
    goto :end
)

REM Try the standard user installation path
set PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" advanced-launcher.py %*
    goto :end
)

REM Try Python launcher
where py >nul 2>&1
if not errorlevel 1 (
    py advanced-launcher.py %*
    goto :end
)

echo ERROR: Python is not installed or not found
echo Please install Python 3.6+ from https://python.org
echo Or run: winget install Python.Python.3.12
pause
exit /b 1

:end
pause