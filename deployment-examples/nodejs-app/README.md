# Node.js Express Application Deployment Test

This example demonstrates deploying a Node.js Express application to different Linux distributions.

## Files
- `package.json` - Node.js dependencies
- `server.js` - Express server
- `deploy.sh` - Deployment script
- `test-deployment.sh` - Testing script

## Test on Different Distros

### Ubuntu/Debian (apt-based)
```bash
# SSH into Ubuntu VPS
ssh vpsuser@localhost -p 2201

# Copy files
cp -r /home/vpsuser/shared/deployment-examples/nodejs-app ./
cd nodejs-app

# Install Node.js (if not already installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Deploy
bash deploy.sh
```

### Rocky/CentOS (dnf/yum-based)
```bash
# SSH into Rocky VPS
ssh vpsuser@localhost -p 2203

# Copy files
cp -r /home/vpsuser/shared/deployment-examples/nodejs-app ./
cd nodejs-app

# Install Node.js (if not already installed)
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo dnf install -y nodejs npm

# Deploy
bash deploy.sh
```

### Alpine (apk-based)
```bash
# SSH into Alpine VPS
ssh vpsuser@localhost -p 2205

# Copy files
cp -r /home/vpsuser/shared/deployment-examples/nodejs-app ./
cd nodejs-app

# Install Node.js (if not already installed)
sudo apk add nodejs npm

# Deploy
bash deploy.sh
```

## Testing
After deployment on any distro:
- Application runs on port 3000
- Access via http://localhost:300X (where X is the distro-specific port)
- Check logs with `pm2 logs` or `docker logs`