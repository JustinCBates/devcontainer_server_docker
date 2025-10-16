#!/bin/bash

# VPS Deployment Script for Node.js Application
set -e

echo "🚀 Starting VPS deployment of Node.js application..."
echo "=================================================="

# Check if we're running as the correct user
if [ "$USER" != "vpsuser" ]; then
    echo "⚠️  Warning: Not running as vpsuser. Current user: $USER"
fi

# Get system information
echo "📋 System Information:"
echo "Hostname: $(hostname)"
echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"')"
echo "Architecture: $(uname -m)"
echo "Kernel: $(uname -r)"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Installing Node.js..."
    
    # Detect package manager and install Node.js
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif command -v dnf &> /dev/null; then
        # Rocky/CentOS with dnf
        curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
        sudo dnf install -y nodejs npm
    elif command -v yum &> /dev/null; then
        # CentOS with yum
        curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
        sudo yum install -y nodejs npm
    elif command -v apk &> /dev/null; then
        # Alpine Linux
        sudo apk add nodejs npm
    else
        echo "❌ Unknown package manager. Please install Node.js manually."
        exit 1
    fi
else
    echo "✅ Node.js is installed: $(node --version)"
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not available!"
    exit 1
else
    echo "✅ npm is available: $(npm --version)"
fi

# Install PM2 globally if not present
if ! command -v pm2 &> /dev/null; then
    echo "📦 Installing PM2 process manager..."
    sudo npm install -g pm2
else
    echo "✅ PM2 is available: $(pm2 --version)"
fi

# Install application dependencies
echo "📦 Installing application dependencies..."
npm install

# Create logs directory
mkdir -p logs

# Stop existing PM2 process if running
echo "🛑 Stopping existing application..."
pm2 stop vps-test-app 2>/dev/null || echo "No existing process to stop"
pm2 delete vps-test-app 2>/dev/null || echo "No existing process to delete"

# Start the application with PM2
echo "🚀 Starting application with PM2..."
pm2 start server.js --name vps-test-app --log ./logs/app.log --error ./logs/error.log

# Save PM2 process list
pm2 save

# Setup PM2 to start on boot (optional)
echo "⚙️ Setting up PM2 startup script..."
pm2 startup 2>/dev/null | grep -E "sudo env|sudo systemctl" | bash || echo "PM2 startup setup skipped (may need manual configuration)"

# Show application status
echo ""
echo "📊 Application Status:"
echo "====================="
pm2 status

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🔗 Application URLs:"
echo "Local: http://localhost:3000"
echo "Health check: http://localhost:3000/health"
echo "System info: http://localhost:3000/distro-info"
echo ""
echo "📋 Useful commands:"
echo "pm2 logs vps-test-app    # View logs"
echo "pm2 restart vps-test-app # Restart app"
echo "pm2 stop vps-test-app    # Stop app"
echo "pm2 monit               # Monitor processes"

# Test the application
echo "🧪 Testing application..."
sleep 3
if curl -f http://localhost:3000/health &>/dev/null; then
    echo "✅ Application is responding to health checks"
else
    echo "⚠️ Application may not be responding yet (this is normal, try again in a moment)"
fi