# SUSE Family Configuration
# openSUSE distribution using zypper package manager

family_name = "SUSE Family"
package_manager = "zypper"
description = "SUSE-based distributions with zypper package management"

distributions = {
    "opensuse": {
        "name": "openSUSE Leap 15.5",
        "description": "Stable, professional-grade Linux distribution",
        "container": "opensuse-vps",
        "port": 2206,
        "volume": "opensuse-persistent",
        "dockerfile_path": "../distros/suse",
        "representative": True  # This is the family representative
    }
}

# Family-specific build commands
build_commands = [
    "zypper refresh",
    "zypper update -y",
    "zypper install -y curl wget git vim nano"
]

# Family-specific test commands
test_commands = [
    "zypper --version",
    "rpm --version",
    "systemctl --version"
]

# SSH configuration
ssh_config = {
    "user": "vpsuser",
    "password": "vpsuser123",
    "default_shell": "/bin/bash"
}