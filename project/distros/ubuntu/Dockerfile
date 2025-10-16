# Ubuntu VPS Simulation
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install common VPS packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    systemd \
    systemd-sysv \
    rsyslog \
    cron \
    logrotate \
    ufw \
    fail2ban \
    python3 \
    python3-pip \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Docker (common on VPS)
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# Create VPS user
RUN useradd -m -s /bin/bash vpsuser \
    && echo "vpsuser:vpsuser123" | chpasswd \
    && usermod -aG sudo,docker vpsuser \
    && echo "vpsuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH
RUN mkdir /var/run/sshd \
    && echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config \
    && echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config \
    && echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config \
    && echo 'Port 22' >> /etc/ssh/sshd_config

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