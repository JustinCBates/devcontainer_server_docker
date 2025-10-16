#!/usr/bin/env python3
"""
Advanced VPS Environment Launcher
A Python-based interactive launcher for managing multi-distribution VPS simulation environments
with state management capabilities including fresh installs, persistent servers, upgrades,
snapshots, and restore functionality.
"""

import os
import sys
import subprocess
import json
import argparse
import time
from typing import Dict, List, Optional, Tuple

# Linux distribution configurations organized by family
LINUX_FAMILIES = {
    "debian": {
        "name": "Debian Family",
        "description": "Debian-based distributions (apt package manager)",
        "distributions": {
            "ubuntu": {
                "name": "Ubuntu 22.04 LTS",
                "description": "Popular, user-friendly Ubuntu distribution",
                "container": "ubuntu-vps",
                "port": 2201,
                "volume": "ubuntu-persistent"
            },
            "debian": {
                "name": "Debian 12 (Bookworm)",
                "description": "Stable Debian base distribution",
                "container": "debian-vps", 
                "port": 2202,
                "volume": "debian-persistent"
            }
        }
    },
    "redhat": {
        "name": "Red Hat Family",
        "description": "RHEL-based distributions (yum/dnf package manager)",
        "distributions": {
            "rocky": {
                "name": "Rocky Linux 9",
                "description": "Enterprise-grade RHEL alternative",
                "container": "rocky-vps",
                "port": 2203,
                "volume": "rocky-persistent"
            },
            "centos": {
                "name": "CentOS Stream 9",
                "description": "Upstream development platform for RHEL",
                "container": "centos-vps",
                "port": 2204,
                "volume": "centos-persistent"
            }
        }
    },
    "alpine": {
        "name": "Alpine Family",
        "description": "Lightweight distributions (apk package manager)",
        "distributions": {
            "alpine": {
                "name": "Alpine Linux 3.18",
                "description": "Security-oriented, lightweight Linux",
                "container": "alpine-vps",
                "port": 2205,
                "volume": "alpine-persistent"
            }
        }
    },
    "suse": {
        "name": "SUSE Family", 
        "description": "SUSE-based distributions (zypper package manager)",
        "distributions": {
            "opensuse": {
                "name": "openSUSE Leap 15.5",
                "description": "Stable SUSE enterprise distribution",
                "container": "opensuse-vps",
                "port": 2206,
                "volume": "opensuse-persistent"
            }
        }
    },
    "arch": {
        "name": "Arch Family",
        "description": "Rolling release distributions (pacman package manager)",
        "distributions": {
            "arch": {
                "name": "Arch Linux",
                "description": "Rolling release, cutting-edge Linux",
                "container": "arch-vps",
                "port": 2207,
                "volume": "arch-persistent"
            },
            "slackware": {
                "name": "Slackware 15.0",
                "description": "Veteran Linux distribution",
                "container": "slackware-vps",
                "port": 2208,
                "volume": "slackware-persistent"
            }
        }
    }
}

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
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
            print(f"{Colors.RED}Error executing command: {e}{Colors.RESET}")
        return False, str(e)

