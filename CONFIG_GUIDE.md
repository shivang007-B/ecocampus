# Configuration Guide for EcoCampus Backend

## Environment Configuration

### Development Environment (.env.dev)

```
APP_NAME=EcoCampus Backend
DEBUG=True
VERSION=1.0.0

# Database - Development
DATABASE_URL=postgresql://postgres:password@localhost:5432/ecocampus_dev
DATABASE_URL_TEST=postgresql://postgres:password@localhost:5432/ecocampus_test

# Security - Development (NEVER use these values in production!)
SECRET_KEY=dev-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional APIs
OPENWEATHER_API_KEY=
CLIMATIQ_API_KEY=
ELECTRICITYMAP_API_KEY=

# CORS - Development
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","http://127.0.0.1:3000","http://127.0.0.1:8080","http://localhost:5173"]

# Redis - Development
REDIS_URL=redis://localhost:6379/0

# MQTT - Development
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=campus/iot/#
```

### Production Environment (.env.prod)

```
APP_NAME=EcoCampus Backend
DEBUG=False
VERSION=1.0.0

# Database - Production (Use managed database service)
DATABASE_URL=postgresql://user:password@db-prod.example.com:5432/ecocampus
DATABASE_URL_TEST=postgresql://user:password@db-prod.example.com:5432/ecocampus_test

# Security - Production (Generate strong random keys)
SECRET_KEY=<use-strong-random-key-minimum-32-characters>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
OPENWEATHER_API_KEY=<your-api-key>
CLIMATIQ_API_KEY=<your-api-key>
ELECTRICITYMAP_API_KEY=<your-api-key>

# CORS - Production
CORS_ORIGINS=["https://ecocampus.example.com","https://app.ecocampus.example.com"]

# Redis - Production (Use managed Redis service)
REDIS_URL=redis://:password@redis-prod.example.com:6379/0

# MQTT - Production
MQTT_BROKER=mqtt-prod.example.com
MQTT_PORT=8883
MQTT_TOPIC=campus/iot/#
```

## Database Setup

### PostgreSQL Initial Setup

```bash
# Create main database
createdb ecocampus -U postgres

# Create test database
createdb ecocampus_test -U postgres

# Connect to database
psql -U postgres -d ecocampus

# Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "json";
```

### User and Permissions

```sql
-- Create application user (for production)
CREATE USER ecocampus_app WITH PASSWORD 'strong_password_here';

-- Grant permissions
GRANT CONNECT ON DATABASE ecocampus TO ecocampus_app;
GRANT USAGE ON SCHEMA public TO ecocampus_app;
GRANT CREATE ON SCHEMA public TO ecocampus_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ecocampus_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ecocampus_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO ecocampus_app;
```

## API Keys Configuration

### OpenWeatherMap
1. Visit https://openweathermap.org/api
2. Create an account
3. Subscribe to "Current weather data" API (free tier available)
4. Copy API key to `OPENWEATHER_API_KEY`

### Climatiq (Carbon Accounting)
1. Visit https://www.climatiq.io/
2. Sign up for API access
3. Copy API key to `CLIMATIQ_API_KEY`

### ElectricityMap
1. Visit https://www.electricitymap.org/
2. Sign up for API access
3. Copy API key to `ELECTRICITYMAP_API_KEY`

## Docker Configuration

### Building Custom Image

```bash
# Build image
docker build -t ecocampus-api:1.0 .

# Tag for registry
docker tag ecocampus-api:1.0 myregistry.azurecr.io/ecocampus-api:1.0

# Push to registry
docker push myregistry.azurecr.io/ecocampus-api:1.0
```

### Docker Compose Override

Create `docker-compose.override.yml` for development:

```yaml
version: '3.8'
services:
  api:
    build: .
    environment:
      DEBUG: "True"
      DATABASE_URL: postgresql://postgres:password@postgres:5432/ecocampus
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      mqtt:
        condition: service_started
```

## MQTT Configuration

### mosquitto.conf

```
# =================================================================
# Default authentication and access control
# =================================================================

# Allow anonymous access for testing (change in production)
allow_anonymous true

# Listen on all interfaces
listener 1883
protocol mqtt

listener 9001
protocol websockets

# =================================================================
# Security
# =================================================================

# Password file location
# password_file /etc/mosquitto/passwd

# ACL file location
# acl_file /etc/mosquitto/acl.txt

# =================================================================
# Persistence
# =================================================================

persistence true
persistence_location /mosquitto/data/

# =================================================================
# Logging
# =================================================================

log_dest file /mosquitto/log/mosquitto.log
log_dest stdout
log_type all
log_timestamp true
```

### ACL Configuration (mosquitto-acl.txt)

```
# Default ACL
user anonymous
topic read $SYS/#
topic write campus/+/+/#

user admin_user
topic read #
topic write #

user app_user
topic read campus/#
topic write campus/iot/#
```

## Redis Configuration

### redis.conf Key Settings

```
# Bind to localhost and network interface
bind 0.0.0.0

# Port
port 6379

# Database count
databases 16

# Persistence
save 900 1
save 300 10
save 60 10000

# Max memory
maxmemory 512mb
maxmemory-policy allkeys-lru

# Security (production)
requirepass your-strong-password

# Replication
# slaveof <host> <port>

# Clustering (optional)
# cluster-enabled yes
```

## SSL/TLS Configuration

### Generate Self-Signed Certificate (Development)

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### Nginx Configuration for HTTPS

```nginx
upstream ecocampus_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name ecocampus.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ecocampus.example.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://ecocampus_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://ecocampus_api/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Monitoring and Logging

### Logging Configuration

```python
# app/core/logging_config.py
import logging
import json
from pythonjsonlogger import jsonlogger

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # JSON formatter for structured logging
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # File handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
```

### Health Check Endpoints

All health checks available at:
- `GET /health` - Basic health check
- `GET /health/db` - Database connection check
- `GET /health/redis` - Redis connection check
- `GET /health/mqtt` - MQTT broker check

## Performance Tuning

### Database Connection Pool

```python
# app/core/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Number of connections to keep in pool
    max_overflow=40,  # Maximum overflow connections
    pool_recycle=3600,  # Recycle connections every hour
    pool_pre_ping=True,  # Verify connection before use
)
```

### Redis Caching

```python
# Cache settings in config.py
CACHE_TTL = 3600  # 1 hour
CACHE_KEY_PREFIX = "ecocampus:"
```

### Worker Configuration

```python
# Celery configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

## Backup and Recovery

### Database Backup

```bash
# Full backup
pg_dump -U postgres -d ecocampus > backup_$(date +%Y%m%d).sql

# Backup with compression
pg_dump -U postgres -d ecocampus | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore
psql -U postgres -d ecocampus < backup.sql
```

### Redis Backup

```bash
# Backup RDB file
docker cp ecocampus-redis:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb

# Restore
docker cp redis_backup_$(date +%Y%m%d).rdb ecocampus-redis:/data/dump.rdb
```

## Troubleshooting

### Check Service Status

```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f api
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f mqtt

# Restart services
docker-compose restart
```

### Database Issues

```bash
# Check connections
psql -U postgres -d ecocampus -c "SELECT * FROM pg_stat_activity;"

# Kill idle connections
psql -U postgres -d ecocampus -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'ecocampus' AND state = 'idle';"
```

### Clear Caches

```bash
# Redis flush
redis-cli FLUSHALL

# Via API
curl -X POST http://localhost:8000/admin/cache/clear
```
