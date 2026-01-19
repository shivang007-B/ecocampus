# 🚀 EcoCampus - Complete Deployment Guide

This document provides everything you need to deploy and run the EcoCampus application in production and development environments.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Troubleshooting](#troubleshooting)
6. [Performance Tuning](#performance-tuning)

---

## 📦 Prerequisites

### Minimum Requirements

- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18+)
- **Python**: 3.11+
- **Node.js**: 18+
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 500MB free space

### Optional Requirements

- **PostgreSQL**: 13+ (for production)
- **Redis**: 7+ (for caching)
- **Docker**: 20+ (for containerized deployment)
- **Nginx**: (for reverse proxy in production)

---

## 🛠️ Development Setup

### Windows Setup

#### Step 1: Prerequisites Installation

```bash
# Install Python 3.11+
# Download from: https://www.python.org/downloads/

# Install Node.js 18+
# Download from: https://nodejs.org/

# Verify installations
python --version
node --version
npm --version
```

#### Step 2: Clone/Extract Project

```bash
# Extract the project folder
cd ecocampus
```

#### Step 3: Automated Setup

```bash
# Run automated setup
python setup.py
```

#### Step 4: Manual Setup (if needed)

```bash
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

#### Step 5: Start Services

```bash
# Terminal 1: Start Backend
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

#### Step 6: Access Application

```
Frontend: http://localhost:5173
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

### macOS/Linux Setup

#### Step 1: Prerequisites Installation

```bash
# macOS - Using Homebrew
brew install python@3.11 node

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv nodejs npm

# Verify installations
python3 --version
node --version
npm --version
```

#### Step 2: Project Setup

```bash
# Extract project
cd ecocampus

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

cd frontend
npm install
cd ..
```

#### Step 3: Configure Environment

```bash
# Copy and edit .env if needed
cp .env .env.local
# Edit .env.local with your settings
```

#### Step 4: Database Setup (Optional - for PostgreSQL)

```bash
# Install PostgreSQL
brew install postgresql  # macOS
sudo apt-get install postgresql postgresql-contrib  # Linux

# Create database
createdb ecocampus
```

#### Step 5: Start Services

```bash
# Terminal 1: Backend
source venv/bin/activate
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## 🚀 Production Deployment

### Backend Production Setup

#### Step 1: Install Production Dependencies

```bash
# Install system dependencies
sudo apt-get install python3.11 python3.11-venv postgresql redis-server

# Create application directory
sudo mkdir -p /opt/ecocampus
sudo chown $USER:$USER /opt/ecocampus

# Copy project
cp -r ecocampus/* /opt/ecocampus/
cd /opt/ecocampus
```

#### Step 2: Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn uvicorn[standard]
```

#### Step 3: Configure Production Environment

```bash
# Create production .env
cat > .env << 'EOF'
DEBUG=false
APP_NAME=EcoCampus
VERSION=1.0.0

# Production database
DATABASE_URL=postgresql://user:password@localhost:5432/ecocampus

# Security
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS for production
CORS_ORIGINS=["https://yourdomain.com"]

# Redis
REDIS_URL=redis://localhost:6379/0

# Production settings
WORKERS=4
WORKER_CLASS=uvicorn.workers.UvicornWorker
EOF
```

#### Step 4: Database Migration

```bash
# Create tables
python -c "from backend.core.database import create_tables; create_tables()"

# Create admin user
python << 'EOF'
from backend.core.database import SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email='admin@yourdomain.com',
    username='admin',
    full_name='Admin User',
    hashed_password=get_password_hash('secure_password'),
    is_superuser=True,
    is_active=True
)
db.add(admin)
db.commit()
db.close()
print("Admin user created!")
EOF
```

#### Step 5: Setup Systemd Service

```bash
# Create systemd service file
sudo tee /etc/systemd/system/ecocampus.service << 'EOF'
[Unit]
Description=EcoCampus API Service
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=/opt/ecocampus
Environment="PATH=/opt/ecocampus/venv/bin"
ExecStart=/opt/ecocampus/venv/bin/gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    backend.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ecocampus
sudo systemctl start ecocampus
sudo systemctl status ecocampus
```

### Frontend Production Build

```bash
# Build frontend
cd frontend
npm run build

