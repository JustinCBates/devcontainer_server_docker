#!/bin/bash

# VPS Deployment Script for Python Flask Application
set -e

echo "🐍 Starting VPS deployment of Python Flask application..."
echo "======================================================="

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

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    echo "Installing Python3..."
    
    # Detect package manager and install Python
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v dnf &> /dev/null; then
        # Rocky/CentOS with dnf
        sudo dnf install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        # CentOS with yum
        sudo yum install -y python3 python3-pip
    elif command -v apk &> /dev/null; then
        # Alpine Linux
        sudo apk add python3 py3-pip py3-virtualenv
    else
        echo "❌ Unknown package manager. Please install Python3 manually."
        exit 1
    fi
else
    echo "✅ Python3 is installed: $(python3 --version)"
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not available!"
    exit 1
else
    echo "✅ pip3 is available: $(pip3 --version)"
fi

# Create virtual environment
echo "🏗️ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install application dependencies
echo "📦 Installing application dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p instance

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Test the application first
echo "🧪 Testing application..."
python3 -c "from app import app; print('✅ Application imports successfully')"

# Stop any existing gunicorn processes
echo "🛑 Stopping existing application..."
pkill -f "gunicorn.*flask-vps-app" || echo "No existing processes to stop"
sleep 2

# Start the application with Gunicorn
echo "🚀 Starting application with Gunicorn..."
gunicorn --config gunicorn.conf.py wsgi:application &

# Wait a moment for the application to start
sleep 5

# Check if the application is running
if pgrep -f "gunicorn.*flask-vps-app" > /dev/null; then
    echo "✅ Application is running!"
    
    # Get the process info
    echo ""
    echo "📊 Application Status:"
    echo "====================="
    ps aux | grep -E "(gunicorn.*flask-vps-app|PID)" | head -n 5
    
    echo ""
    echo "✅ Deployment completed successfully!"
    echo ""
    echo "🔗 Application URLs:"
    echo "Local: http://localhost:5000"
    echo "Health check: http://localhost:5000/health"
    echo "System info: http://localhost:5000/system"
    echo ""
    echo "📋 Useful commands:"
    echo "tail -f logs/gunicorn.log     # View logs"
    echo "pkill -f gunicorn             # Stop app"
    echo "source venv/bin/activate      # Activate virtual environment"
    
    # Test the application
    echo "🧪 Testing application..."
    sleep 2
    if curl -f http://localhost:5000/health &>/dev/null; then
        echo "✅ Application is responding to health checks"
    else
        echo "⚠️ Application may not be responding yet (this is normal, try again in a moment)"
    fi
else
    echo "❌ Failed to start application!"
    echo "Check logs/gunicorn.log for details"
    exit 1
fi