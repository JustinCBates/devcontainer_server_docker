# VPS Build Configuration Record

This document maintains a comprehensive record of all VPS build configurations, settings, and specifications.

## Build Summary (as of October 19, 2025)

| Distribution | Base Image | Size | SSH Port | Status | Build Time |
|-------------|------------|------|----------|--------|------------|
| Debian 12 | debian:bookworm-slim | ~2.16GB* | 2202 | ✅ Built | ~3-4 min |
| Ubuntu 22.04 LTS | ubuntu:22.04 | 2.07GB | 2203 | ✅ Built | ~3-4 min |
| CentOS Stream 9 | quay.io/centos/centos:stream9 | 1.77GB | 2204 | ✅ Built | ~4-5 min |
| Alpine Linux 3.18 | alpine:3.18 | 1.02GB | 2205 | ✅ Built | ~2-3 min |
| Rocky Linux 9 | rockylinux:9 | 1.91GB | 2206 | ✅ Built | ~1.5 min |
| Slackware | slackware:15.0 | TBD | 2207 | 🔄 Pending | Est. 4-6 min |
| Arch Linux | archlinux:latest | TBD | 2208 | ❌ Failed | Package conflicts |
| openSUSE Leap | opensuse/leap:15.5 | TBD | 2209 | ❌ Failed | User group issues |

*Size estimated from previous build; image may have been cleaned up

## Detailed Build Configurations

### 1. Debian 12 (Bookworm) VPS
**Base Image:** `debian:bookworm-slim`
**Package Manager:** apt
**Key Packages:** openssh-server, sudo, curl, wget, git, vim, htop, systemd, rsyslog, docker-ce
**SSH Config:** PermitRootLogin yes, PasswordAuthentication yes
**Users:** root (root123), vpsuser (vpsuser123)
**Special Features:** 
- Docker-in-Docker enabled
- Full systemd support
- UFW firewall
- Fail2ban security

### 2. Ubuntu 22.04 LTS VPS  
**Base Image:** `ubuntu:22.04`
**Package Manager:** apt
**Key Packages:** openssh-server, sudo, curl, wget, git, vim, htop, systemd, rsyslog, docker-ce
**SSH Config:** PermitRootLogin yes, PasswordAuthentication yes
**Users:** root (root123), vpsuser (vpsuser123)
**Special Features:**
- Docker-in-Docker enabled
- Full systemd support
- UFW firewall
- Fail2ban security
- Same package set as Debian but Ubuntu base

### 3. CentOS Stream 9 VPS
**Base Image:** `quay.io/centos/centos:stream9`
**Package Manager:** dnf
**Key Packages:** openssh-server, sudo, curl, wget, git, vim, htop, systemd, rsyslog, docker-ce
**SSH Config:** PermitRootLogin yes, PasswordAuthentication yes
**Users:** root (root123), vpsuser (vpsuser123)
**Special Features:**
- EPEL repository enabled
- Docker-in-Docker enabled
- FirewallD instead of UFW
- Uses `--allowerasing` flag for curl conflicts

### 4. Alpine Linux 3.18 VPS (Lightweight)
**Base Image:** `alpine:3.18`
**Package Manager:** apk
**Key Packages:** openssh, sudo, curl, wget, git, vim, htop, bash, rsyslog, docker
**SSH Config:** PermitRootLogin yes, PasswordAuthentication yes
**Users:** root (root123), vpsuser (vpsuser123)
**Special Features:**
- Smallest image size (1.02GB)
- Uses musl libc instead of glibc
- Built-in Docker and docker-compose
- dcron instead of standard cron
- Shadow package for user management