def show_header():
    """Display the application header"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}")
    print("🐳 Advanced VPS Environment Launcher")
    print("Multi-Distribution Docker-based VPS Simulation Platform")
    print(f"{'='*70}{Colors.RESET}")
    print()

def show_mode_options() -> List[str]:
    """Display available modes and return list of mode keys"""
    print(f"{Colors.YELLOW}Select Launch Mode:{Colors.RESET}")
    print(f"{Colors.YELLOW}{'='*20}{Colors.RESET}")
    print()
    
    modes = [
        ("fresh", "🧹 Fresh Install", "Clean container, no persistent data, fastest startup"),
        ("persistent", "💾 Persistent Server", "Data persists between sessions, acts like real VPS"),
        ("upgrade", "🔄 Upgrade Mode", "Update existing persistent server with latest packages"),
        ("snapshot", "📸 Create Snapshot", "Save current server state for later restore"),
        ("restore", "📥 Restore Snapshot", "Restore from a previous snapshot")
    ]
    
    for i, (key, title, desc) in enumerate(modes, 1):
        print(f"{Colors.GREEN}[{i}] {title}{Colors.RESET}")
        print(f"     {Colors.GRAY}{desc}{Colors.RESET}")
        print()
    
    return [mode[0] for mode in modes]

def show_linux_families() -> List[str]:
    """Display Linux families and return list of family keys"""
    print(f"{Colors.YELLOW}Select Linux Family:{Colors.RESET}")
    print(f"{Colors.YELLOW}{'='*21}{Colors.RESET}")
    print()
    
    family_keys = list(LINUX_FAMILIES.keys())
    for i, family_key in enumerate(family_keys, 1):
        family = LINUX_FAMILIES[family_key]
        distro_count = len(family["distributions"])
        print(f"{Colors.GREEN}[{i}] {family['name']}{Colors.RESET}")
        print(f"     {Colors.GRAY}{family['description']}{Colors.RESET}")
        print(f"     {Colors.GRAY}Available distributions: {distro_count}{Colors.RESET}")
        print()
    
    return family_keys

def show_distributions(family_key: str) -> List[str]:
    """Display distributions in a family and return list of distro keys"""
    family = LINUX_FAMILIES[family_key]
    
    print(f"{Colors.YELLOW}Available Distributions in {family['name']}:{Colors.RESET}")
    header_length = 35 + len(family['name'])
    print(f"{Colors.YELLOW}{'='*header_length}{Colors.RESET}")
    print()
    
    distro_keys = list(family["distributions"].keys())
    for i, distro_key in enumerate(distro_keys, 1):
        distro = family["distributions"][distro_key]
        
        # Check if persistent volume exists
        success, output = run_command(f'docker volume ls --format "{{{{.Name}}}}" | findstr {distro["volume"]}')
        persistent_status = f" {Colors.BLUE}[HAS PERSISTENT DATA]{Colors.RESET}" if success and output else f" {Colors.GRAY}[CLEAN]{Colors.RESET}"
        
        print(f"{Colors.GREEN}[{i}] {distro['name']}{persistent_status}")
        print(f"     {Colors.GRAY}{distro['description']}{Colors.RESET}")
        print(f"     {Colors.GRAY}SSH Port: {distro['port']}{Colors.RESET}")
        print(f"     {Colors.GRAY}Container: {distro['container']}{Colors.RESET}")
        
        if success and output:
            print(f"     {Colors.BLUE}State Volume: {distro['volume']} (exists){Colors.RESET}")
        else:
            print(f"     {Colors.GRAY}State Volume: {distro['volume']} (clean){Colors.RESET}")
        print()
    
    return distro_keys

def show_existing_snapshots(distro_key: str) -> List[str]:
    """Display existing snapshots for a distribution"""
    print(f"{Colors.YELLOW}Available Snapshots for {distro_key}:{Colors.RESET}")
    print(f"{Colors.YELLOW}{'='*34}{Colors.RESET}")
    print()
    
    # List snapshots (stored as named volumes)
    success, output = run_command(f'docker volume ls --format "{{{{.Name}}}}" | findstr {distro_key}-snapshot-')
    
    if success and output:
        snapshots = output.split('\n')
        for i, snapshot in enumerate(snapshots, 1):
            snapshot_name = snapshot.replace(f"{distro_key}-snapshot-", "")
            print(f"{Colors.GREEN}[{i}] {snapshot_name}{Colors.RESET}")
            
            # Try to get creation date from volume metadata
            vol_success, vol_output = run_command(f'docker volume inspect {snapshot}')
            if vol_success:
                try:
                    vol_data = json.loads(vol_output)
                    created_date = vol_data[0].get('CreatedAt', 'Unknown')
                    print(f"     {Colors.GRAY}Created: {created_date}{Colors.RESET}")
                except:
                    print(f"     {Colors.GRAY}Created: Unknown{Colors.RESET}")
            print()
        return snapshots
    else:
        print(f"{Colors.GRAY}No snapshots found for {distro_key}{Colors.RESET}")
        print()
        return []

def get_user_choice(prompt: str, max_choice: int, extra_options: str = "") -> str:
    """Get user input with validation"""
    while True:
        choice_prompt = f"{Colors.CYAN}{prompt}"
        if extra_options:
            choice_prompt += f" {Colors.GRAY}({extra_options}){Colors.RESET}"
        choice_prompt += f"{Colors.CYAN}: {Colors.RESET}"
        
        choice = input(choice_prompt).strip().lower()
        
        if choice in ['q', 'quit']:
            print(f"{Colors.YELLOW}Goodbye!{Colors.RESET}")
            sys.exit(0)
        
        if choice in ['b', 'back']:
            return "back"
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= max_choice:
                return str(choice_num)
        except ValueError:
            pass
        
        print(f"{Colors.RED}Invalid choice. Please enter a number between 1 and {max_choice}{Colors.RESET}")
        if extra_options:
            print(f"{Colors.RED}Or use: {extra_options}{Colors.RESET}")
        print()

def start_persistent_container(distro_key: str, volume_names: List[str]) -> bool:
    """Start container with persistent volume using override file"""
    distro = None
    for family in LINUX_FAMILIES.values():
        if distro_key in family["distributions"]:
            distro = family["distributions"][distro_key]
            break
    
    if not distro:
        return False
    
    # Create temporary docker-compose override for persistent volumes
    override_content = f"""services:
  {distro_key}-vps:
    volumes:
      - {volume_names[0]}:/home/vpsuser/persistent
      - {volume_names[0]}:/var/lib/persistent-data
