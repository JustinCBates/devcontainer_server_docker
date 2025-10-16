# 🐳 Multi-Distribution VPS Testing Environment

A comprehensive Docker-based testing environment that simulates multiple Linux VPS distributions for local deployment testing. Test your applications across 8 different Linux distributions organized by family, with advanced state management capabilities.

## 🔧 WSL & Docker Desktop Management

**Need to reinstall or optimize Docker Desktop and WSL 2?** Check out our dedicated toolkit:

**📦 [WSL & Docker Desktop Manager](../wsl-and-docker-desktop-manager/)** - Complete automation for:
- 💾 Backing up Docker containers, images, and volumes
- 🗑️ Safely uninstalling Docker Desktop and WSL
- 🚀 Reinstalling WSL 2 with dynamic disk allocation (expandable storage)
- 🐳 Reinstalling Docker Desktop with optimized WSL 2 backend
- 📊 Windows 11 specific optimizations and monitoring tools

Perfect for solving storage issues, performance problems, or when you need a clean slate for Docker and WSL!

## 🎨 TUI Form Designer

**Looking to create beautiful terminal user interfaces?** Check out our TUI development toolkit:

**📦 [TUI Form Designer](../TUI_Form_Designer/)** - Professional TUI development platform:
- 🖼️ Visual form designer for terminal applications
- 🐍 Python-based framework with modern architecture  
- 🎯 Component-based UI system
- 📋 Form validation and data handling
- 🚀 Cross-platform terminal applications

Perfect for creating professional command-line tools and terminal-based applications!

## 🎛️ Multi-Repository Development Workspace

**Want to work with all three projects simultaneously?** Use our integrated VS Code workspace:

**🚀 Open the Workspace**: `multi-repo-workspace.code-workspace`
- 🐳 **VPS Testing Environment** (this repository)
- 🔧 **WSL & Docker Manager** (system management)
- 🎨 **TUI Form Designer** (terminal UI development)

**Quick Start**: File → Open Workspace from File... → `multi-repo-workspace.code-workspace`

## �🚀 **START HERE** - One Script Per Platform

### Windows Users (PowerShell)
```cmd
.\START-WINDOWS.bat
```

### Linux/macOS Users
```bash
./start-linux.sh
```

**That's it!** These are the ONLY two scripts you need to remember for launching the interactive VPS environment.

## 📁 Clean Workspace Structure

```
Root Directory/
├── START-WINDOWS.bat     ← Windows launcher
├── start-linux.sh        ← Linux launcher  
├── docker-compose.yml    ← Docker configuration
├── README.md            ← This documentation
└── project/             ← All other files organized here
    ├── advanced-launcher.py
    ├── organized-family-builder.py
    ├── families/        ← Family-based build system
    ├── distros/         ← Distribution Dockerfiles
    ├── deployment-examples/
    └── ... (build & test scripts)
```

**No more confusion!** Just 4 essential files in the root directory.

## 🎯 Purpose

Perfect for developers who need to:
- **Test deployments** across different Linux distributions locally
- **Validate application compatibility** before production deployment
- **Learn deployment procedures** on various distros without VPS costs
- **Practice server administration** on different Linux families
- **Test automation scripts** across multiple environments
- **Simulate upgrade scenarios** with snapshot and restore capabilities

## � Prerequisites