### 5. Rocky Linux 9 VPS (RHEL-based)
**Base Image:** `rockylinux:9`
**Package Manager:** dnf
**Key Packages:** openssh-server, sudo, curl, wget, git, vim, htop, systemd, rsyslog, docker-ce
**SSH Config:** PermitRootLogin yes, PasswordAuthentication yes  
**Users:** root (root123), vpsuser (vpsuser123)
**Special Features:**
- EPEL repository enabled
- Docker-in-Docker enabled
- FirewallD configuration
- Uses `--allowerasing` flag for curl conflicts
- RHEL-compatible enterprise features

## Common Build Patterns

### Standard User Setup (All Distributions)
```bash
# Create vpsuser with home directory
useradd -m -s /bin/bash vpsuser
echo "vpsuser:vpsuser123" | chpasswd

# Add to appropriate groups (varies by distro)
# Debian/Ubuntu: sudo, docker
# CentOS/Rocky: wheel, docker  
# Alpine: wheel, docker
usermod -aG [groups] vpsuser
```

### SSH Configuration (All Distributions)
```bash
# Generate SSH host keys
ssh-keygen -A

# Configure SSH daemon
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config
```

### Docker Installation Patterns

**Debian/Ubuntu Family:**
```bash
# Add Docker's official GPG key and repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io
```

**RHEL Family (CentOS/Rocky):**
```bash  
# Add Docker repository and install
dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
dnf install -y docker-ce docker-ce-cli containerd.io
```

**Alpine:**
```bash
# Docker is available in main repository
apk add docker docker-compose
```

## VPS Simulation Settings

### Hostname Configuration
Each VPS gets a unique hostname:
- Debian: `vps-debian-01`
- Ubuntu: `vps-ubuntu-01`  
- CentOS: `vps-centos-01`
- Alpine: `vps-alpine-01`
- Rocky: `vps-rocky-01`

### Mock IP Addresses (for documentation)
- Debian: 192.168.100.10
- Ubuntu: 192.168.100.11
- CentOS: 192.168.100.12
- Alpine: 192.168.100.13
- Rocky: 192.168.100.14

### Port Mappings
- SSH ports: 2202-2209 (mapped to container port 22)
- Web ports: 8080-8087 (mapped to container port 80)
- Each VPS gets consecutive ports for easy management

## Build Troubleshooting

### Known Issues and Solutions

**RHEL Family (CentOS/Rocky) - Curl Conflicts:**
```dockerfile
# Solution: Use --allowerasing flag
RUN dnf install -y --allowerasing curl
```

**Arch Linux - Package Naming:**
```dockerfile
# Issue: rsyslog not available
# Solution: Use syslog-ng instead
RUN pacman -S --noconfirm syslog-ng
```

**openSUSE - User Groups:**
```dockerfile
# Issue: wheel group configuration
# Solution: Use users group or configure wheel properly
```

## Performance Metrics

### Build Times (Approximate)
- Alpine: Fastest (2-3 minutes) - minimal packages
- Rocky: Fast (1.5-2 minutes) - cached layers
- CentOS: Medium (4-5 minutes) - RHEL complexity
- Debian/Ubuntu: Medium (3-4 minutes) - comprehensive packages
- Slackware: Slowest (4-6 minutes estimated) - package complexity

### Image Sizes
- Alpine: Smallest (1.02GB) - musl-based, minimal
- Rocky: Compact (1.91GB) - efficient RHEL
- CentOS: Medium (1.77GB) - standard RHEL
- Ubuntu: Large (2.07GB) - comprehensive packages
- Debian: Large (~2.16GB) - full feature set

## Testing Validation

Each built VPS is tested for:
1. SSH connectivity on assigned port
2. User authentication (root and vpsuser)
3. Docker-in-Docker functionality  
4. Network tool availability
5. Package manager functionality
6. Service management (systemd/init)

## Maintenance Notes

- Images should be rebuilt periodically for security updates
- Test network connectivity after each build
- Verify SSH access before marking as complete
- Document any package conflicts for future builds
- Keep build times under 6 minutes for user experience

---
*Last Updated: October 19, 2025*
*Next Review: When all 8 distributions are built and tested*