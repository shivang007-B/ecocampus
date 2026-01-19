# 🚀 EcoCampus Quick Reference Card

## ⚡ 30-Second Start

### Windows
```bash
python setup.py
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
cd frontend && npm run dev
```

### Mac/Linux
```bash
python3 setup.py
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
cd frontend && npm run dev
```

---

## 🔑 Login
- **Email**: admin@ecocampus.com
- **Password**: password123

---

## 🌐 URLs
| What | URL |
|------|-----|
| App | http://localhost:5173 |
| API | http://localhost:8000 |
| Docs | http://localhost:8000/docs |

---

## 📦 Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (optional, SQLite included)

---

## 🐳 Docker
```bash
docker-compose up -d
```

---

## 📁 File Structure
```
backend/          → API & database
frontend/         → React app  
requirements.txt  → Python deps
.env              → Config
setup.py          → Setup script
```

---

## 🆘 Common Issues

| Problem | Fix |
|---------|-----|
| Port 8000 in use | Kill process or use different port |
| npm not found | Install Node.js |
| DB error | Check .env DATABASE_URL |
| Can't login | Ensure backend is running |

---

## 📚 Documentation
- README.md - Full docs
- START_HERE.md - Getting started
- DEPLOYMENT_GUIDE.md - Production setup
- APPLICATION_READY.md - Completion status

---

## ✅ You Have

✅ Complete backend API  
✅ React frontend  
✅ Authentication  
✅ Database models  
✅ Docker support  
✅ Full documentation  

---

**Ready to go! 🌱**
