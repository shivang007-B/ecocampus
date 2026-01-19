# 🎯 HOW TO OPEN & RUN ECOCAMPUS

## ⚡ FASTEST WAY (3 Steps)

### Step 1: Setup (One Time Only)
```bash
python setup.py
```
This will:
- ✅ Install all Python packages
- ✅ Install all Node.js packages  
- ✅ Create database
- ✅ Create demo admin user

### Step 2: Start Backend (Terminal 1)
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.0.0 ready in xxx ms

➜ Local: http://localhost:5173/
```

---

## 🌐 OPEN IN BROWSER

Click one of these links:

1. **Application**: http://localhost:5173
2. **API Docs**: http://localhost:8000/docs
3. **Health Check**: http://localhost:8000/health

---

## 🔑 LOGIN

Use these credentials:

**Email:** `admin@ecocampus.com`  
**Password:** `password123`

---

## ✅ VERIFY IT WORKS

After login, you should see:
- ✅ Dashboard with metrics
- ✅ Campus page to add locations
- ✅ Emissions page to track carbon
- ✅ Settings page for profile

---

## 🐳 ALTERNATIVE: USE DOCKER

If you have Docker installed:

```bash
docker-compose up -d
```

Then open: http://localhost:5173

---

## 🆘 QUICK TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| "npm: command not found" | Install Node.js from nodejs.org |
| "Port 8000 in use" | Kill process or use different port |
| "Cannot connect to API" | Make sure backend is running |
| "npm install fails" | Delete `node_modules` and `package-lock.json`, try again |

---

## 📱 WHAT YOU GET

Once running, you'll have access to:

✅ **Dashboard** - View real-time emissions and statistics  
✅ **Emissions Tracking** - Record new emissions from multiple sources  
✅ **Campus Management** - Add and manage multiple campus locations  
✅ **User Settings** - Manage profile and preferences  
✅ **API Documentation** - Full Swagger API docs  

---

## 📚 MORE HELP

Need more information? Check these files:

- **QUICK_REFERENCE.md** - One-page cheat sheet
- **START_HERE.md** - Detailed getting started guide
- **APPLICATION_READY.md** - Completion status
- **README.md** - Full documentation

---

## 🎉 YOU'RE ALL SET!

Your complete EcoCampus application is ready to use!

Just run the 3 steps above and you're good to go. 🚀

---

*Made with 💚 for sustainable campuses*
