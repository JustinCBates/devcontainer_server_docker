# VPS Testing Commands

This document contains essential commands for testing VPS functionality and connectivity.

## SSH Connection

First, connect to your VPS:
```bash
ssh -p 2202 vpsuser@localhost
```
Password: `vpsuser123`

## Repository Connectivity Tests

Run these commands as `vpsuser` to verify your VPS can reach external repositories and services:

### 0. Install Missing Network Tools (if needed)
```bash
# Some minimal containers don't include ping/network tools
sudo apt update
sudo apt install -y iputils-ping net-tools dnsutils traceroute
```

### 1. Test Debian Repositories
```bash
# Update package lists to test repository connectivity
sudo apt update
```

### 2. Test Internet Connectivity  
```bash
# Test connection to Debian package repositories
curl -I https://deb.debian.org
```

### 3. Test Package Installation
```bash
# Install a package to verify repository access
sudo apt install -y neofetch
```

### 4. Test GitHub Connectivity
```bash
# Verify access to GitHub (for git repositories)
curl -I https://github.com
```

### 5. Test Docker Hub Access
```bash
# Test Docker registry connectivity
docker pull hello-world
```

### 6. Basic Network Test
```bash
# Test basic internet connectivity
ping -c 3 8.8.8.8
```

## Additional VPS System Tests

### System Information
```bash
# Display system information
neofetch

# Check system resources
free -h
df -h

# Check running services
sudo systemctl status
```

### Docker Functionality
```bash
# List Docker images
docker images

# List running containers
docker ps

# Test Docker functionality
docker run --rm hello-world
```

### Network Configuration
```bash
# Check network interfaces
ip addr show

# Check listening ports
sudo netstat -tlnp

# Check firewall status
sudo ufw status
```

## VPS Administration Tests

### User and Permissions
```bash
# Check current user
whoami

# Check sudo permissions
sudo -l

# Check user groups
groups
```

### File System Tests
```bash
# Create test directories
mkdir ~/test-project
cd ~/test-project

# Create test files
echo "Hello VPS World!" > test.txt
cat test.txt

# Test file permissions
chmod 755 test.txt
ls -la test.txt
```

### Service Management
```bash
# Check SSH service
sudo systemctl status ssh

# Check cron service  
sudo systemctl status cron

# View system logs
sudo journalctl --since "1 hour ago" --no-pager
```

## Expected Results

When all tests pass, you should see:

- ✅ `apt update` completes successfully
- ✅ `curl` commands return HTTP 200 responses
- ✅ Package installation works without errors
- ✅ Docker pulls images successfully
- ✅ Network connectivity to external services
- ✅ All system services running normally

## Troubleshooting

If any tests fail:

1. **"Command not found" errors**: Install missing tools with `sudo apt install -y iputils-ping net-tools dnsutils`
2. **Repository Access Issues**: Check DNS resolution and internet connectivity
3. **Permission Errors**: Ensure user has proper sudo access
4. **Docker Issues**: Verify Docker daemon is running (`sudo systemctl status docker`)
5. **Network Problems**: Check container network configuration

## Quick Test Script

Save this as a script to run all tests at once:

```bash
#!/bin/bash
echo "=== VPS Connectivity Test Suite ==="
echo "1. Testing repositories..."
sudo apt update > /dev/null 2>&1 && echo "✅ Repositories OK" || echo "❌ Repository access failed"

echo "2. Testing internet..."
curl -s -I https://deb.debian.org > /dev/null 2>&1 && echo "✅ Internet OK" || echo "❌ Internet access failed"

echo "3. Testing GitHub..."
curl -s -I https://github.com > /dev/null 2>&1 && echo "✅ GitHub OK" || echo "❌ GitHub access failed"

echo "4. Testing Docker Hub..."
docker pull hello-world > /dev/null 2>&1 && echo "✅ Docker Hub OK" || echo "❌ Docker Hub access failed"

echo "5. Testing DNS..."
ping -c 1 8.8.8.8 > /dev/null 2>&1 && echo "✅ DNS OK" || echo "❌ DNS resolution failed"

echo "=== Test Complete ==="
```

---

*Last updated: October 19, 2025*
*VPS Environment: Debian 12 (Bookworm)*