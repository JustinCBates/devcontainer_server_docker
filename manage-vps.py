#!/usr/bin/env python3
"""
VPS Management Utility
Simple management script for VPS containers
"""

import sys
import subprocess
import argparse
from typing import Tuple

# Linux distribution configurations (simplified for management)
DISTRO_CONFIG = {
    "ubuntu": {"container": "ubuntu-vps", "port": 2201},
    "debian": {"container": "debian-vps", "port": 2202},
    "rocky": {"container": "rocky-vps", "port": 2203},
    "centos": {"container": "centos-vps", "port": 2204},
    "alpine": {"container": "alpine-vps", "port": 2205},
    "opensuse": {"container": "opensuse-vps", "port": 2206},
    "arch": {"container": "arch-vps", "port": 2207},
    "slackware": {"container": "slackware-vps", "port": 2208}
}

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def run_command(command: str, capture_output: bool = True) -> Tuple[bool, str]:
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
        return False, str(e)

def show_status():
    """Show status of all VPS containers"""
    print(f"{Colors.CYAN}VPS Container Status:{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*22}{Colors.RESET}")
    print()
    
    success, output = run_command("docker ps --format \"table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\"")
    
    if success:
        lines = output.split('\n')
        if len(lines) > 1:  # Has header + data
            print(f"{Colors.WHITE}{lines[0]}{Colors.RESET}")  # Header
            for line in lines[1:]:
                if any(distro in line for distro in DISTRO_CONFIG.keys()):
                    if "Up" in line:
                        print(f"{Colors.GREEN}{line}{Colors.RESET}")
                    else:
                        print(f"{Colors.YELLOW}{line}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}No VPS containers are currently running{Colors.RESET}")
    else:
        print(f"{Colors.RED}Error checking container status: {output}{Colors.RESET}")

def connect_to_vps(distro: str):
    """Connect to a VPS via SSH"""
    if distro not in DISTRO_CONFIG:
        print(f"{Colors.RED}Unknown distribution: {distro}{Colors.RESET}")
        print(f"{Colors.YELLOW}Available: {', '.join(DISTRO_CONFIG.keys())}{Colors.RESET}")
        return
    
    config = DISTRO_CONFIG[distro]
    
    # Check if container is running
    success, output = run_command(f'docker ps --filter "name={config["container"]}" --format "{{{{.Names}}}}"')
    
    if not success or not output:
        print(f"{Colors.RED}Container {config['container']} is not running{Colors.RESET}")
        print(f"{Colors.YELLOW}Start it first with: python advanced-launcher.py --family <family> --distribution {distro}{Colors.RESET}")
        return
    
    print(f"{Colors.GREEN}Connecting to {distro} VPS...{Colors.RESET}")
    print(f"{Colors.CYAN}SSH: ssh vpsuser@localhost -p {config['port']}{Colors.RESET}")
    print(f"{Colors.CYAN}Password: vpsuser123{Colors.RESET}")
    print()
    
    # Execute SSH connection
    ssh_command = f"ssh vpsuser@localhost -p {config['port']}"
    subprocess.run(ssh_command, shell=True)

def stop_all_vps():
    """Stop all VPS containers"""
    print(f"{Colors.YELLOW}Stopping all VPS containers...{Colors.RESET}")
    
    success, output = run_command("docker-compose down", capture_output=False)
    
    if success:
        print(f"{Colors.GREEN}All VPS containers stopped{Colors.RESET}")
    else:
        print(f"{Colors.RED}Error stopping containers{Colors.RESET}")

def main():
    parser = argparse.ArgumentParser(description="VPS Management Utility")
    subparsers = parser.add_subparsers(dest='action', help='Available actions')
    
    # Status command
    subparsers.add_parser('status', help='Show status of all VPS containers')
    
    # Connect command
    connect_parser = subparsers.add_parser('connect', help='Connect to a VPS via SSH')
    connect_parser.add_argument('distro', help='Distribution to connect to')
    
    # Stop command
    subparsers.add_parser('stop', help='Stop all VPS containers')
    
    args = parser.parse_args()
    
    if args.action == 'status':
        show_status()
    elif args.action == 'connect':
        connect_to_vps(args.distro)
    elif args.action == 'stop':
        stop_all_vps()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()