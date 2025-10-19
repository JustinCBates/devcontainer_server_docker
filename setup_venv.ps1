# VPS Testing Environment - Python Virtual Environment Setup
# This script creates and configures a Python virtual environment for TUI integration

# Configuration
$venvPath = ".\.venv"
$tuiSourcePath = "..\TUI_Form_Designer"
$projectRequirements = @(
    "tui-form-designer>=1.0.0",
    "questionary>=2.0.0", 
    "pyyaml>=6.0",
    "pydantic>=2.0.0"
)

Write-Information "🐳 VPS Testing Environment - Virtual Environment Setup" -Tags Title
Write-Information "" -Tags Info

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Information "✅ Python found: $pythonVersion" -Tags Success
}
catch {
    Write-Error "❌ Python not found. Please install Python 3.8+ first."
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path $venvPath)) {
    Write-Information "🔧 Creating Python virtual environment..." -Tags Info
    python -m venv $venvPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Information "✅ Virtual environment created at: $venvPath" -Tags Success
    } else {
        Write-Error "❌ Failed to create virtual environment"
        exit 1
    }
} else {
    Write-Information "✅ Virtual environment already exists at: $venvPath" -Tags Success
}

# Activate virtual environment
Write-Information "🔌 Activating virtual environment..." -Tags Info
& "$venvPath\Scripts\Activate.ps1"

# Verify activation
if ($env:VIRTUAL_ENV) {
    Write-Information "✅ Virtual environment activated: $env:VIRTUAL_ENV" -Tags Success
} else {
    Write-Error "❌ Failed to activate virtual environment"
    exit 1
}

# Upgrade pip
Write-Information "⬆️ Upgrading pip..." -Tags Info
python -m pip install --upgrade pip

# Install TUI Form Designer in editable mode (development install)
Write-Information "📦 Installing TUI Form Designer in editable mode..." -Tags Info
if (Test-Path $tuiSourcePath) {
    # Install both engine and editor packages in editable mode
    python -m pip install -e "$tuiSourcePath\src\tui_form_engine"
    python -m pip install -e "$tuiSourcePath\src\tui_form_editor"
    Write-Information "✅ TUI Form Designer installed in editable mode" -Tags Success
} else {
    Write-Warning "⚠️ TUI Form Designer source not found at: $tuiSourcePath"
    Write-Information "Installing from PyPI instead..." -Tags Info
    python -m pip install tui-form-designer
}

# Install project requirements
Write-Information "📋 Installing TUI integration requirements..." -Tags Info
foreach ($requirement in $projectRequirements) {
    python -m pip install $requirement
}
Write-Information "✅ Requirements installed successfully" -Tags Success

# Verify TUI installation
Write-Information "🧪 Verifying TUI installation..." -Tags Info
$tuiTest = python -c "
try:
    from tui_form_designer import FlowEngine
    print('✅ TUI Form Designer import successful')
    engine = FlowEngine()
    print('✅ TUI FlowEngine initialization successful')
except ImportError as e:
    print(f'❌ TUI import failed: {e}')
except Exception as e:
    print(f'❌ TUI initialization failed: {e}')
"

Write-Information $tuiTest -Tags Info

# Show installed packages
Write-Information "📊 Installed packages:" -Tags Info
python -m pip list
Write-Information "`n🎉 Virtual environment setup complete!" -Tags Success
Write-Information "To activate in future sessions, run: .\.venv\Scripts\Activate.ps1" -Tags Info
Write-Information "To deactivate, run: deactivate" -Tags Info