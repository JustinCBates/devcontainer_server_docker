#!/usr/bin/env python3
"""
Docker Image Testing and Validation Script
Tests that Docker images are properly built and functional
"""

import os
import sys
import subprocess
import json
import time
from typing import Dict, List, Tuple, Optional

# Import configuration from advanced-launcher
try:
    from advanced_launcher import LINUX_FAMILIES, Colors, run_command
except ImportError:
    # If import fails, define the essential components locally
    class Colors:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        GRAY = '\033[90m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
    
    def run_command(command: str, capture_output: bool = True, suppress_errors: bool = True) -> Tuple[bool, str]:
        """Execute a shell command and return success status and output"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                success = result.returncode == 0
                output = result.stdout.strip() if success else result.stderr.strip()
            else:
                result = subprocess.run(command, shell=True)
                success = result.returncode == 0
                output = ""
            return success, output
        except Exception as e:
            if not suppress_errors:
                print(f"Error executing command: {e}")
            return False, str(e)
    
    # Define Linux families locally
    LINUX_FAMILIES = {
        "debian": {
            "name": "Debian Family",
            "distributions": {
                "ubuntu": {"name": "Ubuntu 22.04 LTS", "container": "ubuntu-vps", "port": 2201},
                "debian": {"name": "Debian 12 (Bookworm)", "container": "debian-vps", "port": 2202}
            }
        },
        "redhat": {
            "name": "Red Hat Family", 
            "distributions": {
                "rocky": {"name": "Rocky Linux 9", "container": "rocky-vps", "port": 2203},
                "centos": {"name": "CentOS Stream 9", "container": "centos-vps", "port": 2204}
            }
        },
        "alpine": {
            "name": "Alpine Family",
            "distributions": {
                "alpine": {"name": "Alpine Linux 3.18", "container": "alpine-vps", "port": 2205}
            }
        },
        "suse": {
            "name": "SUSE Family",
            "distributions": {
                "opensuse": {"name": "openSUSE Leap 15.5", "container": "opensuse-vps", "port": 2206}
            }
        },
        "arch": {
            "name": "Arch Family",
            "distributions": {
                "arch": {"name": "Arch Linux", "container": "arch-vps", "port": 2207},
                "slackware": {"name": "Slackware 15.0", "container": "slackware-vps", "port": 2208}
            }
        }
    }

class DockerImageTester:
    """Test and validate Docker images for VPS environments"""
    
    def __init__(self):
        self.test_results = {}
        self.failed_tests = []
        
    def show_header(self):
        """Display testing header"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}")
        print("🧪 Docker Image Testing & Validation")
        print("Multi-Distribution VPS Image Verification")
        print(f"{'='*70}{Colors.RESET}")
        print()

    def check_docker_installed(self) -> bool:
        """Check if Docker is installed and running"""
        print(f"{Colors.YELLOW}🔍 Checking Docker installation...{Colors.RESET}")
        
        # Check if Docker command exists
        success, output = run_command("docker --version")
        if not success:
            print(f"{Colors.RED}❌ Docker is not installed or not in PATH{Colors.RESET}")
            print(f"{Colors.GRAY}Please install Docker Desktop from https://docker.com{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ Docker found: {output}{Colors.RESET}")
        
        # Check if Docker daemon is running
        success, output = run_command("docker info")
        if not success:
            print(f"{Colors.RED}❌ Docker daemon is not running{Colors.RESET}")
            print(f"{Colors.GRAY}Please start Docker Desktop{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ Docker daemon is running{Colors.RESET}")
        return True

    def check_docker_compose_file(self) -> bool:
        """Verify docker-compose.yml exists and is valid"""
        print(f"{Colors.YELLOW}🔍 Checking docker-compose.yml...{Colors.RESET}")
        
        compose_file = "../docker-compose.yml"
        if not os.path.exists(compose_file):
            print(f"{Colors.RED}❌ docker-compose.yml not found at {compose_file}{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ docker-compose.yml found{Colors.RESET}")
        
        # Validate docker-compose syntax
        success, output = run_command("docker-compose -f ../docker-compose.yml config --quiet")
        if not success:
            print(f"{Colors.RED}❌ docker-compose.yml has syntax errors:{Colors.RESET}")
            print(f"{Colors.RED}{output}{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ docker-compose.yml syntax is valid{Colors.RESET}")
        return True

    def list_available_images(self) -> Dict[str, str]:
        """List all available VPS image configurations"""
        print(f"{Colors.YELLOW}🔍 Scanning available VPS configurations...{Colors.RESET}")
        
        images = {}
        for family_key, family in LINUX_FAMILIES.items():
            for distro_key, distro in family["distributions"].items():
                image_name = f"devcontainer_server_docker_{distro['container']}"
                dockerfile_path = f"../distros/{distro_key}/Dockerfile"
                
                if os.path.exists(dockerfile_path):
                    images[distro_key] = {
                        "name": distro["name"],
                        "container": distro["container"],
                        "image_name": image_name,
                        "dockerfile": dockerfile_path,
                        "port": distro["port"]
                    }
                    print(f"{Colors.GREEN}  ✓ {distro['name']} ({distro_key}){Colors.RESET}")
                else:
                    print(f"{Colors.RED}  ✗ {distro['name']} - Dockerfile missing{Colors.RESET}")
        
        print(f"{Colors.CYAN}Found {len(images)} available configurations{Colors.RESET}")
        return images

    def test_image_build(self, distro_key: str, config: Dict) -> bool:
        """Test building a specific Docker image"""
        print(f"{Colors.YELLOW}🔨 Testing build: {config['name']}...{Colors.RESET}")
        
        # Build the image
        build_cmd = f"docker-compose -f ../docker-compose.yml build {config['container']}"
        print(f"{Colors.GRAY}Running: {build_cmd}{Colors.RESET}")
        
        success, output = run_command(build_cmd, capture_output=False)
        
        if success:
            print(f"{Colors.GREEN}✅ Build successful: {config['name']}{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Build failed: {config['name']}{Colors.RESET}")
            if output:
                print(f"{Colors.RED}Error: {output}{Colors.RESET}")
            self.failed_tests.append(f"Build failed for {config['name']}")
            return False

    def test_image_exists(self, config: Dict) -> bool:
        """Check if Docker image exists locally"""
        print(f"{Colors.YELLOW}🔍 Checking image: {config['name']}...{Colors.RESET}")
        
        # Check if image exists (cross-platform approach)
        success, output = run_command('docker images --format "{{.Repository}}:{{.Tag}}"')
        
        if success and config["image_name"] in output:
            print(f"{Colors.GREEN}✅ Image exists: {config['name']}{Colors.RESET}")
            print(f"{Colors.GRAY}   Image: {output}{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Image not found: {config['name']}{Colors.RESET}")
            return False

    def test_container_start(self, distro_key: str, config: Dict) -> bool:
        """Test starting and basic functionality of container"""
        print(f"{Colors.YELLOW}🚀 Testing container start: {config['name']}...{Colors.RESET}")
        
        # Stop any existing container
        run_command(f"docker-compose -f ../docker-compose.yml --profile {distro_key} down")
        
        # Start the container
        success, output = run_command(f"docker-compose -f ../docker-compose.yml --profile {distro_key} up -d")
        
        if not success:
            print(f"{Colors.RED}❌ Failed to start container: {config['name']}{Colors.RESET}")
            self.failed_tests.append(f"Container start failed for {config['name']}")
            return False
        
        print(f"{Colors.GREEN}✅ Container started: {config['name']}{Colors.RESET}")
        
        # Wait for container to initialize
        print(f"{Colors.GRAY}   Waiting for services to initialize...{Colors.RESET}")
        time.sleep(15)
        
        # Test SSH connectivity
        print(f"{Colors.YELLOW}🔑 Testing SSH connectivity...{Colors.RESET}")
        ssh_test_cmd = f'docker exec {config["container"]} systemctl is-active sshd'
        success, output = run_command(ssh_test_cmd)
        
        if success and "active" in output:
            print(f"{Colors.GREEN}✅ SSH service is running{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠️  SSH service status unclear{Colors.RESET}")
        
        # Test if container is healthy
        container_check_cmd = f'docker ps --filter "name={config["container"]}" --format "{{{{.Status}}}}"'
        success, status = run_command(container_check_cmd)
        
        if success and status:
            print(f"{Colors.GREEN}✅ Container status: {status}{Colors.RESET}")
            
            # Stop the test container
            run_command(f"docker-compose -f ../docker-compose.yml --profile {distro_key} down")
            return True
        else:
            print(f"{Colors.RED}❌ Container health check failed{Colors.RESET}")
            self.failed_tests.append(f"Container health check failed for {config['name']}")
            return False

    def test_all_images(self, build_missing: bool = False) -> None:
        """Test all available images"""
        print(f"{Colors.CYAN}🧪 Running comprehensive image tests...{Colors.RESET}")
        print()
        
        images = self.list_available_images()
        if not images:
            print(f"{Colors.RED}❌ No image configurations found{Colors.RESET}")
            return
        
        print()
        
        for distro_key, config in images.items():
            print(f"{Colors.BOLD}{Colors.CYAN}Testing: {config['name']} ({distro_key}){Colors.RESET}")
            print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
            
            # Check if image exists
            image_exists = self.test_image_exists(config)
            
            # Build if missing and requested
            if not image_exists and build_missing:
                build_success = self.test_image_build(distro_key, config)
                if build_success:
                    image_exists = True
            
            # Test container functionality if image exists
            if image_exists:
                container_test = self.test_container_start(distro_key, config)
                self.test_results[distro_key] = {
                    "name": config["name"],
                    "image_exists": True,
                    "container_test": container_test,
                    "overall": container_test
                }
            else:
                self.test_results[distro_key] = {
                    "name": config["name"],
                    "image_exists": False,
                    "container_test": False,
                    "overall": False
                }
            
            print()

    def show_test_summary(self) -> None:
        """Display test results summary"""
        print(f"{Colors.BOLD}{Colors.CYAN}📊 Test Results Summary{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        print()
        
        passed = 0
        total = len(self.test_results)
        
        for distro_key, result in self.test_results.items():
            status_icon = "✅" if result["overall"] else "❌"
            status_color = Colors.GREEN if result["overall"] else Colors.RED
            
            print(f"{status_icon} {Colors.WHITE}{result['name']:<20}{Colors.RESET} "
                  f"{status_color}{'PASS' if result['overall'] else 'FAIL'}{Colors.RESET}")
            
            if not result["image_exists"]:
                print(f"   {Colors.GRAY}└─ Image not built{Colors.RESET}")
            elif not result["container_test"]:
                print(f"   {Colors.GRAY}└─ Container test failed{Colors.RESET}")
            
            if result["overall"]:
                passed += 1
        
        print()
        print(f"{Colors.BOLD}Results: {Colors.GREEN}{passed}/{total} PASSED{Colors.RESET}")
        
        if self.failed_tests:
            print(f"{Colors.RED}Failed Tests:{Colors.RESET}")
            for failure in self.failed_tests:
                print(f"  • {failure}")
        
        print()

def main():
    """Main testing function"""
    tester = DockerImageTester()
    tester.show_header()
    
    # Check prerequisites
    if not tester.check_docker_installed():
        input("Press Enter to exit...")
        return
    
    print()
    
    if not tester.check_docker_compose_file():
        input("Press Enter to exit...")
        return
    
    print()
    
    # Ask user what to test
    print(f"{Colors.YELLOW}Select testing mode:{Colors.RESET}")
    print(f"{Colors.GREEN}[1] Test existing images only{Colors.RESET}")
    print(f"{Colors.GREEN}[2] Build missing images and test all{Colors.RESET}")
    print(f"{Colors.GREEN}[3] List available configurations{Colors.RESET}")
    print()
    
    choice = input(f"{Colors.CYAN}Enter choice [1-3]: {Colors.RESET}").strip()
    
    if choice == "1":
        tester.test_all_images(build_missing=False)
        tester.show_test_summary()
    elif choice == "2":
        print(f"{Colors.YELLOW}⚠️  This will build all missing images (may take a while){Colors.RESET}")
        confirm = input(f"{Colors.CYAN}Continue? [y/N]: {Colors.RESET}").strip().lower()
        if confirm == 'y':
            tester.test_all_images(build_missing=True)
            tester.show_test_summary()
    elif choice == "3":
        tester.list_available_images()
    else:
        print(f"{Colors.RED}Invalid choice{Colors.RESET}")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()