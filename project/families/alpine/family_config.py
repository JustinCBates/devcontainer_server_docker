# Alpine Family Configuration  
# Alpine Linux distribution using apk package manager

family_name = "Alpine Family"
package_manager = "apk"
description = "Lightweight distributions with apk package management"

distributions = {
    "alpine": {
        "name": "Alpine Linux 3.18",
        "description": "Security-oriented, lightweight Linux distribution",
        "container": "alpine-vps",
        "port": 2205,
        "volume": "alpine-persistent",
        "dockerfile_path": "../distros/alpine",
        "representative": True  # This is the family representative
    }
}

# Family-specific build commands
build_commands = [
    "apk update",
    "apk upgrade",
    "apk add curl wget git vim nano"
]

# Family-specific test commands
test_commands = [
    "apk --version",
    "busybox --version",
    "rc-service --version"
]

# SSH configuration
ssh_config = {
    "user": "vpsuser",
    "password": "vpsuser123",
    "default_shell": "/bin/ash"
}