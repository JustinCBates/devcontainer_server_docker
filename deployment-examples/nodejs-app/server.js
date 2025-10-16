const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const os = require('os');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.static('public'));

// Routes
app.get('/', (req, res) => {
    const systemInfo = {
        hostname: os.hostname(),
        platform: os.platform(),
        arch: os.arch(),
        release: os.release(),
        uptime: os.uptime(),
        memory: {
            total: Math.round(os.totalmem() / 1024 / 1024) + ' MB',
            free: Math.round(os.freemem() / 1024 / 1024) + ' MB'
        },
        cpus: os.cpus().length,
        loadavg: os.loadavg(),
        timestamp: new Date().toISOString()
    };

    res.json({
        message: 'VPS Test Application Running Successfully!',
        status: 'healthy',
        environment: process.env.NODE_ENV || 'development',
        system: systemInfo
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

app.get('/distro-info', (req, res) => {
    try {
        // Try to read OS release info
        let distroInfo = 'Unknown';
        
        try {
            const osRelease = fs.readFileSync('/etc/os-release', 'utf8');
            const lines = osRelease.split('\n');
            const info = {};
            
            lines.forEach(line => {
                const [key, value] = line.split('=');
                if (key && value) {
                    info[key] = value.replace(/"/g, '');
                }
            });
            
            distroInfo = {
                name: info.NAME || 'Unknown',
                version: info.VERSION || 'Unknown',
                id: info.ID || 'Unknown',
                prettyName: info.PRETTY_NAME || 'Unknown'
            };
        } catch (err) {
            distroInfo = 'Could not read /etc/os-release';
        }

        res.json({
            distro: distroInfo,
            kernel: os.release(),
            hostname: os.hostname()
        });
    } catch (error) {
        res.status(500).json({
            error: 'Failed to get distro info',
            message: error.message
        });
    }
});

app.get('/test-database', (req, res) => {
    // Simulate database connection test
    const dbTests = [
        { name: 'PostgreSQL', port: 5432, status: 'simulated' },
        { name: 'MySQL', port: 3306, status: 'simulated' },
        { name: 'Redis', port: 6379, status: 'simulated' },
        { name: 'MongoDB', port: 27017, status: 'simulated' }
    ];

    res.json({
        message: 'Database connectivity test (simulated)',
        tests: dbTests,
        note: 'This is a simulation. Implement actual database connections as needed.'
    });
});

app.post('/deploy-test', (req, res) => {
    const { service, version } = req.body;
    
    res.json({
        message: 'Deployment test received',
        service: service || 'unknown',
        version: version || '1.0.0',
        deployedAt: new Date().toISOString(),
        server: os.hostname()
    });
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: 'Something went wrong!',
        message: err.message
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        error: 'Not Found',
        message: `Route ${req.originalUrl} not found`
    });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 VPS Test Application running on port ${PORT}`);
    console.log(`📍 Server: ${os.hostname()}`);
    console.log(`🐧 Platform: ${os.platform()} ${os.release()}`);
    console.log(`⏰ Started at: ${new Date().toISOString()}`);
});