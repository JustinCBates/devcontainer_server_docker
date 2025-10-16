#!/usr/bin/env python3
"""
Organized Family Build System
Modular build system with family-specific units and organized structure
"""

import os
import sys
import subprocess
import time
import importlib.util
from datetime import datetime
from pathlib import Path

class OrganizedFamilyBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.families_dir = self.project_root / "project" / "families"
        self.families = {}
        self.results = {}
        self.start_time = None
        
        # Load all family configurations
        self.load_family_configurations()

    def log(self, message, level="INFO"):
        """Log message with timestamp and color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "",
            "SUCCESS": "\033[92m",
            "ERROR": "\033[91m", 
            "WARNING": "\033[93m",
            "HEADER": "\033[96m\033[1m"
        }
        reset = "\033[0m"
        color = colors.get(level, "")
        print(f"{color}[{timestamp}] {level}: {message}{reset}")

    def load_family_configurations(self):
        """Dynamically load all family configurations"""
        self.log("Loading family configurations...", "HEADER")
        
        if not self.families_dir.exists():
            self.log(f"Families directory not found: {self.families_dir}", "ERROR")
            return
            
        for family_dir in self.families_dir.iterdir():
            if family_dir.is_dir() and (family_dir / "family_config.py").exists():
                try:
                    # Load family configuration module
                    config_path = family_dir / "family_config.py"
                    spec = importlib.util.spec_from_file_location("family_config", config_path)
                    config_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(config_module)
                    
                    # Extract family information
                    family_key = family_dir.name
                    self.families[family_key] = {
                        "name": getattr(config_module, "family_name", family_key.title()),
                        "package_manager": getattr(config_module, "package_manager", "unknown"),
                        "description": getattr(config_module, "description", ""),
                        "distributions": getattr(config_module, "distributions", {}),
                        "build_commands": getattr(config_module, "build_commands", []),
                        "test_commands": getattr(config_module, "test_commands", []),
                        "ssh_config": getattr(config_module, "ssh_config", {}),
                        "config_path": config_path
                    }
                    
                    # Find representative distribution
                    representative = None
                    for distro_key, distro_config in self.families[family_key]["distributions"].items():
                        if distro_config.get("representative", False):
                            representative = distro_key
                            break
                    
                    self.families[family_key]["representative"] = representative
                    
                    self.log(f"Loaded {self.families[family_key]['name']} ({len(self.families[family_key]['distributions'])} distributions)", "SUCCESS")
                    
                except Exception as e:
                    self.log(f"Failed to load {family_dir.name}: {e}", "ERROR")
        
        self.log(f"Loaded {len(self.families)} families", "HEADER")

    def run_cmd(self, cmd, show_output=True, timeout=300):
        """Execute command with optional output and timeout"""
        try:
            if show_output:
                process = subprocess.Popen(
                    cmd, shell=True, stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1
                )
                
                output_lines = []
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                        output_lines.append(output.strip())
                
                return process.poll() == 0, '\n'.join(output_lines)
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
                return result.returncode == 0, result.stdout.strip()
        except subprocess.TimeoutExpired:
            self.log(f"Command timed out: {cmd}", "ERROR")
            return False, "Timeout"
        except Exception as e:
            self.log(f"Command failed: {e}", "ERROR")
            return False, str(e)

    def check_prerequisites(self):
        """Check system prerequisites"""
        self.log("Checking prerequisites...", "HEADER")
        
        # Check Docker
        success, output = self.run_cmd("docker --version", show_output=False)
        if not success:
            self.log("Docker not found", "ERROR")
            return False
        self.log(f"Docker: {output}", "SUCCESS")
        
        # Check Docker daemon
        success, _ = self.run_cmd("docker info", show_output=False, timeout=10)
        if not success:
            self.log("Docker daemon not running", "ERROR")
            return False
        self.log("Docker daemon running", "SUCCESS")
        
        # Check docker-compose.yml
        if not (self.project_root / "docker-compose.yml").exists():
            self.log("docker-compose.yml not found", "ERROR")
            return False
        self.log("docker-compose.yml found", "SUCCESS")
        
        return True

    def build_family_unit(self, family_key):
        """Build unit for a specific family"""
        if family_key not in self.families:
            self.log(f"Family {family_key} not found", "ERROR")
            return False
            
        family = self.families[family_key]
        representative = family["representative"]
        
        if not representative:
            self.log(f"No representative defined for {family['name']}", "ERROR")
            return False
            
        distro_config = family["distributions"][representative]
        
        self.log(f"Building {family['name']} unit...", "HEADER")
        self.log(f"Representative: {distro_config['name']}", "INFO")
        self.log(f"Container: {distro_config['container']}", "INFO")
        self.log(f"Package Manager: {family['package_manager']}", "INFO")
        
        # Build the representative distribution
        build_cmd = f"docker compose build {distro_config['container']}"
        self.log(f"Executing: {build_cmd}", "INFO")
        
        success, output = self.run_cmd(build_cmd, show_output=True)
        
        if success:
            self.log(f"Successfully built {family['name']} unit", "SUCCESS")
            return True
        else:
            self.log(f"Failed to build {family['name']} unit", "ERROR")
            return False

    def test_family_unit(self, family_key):
        """Test unit for a specific family"""
        if family_key not in self.families:
            return False
            
        family = self.families[family_key]
        representative = family["representative"]
        distro_config = family["distributions"][representative]
        
        self.log(f"Testing {family['name']} unit...", "HEADER")
        
        # Start container
        start_cmd = f"docker compose --profile {representative} up -d"
        success, _ = self.run_cmd(start_cmd, show_output=False)
        
        if not success:
            self.log(f"Failed to start {distro_config['container']}", "ERROR")
            return False
            
        # Wait for initialization
        self.log("Waiting for container initialization...", "INFO")
        time.sleep(15)
        
        # Check if running
        check_cmd = f'docker ps --filter "name={distro_config["container"]}" --format "{{{{.Names}}}}"'
        success, output = self.run_cmd(check_cmd, show_output=False)
        
        if success and distro_config["container"] in output:
            self.log(f"{distro_config['container']} is running", "SUCCESS")
            
            # Test package manager
            if family["test_commands"]:
                for test_cmd in family["test_commands"][:1]:  # Test first command
                    exec_cmd = f'docker exec {distro_config["container"]} {test_cmd}'
                    test_success, test_output = self.run_cmd(exec_cmd, show_output=False)
                    if test_success:
                        self.log(f"Package manager test passed: {test_cmd}", "SUCCESS")
                    else:
                        self.log(f"Package manager test failed: {test_cmd}", "WARNING")
            
            # Stop container
            stop_cmd = f"docker compose --profile {representative} down"
            self.run_cmd(stop_cmd, show_output=False)
            return True
        else:
            self.log(f"{distro_config['container']} failed health check", "ERROR")
            return False

    def build_all_family_units(self):
        """Build all family units (representatives)"""
        self.start_time = datetime.now()
        
        self.log("Building All Family Units", "HEADER")
        self.log("=" * 60, "HEADER")
        
        if not self.check_prerequisites():
            return False
            
        for family_key in self.families.keys():
            print(f"\n{'=' * 60}")
            build_success = self.build_family_unit(family_key)
            test_success = False
            
            if build_success:
                test_success = self.test_family_unit(family_key)
                
            self.results[family_key] = {
                "name": self.families[family_key]["name"],
                "representative": self.families[family_key]["representative"],
                "build_success": build_success,
                "test_success": test_success,
                "overall_success": build_success and test_success
            }

    def show_family_summary(self):
        """Show organized summary of all families"""
        end_time = datetime.now()
        duration = end_time - self.start_time if self.start_time else "Unknown"
        
        print(f"\n{'=' * 70}")
        self.log("ORGANIZED FAMILY BUILD SUMMARY", "HEADER")
        print(f"{'=' * 70}")
        
        passed = 0
        total = len(self.results)
        
        print(f"{'Family':<18} {'Representative':<12} {'Build':<8} {'Test':<8} {'Status':<8}")
        print("-" * 70)
        
        for family_key, result in self.results.items():
            family = self.families[family_key]
            rep_config = family["distributions"][result["representative"]]
            
            build_status = "PASS" if result["build_success"] else "FAIL"
            test_status = "PASS" if result["test_success"] else "FAIL"
            overall_status = "PASS" if result["overall_success"] else "FAIL"
            
            print(f"{result['name'][:17]:<18} {result['representative']:<12} {build_status:<8} {test_status:<8} {overall_status:<8}")
            
            if result["overall_success"]:
                passed += 1
        
        print("-" * 70)
        print(f"Results: {passed}/{total} family units successful")
        print(f"Duration: {duration}")
        
        # Connection information
        if passed > 0:
            print(f"\n{'=' * 70}")
            self.log("CONNECTION INFORMATION", "HEADER") 
            print(f"{'=' * 70}")
            
            for family_key, result in self.results.items():
                if result["overall_success"]:
                    family = self.families[family_key]
                    rep_config = family["distributions"][result["representative"]]
                    ssh_config = family["ssh_config"]
                    
                    print(f"{result['name']}:")
                    print(f"  ssh {ssh_config.get('user', 'vpsuser')}@localhost -p {rep_config['port']}")
                    print(f"  Container: {rep_config['container']}")
                    print(f"  Password: {ssh_config.get('password', 'vpsuser123')}")
                    print(f"  Package Manager: {family['package_manager']}")
                    print()

    def interactive_menu(self):
        """Interactive menu for family operations"""
        while True:
            print(f"\n{'=' * 50}")
            self.log("ORGANIZED FAMILY BUILD SYSTEM", "HEADER")
            print(f"{'=' * 50}")
            
            print("\nLoaded Families:")
            for family_key, family in self.families.items():
                rep = family["representative"]
                print(f"  {family['name']} ({family['package_manager']}) - Representative: {rep}")
            
            print(f"\nOptions:")
            print("[1] Build all family units")
            print("[2] Build specific family unit")
            print("[3] Test specific family unit") 
            print("[4] Show family details")
            print("[5] Check prerequisites")
            print("[q] Quit")
            
            choice = input(f"\nSelect option: ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '1':
                self.build_all_family_units()
                self.show_family_summary()
            elif choice == '2':
                print(f"\nAvailable families: {', '.join(self.families.keys())}")
                family_key = input("Enter family key: ").strip().lower()
                if family_key in self.families:
                    self.build_family_unit(family_key)
                else:
                    self.log("Invalid family key", "ERROR")
            elif choice == '3':
                print(f"\nAvailable families: {', '.join(self.families.keys())}")
                family_key = input("Enter family key: ").strip().lower()
                if family_key in self.families:
                    self.test_family_unit(family_key)
                else:
                    self.log("Invalid family key", "ERROR")
            elif choice == '4':
                self.show_family_details()
            elif choice == '5':
                self.check_prerequisites()
            else:
                self.log("Invalid choice", "ERROR")

    def show_family_details(self):
        """Show detailed information about all families"""
        print(f"\n{'=' * 70}")
        self.log("FAMILY DETAILS", "HEADER")
        print(f"{'=' * 70}")
        
        for family_key, family in self.families.items():
            print(f"\n{family['name']} ({family_key})")
            print("-" * 40)
            print(f"Package Manager: {family['package_manager']}")
            print(f"Description: {family['description']}")
            print(f"Representative: {family['representative']}")
            print(f"Distributions:")
            
            for distro_key, distro in family['distributions'].items():
                rep_marker = " (REPRESENTATIVE)" if distro.get('representative', False) else ""
                print(f"  - {distro['name']} ({distro_key}){rep_marker}")
                print(f"    Container: {distro['container']}")
                print(f"    Port: {distro['port']}")

def main():
    """Main execution function"""
    builder = OrganizedFamilyBuilder()
    
    if len(builder.families) == 0:
        print("No family configurations found. Please check the project/families directory.")
        return
        
    # Check if running non-interactively
    if len(sys.argv) > 1 and sys.argv[1] == '--build-all':
        builder.build_all_family_units()
        builder.show_family_summary()
    else:
        builder.interactive_menu()

if __name__ == "__main__":
    main()