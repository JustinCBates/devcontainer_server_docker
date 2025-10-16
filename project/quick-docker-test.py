#!/usr/bin/env python3
"""
Quick Docker Test - Simple verification script
"""
import os
import subprocess

def run_cmd(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def main():
    print("🧪 Quick Docker Test")
    print("=" * 30)
    
    # Test 1: Docker version
    print("\n1. Testing Docker installation...")
    success, output, error = run_cmd("docker --version")
    if success:
        print(f"✅ Docker found: {output}")
    else:
        print(f"❌ Docker not found: {error}")
        return
    
    # Test 2: Docker daemon
    print("\n2. Testing Docker daemon...")
    success, output, error = run_cmd("docker info")
    if success:
        print("✅ Docker daemon is running")
    else:
        print(f"❌ Docker daemon issue: {error}")
        return
    
    # Test 3: Docker Compose
    print("\n3. Testing Docker Compose...")
    success, output, error = run_cmd("docker-compose --version")
    if success:
        print(f"✅ Docker Compose found: {output}")
    else:
        print(f"❌ Docker Compose issue: {error}")
    
    # Test 4: Check project structure
    print("\n4. Checking project structure...")
    
    # Check for docker-compose.yml
    if os.path.exists("docker-compose.yml"):
        print("✅ docker-compose.yml found")
        
        # Validate syntax
        success, output, error = run_cmd("docker-compose config --quiet")
        if success:
            print("✅ docker-compose.yml syntax is valid")
        else:
            print(f"❌ docker-compose.yml has errors: {error}")
    else:
        print("❌ docker-compose.yml not found")
    
    # Check for distros directory
    if os.path.exists("project/distros"):
        distros = os.listdir("project/distros")
        print(f"✅ Found {len(distros)} distribution configs: {', '.join(distros)}")
        
        # Check for Dockerfiles
        for distro in distros:
            dockerfile_path = f"project/distros/{distro}/Dockerfile"
            if os.path.exists(dockerfile_path):
                print(f"  ✅ {distro}/Dockerfile exists")
            else:
                print(f"  ❌ {distro}/Dockerfile missing")
    else:
        print("❌ project/distros directory not found")
    
    # Test 5: List existing images
    print("\n5. Checking existing Docker images...")
    success, output, error = run_cmd("docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}'")
    if success and output:
        print("✅ Existing Docker images:")
        print(output)
    else:
        print("ℹ️  No existing Docker images found")
    
    print("\n" + "=" * 50)
    print("Docker environment test complete!")
    print("\nNext steps:")
    print("1. To build all images: docker-compose build")
    print("2. To test specific image: docker-compose build ubuntu-vps")
    print("3. To run full launcher: .\\START-WINDOWS.bat")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")