# Output is in frontend/dist
# Deploy dist folder to web server or CDN
```

### Nginx Reverse Proxy Setup

```bash
# Install Nginx
sudo apt-get install nginx

# Create Nginx config
sudo tee /etc/nginx/sites-available/ecocampus << 'EOF'
upstream ecocampus_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 100M;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Frontend
    location / {
        alias /opt/ecocampus/frontend/dist/;
        try_files $uri $uri/ /index.html;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # API
    location /api/ {
        proxy_pass http://ecocampus_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /opt/ecocampus/frontend/dist/;
        expires 30d;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/ecocampus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL Certificate Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

## 🐳 Docker Deployment

### Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Custom Docker Setup

```bash
# Build image
docker build -t ecocampus:latest .

# Run container
docker run -d \
  --name ecocampus \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/ecocampus \
  -e DEBUG=false \
  ecocampus:latest
```

### Docker on Cloud Providers

#### AWS ECS
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com
docker tag ecocampus:latest ACCOUNT.dkr.ecr.REGION.amazonaws.com/ecocampus:latest
docker push ACCOUNT.dkr.ecr.REGION.amazonaws.com/ecocampus:latest
```

#### Google Cloud Run
```bash
# Push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/ecocampus
gcloud run deploy ecocampus --image gcr.io/PROJECT-ID/ecocampus
```

#### Azure Container Instances
```bash
# Push to ACR
az acr build --registry myregistry --image ecocampus:latest .
az container create --resource-group mygroup --name ecocampus --image myregistry.azurecr.io/ecocampus:latest
```

---

## 🐛 Troubleshooting

### Port Issues

```bash
# Check port usage (Linux/Mac)
lsof -i :8000
lsof -i :5173

# Kill process
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Access PostgreSQL
psql -U postgres -d ecocampus

# View application logs
tail -f /var/log/syslog | grep ecocampus
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R $USER:$USER /opt/ecocampus

# Fix file permissions
chmod 755 /opt/ecocampus
chmod 644 /opt/ecocampus/.env
```

### Certificate Issues

```bash
# Renew certificate manually
sudo certbot renew --force-renewal

# Check certificate expiry
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -text -noout | grep -A 2 "Validity"
```

---

## ⚡ Performance Tuning

### Backend Optimization

```python
# In .env
WORKERS=4  # Number of worker processes (2-4x CPU cores)
WORKER_TIMEOUT=120
KEEP_ALIVE=5
```

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_emission_campus ON campus_emissions(campus_id);
CREATE INDEX idx_emission_date ON campus_emissions(recorded_date);

-- Enable query logging
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();
```

### Redis Caching

```python
# Configure caching in backend
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600  # 1 hour
```

### Frontend Optimization

```bash
# Build optimization
cd frontend
npm run build -- --minify

# Enable gzip compression in Nginx
gzip on;
gzip_types text/css application/javascript application/json;
```

---

## 📊 Monitoring

### Application Monitoring

```bash
# System monitoring
top
df -h
netstat -tnp

# Application logs
journalctl -u ecocampus -f
```

### Uptime Monitoring

```bash
# Install monitoring tool
sudo apt-get install monit

# Configure monit for application
sudo nano /etc/monit/monitrc
```

---

## 🔒 Security Checklist

- [ ] Change default passwords
- [ ] Set strong SECRET_KEY in production
- [ ] Enable HTTPS with SSL certificate
- [ ] Configure firewall rules
- [ ] Enable database backups
- [ ] Setup log rotation
- [ ] Configure monitoring and alerts
- [ ] Regular security updates
- [ ] Change default API keys
- [ ] Setup rate limiting

---

## 📞 Support & Resources

- Documentation: See README.md
- API Docs: http://yourdomain.com/docs
- Issues: Check application logs
- Help: Review troubleshooting section above

---

**Last Updated**: 2024
**Version**: 1.0.0
