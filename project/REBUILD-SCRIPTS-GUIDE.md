# VPS Rebuild Scripts Usage Guide

This directory contains two scripts to rebuild all VPS Docker images:

## PowerShell Script (Recommended)

**File:** `rebuild-all-vps.ps1`

### Basic Usage
```powershell
# Interactive rebuild (with confirmation)
.\rebuild-all-vps.ps1

# Force rebuild without confirmation  
.\rebuild-all-vps.ps1 -Force

# Clean existing images first, then rebuild
.\rebuild-all-vps.ps1 -Force -CleanFirst

# Build only specific distributions
.\rebuild-all-vps.ps1 -Only "Alpine","Rocky"

# Skip post-build testing
.\rebuild-all-vps.ps1 -Force -SkipTests
```

### Features
- ✅ **Time Estimates:** Shows expected build time for each distribution
- ✅ **Progress Tracking:** Real-time progress updates during builds
- ✅ **Timeout Protection:** Prevents hanging builds (auto-timeout)
- ✅ **Detailed Logging:** Comprehensive success/failure reporting
- ✅ **Post-Build Testing:** Verifies images work after building
- ✅ **Selective Building:** Build only specific distributions
- ✅ **Smart Ordering:** Builds fastest distributions first

### Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| `-Force` | Skip confirmation prompt | `-Force` |
| `-CleanFirst` | Remove existing images before rebuild | `-CleanFirst` |
| `-SkipTests` | Skip post-build functionality tests | `-SkipTests` |
| `-Only` | Build only specified distributions | `-Only "Alpine","Ubuntu"` |

## Batch Script (Simple)

**File:** `rebuild-all-vps.bat`

### Basic Usage
```batch
# Double-click the file or run from command prompt
rebuild-all-vps.bat
```

### Features
- ✅ **Simple Interface:** Basic prompts and confirmations
- ✅ **Time Estimates:** Shows expected build times
- ✅ **Sequential Building:** Builds in optimal order (fastest first)  
- ✅ **Success Tracking:** Counts successful vs failed builds
- ✅ **Final Summary:** Shows built images and sizes

## Build Order & Time Estimates

Both scripts build in this optimal order:

| Order | Distribution | Estimated Time | SSH Port |
|-------|-------------|----------------|----------|
| 1 | Alpine Linux 3.18 | 2-3 minutes | 2205 |
| 2 | Rocky Linux 9 | 1.5-2 minutes | 2206 |
| 3 | CentOS Stream 9 | 4-5 minutes | 2204 |
| 4 | Ubuntu 22.04 LTS | 3-4 minutes | 2203 |
| 5 | Debian 12 Bookworm | 3-4 minutes | 2202 |

**Total Estimated Time:** 15-20 minutes maximum

## Prerequisites

Before running either script:

1. **Docker Desktop** must be running
2. **Sufficient disk space** (≥10GB available)
3. **Working directory** must be the project folder
4. **Network connectivity** for downloading packages

## Troubleshooting

### Common Issues

**"Docker command not found"**
```powershell
# Ensure Docker Desktop is running and PATH is configured
docker --version
```

**"Build timeout" or hanging builds**
```powershell
# Use PowerShell script with timeout protection
.\rebuild-all-vps.ps1 -Force
```

**"Insufficient disk space"**
```powershell
# Clean old Docker data first
docker system prune -a
.\rebuild-all-vps.ps1 -CleanFirst
```

**Individual distribution failures**
```powershell
# Rebuild only failed distributions
.\rebuild-all-vps.ps1 -Only "Debian","Ubuntu"
```

### Manual Rebuilds

If scripts fail, rebuild individual images manually:

```bash
# Alpine (fastest)
docker build -t alpine-vps:latest -f distros/alpine/Dockerfile distros/alpine/

# Rocky Linux
docker build -t rocky-vps:latest -f distros/rocky/Dockerfile distros/rocky/

# CentOS Stream  
docker build -t centos-vps:latest -f distros/centos/Dockerfile distros/centos/

# Ubuntu
docker build -t ubuntu-vps:latest -f distros/ubuntu/Dockerfile distros/ubuntu/

# Debian
docker build -t debian-vps:latest -f distros/debian/Dockerfile distros/debian/
```

## Post-Build Verification

After rebuilding, verify images work:

```powershell
# Check all built images
docker images --filter reference="*-vps:latest"

# Test Alpine VPS (quickest test)
docker run -d --name test-alpine -p 2205:22 alpine-vps:latest
ssh -p 2205 vpsuser@localhost  # Password: vpsuser123

# Clean up test
docker rm -f test-alpine
```

## Integration with Testing

After successful rebuild, update your testing workflow:

1. **Update documentation:** Run todo item "Update VPS documentation"
2. **Test all builds:** Run todo item "Test all VPS builds" 
3. **Verify SSH connectivity:** Use `docs/VPS-TESTING-COMMANDS.md`

---
**Next Steps After Rebuild:**
- Test VPS connectivity: `ssh -p 2202 vpsuser@localhost`
- Check build record: `docs/VPS-BUILD-RECORD.md`  
- Run comprehensive tests: `docs/VPS-TESTING-COMMANDS.md`