### Required Software
- **Docker Desktop** - Container runtime
  - Windows: Download from [docker.com](https://docker.com)
  - Enable WSL2 backend for best performance
- **Python 3.6+** - For the launcher scripts
  - Install: `winget install Python.Python.3.12`
  - Or download from [python.org](https://python.org)
- **SSH Client** - For connecting to VPS containers
  - Windows: Built into Windows 10/11
  - Or use PuTTY, Windows Terminal, etc.

### System Requirements
- **RAM**: 4GB+ (8GB recommended for multiple containers)
- **Storage**: 10GB+ free space for container images
- **Network**: Internet access for building containers

## �🐧 Available Distributions

### Debian Family (apt package manager)
| Distribution | SSH Port | Container Name | Volume |
|-------------|----------|----------------|---------|
| Ubuntu 22.04 LTS | 2201 | ubuntu-vps | ubuntu-persistent |
| Debian 12 Bookworm | 2202 | debian-vps | debian-persistent |

### Red Hat Family (yum/dnf package manager)
| Distribution | SSH Port | Container Name | Volume |
|-------------|----------|----------------|---------|
| Rocky Linux 9 | 2203 | rocky-vps | rocky-persistent |
| CentOS Stream 9 | 2204 | centos-vps | centos-persistent |

### Alpine Family (apk package manager)
| Distribution | SSH Port | Container Name | Volume |
|-------------|----------|----------------|---------|
| Alpine Linux 3.18 | 2205 | alpine-vps | alpine-persistent |

### SUSE Family (zypper package manager)
| Distribution | SSH Port | Container Name | Volume |
|-------------|----------|----------------|---------|
| openSUSE Leap 15.5 | 2206 | opensuse-vps | opensuse-persistent |

### Arch Family (pacman package manager)
| Distribution | SSH Port | Container Name | Volume |
|-------------|----------|----------------|---------|
| Arch Linux | 2207 | arch-vps | arch-persistent |
| Slackware 15.0 | 2208 | slackware-vps | slackware-persistent |

## 🚀 Quick Start

### Interactive Launcher (Recommended)
```cmd
# Start the interactive launcher
.\launch-vps.bat

# Or directly with Python
python advanced-launcher.py
```

### Command Line Usage
```cmd
# Fresh Ubuntu container (no persistent data)
python advanced-launcher.py --family debian --distribution ubuntu --mode fresh

# Persistent Rocky Linux server
python advanced-launcher.py --family redhat --distribution rocky --mode persistent

# Create a snapshot
python advanced-launcher.py --family debian --distribution ubuntu --mode snapshot --state backup1

# Restore from snapshot
python advanced-launcher.py --family debian --distribution ubuntu --mode restore --state backup1

# Upgrade existing server
python advanced-launcher.py --family redhat --distribution rocky --mode upgrade
```

### Management Commands
```cmd
# Check status of all VPS containers
python manage-vps.py status

# Connect to a specific VPS
python manage-vps.py connect ubuntu
python manage-vps.py connect rocky

# Stop all VPS containers
python manage-vps.py stop
```

### SSH Access
```bash
# Connect to any VPS (password: vpsuser123)
ssh vpsuser@localhost -p 2201  # Ubuntu
ssh vpsuser@localhost -p 2203  # Rocky Linux
ssh vpsuser@localhost -p 2205  # Alpine Linux
# ... etc
```

## 🎮 Launch Modes

### 🧹 Fresh Install Mode
- **Clean container** with no persistent data
- **Fastest startup** time
- **Perfect for testing** clean deployments
- **All changes lost** when container stops

### 💾 Persistent Server Mode  
- **Data persists** between sessions
- **Acts like a real VPS** with permanent storage
- **Changes saved automatically** to named volumes
- **Ideal for development** and iterative testing

### � Upgrade Mode
- **Updates existing** persistent server
- **Rebuilds image** with latest packages  
- **Preserves user data** and configurations
- **Simulates real server** upgrades

### 📸 Snapshot Mode
- **Saves current server state** to named backup
- **Creates restore points** before major changes
- **Multiple snapshots** per distribution supported
- **Quick rollback capability**

### 📥 Restore Mode
- **Restores from previous snapshots**
- **Overwrites current** persistent data
- **Interactive snapshot selection**
- **Perfect for testing** different configurations

## �🛠️ Each VPS Includes

- **SSH Server** - Full terminal access with key/password auth
- **Docker** - Container runtime for testing deployments  
- **Package Managers** - apt, dnf/yum, apk, zypper, pacman (distro-specific)
- **Development Tools** - git, vim, nano, htop, curl, wget, build-essential
- **Programming Languages** - Python3, Node.js, development libraries
- **System Tools** - systemd, cron, firewall, networking tools
- **User Account** - `vpsuser` with sudo privileges (password: vpsuser123)
- **Persistent Storage** - Optional volumes for data persistence

## 📁 Project Structure

```
.
├── distros/                    # Individual distribution configs
│   ├── ubuntu/Dockerfile      # Ubuntu 22.04 LTS setup
│   ├── debian/Dockerfile      # Debian 12 Bookworm setup  
│   ├── rocky/Dockerfile       # Rocky Linux 9 setup
│   ├── centos/Dockerfile      # CentOS Stream 9 setup
│   ├── alpine/Dockerfile      # Alpine Linux 3.18 setup
│   ├── opensuse/Dockerfile    # openSUSE Leap 15.5 setup
│   ├── arch/Dockerfile        # Arch Linux setup
│   └── slackware/Dockerfile   # Slackware 15.0 setup
├── advanced-launcher.py       # Main Python launcher (interactive & CLI)
├── manage-vps.py             # VPS management utilities
├── launch-vps.bat            # Windows batch launcher
├── vps.bat                   # Quick alias
├── docker-compose.yml        # Multi-VPS orchestration with profiles
└── README.md                 # This file
```
├── stop-server.ps1           # Shutdown script
└── manage-vps.ps1            # VPS management utilities
```

## 🔧 Management Commands

### PowerShell Scripts

```powershell
# List available VPS environments
.\manage-vps.ps1 -Action list

# Check status of all containers
.\manage-vps.ps1 -Action status

# Connect to a specific VPS
.\manage-vps.ps1 -Action connect -Distro ubuntu

# View logs
.\manage-vps.ps1 -Action logs -Service ubuntu-vps

# Restart a service
.\manage-vps.ps1 -Action restart -Service debian-vps

# Rebuild all images
.\manage-vps.ps1 -Action build
```

### Docker Compose Profiles

```bash
# Start specific distributions
docker-compose --profile ubuntu up -d
docker-compose --profile rhel up -d      # Rocky + CentOS
docker-compose --profile testing up -d   # Include test services

# Stop specific distributions
docker-compose --profile debian down
```

## 🧪 Testing Deployments

### Node.js Application Example

1. **Copy example to VPS:**
   ```bash
   ssh vpsuser@localhost -p 2201
   cp -r /home/vpsuser/shared/deployment-examples/nodejs-app ./
   cd nodejs-app
   ```

2. **Deploy:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Test:**
   ```bash
   curl http://localhost:3000
   curl http://localhost:3000/health
   ```

### Python Flask Application Example

1. **Copy example to VPS:**
   ```bash
   ssh vpsuser@localhost -p 2202  # Debian VPS
   cp -r /home/vpsuser/shared/deployment-examples/python-flask ./
   cd python-flask
   ```

2. **Deploy:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Test:**
   ```bash
   curl http://localhost:5000
   curl http://localhost:5000/system
   ```

## 🌐 Network Access

Each VPS has dedicated ports for external access:

### From Your Host Machine
- **Ubuntu**: http://localhost:3001, http://localhost:5001, http://localhost:8001
- **Debian**: http://localhost:3002, http://localhost:5002, http://localhost:8002
- **Rocky**: http://localhost:3003, http://localhost:5003, http://localhost:8003
- **CentOS**: http://localhost:3004, http://localhost:5004, http://localhost:8004
- **Alpine**: http://localhost:3005, http://localhost:5005, http://localhost:8005

### Between VPS Containers
All VPS containers can communicate with each other using:
- Container names: `ubuntu-vps`, `debian-vps`, etc.
- IP addresses: 172.20.0.10, 172.20.0.20, etc.

## 📋 Common Use Cases

### 1. Cross-Distribution Testing
Deploy the same application to multiple distros and compare:
```bash
# Test on Ubuntu
ssh vpsuser@localhost -p 2201
./deploy-app.sh

# Test on Rocky Linux
ssh vpsuser@localhost -p 2203
./deploy-app.sh

# Test on Alpine
ssh vpsuser@localhost -p 2205
./deploy-app.sh
```

### 2. Package Manager Testing
Learn different package managers:
```bash
# Ubuntu/Debian (apt)
sudo apt update && sudo apt install nginx

# Rocky/CentOS (dnf)
sudo dnf install nginx

# Alpine (apk)
sudo apk add nginx
```

### 3. Service Management Testing
Test systemd vs other init systems:
```bash
# Most distros (systemd)
sudo systemctl start nginx
sudo systemctl enable nginx

# Alpine (OpenRC)
sudo rc-service nginx start
sudo rc-update add nginx default
```

### 4. Automation Script Testing
Test deployment automation across distros:
```bash
# Your script should handle different package managers
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y $PACKAGE
elif command -v dnf &> /dev/null; then
    sudo dnf install -y $PACKAGE
elif command -v apk &> /dev/null; then
    sudo apk add $PACKAGE
fi
```

## 🔒 Security Notes

- **Development Only**: This environment is for testing, not production
- **Default Passwords**: All VPS use `vpsuser:vpsuser123` for convenience
- **Privileged Containers**: Required for systemd and Docker-in-Docker
- **Open Ports**: All containers expose multiple ports to localhost only

## 🛠️ Customization

### Adding a New Distribution
1. Create `distros/newdistro/Dockerfile`
2. Add service to `docker-compose.yml`
3. Update port mappings and network settings
4. Add to management scripts

### Modifying VPS Configuration
Each `distros/*/Dockerfile` can be customized to:
- Install additional packages
- Configure services differently
- Add custom users or SSH keys
- Mount additional volumes

### Adding Custom Applications
Place your deployment examples in:
- `deployment-examples/your-app/`
- Include README, deployment scripts, and test files
- Use the shared folder to make them available to all VPS

## 🔄 Cleanup

```powershell
# Stop all containers
.\stop-server.ps1

# Remove all containers and volumes
.\stop-server.ps1 -RemoveVolumes

# Clean up Docker system
docker system prune -a
```

## 💡 Pro Tips

1. **Use VS Code Remote**: Connect VS Code directly to containers for development
2. **Snapshot States**: Use `docker commit` to save configured VPS states
3. **Volume Backups**: Back up important data from Docker volumes
4. **Resource Monitoring**: Use `docker stats` to monitor resource usage
5. **Network Testing**: Test inter-container communication and load balancing

This environment gives you a complete Linux VPS testing lab right on your laptop! 🚀