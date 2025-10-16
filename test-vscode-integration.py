#!/usr/bin/env python3
"""
VS Code Integration Test Script
Test script to verify debugging and launch configurations work properly
"""

import sys
import os
import subprocess
from typing import List

def test_python_environment():
    """Test if Python environment is working correctly"""
    print("🐍 Testing Python Environment...")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Working Directory: {os.getcwd()}")
    print("✅ Python environment test passed!")
    print()

def test_docker_availability():
    """Test if Docker is available"""
    print("🐳 Testing Docker Availability...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Docker Version: {result.stdout.strip()}")
            print("✅ Docker test passed!")
        else:
            print("❌ Docker not available")
    except FileNotFoundError:
        print("❌ Docker command not found")
    print()

def test_file_accessibility():
    """Test if launcher files are accessible"""
    print("📁 Testing File Accessibility...")
    files_to_check = [
        "advanced-launcher.py",
        "manage-vps.py", 
        "docker-compose.yml",
        "requirements.txt"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Found")
        else:
            print(f"❌ {file_path} - Missing")
    print()

def test_import_modules():
    """Test if required modules can be imported"""
    print("📦 Testing Module Imports...")
    modules_to_test = [
        "subprocess",
        "json", 
        "argparse",
        "time",
        "os",
        "sys",
        "typing"
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - Imported successfully")
        except ImportError as e:
            print(f"❌ {module_name} - Import failed: {e}")
    print()

def main():
    """Main test function"""
    print("🧪 VS Code Integration Test")
    print("=" * 40)
    print()
    
    test_python_environment()
    test_docker_availability()
    test_file_accessibility() 
    test_import_modules()
    
    print("🎯 Test Summary:")
    print("If all tests passed, VS Code debugging should work correctly!")
    print("Use F5 or Run > Start Debugging to test the launch configurations.")
    print()
    
    # Test breakpoint functionality
    breakpoint_test = "This line can be used to test breakpoints"
    print(f"🔍 Breakpoint test: {breakpoint_test}")

if __name__ == "__main__":
    main()