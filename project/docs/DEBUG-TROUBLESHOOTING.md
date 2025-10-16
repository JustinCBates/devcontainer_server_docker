# 🔧 VS Code Debugging Troubleshooting Guide

If the VS Code Run and Debug (F5) isn't working, follow these steps to fix it:

## 🐍 Step 1: Check Python Extension

1. **Install Python Extension**:
   - Press `Ctrl+Shift+X` to open Extensions
   - Search for "Python" by Microsoft
   - Install the official Python extension
   - **Also install "Python Debugger"** extension

2. **Verify Extension is Active**:
   - Open any `.py` file
   - Check bottom-left status bar shows Python version
   - If not, the extension isn't loaded properly

## 🎯 Step 2: Select Python Interpreter

1. **Manual Selection**:
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter" 
   - Choose the Python 3.12 installation (NOT Windows Store version)
   - Should be: `C:\Users\{username}\AppData\Local\Programs\Python\Python312\python.exe`

2. **Automatic Fix**:
   ```cmd
   python fix-python-vscode.py
   ```

## 🔍 Step 3: Verify Configuration

1. **Check launch.json**:
   - Open `.vscode/launch.json`
   - Verify `"type": "debugpy"` (not "python")
   - Check `"program": "${workspaceFolder}/advanced-launcher.py"`

2. **Test Simple Debug**:
   - Open `debug-test.py`
   - Set a breakpoint (click left margin, red dot appears)
   - Press `F5` and select "🐛 Simple Debug Test"
   - Should stop at breakpoint

## 🚨 Step 4: Common Issues & Solutions

### Issue: "No configurations found"
**Solution**: 
- Make sure you're in the project root folder
- Open the workspace: `File > Open Workspace > vps-environment.code-workspace`

### Issue: "Python not found"
**Solution**:
```powershell
# Find Python installation
where python
# Or use our fix script
python fix-python-vscode.py
```

### Issue: Debug console shows nothing
**Solution**:
- Check `"console": "integratedTerminal"` in launch.json
- Try changing to `"console": "internalConsole"`

### Issue: Breakpoints not hit
**Solution**:
- Ensure `"justMyCode": true` in launch.json
- Check Python file has no syntax errors
- Verify breakpoint is on executable line (not comments/empty lines)

## 🧪 Step 5: Test Debug Configurations

Try these debug configurations in order:

1. **🐛 Simple Debug Test** - Basic Python debugging
2. **🧪 Test VS Code Integration** - Environment validation  
3. **📚 Show Launcher Help** - Test launcher with --help
4. **🚀 Launch VPS Environment (Interactive)** - Full launcher

## 💡 Step 6: Advanced Troubleshooting

### Enable Debug Logging
Add to `.vscode/settings.json`:
```json
{
    "python.logging.level": "debug",
    "debug.allowBreakpointsEverywhere": true,
    "debug.showBreakpointsInOverviewRuler": true
}
```

### Manual Launch Test
```powershell
# Test Python directly
python --version
python advanced-launcher.py --help
python debug-test.py
```

### Reset VS Code Python
1. Press `Ctrl+Shift+P`
2. Type "Python: Clear Cache and Reload Window"
3. Select and restart VS Code

## 🎯 Quick Fix Commands

```cmd
# Fix Python configuration
python fix-python-vscode.py

# Test environment
python test-vscode-integration.py

# Simple debug test
python debug-test.py

# Test launcher
python advanced-launcher.py --help
```

## ✅ Success Checklist

- [ ] Python extension installed and active
- [ ] Correct Python interpreter selected (not Windows Store)  
- [ ] launch.json uses `"type": "debugpy"`
- [ ] Can set breakpoints (red dots appear)
- [ ] Simple debug test works with F5
- [ ] Integrated terminal shows output
- [ ] Can step through code (F10, F11)

## 🆘 Still Not Working?

1. **Restart VS Code** completely
2. **Open workspace file**: `vps-environment.code-workspace`
3. **Try different debug configuration**: Start with "🐛 Simple Debug Test"
4. **Check VS Code output**: `View > Output > Python`
5. **Reinstall Python extension** if needed

Once debugging works, you'll be able to:
- Set breakpoints in `advanced-launcher.py`
- Inspect variables like `LINUX_FAMILIES`
- Step through the VPS selection logic
- Debug Docker command execution
- Monitor container startup process

Happy debugging! 🐛✨