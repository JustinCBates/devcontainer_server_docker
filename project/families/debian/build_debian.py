#!/usr/bin/env python3
"""
Debian Family Builder
Handles building and testing for Debian-based distributions
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from families.debian.family_config import distributions, family_name, build_commands, test_commands
except ImportError:
    print("Error: Could not load family configuration")
    sys.exit(1)

class DebianFamilyBuilder:
    def __init__(self):
        self.family_name = family_name
        self.distributions = distributions
        self.representative = self.get_representative()
        
    def get_representative(self):
        """Get the representative distribution for this family"""
        for distro_key, config in self.distributions.items():
            if config.get("representative", False):
                return distro_key, config
        return None, None
        
    def run_cmd(self, cmd, show_output=True):
        """Execute command with optional output"""
        try:
            if show_output:
                result = subprocess.run(cmd, shell=True, text=True)
                return result.returncode == 0
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.returncode == 0, result.stdout.strip()
        except Exception as e:
            print(f"Command failed: {e}")
            return False
            
    def build_representative(self):
        """Build the family representative distribution"""
        if not self.representative[0]:
            print("No representative distribution defined for Debian family")
            return False
            
        distro_key, config = self.representative
        print(f"Building {self.family_name} representative: {config['name']}")
        
        # Build using docker-compose
        build_cmd = f"docker compose build {config['container']}"
        success = self.run_cmd(build_cmd)
        
        if success:
            print(f"✓ Successfully built {config['container']}")
            return True
        else:
            print(f"✗ Failed to build {config['container']}")
            return False
            
    def build_all_distributions(self):
        """Build all distributions in this family"""
        results = {}
        
        for distro_key, config in self.distributions.items():
            print(f"Building {config['name']}...")
            
            build_cmd = f"docker compose build {config['container']}"
            success = self.run_cmd(build_cmd)
            results[distro_key] = success
            
            if success:
                print(f"✓ Successfully built {config['container']}")
            else:
                print(f"✗ Failed to build {config['container']}")
                
        return results
        
    def test_distribution(self, distro_key):
        """Test a specific distribution"""
        if distro_key not in self.distributions:
            print(f"Distribution {distro_key} not found in {self.family_name}")
            return False
            
        config = self.distributions[distro_key]
        print(f"Testing {config['name']}...")
        
        # Start container
        start_cmd = f"docker compose --profile {distro_key} up -d"
        if not self.run_cmd(start_cmd, show_output=False)[0]:
            print(f"✗ Failed to start {config['container']}")
            return False
            
        # Wait for startup
        import time
        time.sleep(10)
        
        # Test container is running
        check_cmd = f'docker ps --filter "name={config["container"]}" --format "{{{{.Names}}}}"'
        running, output = self.run_cmd(check_cmd, show_output=False)
        
        if running and config["container"] in output:
            print(f"✓ {config['container']} is running")
            
            # Stop container
            stop_cmd = f"docker compose --profile {distro_key} down"
            self.run_cmd(stop_cmd, show_output=False)
            return True
        else:
            print(f"✗ {config['container']} is not running properly")
            return False

def main():
    builder = DebianFamilyBuilder()
    
    print("Debian Family Build Options:")
    print("[1] Build representative only (Ubuntu)")
    print("[2] Build all distributions")
    print("[3] Test representative")
    
    choice = input("Select option [1-3]: ").strip()
    
    if choice == "1":
        builder.build_representative()
    elif choice == "2":
        builder.build_all_distributions()
    elif choice == "3":
        if builder.representative[0]:
            builder.test_distribution(builder.representative[0])
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()