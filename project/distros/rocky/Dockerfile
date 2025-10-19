# Rocky Linux VPS Simulation (RHEL-based)
FROM rockylinux:9

# Install EPEL repository and common VPS packages
RUN dnf update -y && dnf install -y epel-release \
    && dnf install -y --allowerasing \
    openssh-server \
    sudo \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    unzip \
    yum-utils \
    device-mapper-persistent-data \
    lvm2 \
    systemd \
    rsyslog \
    cronie \
    logrotate \
    firewalld \
    python3 \
    python3-pip \
    nodejs \
    npm \
    gcc \
    gcc-c++ \
    make \
    && dnf clean all

# Install Docker
RUN dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo \
    && dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin \
    && dnf clean all

# Create VPS user
RUN useradd -m -s /bin/bash vpsuser \
    && echo "vpsuser:vpsuser123" | chpasswd \
    && usermod -aG wheel,docker vpsuser \
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