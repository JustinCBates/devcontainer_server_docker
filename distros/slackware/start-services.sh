#!/bin/bash
set -e

# Start Docker daemon in background (if available)
dockerd &

# Start SSH daemon
/usr/sbin/sshd -D &

# Start cron
cron &

# Keep container running
tail -f /dev/null