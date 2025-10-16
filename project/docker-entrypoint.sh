#!/bin/bash
set -e

# Start supervisor in the background to manage services
echo "Starting Debian Docker Server..."

# Ensure Docker daemon is stopped before starting with supervisor
if pgrep dockerd > /dev/null; then
    echo "Stopping existing Docker daemon..."
    pkill dockerd || true
    sleep 2
fi

# Ensure proper permissions for Docker socket
mkdir -p /var/run
chown root:docker /var/run 2>/dev/null || true

# Create shared directories
mkdir -p /home/serveruser/shared
mkdir -p /home/serveruser/deployments
chown -R serveruser:serveruser /home/serveruser/shared /home/serveruser/deployments

echo "Docker-in-Docker Debian server is ready!"
echo "SSH access: ssh serveruser@localhost -p 2222 (password: serveruser)"
echo "Docker daemon will be available at: tcp://localhost:2376"

# Execute the command passed to the container
exec "$@"