# Slackware Linux VPS Simulation
FROM vbatts/slackware:current

# Install common packages (Slackware uses different package management)
RUN slackpkg -default_answer=y -batch=on update && \
    slackpkg -default_answer=y -batch=on install openssh curl wget git vim nano htop \
    && slackpkg -default_answer=y -batch=on install python3 \
    && slackpkg clean-system

# Install additional tools manually
RUN curl -fsSL https://get.docker.com | sh || true

# Create VPS user
RUN useradd -m -s /bin/bash vpsuser \
    && echo "vpsuser:vpsuser123" | chpasswd \
    && usermod -aG wheel vpsuser \
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