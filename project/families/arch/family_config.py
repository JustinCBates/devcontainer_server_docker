# Arch Family Configuration
# Arch Linux and Slackware distributions using pacman package manager

family_name = "Arch Family"
package_manager = "pacman"
description = "Rolling release distributions with pacman package management"

distributions = {
    "arch": {
        "name": "Arch Linux",
        "description": "Lightweight, flexible rolling release distribution",
        "container": "arch-vps",
        "port": 2207,
        "volume": "arch-persistent",
        "dockerfile_path": "../distros/arch",
        "representative": True  # This is the family representative
    },
    "slackware": {
        "name": "Slackware 15.0",
        "description": "One of the oldest Linux distributions",
        "container": "slackware-vps",
        "port": 2208,
        "volume": "slackware-persistent",
        "dockerfile_path": "../distros/slackware",
        "representative": False
    }
}

# Family-specific build commands
build_commands = [
    "pacman -Sy",
    "pacman -Su --noconfirm",
    "pacman -S --noconfirm curl wget git vim nano"
]

# Family-specific test commands
test_commands = [
    "pacman --version",
    "systemctl --version"
]

# SSH configuration
ssh_config = {
    "user": "vpsuser",
    "password": "vpsuser123",
    "default_shell": "/bin/bash"
}