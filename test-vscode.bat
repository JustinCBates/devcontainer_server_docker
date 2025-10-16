@echo off
REM VS Code Integration Test
REM Tests the Python environment and VS Code debugging setup

echo Testing VS Code integration...
echo.

REM Try different Python executables
where python >nul 2>&1
if not errorlevel 1 (
    python test-vscode-integration.py
    goto :end
)

REM Try the standard user installation path
set PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" test-vscode-integration.py
    goto :end
)

REM Try Python launcher
where py >nul 2>&1
if not errorlevel 1 (
    py test-vscode-integration.py
    goto :end
)

echo ERROR: Python is not found. Please install Python or check your PATH.
pause
exit /b 1

:end
echo.
echo VS Code Integration Test Complete
pause