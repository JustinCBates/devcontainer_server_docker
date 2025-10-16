# Debian server with Docker-in-Docker capability
FROM debian:bookworm-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV DOCKER_VERSION=24.0.7

# Install system dependencies
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    supervisor \
    openssh-server \
    sudo \
    vim \
    git \
    htop \
    net-tools \
    iputils-ping \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Add Docker's official GPG key and repository
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
RUN apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with sudo privileges
RUN useradd -m -s /bin/bash serveruser \
    && echo "serveruser:serveruser" | chpasswd \
    && usermod -aG sudo,docker serveruser \
    && echo "serveruser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH
RUN mkdir /var/run/sshd \
    && echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config \
    && echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config \
    && echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config

# Create supervisor configuration
RUN mkdir -p /var/log/supervisor

# Copy configuration files
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Create directories for Docker socket and data
RUN mkdir -p /var/lib/docker

# Expose ports
EXPOSE 22 2376 80 443 8080 8443 3000 5000

# Set working directory
WORKDIR /home/serveruser

# Switch to non-root user for safety
USER serveruser

# Entry point
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]