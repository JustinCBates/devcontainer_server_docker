#!/bin/bash
set -e

# Start Docker daemon in background
dockerd &

# Start SSH daemon
/usr/sbin/sshd -D &

# Start cron
service cron start &

# Keep container running
tail -f /dev/null