# EcoCampus Backend API

A comprehensive backend system for real-time carbon emissions tracking and sustainability management in campus environments.

## Features

- **Real-time Carbon Tracking**: Monitor emissions from multiple sources (electricity, transportation, waste, food, water)
- **IoT Integration**: MQTT-based IoT device management and real-time data collection
- **User Management**: Role-based access control (admin, user, superuser)
- **Emissions Analytics**: Comprehensive carbon footprint calculations and trend analysis
- **Sustainability Challenges**: Gamified challenges to promote eco-friendly behavior
- **Campus Management**: Multi-building, multi-department campus management
- **Data Visualization**: Dashboard and reporting capabilities
- **API First Design**: RESTful API with comprehensive documentation

## Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Real-time**: Redis for caching and WebSocket support
- **IoT**: MQTT broker (Mosquitto) for device communication
- **Authentication**: JWT-based authentication
- **Task Queue**: Celery for background tasks

## Project Structure

```
ECO-campus/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py          # Authentication endpoints
│   │       │   ├── users.py         # User management
│   │       │   ├── campus.py        # Campus management
│   │       │   ├── carbon.py        # Carbon tracking
│   │       │   └── iot.py           # IoT device management
│   │       └── api.py               # API router
│   ├── core/
│   │   ├── config.py                # Configuration settings
│   │   ├── database.py              # Database setup
│   │   └── security.py              # JWT and security utilities
│   ├── models/
│   │   ├── user.py                  # User and activity models
│   │   ├── campus.py                # Campus and building models
│   │   └── carbon.py                # Carbon tracking models
│   ├── schemas/
│   │   ├── user.py                  # Pydantic user schemas
│   │   ├── campus.py                # Campus schemas
│   │   └── carbon.py                # Carbon tracking schemas
│   ├── services/
│   │   ├── carbon_calculator.py     # Carbon calculation logic
│   │   ├── data_service.py          # Data operations
│   │   └── iot_service.py           # IoT data handling
│   ├── utils/
│   │   ├── constants.py             # Emission factors and constants
│   │   └── helpers.py               # Utility functions
│   └── main.py                      # Application entry point
├── docker-compose.yml               # Docker services configuration
├── dockerfile                       # Docker image definition
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
└── README.md                        # This file
```

## Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional but recommended)
- PostgreSQL 15+
- Redis 7+
- Mosquitto MQTT broker

### Local Setup

1. **Clone the repository**
```bash
cd ECO-campus
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
Copy `.env.example` to `.env` and update with your settings:
```bash
cp .env.example .env
```

5. **Setup database**
```bash
# Create database
createdb ecocampus -U postgres

# Run migrations
alembic upgrade head
```

6. **Start Redis**
```bash
redis-server
```

7. **Start MQTT Broker**
```bash
mosquitto -c mosquitto.conf
```

8. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Setup (Recommended)

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis on port 6379
- MQTT broker on port 1883
- FastAPI application on port 8000

2. **Initialize database**
```bash
docker-compose exec api python -c "from app.core.database import create_tables; create_tables()"
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info
- `PUT /api/v1/auth/me` - Update user profile
- `POST /api/v1/auth/refresh` - Refresh access token

#### Campus Management
- `POST /api/v1/campuses/` - Create campus
- `GET /api/v1/campuses/` - List campuses
- `GET /api/v1/campuses/{id}` - Get campus details
- `POST /api/v1/campuses/{id}/buildings` - Add building
- `POST /api/v1/campuses/{id}/emissions` - Record emissions

#### Carbon Tracking
- `POST /api/v1/carbon/emissions` - Record emission data
- `GET /api/v1/carbon/emissions` - Get emission records
- `POST /api/v1/carbon/targets` - Set emission targets
- `GET /api/v1/carbon/dashboard` - Get dashboard summary

#### IoT Devices
- `POST /api/v1/iot/devices` - Register IoT device
- `GET /api/v1/iot/devices` - List devices
- `POST /api/v1/iot/readings` - Submit device readings
- `WS /api/v1/iot/stream` - WebSocket for real-time data

## Configuration

### Environment Variables

Key environment variables in `.env`:

```
# Application
APP_NAME=EcoCampus Backend
DEBUG=True
VERSION=1.0.0

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/ecocampus

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
OPENWEATHER_API_KEY=your-api-key
CLIMATIQ_API_KEY=your-api-key
ELECTRICITYMAP_API_KEY=your-api-key

# Redis
REDIS_URL=redis://localhost:6379/0

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=campus/iot/#
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Code Formatting and Linting

```bash
# Format code
black app/

# Check linting
flake8 app/

# Type checking
mypy app/
```

## Architecture

### Authentication Flow
1. User registers with email/password
2. Password hashed with bcrypt
3. User logs in, receives JWT token
4. Token validated for protected endpoints
5. Role-based access control enforced

### Data Models

- **User**: User accounts with roles (admin, user, superuser)
- **Campus**: Main campus entity with buildings and departments
- **Building**: Individual building with IoT devices
- **IoTDevice**: Sensor devices (energy, water, temperature)
- **CampusEmission**: Daily emission records by source
- **UserActivity**: Individual user activities and carbon footprint
- **Challenge**: Sustainability challenges and gamification
- **EmissionTarget**: Campus emission reduction targets

### Services

- **CarbonCalculator**: Calculates emissions from various sources using emission factors
- **DataService**: Handles campus data operations and analytics
- **IoTService**: Manages MQTT connections and real-time device data

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure CORS origins properly
- [ ] Use strong database password
- [ ] Enable SSL/TLS for database
- [ ] Setup proper logging
- [ ] Configure backup strategy
- [ ] Setup monitoring and alerts
- [ ] Use environment-specific configs

### Deployment Options

- **Docker**: Use Docker Compose for containerized deployment
- **AWS**: Deploy using ECS, RDS, ElastiCache
- **Heroku**: Compatible with Procfile configuration
- **DigitalOcean**: App Platform or Droplets

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
psql -U postgres -d ecocampus

# Verify DATABASE_URL in .env
# Default: postgresql://postgres:password@localhost:5432/ecocampus
```

### Redis Connection Issues
```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Verify REDIS_URL in .env
```

### MQTT Connection Issues
```bash
# Check Mosquitto is running
mosquitto -v

# Test MQTT connection
mosquitto_sub -h localhost -t "test/topic"
```

## Contributing

1. Create a feature branch: `git checkout -b feature/feature-name`
2. Make your changes and commit: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/feature-name`
4. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and support:
- GitHub Issues: [Create an issue]
- Email: support@ecocampus.local
- Documentation: [Full docs]

## Acknowledgments

- Emission factors based on IPCC 2023 and Indian government reports
- Weather data from OpenWeatherMap API
- MQTT implementation using Eclipse Mosquitto
#   e c o c a m p u s  
 #   e c o c a m p u s  
 