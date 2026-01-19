# Installation and Deployment Guide

## Summary of Backend Setup

The EcoCampus backend is now properly configured with:

✓ **All files organized correctly** in a production-ready structure
✓ **All imports fixed** - proper import paths and module structure  
✓ **All endpoints configured** - Auth, Campus, Carbon, IoT, Users
✓ **Database models** - User, Campus, Building, IoT, Emissions, Challenges
✓ **API schemas** - Complete Pydantic models for validation
✓ **Services** - Carbon calculator, Data service, IoT service
✓ **Configuration** - Environment variables and settings
✓ **Docker support** - docker-compose.yml for easy deployment
✓ **Documentation** - README, QUICKSTART, CONFIG_GUIDE

## Installation Steps

### Step 1: Install Dependencies

```bash
# Option A: Using pip (local development)
pip install -r requirements.txt

# Option B: Using Docker (recommended for production)
docker-compose build
```

### Step 2: Configure Environment

The `.env` file is already created with default values. Update it with your settings:

```bash
# Edit .env file
# Key settings to change:
# - SECRET_KEY: Generate a strong random key
# - DATABASE_URL: Set your PostgreSQL connection string
# - API Keys: Add OpenWeatherMap, Climatiq keys if needed
```

### Step 3: Setup Database

#### Using Docker (Recommended):
```bash
# Start all services
docker-compose up -d

# Initialize database
docker-compose exec api python -c "from app.core.database import create_tables; create_tables()"
```

#### Local Setup (Windows):
```bash
# Create PostgreSQL database
createdb ecocampus -U postgres

# Install Redis (download from: https://github.com/microsoftarchive/redis/releases)
# Install Mosquitto (download from: https://mosquitto.org/download/)

# Create tables
python -c "from app.core.database import create_tables; create_tables()"
```

#### Local Setup (Linux/Mac):
```bash
# Create PostgreSQL database
createdb ecocampus -U postgres

# Install Redis
brew install redis  # macOS
sudo apt-get install redis-server  # Linux

# Install Mosquitto
brew install mosquitto  # macOS
sudo apt-get install mosquitto  # Linux

# Create tables
python -c "from app.core.database import create_tables; create_tables()"
```

### Step 4: Run Application

#### Using Docker:
```bash
docker-compose up
```

#### Local Development:
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Mosquitto
mosquitto -c mosquitto.conf

# Terminal 3: FastAPI (from virtual environment)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Create Admin User

```bash
python -c "
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

db = SessionLocal()
admin = User(
    email='admin@ecocampus.local',
    username='admin',
    full_name='Administrator',
    hashed_password=get_password_hash('admin123'),
    is_active=True,
    is_superuser=True
)
db.add(admin)
db.commit()
print('Admin user created successfully!')
print('Login with: admin / admin123')
"
```

### Step 6: Access Application

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Base URL**: http://localhost:8000/api/v1

## Project Structure

```
ECO-campus/
├── app/                              # Main application
│   ├── api/v1/endpoints/             # API endpoints
│   │   ├── auth.py                   # Authentication (login, register, JWT)
│   │   ├── users.py                  # User management
│   │   ├── campus.py                 # Campus and building management
│   │   ├── carbon.py                 # Carbon emissions tracking
│   │   └── iot.py                    # IoT device management
│   ├── core/                         # Core functionality
│   │   ├── config.py                 # Configuration settings
│   │   ├── database.py               # Database connection
│   │   └── security.py               # JWT and password security
│   ├── models/                       # SQLAlchemy models
│   │   ├── user.py                   # User, Activity, Challenge models
│   │   ├── campus.py                 # Campus, Building, Department, IoT
│   │   └── carbon.py                 # Emissions, Targets, Credits
│   ├── schemas/                      # Pydantic validation schemas
│   │   ├── user.py                   # User DTOs
│   │   ├── campus.py                 # Campus DTOs
│   │   └── carbon.py                 # Carbon DTOs
│   ├── services/                     # Business logic
│   │   ├── carbon_calculator.py      # Emission calculations
│   │   ├── data_service.py           # Data operations
│   │   └── iot_service.py            # MQTT/IoT handling
│   ├── utils/                        # Utilities
│   │   ├── constants.py              # Emission factors
│   │   └── helpers.py                # Helper functions
│   └── main.py                       # Application entry point
├── tests/                            # Test suite
├── docker-compose.yml                # Docker services
├── dockerfile                        # Docker image
├── requirements.txt                  # Python dependencies
├── .env                              # Environment variables
├── validate.py                       # Validation script
├── README.md                         # Full documentation
├── QUICKSTART.md                     # Quick start guide
├── CONFIG_GUIDE.md                   # Configuration guide
└── setup.bat / setup.sh              # Setup scripts
```

## Key Features Implemented

### Authentication & Security
- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control (User, Admin, Superuser)
- Token refresh mechanism

### Campus Management
- Multiple campus support
- Building and department management
- Multi-tenant architecture
- Area and occupancy tracking

### Carbon Tracking
- Real-time emission monitoring
- Emission calculation from multiple sources:
  - Electricity consumption
  - Transportation
  - Waste management
  - Food consumption
  - Water usage
- Emission targets and reduction tracking
- Carbon credits management
- Leaderboard and gamification

