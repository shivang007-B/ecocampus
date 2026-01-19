# EcoCampus - Ready to Run Application

A comprehensive real-time carbon emissions tracking and sustainability management system for campuses.

## 🌍 Features

- **Real-time Carbon Tracking**: Monitor campus emissions from multiple sources
- **Interactive Dashboard**: Visual analytics and trend analysis
- **Campus Management**: Multi-building campus organization
- **Emissions Recording**: Easy-to-use emission logging system
- **User Management**: Role-based access control
- **API Documentation**: Full REST API with Swagger UI
- **Responsive Design**: Mobile-friendly modern interface

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or SQLite for development)
- npm or yarn

### Installation (Windows)

1. **Extract the project** to your desired location

2. **Open PowerShell or CMD** in the project directory

3. **Run setup** (first time only):
   ```bash
   python setup.py
   ```
   Or manually:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install && cd ..
   ```

4. **Start Backend** (Terminal 1):
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

6. **Open Browser**:
   - Application: http://localhost:5173
   - API Docs: http://localhost:8000/docs

### Installation (Linux/Mac)

1. **Extract the project** to your desired location

2. **Open Terminal** in the project directory

3. **Run setup**:
   ```bash
   bash setup.sh
   ```
   Or manually:
   ```bash
   pip3 install -r requirements.txt
   cd frontend && npm install && cd ..
   ```

4. **Start Backend** (Terminal 1):
   ```bash
   python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

6. **Open Browser**:
   - Application: http://localhost:5173
   - API Docs: http://localhost:8000/docs

## 📝 Demo Credentials

```
Email: admin@ecocampus.com
Password: password123
```

## 📁 Project Structure

```
ecocampus/
├── backend/                    # FastAPI backend
│   ├── api/                   # API endpoints
│   ├── models/                # Database models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── core/                  # Config, security, database
│   ├── utils/                 # Utilities and helpers
│   └── main.py                # Application entry point
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── api/              # API client
│   │   ├── stores/           # Zustand stores
│   │   ├── utils/            # Utility functions
│   │   └── App.jsx           # Main app component
│   ├── package.json
│   └── vite.config.js
│
├── requirements.txt           # Python dependencies
├── setup.bat / setup.sh       # Setup scripts
├── start_backend.bat/sh       # Backend startup script
├── start_frontend.bat/sh      # Frontend startup script
└── README.md                  # This file
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token

### Users
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/{id}` - Delete user

### Campus
- `GET /api/v1/campuses` - Get all campuses
- `GET /api/v1/campuses/{id}` - Get campus by ID
- `POST /api/v1/campuses` - Create campus
- `PUT /api/v1/campuses/{id}` - Update campus
- `DELETE /api/v1/campuses/{id}` - Delete campus

### Emissions
- `GET /api/v1/carbon/emissions` - Get all emissions
- `GET /api/v1/carbon/emissions/{id}` - Get emission by ID
- `POST /api/v1/carbon/emissions` - Create emission
- `PUT /api/v1/carbon/emissions/{id}` - Update emission
- `DELETE /api/v1/carbon/emissions/{id}` - Delete emission

### IoT Devices
- `GET /api/v1/iot/devices` - Get all IoT devices
- `GET /api/v1/iot/devices/{id}` - Get device by ID
- `POST /api/v1/iot/devices` - Create device
- `PUT /api/v1/iot/devices/{id}` - Update device
- `DELETE /api/v1/iot/devices/{id}` - Delete device

## 🔧 Configuration

### Backend Configuration (.env)
```
DATABASE_URL=postgresql://user:password@localhost/ecocampus
SECRET_KEY=your-secret-key-here
DEBUG=true
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### Frontend Configuration (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=EcoCampus
```

## 🐛 Troubleshooting

### Port Already in Use
- Backend (port 8000): Kill existing process or use different port
- Frontend (port 5173): Kill existing process or Vite will use next available

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- For development, you can use SQLite instead

### CORS Error
- Check CORS_ORIGINS in backend .env
- Ensure frontend URL is in the list

### Dependencies Not Installing
- Update pip: `python -m pip install --upgrade pip`
- Clear cache: `pip install --no-cache-dir -r requirements.txt`

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Frontend**: Source code in `frontend/src/`
- **Backend**: Source code in `backend/`

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Check terminal for backend errors

## 📄 License

This project is part of EcoCampus Initiative for sustainable campus management.

---

**Ready to make your campus greener! 🌱**
