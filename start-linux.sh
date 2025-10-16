#!/bin/bash
# ==============================================================================
#              VPS ENVIRONMENT LAUNCHER FOR LINUX/macOS
# ==============================================================================
# This is THE script to run from Linux/macOS to start the VPS environment
# Usage: ./start-linux.sh
# ==============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${BLUE}"
    echo "================================================================"
    echo "                VPS ENVIRONMENT LAUNCHER"
    echo "                   Linux/macOS Version"
    echo "================================================================"
    echo -e "${NC}"
}

# Function to check for Python
check_python() {
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}Found Python3${NC}"
        return 0
    elif command -v python &> /dev/null; then
        echo -e "${GREEN}Found Python${NC}"
        return 1
    else
        echo -e "${RED}ERROR: Python not found${NC}"
        echo ""
        echo "Please install Python 3.6+ using your package manager:"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3"
        echo "  CentOS/RHEL:   sudo yum install python3"
        echo "  macOS:         brew install python3"
        echo ""
        exit 1
    fi
}

# Main execution
clear
print_header

echo -e "${YELLOW}Starting the interactive VPS environment launcher...${NC}"
echo ""

# Check Python and run launcher
if check_python; then
    python3 project/advanced-launcher.py "$@"
else
    python project/advanced-launcher.py "$@"
fi

echo ""
echo "Press any key to exit..."
read -n 1