### IoT Integration
- MQTT-based device communication
- Real-time sensor data collection
- Device management and maintenance tracking
- WebSocket support for real-time updates
- Bulk reading upload

### User Activities
- Track individual user activities
- Personal carbon footprint calculation
- Sustainability challenges
- User achievements and rewards

### Analytics & Reporting
- Campus dashboard
- Emission trends and analysis
- Comparisons and benchmarking
- Data export capabilities

## Available API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Register new user
- `POST /login` - Login with credentials
- `GET /me` - Get current user profile
- `PUT /me` - Update profile
- `POST /refresh` - Refresh JWT token
- `GET /validate` - Validate token

### Campus Management (`/api/v1/campuses`)
- `POST /` - Create campus
- `GET /` - List campuses
- `GET /{id}` - Get campus details
- `PUT /{id}` - Update campus
- `POST /{id}/buildings` - Add building
- `GET /{id}/buildings` - List buildings

### Carbon Tracking (`/api/v1/carbon`)
- `POST /emissions` - Record emission data
- `GET /emissions` - Query emissions
- `PUT /emissions/{id}` - Update emission record
- `POST /targets` - Set reduction targets
- `GET /dashboard` - Get dashboard summary
- `POST /scenarios` - Run what-if scenarios

### IoT Management (`/api/v1/iot`)
- `POST /devices` - Register device
- `GET /devices` - List devices
- `POST /readings` - Submit readings
- `WS /stream` - WebSocket for real-time data
- `POST /bulk` - Bulk reading upload

### User Management (`/api/v1/users`)
- `GET /` - List users (admin)
- `GET /{id}` - Get user (admin)
- `DELETE /{id}` - Delete user (admin)
- `POST /activities` - Log activity
- `GET /activities` - View activities
- `POST /challenges` - Join challenge

## Environment Variables

Key variables that should be customized:

```
# Security (IMPORTANT: Change these!)
SECRET_KEY=your-super-secret-key-minimum-32-characters
DEBUG=False  # Set to False in production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ecocampus

# External APIs (Optional)
OPENWEATHER_API_KEY=your_api_key
CLIMATIQ_API_KEY=your_api_key
ELECTRICITYMAP_API_KEY=your_api_key

# CORS - Update for your frontend domain
CORS_ORIGINS=["https://yourdomain.com"]

# Deployment
APP_NAME=EcoCampus Backend
VERSION=1.0.0
```

## Verification

Run the validation script to verify everything is set up correctly:

```bash
python validate.py
```

Expected output:
- ✓ Python Version: PASS
- ✓ Project Structure: PASS
- ✓ Dependencies: PASS (after `pip install -r requirements.txt`)
- ✓ Python Syntax: PASS
- ✓ .env File: PASS
- ✓ Imports: PASS

## Troubleshooting

### "ModuleNotFoundError: No module named..."
```bash
# Install missing dependencies
pip install -r requirements.txt
```

### "Connection refused" for database
```bash
# Check PostgreSQL is running
# Windows: Check Services or start from PostgreSQL installer
# Linux: sudo systemctl start postgresql
# Mac: brew services start postgresql
```

### CORS errors when connecting frontend
```
# Update CORS_ORIGINS in .env to include your frontend URL
CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
```

### Port already in use
```bash
# Find and kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

## Production Deployment

### Pre-deployment Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Generate strong `SECRET_KEY`
- [ ] Update `CORS_ORIGINS` with production domain
- [ ] Configure production database (RDS, Managed PostgreSQL)
- [ ] Setup Redis (ElastiCache, Redis Cloud)
- [ ] Enable SSL/TLS certificates
- [ ] Setup automated backups
- [ ] Configure monitoring and alerts
- [ ] Test database migrations
- [ ] Setup proper logging

### Docker Deployment

```bash
# Build image
docker build -t ecocampus-api:1.0 .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=your-secret-key \
  ecocampus-api:1.0
```

### Cloud Deployment Options

- **AWS**: ECS + RDS + ElastiCache + ALB
- **Azure**: App Service + Azure Database + Azure Cache
- **GCP**: Cloud Run + Cloud SQL + Memorystore
- **Heroku**: Heroku Dynos + Heroku Postgres + Heroku Redis
- **DigitalOcean**: App Platform or Droplets

## Next Steps

1. **Review Documentation**
   - Read [README.md](README.md) for full documentation
   - Check [QUICKSTART.md](QUICKSTART.md) for quick examples
   - See [CONFIG_GUIDE.md](CONFIG_GUIDE.md) for advanced setup

2. **Test the API**
   - Access http://localhost:8000/docs
   - Try example API calls
   - Create test data

3. **Integrate Frontend**
   - Update CORS_ORIGINS
   - Test API connectivity
   - Implement authentication flow

4. **Setup Monitoring**
   - Enable application logging
   - Setup error tracking
   - Configure health checks

5. **Deploy to Production**
   - Follow production checklist
   - Use Docker for containerization
   - Setup CI/CD pipeline

## Support

- **Documentation**: See README.md, QUICKSTART.md, CONFIG_GUIDE.md
- **Issues**: Check GitHub issues or create new one
- **Community**: Join discussions
- **Email**: support@ecocampus.local

---

**Backend Setup Complete! You're ready to start developing with EcoCampus.** 🎉
