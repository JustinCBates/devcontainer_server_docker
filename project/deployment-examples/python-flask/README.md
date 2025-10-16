# Python Flask Application Deployment Test

This example demonstrates deploying a Python Flask application to different Linux distributions.

## Files
- `requirements.txt` - Python dependencies
- `app.py` - Flask application
- `wsgi.py` - WSGI entry point
- `deploy.sh` - Deployment script
- `gunicorn.conf.py` - Gunicorn configuration

## Test on Different Distros

### Ubuntu/Debian (apt-based)
```bash
# SSH into Ubuntu VPS
ssh vpsuser@localhost -p 2201

# Copy files and deploy
cp -r /home/vpsuser/shared/deployment-examples/python-flask ./
cd python-flask
bash deploy.sh
```

### Rocky/CentOS (dnf/yum-based)
```bash
# SSH into Rocky VPS
ssh vpsuser@localhost -p 2203

# Copy files and deploy
cp -r /home/vpsuser/shared/deployment-examples/python-flask ./
cd python-flask
bash deploy.sh
```

### Alpine (apk-based)
```bash
# SSH into Alpine VPS
ssh vpsuser@localhost -p 2205

# Copy files and deploy
cp -r /home/vpsuser/shared/deployment-examples/python-flask ./
cd python-flask
bash deploy.sh
```

## Testing
After deployment on any distro:
- Application runs on port 5000
- Access via http://localhost:500X (where X is the distro-specific port)
- API endpoints available for testing