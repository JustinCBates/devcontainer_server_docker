# Debian Family Configuration
# Ubuntu and Debian distributions using apt package manager

family_name = "Debian Family"
package_manager = "apt"
description = "Debian-based distributions with apt package management"

distributions = {
    "ubuntu": {
        "name": "Ubuntu 22.04 LTS",
        "description": "Popular, user-friendly Ubuntu distribution",
        "container": "ubuntu-vps",
        "port": 2201,
        "volume": "ubuntu-persistent",
        "dockerfile_path": "../distros/ubuntu",
        "representative": True  # This is the family representative
    },
    "debian": {
        "name": "Debian 12 (Bookworm)",
        "description": "Stable Debian base distribution",
        "container": "debian-vps",
        "port": 2202,
        "volume": "debian-persistent",
        "dockerfile_path": "../distros/debian",
        "representative": False
    }
}

# Family-specific build commands
build_commands = [
    "apt-get update",
    "apt-get upgrade -y",
    "apt-get install -y curl wget git vim nano"
]

# Family-specific test commands
test_commands = [
    "apt --version",
    "dpkg --version",
    "systemctl --version"
]

# SSH configuration
ssh_config = {
    "user": "vpsuser",
    "password": "vpsuser123",
    "default_shell": "/bin/bash"
}