"""
    
    try:
        with open("docker-compose.override.yml", "w") as f:
            f.write(override_content)
        
        success, _ = run_command(f"docker-compose --profile {distro_key} up -d", capture_output=False)
        return success
    finally:
        # Clean up override file
        if os.path.exists("docker-compose.override.yml"):
            os.remove("docker-compose.override.yml")

def start_vps_environment(family_key: str, distro_key: str, mode: str, state_name: str = "", build_first: bool = False) -> bool:
    """Start VPS environment based on selected mode"""
    family = LINUX_FAMILIES[family_key]
    distro = family["distributions"][distro_key]
    
    print(f"{Colors.GREEN}🚀 Starting VPS Environment...{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*30}{Colors.RESET}")
    print(f"{Colors.WHITE}Family: {family['name']}{Colors.RESET}")
    print(f"{Colors.WHITE}Distribution: {distro['name']}{Colors.RESET}")
    print(f"{Colors.WHITE}Mode: {mode}{Colors.RESET}")
    print(f"{Colors.WHITE}Container: {distro['container']}{Colors.RESET}")
    print()
    
    if mode == "fresh":
        print(f"{Colors.CYAN}🧹 Fresh Install Mode:{Colors.RESET}")
        print(f"{Colors.GRAY}- Clean container (no persistent data){Colors.RESET}")
        print(f"{Colors.GRAY}- Fastest startup{Colors.RESET}")
        print(f"{Colors.GRAY}- All changes lost when stopped{Colors.RESET}")
        print()
        
        # Stop existing container
        run_command(f"docker-compose --profile {distro_key} down")
        
        # Start fresh (no volume mount)
        if build_first:
            run_command(f"docker-compose build {distro['container']}")
        
        success, _ = run_command(f"docker-compose --profile {distro_key} up -d", capture_output=False)
        
    elif mode == "persistent":
        print(f"{Colors.BLUE}💾 Persistent Server Mode:{Colors.RESET}")
        print(f"{Colors.GRAY}- Data persists between sessions{Colors.RESET}")
        print(f"{Colors.GRAY}- Acts like a real VPS{Colors.RESET}")
        print(f"{Colors.GRAY}- Changes saved automatically{Colors.RESET}")
        print()
        
        # Create persistent volume if it doesn't exist
        volume_exists, _ = run_command(f'docker volume ls --format "{{{{.Name}}}}" | findstr {distro["volume"]}')
        if not volume_exists:
            print(f"{Colors.YELLOW}Creating persistent volume: {distro['volume']}{Colors.RESET}")
            run_command(f"docker volume create {distro['volume']}")
        
        # Stop existing container
        run_command(f"docker-compose --profile {distro_key} down")
        
        # Start with persistent volume
        if build_first:
            run_command(f"docker-compose build {distro['container']}")
        
        success = start_persistent_container(distro_key, [distro["volume"]])
        
    elif mode == "upgrade":
        print(f"{Colors.MAGENTA}🔄 Upgrade Mode:{Colors.RESET}")
        print(f"{Colors.GRAY}- Updates existing persistent server{Colors.RESET}")
        print(f"{Colors.GRAY}- Rebuilds image with latest packages{Colors.RESET}")
        print(f"{Colors.GRAY}- Preserves user data and configurations{Colors.RESET}")
        print()
        
        volume_exists, _ = run_command(f'docker volume ls --format "{{{{.Name}}}}" | findstr {distro["volume"]}')
        if not volume_exists:
            print(f"{Colors.RED}❌ No persistent volume found. Use 'persistent' mode first.{Colors.RESET}")
            return False
        
        # Stop container, rebuild, restart with same volume
        run_command(f"docker-compose --profile {distro_key} down")
        print(f"{Colors.YELLOW}Rebuilding with latest packages...{Colors.RESET}")
        run_command(f"docker-compose build --no-cache {distro['container']}")
        
        success = start_persistent_container(distro_key, [distro["volume"]])
        
    elif mode == "snapshot":
        print(f"{Colors.CYAN}📸 Snapshot Mode:{Colors.RESET}")
        print(f"{Colors.GRAY}- Saves current server state{Colors.RESET}")
        print(f"{Colors.GRAY}- Creates named backup for later restore{Colors.RESET}")
        print()
        
        if not state_name:
            state_name = input(f"{Colors.YELLOW}Enter snapshot name: {Colors.RESET}")
        
        snapshot_volume = f"{distro_key}-snapshot-{state_name}"
        
        # Create snapshot by copying persistent volume
        print(f"{Colors.YELLOW}Creating snapshot: {snapshot_volume}{Colors.RESET}")
        run_command(f"docker volume create {snapshot_volume}")
        
        # Copy data from persistent volume to snapshot
        copy_cmd = f'docker run --rm -v "{distro["volume"]}:/source" -v "{snapshot_volume}:/target" alpine sh -c "cp -a /source/. /target/"'
        success, _ = run_command(copy_cmd)
        
        if success:
            print(f"{Colors.GREEN}✅ Snapshot '{state_name}' created successfully!{Colors.RESET}")
        return success
        
    elif mode == "restore":
        print(f"{Colors.YELLOW}📥 Restore Mode:{Colors.RESET}")
        print(f"{Colors.GRAY}- Restores from a previous snapshot{Colors.RESET}")
        print(f"{Colors.GRAY}- Overwrites current persistent data{Colors.RESET}")
        print()
        
        if not state_name:
            snapshots = show_existing_snapshots(distro_key)
            if not snapshots:
                print(f"{Colors.RED}❌ No snapshots available for restore.{Colors.RESET}")
                return False
            
            choice = get_user_choice(f"Select snapshot to restore [1-{len(snapshots)}]", len(snapshots))
            if choice == "back":
                return False
            
            selected_snapshot = snapshots[int(choice) - 1]
            state_name = selected_snapshot.replace(f"{distro_key}-snapshot-", "")
        
        snapshot_volume = f"{distro_key}-snapshot-{state_name}"
        
        # Verify snapshot exists
        snapshot_exists, _ = run_command(f'docker volume ls --format "{{{{.Name}}}}" | findstr {snapshot_volume}')
        if not snapshot_exists:
            print(f"{Colors.RED}❌ Snapshot '{state_name}' not found.{Colors.RESET}")
            return False
        
        # Stop container
        run_command(f"docker-compose --profile {distro_key} down")
        
        # Create/recreate persistent volume
        run_command(f"docker volume rm {distro['volume']}")
        run_command(f"docker volume create {distro['volume']}")
        
        # Restore data from snapshot
        print(f"{Colors.YELLOW}Restoring from snapshot: {state_name}{Colors.RESET}")
        restore_cmd = f'docker run --rm -v "{snapshot_volume}:/source" -v "{distro["volume"]}:/target" alpine sh -c "cp -a /source/. /target/"'
        run_command(restore_cmd)
        
        # Start with restored data
        success = start_persistent_container(distro_key, [distro["volume"]])
    
    if mode != "snapshot":
        # Wait for services to start
        print(f"{Colors.YELLOW}⏳ Waiting for services to initialize...{Colors.RESET}")
        time.sleep(10)
        
        # Check if container is running
        running_success, running_output = run_command(f'docker ps --filter "name={distro["container"]}" --format "{{{{.Names}}}}"')
        
        if running_success and running_output:
            print(f"{Colors.GREEN}✅ Container started successfully!{Colors.RESET}")
            print()
            print(f"{Colors.CYAN}🔗 Connection Information:{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*25}{Colors.RESET}")
            print(f"{Colors.GREEN}SSH: ssh vpsuser@localhost -p {distro['port']}{Colors.RESET}")
            print(f"{Colors.GREEN}Password: vpsuser123{Colors.RESET}")
            print(f"{Colors.BLUE}Mode: {mode}{Colors.RESET}")
            
            if mode in ["persistent", "upgrade", "restore"]:
                print(f"{Colors.BLUE}Persistent Volume: {distro['volume']}{Colors.RESET}")
            print()
            
            print(f"{Colors.CYAN}💡 Quick Commands:{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*18}{Colors.RESET}")
            print(f"{Colors.WHITE}Connect:    python manage-vps.py connect {distro_key}{Colors.RESET}")
            print(f"{Colors.WHITE}Status:     python manage-vps.py status{Colors.RESET}")
            print(f"{Colors.WHITE}Logs:       docker-compose logs -f {distro['container']}{Colors.RESET}")
            print(f"{Colors.WHITE}Stop:       docker-compose --profile {distro_key} down{Colors.RESET}")
            
            if mode in ["persistent", "upgrade"]:
                print(f"{Colors.WHITE}Snapshot:   python advanced-launcher.py --family {family_key} --distribution {distro_key} --mode snapshot --state mybackup{Colors.RESET}")
            
            return True
        else:
            print(f"{Colors.RED}❌ Container failed to start properly!{Colors.RESET}")
            return False
    
    return True

def main():
    """Main function - entry point"""
    parser = argparse.ArgumentParser(description="Advanced VPS Environment Launcher")
    parser.add_argument("--family", help="Linux family key for non-interactive mode")
    parser.add_argument("--distribution", help="Distribution key for non-interactive mode")
    parser.add_argument("--mode", choices=["fresh", "persistent", "upgrade", "snapshot", "restore"],
                       default="fresh", help="Launch mode")
    parser.add_argument("--state", help="State name for snapshot/restore operations")
    parser.add_argument("--build", action="store_true", help="Rebuild containers before starting")
    parser.add_argument("--logs", action="store_true", help="Show logs after starting")
    
    args = parser.parse_args()
    
    # Non-interactive mode
    if args.family and args.distribution:
        if args.family not in LINUX_FAMILIES:
            print(f"{Colors.RED}❌ Unknown family: {args.family}{Colors.RESET}")
            available_families = ", ".join(LINUX_FAMILIES.keys())
            print(f"{Colors.YELLOW}Available families: {available_families}{Colors.RESET}")
            sys.exit(1)
        
        if args.distribution not in LINUX_FAMILIES[args.family]["distributions"]:
            print(f"{Colors.RED}❌ Unknown distribution: {args.distribution} in family {args.family}{Colors.RESET}")
            available_distros = ", ".join(LINUX_FAMILIES[args.family]["distributions"].keys())
            print(f"{Colors.YELLOW}Available distributions: {available_distros}{Colors.RESET}")
            sys.exit(1)
        
        success = start_vps_environment(args.family, args.distribution, args.mode, 
                                      args.state or "", args.build)
        
        if args.logs and success:
            container_name = LINUX_FAMILIES[args.family]["distributions"][args.distribution]["container"]
            run_command(f"docker-compose logs -f {container_name}", capture_output=False)
        return
    
    # Interactive mode
    while True:
        show_header()
        
        # Step 1: Select Mode
        mode_options = show_mode_options()
        mode_choice = get_user_choice(f"Select Mode [1-{len(mode_options)}]", len(mode_options), "q=quit")
        
        if mode_choice == "back":
            continue
        
        selected_mode = mode_options[int(mode_choice) - 1]
        
        # Step 2: Select Linux Family
        show_header()
        print(f"{Colors.GREEN}Selected Mode: {selected_mode}{Colors.RESET}")
        print()
        
        family_keys = show_linux_families()
        family_choice = get_user_choice(f"Select Linux Family [1-{len(family_keys)}]", len(family_keys), "b=back, q=quit")
        
        if family_choice == "back":
            continue
        
        selected_family = family_keys[int(family_choice) - 1]
        
        # Step 3: Select Distribution
        show_header()
        print(f"{Colors.GREEN}Selected Mode: {selected_mode}{Colors.RESET}")
        print(f"{Colors.GREEN}Selected Family: {LINUX_FAMILIES[selected_family]['name']}{Colors.RESET}")
        print()
        
        distro_keys = show_distributions(selected_family)
        distro_choice = get_user_choice(f"Select Distribution [1-{len(distro_keys)}]", len(distro_keys), "b=back, q=quit")
        
        if distro_choice == "back":
            continue
        
        selected_distro = distro_keys[int(distro_choice) - 1]
        
        # Step 4: Handle mode-specific options
        state_name = ""
        if selected_mode == "snapshot":
            state_name = input(f"{Colors.YELLOW}Enter snapshot name: {Colors.RESET}")
        elif selected_mode == "restore":
            snapshots = show_existing_snapshots(selected_distro)
            if not snapshots:
                print(f"{Colors.RED}❌ No snapshots available. Press Enter to continue...{Colors.RESET}")
                input()
                continue
            
            snapshot_choice = get_user_choice(f"Select snapshot [1-{len(snapshots)}]", len(snapshots), "b=back")
            if snapshot_choice == "back":
                continue
            
            state_name = snapshots[int(snapshot_choice) - 1].replace(f"{selected_distro}-snapshot-", "")
        
        # Step 5: Execute
        success = start_vps_environment(selected_family, selected_distro, selected_mode, state_name, args.build)
        
        if success:
            print()
            print(f"{Colors.YELLOW}Press Enter to return to main menu...{Colors.RESET}")
            input()

if __name__ == "__main__":
    main()