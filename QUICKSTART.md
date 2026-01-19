# Quick Start Guide - EcoCampus Backend

## Option 1: Quick Start with Docker (Recommended)

### Prerequisites
- Docker Desktop installed
- 8GB+ RAM available

### Steps

1. **Clone and navigate to project**
```bash
cd ECO-campus
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **Initialize database**
```bash
docker-compose exec api python -c "from app.core.database import create_tables; create_tables()"
```

4. **Create admin user**
```bash
docker-compose exec api python -c "
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
print('Admin user created: admin/admin123')
"
```

5. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - API: http://localhost:8000/api/v1
   - Health Check: http://localhost:8000/health

6. **Login**
   - Username: admin
   - Password: admin123

### Stop services
```bash
docker-compose down
```

---

## Option 2: Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Mosquitto MQTT

### Windows Setup

1. **Install dependencies**
```powershell
# Download and install PostgreSQL from: https://www.postgresql.org/download/windows/
# Download and install Redis from: https://github.com/microsoftarchive/redis/releases
# Download and install Mosquitto from: https://mosquitto.org/download/
```

2. **Run setup script**
```powershell
.\setup.bat
```

3. **Activate virtual environment**
```powershell
.\venv\Scripts\activate
```

4. **Start services** (in separate terminals)
```powershell
# Terminal 1: Redis
redis-server

# Terminal 2: Mosquitto
mosquitto -c mosquitto.conf

# Terminal 3: FastAPI
uvicorn app.main:app --reload
```

### Linux/Mac Setup

1. **Run setup script**
```bash
bash setup.sh
```

2. **Activate virtual environment**
```bash
source venv/bin/activate
```

3. **Start services** (in separate terminals)
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Mosquitto
mosquitto -c mosquitto.conf

# Terminal 3: FastAPI
uvicorn app.main:app --reload
```

---

## API Usage Examples

### 1. Register New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "securepassword123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create Campus
```bash
curl -X POST "http://localhost:8000/api/v1/campuses/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech University",
    "location": "Jaipur, India",
    "area_sqm": 50000,
    "student_count": 5000,
    "staff_count": 500
  }'
```

### 4. Add Building
```bash
curl -X POST "http://localhost:8000/api/v1/campuses/1/buildings" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campus_id": 1,
    "name": "Engineering Building",
    "building_type": "academic",
    "area_sqm": 10000,
    "floor_count": 5
  }'
```

### 5. Record Emissions
```bash
curl -X POST "http://localhost:8000/api/v1/carbon/emissions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campus_id": 1,
    "date": "2024-01-15T00:00:00Z",
    "electricity_emission": 5000,
    "transportation_emission": 2000,
    "waste_emission": 500,
    "food_emission": 1000,
    "water_emission": 100,
    "data_source": "simulated"
  }'
```

### 6. Get Dashboard
```bash
curl -X GET "http://localhost:8000/api/v1/carbon/dashboard?campus_id=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Testing the Application

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test Database Connection
```bash
python -c "from app.core.database import SessionLocal; print(SessionLocal().execute('SELECT 1'))"
```

### Test MQTT Connection
```bash
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"
```

### Test Redis Connection
```bash
redis-cli ping
# Should return: PONG
```

---

## Common Issues and Solutions

### Port Already in Use
```bash
# Windows - Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### PostgreSQL Connection Refused
```bash
# Check PostgreSQL is running
# Windows: Check Services
# Linux: sudo systemctl status postgresql
# Mac: brew services list

# Reset PostgreSQL password (Windows)
# Use pgAdmin or command line tools
```

### Redis Connection Failed
```bash
# Start Redis
redis-server

# Windows: Add to PATH if needed
set PATH=%PATH%;C:\Program Files\Redis
```

### MQTT Connection Failed
```bash
# Start Mosquitto
mosquitto

# Test connection
mosquitto_sub -h localhost -t "#" -v
```

---

## Environment Configuration

Copy and customize `.env.example` to `.env`:

```bash
# Key variables to update:
SECRET_KEY=your-secret-key-here
OPENWEATHER_API_KEY=your-api-key
DEBUG=False  # Set to False for production
```

---

## Next Steps

1. **Explore API Documentation**: Visit http://localhost:8000/docs
2. **Read README.md**: Full documentation and architecture
3. **Check CONFIG_GUIDE.md**: Advanced configuration options
4. **Create sample data**: Use provided endpoints to populate test data
5. **Setup frontend**: Connect with your frontend application

---

## Support and Documentation

- **Full Documentation**: See README.md
- **Configuration Guide**: See CONFIG_GUIDE.md
- **API Docs**: http://localhost:8000/docs (when running)
- **Issues**: Check existing issues or create new ones
- **Email**: support@ecocampus.local

---

## Performance Tips

1. **Use pagination**: Always specify `skip` and `limit` parameters
2. **Cache data**: Utilize Redis caching for frequently accessed data
3. **Batch operations**: Submit multiple IoT readings in batch
4. **Index queries**: Database queries use proper indexing
5. **Monitor health**: Check `/health` endpoint regularly

---

Enjoy using EcoCampus Backend! 🌱
