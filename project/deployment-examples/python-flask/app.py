from flask import Flask, jsonify, request
import os
import platform
import psutil
import socket
from datetime import datetime
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    """Main endpoint with system information"""
    try:
        # Get system information
        system_info = {
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Get memory information
        memory = psutil.virtual_memory()
        memory_info = {
            'total': f"{memory.total / (1024**3):.2f} GB",
            'available': f"{memory.available / (1024**3):.2f} GB",
            'percent': memory.percent,
            'used': f"{memory.used / (1024**3):.2f} GB"
        }
        
        # Get CPU information
        cpu_info = {
            'count': psutil.cpu_count(),
            'percent': psutil.cpu_percent(interval=1),
            'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
        }
        
        return jsonify({
            'message': 'VPS Flask Application Running Successfully!',
            'status': 'healthy',
            'system': system_info,
            'memory': memory_info,
            'cpu': cpu_info
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get system information',
            'message': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'flask-vps-app'
    })

@app.route('/system')
def system_details():
    """Detailed system information"""
    try:
        # Get Linux distribution info
        distro_info = {}
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        distro_info[key] = value.strip('"')
        except FileNotFoundError:
            distro_info = {'error': 'Cannot read /etc/os-release'}
        
        # Get disk usage
        disk_usage = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': f"{usage.total / (1024**3):.2f} GB",
                    'used': f"{usage.used / (1024**3):.2f} GB",
                    'free': f"{usage.free / (1024**3):.2f} GB",
                    'percent': f"{(usage.used / usage.total) * 100:.1f}%"
                })
            except PermissionError:
                continue
        
        # Get network information
        network_info = {}
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                network_info[interface] = []
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        network_info[interface].append({
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })
        except Exception as e:
            network_info = {'error': str(e)}
        
        return jsonify({
            'distro': distro_info,
            'disk_usage': disk_usage,
            'network': network_info,
            'processes': len(psutil.pids()),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get detailed system information',
            'message': str(e)
        }), 500

@app.route('/test-command', methods=['POST'])
def test_command():
    """Test running system commands (be careful with this in production!)"""
    try:
        data = request.get_json() or {}
        command = data.get('command', 'whoami')
        
        # Whitelist of safe commands for testing
        safe_commands = [
            'whoami', 'pwd', 'date', 'uptime', 'df -h', 'free -h', 
            'ps aux | head -20', 'ls -la', 'cat /etc/os-release',
            'uname -a', 'hostname'
        ]
        
        if command not in safe_commands:
            return jsonify({
                'error': 'Command not allowed',
                'allowed_commands': safe_commands
            }), 400
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        
        return jsonify({
            'command': command,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load-test')
def load_test():
    """Simple endpoint for load testing"""
    import random
    import time
    
    # Simulate some work
    work_duration = random.uniform(0.1, 0.5)
    time.sleep(work_duration)
    
    return jsonify({
        'message': 'Load test endpoint',
        'work_duration': work_duration,
        'timestamp': datetime.now().isoformat(),
        'server': socket.gethostname()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred'
    }), 500

if __name__ == '__main__':
    # Development server (use gunicorn in production)
    app.run(debug=True, host='0.0.0.0', port=5000)