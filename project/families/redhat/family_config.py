# Red Hat Family Configuration
# Rocky Linux and CentOS distributions using dnf/yum package manager

family_name = "Red Hat Family"
package_manager = "dnf"
description = "RHEL-based distributions with dnf/yum package management"

distributions = {
    "rocky": {
        "name": "Rocky Linux 9",
        "description": "Enterprise-grade RHEL alternative",
        "container": "rocky-vps",
        "port": 2203,
        "volume": "rocky-persistent",
        "dockerfile_path": "../distros/rocky",
        "representative": True  # This is the family representative
    },
    "centos": {
        "name": "CentOS Stream 9",
        "description": "Community Enterprise Operating System",
        "container": "centos-vps",
        "port": 2204,
        "volume": "centos-persistent",
        "dockerfile_path": "../distros/centos",
        "representative": False
    }
}

# Family-specific build commands
build_commands = [
    "dnf update -y",
    "dnf upgrade -y",
    "dnf install -y curl wget git vim nano"
]

# Family-specific test commands
test_commands = [
    "dnf --version",
    "rpm --version",
    "systemctl --version"
]

# SSH configuration
ssh_config = {
    "user": "vpsuser",
    "password": "vpsuser123",
    "default_shell": "/bin/bash"
}