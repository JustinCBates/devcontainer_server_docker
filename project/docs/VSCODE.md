# 🚀 VS Code Development Setup

This document explains how to use VS Code for developing and debugging the VPS Testing Environment.

## 📋 Prerequisites

1. **VS Code Extensions** (will be recommended automatically):
   - `ms-python.python` - Python language support
   - `ms-vscode.vscode-docker` - Docker integration
   - `redhat.vscode-yaml` - YAML language support
   - `ms-vscode.powershell` - PowerShell support

2. **Python 3.6+** installed and accessible
3. **Docker Desktop** running

## 🎮 Quick Start

### 1. Open Workspace
```bash
# Open the workspace file
code vps-environment.code-workspace
```

### 2. Run Configurations (F5 or Run > Start Debugging)

Available debug configurations:
- **🚀 Interactive VPS Launcher** - Full interactive mode
- **🧹 Launch Fresh Ubuntu** - Quick fresh Ubuntu container
- **💾 Launch Persistent Rocky Linux** - Persistent Rocky server
- **🔍 VPS Status Check** - Check all container status
- **🛑 Stop All VPS** - Stop all containers
- **📸 Create Ubuntu Snapshot** - Create snapshot for debugging
- **🔄 Upgrade Alpine Linux** - Test upgrade functionality
- **🐍 Debug Launcher** - Full debugging with breakpoints

### 3. Tasks (Ctrl+Shift+P > "Tasks: Run Task")

Available tasks:
- **🚀 Launch Interactive VPS Environment** - Interactive launcher
- **🔍 Check VPS Status** - Status check
- **🛑 Stop All VPS Containers** - Stop all
- **🧹 Quick Launch: Fresh Ubuntu** - Quick Ubuntu
- **💾 Quick Launch: Persistent Rocky Linux** - Quick Rocky
- **🐳 Build All Docker Images** - Build containers
- **🧼 Clean Docker Resources** - Clean up Docker
- **📚 Show Help** - Display help

## 🔧 Development Workflow

### Debugging Python Scripts
1. Set breakpoints in `advanced-launcher.py` or `manage-vps.py`
2. Select a debug configuration (F5)
3. Use VS Code's debugging features:
   - Step through code (F10, F11)
   - Inspect variables
   - Watch expressions
   - Call stack analysis

### Testing Changes
1. Use **🧪 VS Code Integration Test** task to verify setup
2. Test individual components with specific launch configs
3. Use breakpoints to debug complex logic

### Container Development
1. Use Docker extension to:
   - View running containers
   - Inspect container logs
   - Execute commands in containers
   - Build and manage images

## 📁 Workspace Structure

```
📁 .vscode/
├── 🚀 launch.json          # Debug configurations
├── ⚙️  settings.json        # Workspace settings  
├── 📋 tasks.json           # Task definitions
└── 🔌 extensions.json     # Recommended extensions

📁 Project Files
├── 🐍 advanced-launcher.py # Main launcher (set breakpoints here)
├── 🐍 manage-vps.py       # Management utilities
├── 🐍 test-vscode-integration.py # Integration test
├── 🪟 test-vscode.bat     # Test runner
└── 📖 VSCODE.md           # This file
```

## 🐛 Debugging Tips

### Common Breakpoint Locations
```python
# In advanced-launcher.py
def start_vps_environment():  # Line ~285 - Main function
def show_distributions():    # Line ~175 - Distribution display
def get_user_choice():      # Line ~245 - User input handling

# In manage-vps.py  
def show_status():          # Line ~35 - Status checking
def connect_to_vps():       # Line ~55 - SSH connection
```

### Debugging Variables
- `LINUX_FAMILIES` - Distribution configurations
- `args` - Command line arguments
- `success, output` - Command execution results
- Container names and ports

### Debugging Docker Commands
Set breakpoints in `run_command()` function to inspect:
- Docker command execution
- Command output and errors
- Container state changes

## 🚨 Troubleshooting

### Python Not Found
1. Check `.vscode/settings.json` has correct Python path
2. Install Python extension for VS Code
3. Select correct Python interpreter (Ctrl+Shift+P > "Python: Select Interpreter")

### Docker Issues
1. Ensure Docker Desktop is running
2. Check Docker extension is installed
3. Verify Docker commands work in terminal

### Debug Configuration Issues
1. Ensure you're in the workspace folder
2. Check `launch.json` syntax
3. Verify Python files exist and are accessible

## 💡 Pro Tips

1. **Use Integrated Terminal** - All commands run in VS Code terminal
2. **Watch Variables** - Add variables to Watch panel during debugging
3. **Conditional Breakpoints** - Right-click breakpoint for conditions
4. **Log Points** - Add log messages without stopping execution
5. **Multi-file Debugging** - Set breakpoints across multiple files

## 🎯 Example Debugging Session

1. Open `advanced-launcher.py`
2. Set breakpoint on line with `start_vps_environment()`
3. Press F5 and select "🚀 Interactive VPS Launcher"
4. Step through family selection logic
5. Inspect `LINUX_FAMILIES` variable
6. Continue to container startup
7. Monitor Docker command execution

Happy debugging! 🐛✨