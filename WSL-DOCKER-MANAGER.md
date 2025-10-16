# 🔧 WSL & Docker Desktop Management

This folder contains the **WSL & Docker Desktop Manager** - a dedicated toolkit for managing your Docker and WSL 2 installation on Windows 11.

## 🚀 Quick Access

```powershell
# Navigate to the management tools (from LocalRepos directory)
cd ..\wsl-and-docker-desktop-manager

# Or from devcontainer_server_docker directory
cd ..\..\wsl-and-docker-desktop-manager

# Run the complete reinstallation process
.\MASTER-REINSTALL.ps1 -Phase all

# Or run individual phases
.\MASTER-REINSTALL.ps1 -Phase backup
.\MASTER-REINSTALL.ps1 -Phase uninstall-docker  
.\MASTER-REINSTALL.ps1 -Phase uninstall-wsl
.\MASTER-REINSTALL.ps1 -Phase install-wsl
.\MASTER-REINSTALL.ps1 -Phase install-docker
.\MASTER-REINSTALL.ps1 -Phase restore
```

## 📋 What It Does

- **💾 Backup**: All Docker containers, images, and volumes
- **🗑️ Uninstall**: Complete removal of Docker Desktop and WSL
- **🔧 Reinstall**: WSL 2 with dynamic disk allocation (expandable storage)
- **🐳 Optimize**: Docker Desktop with WSL 2 backend for better performance
- **📊 Monitor**: Built-in tools for system monitoring and maintenance

## 🎯 Perfect For

- **Storage Issues**: When Docker runs out of disk space
- **Performance Problems**: Slow Docker or WSL performance
- **Clean Installation**: Starting fresh with optimized settings
- **Windows 11 Optimization**: Taking advantage of latest features

## 📖 Documentation

See the complete guide in the `wsl-and-docker-desktop-manager` folder:
- **README.md** - Full documentation and Windows 11 optimizations
- **COMPLETE-REINSTALL-GUIDE.md** - Step-by-step process guide
- **CHANGELOG.md** - Version history and updates

## 🔗 Repository

This toolkit is maintained in a separate repository:
**https://github.com/JustinCBates/wsl-and-docker-desktop-manager**

---
*This toolkit was created to solve common Docker Desktop and WSL storage and performance issues on Windows 11.*