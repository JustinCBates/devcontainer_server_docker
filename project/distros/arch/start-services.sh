#!/bin/bash
set -e

# Start Docker daemon in background
dockerd &

# Start SSH daemon
/usr/sbin/sshd -D &

# Start cron
crond &

# Keep container running
tail -f /dev/null