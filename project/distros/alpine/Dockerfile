# Alpine Linux VPS Simulation (Lightweight)
FROM alpine:3.18

# Install common VPS packages
RUN apk update && apk add --no-cache \
    openssh \
    sudo \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    unzip \
    bash \
    shadow \
    rsyslog \
    dcron \
    logrotate \
    iptables \
    fail2ban \
    python3 \
    py3-pip \
    nodejs \
    npm \
    build-base \
    docker \
    docker-compose \
    && rm -rf /var/cache/apk/*

# Create VPS user
RUN adduser -D -s /bin/bash vpsuser \
    && echo "vpsuser:vpsuser123" | chpasswd \
    && adduser vpsuser wheel \
    && adduser vpsuser docker \
    && echo "vpsuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH
RUN ssh-keygen -A \
    && echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config \
    && echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config \
    && echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config

# Create startup script
COPY start-services.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-services.sh

# Set up working directory
WORKDIR /home/vpsuser
RUN chown vpsuser:vpsuser /home/vpsuser

# Create common directories
RUN mkdir -p /home/vpsuser/{projects,deployments,logs,backups} \
    && chown -R vpsuser:vpsuser /home/vpsuser

# Expose common VPS ports
EXPOSE 22 80 443 3000 5000 8000 8080 8443 9000

# Start services
CMD ["/usr/local/bin/start-services.sh"]