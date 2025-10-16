#!/usr/bin/env python3
"""
Python Interpreter Discovery Script
Helps VS Code find the correct Python interpreter
"""

import sys
import os
import subprocess
import json

def find_python_executables():
    """Find all available Python executables"""
    python_paths = []
    
    # Common Python installation paths on Windows
    common_paths = [
        os.path.expanduser("~/AppData/Local/Programs/Python/Python312/python.exe"),
        os.path.expanduser("~/AppData/Local/Programs/Python/Python311/python.exe"),
        os.path.expanduser("~/AppData/Local/Programs/Python/Python310/python.exe"),
        "C:/Python312/python.exe",
        "C:/Python311/python.exe", 
        "C:/Python310/python.exe",
    ]
    
    # Check common paths
    for path in common_paths:
        if os.path.exists(path):
            python_paths.append(path)
    
    # Try to find python in PATH
    try:
        result = subprocess.run(['where', 'python'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line and os.path.exists(line):
                    python_paths.append(line.strip())
    except:
        pass
    
    # Try py launcher
    try:
        result = subprocess.run(['where', 'py'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line and os.path.exists(line):
                    python_paths.append(line.strip())
    except:
        pass
    
    return list(set(python_paths))  # Remove duplicates

def get_python_info(python_path):
    """Get information about a Python installation"""
    try:
        result = subprocess.run([python_path, '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            return {
                "path": python_path,
                "version": version,
                "available": True
            }
    except:
        pass
    
    return {
        "path": python_path,
        "version": "Unknown",
        "available": False
    }

def create_vscode_settings():
    """Create VS Code settings with the best Python interpreter"""
    python_paths = find_python_executables()
    
    if not python_paths:
        print("❌ No Python installations found!")
        return False
    
    # Filter out Windows Store Python and select the best one
    working_pythons = []
    for path in python_paths:
        info = get_python_info(path)
        # Skip Windows Store Python (usually doesn't work properly)
        if "WindowsApps" not in path and info["available"]:
            working_pythons.append(path)
    
    if not working_pythons:
        print("❌ No working Python installations found!")
        return False
    
    # Use the first working Python
    best_python = working_pythons[0]
    
    print(f"🐍 Found Python installations:")
    for path in python_paths:
        info = get_python_info(path)
        status = "✅" if info["available"] and "WindowsApps" not in path else "❌"
        note = " (Windows Store - skipped)" if "WindowsApps" in path else ""
        print(f"  {status} {info['version']} - {info['path']}{note}")
    
    print(f"\n🎯 Selected: {best_python}")
    
    # Update .vscode/settings.json
    settings_path = ".vscode/settings.json"
    settings = {}
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        except:
            pass
    
    # Update Python path (use forward slashes for JSON)
    python_path_json = best_python.replace("\\", "/")
    settings["python.defaultInterpreterPath"] = python_path_json
    settings["python.pythonPath"] = python_path_json
    
    # Write back
    try:
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        print(f"✅ Updated {settings_path} with Python interpreter: {python_path_json}")
        return True
    except Exception as e:
        print(f"❌ Failed to update settings: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Python Interpreter Discovery for VS Code")
    print("=" * 50)
    
    # Check current Python
    print(f"Current Python: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print()
    
    # Find and configure best Python
    if create_vscode_settings():
        print("\n🎉 VS Code Python configuration updated!")
        print("   Restart VS Code and try debugging again (F5)")
    else:
        print("\n❌ Failed to configure VS Code")
        print("   Please manually set Python interpreter in VS Code:")
        print("   Ctrl+Shift+P > 'Python: Select Interpreter'")

if __name__ == "__main__":
    main()