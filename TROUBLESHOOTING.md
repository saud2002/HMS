# 🔧 HMS Troubleshooting Guide

## 🌐 Server Access Issues

### Problem: "http://0.0.0.0:8000/ shows nothing"

**Solution:** Use the correct URL format:
- ✅ **Correct:** http://127.0.0.1:8000 or http://localhost:8000
- ❌ **Wrong:** http://0.0.0.0:8000

### Problem: "Connection refused" or "Can't reach server"

**Solutions:**
1. **Check if server is running:**
   ```cmd
   cd backend
   python start.py
   ```

2. **Verify server status:**
   ```cmd
   python quick_test.py
   ```

3. **Test specific endpoint:**
   ```cmd
   python -c "import requests; print(requests.get('http://127.0.0.1:8000/api/health').json())"
   ```

## 🚀 Starting the Server

### Method 1: Using start.py (Recommended)
```cmd
cd backend
venv\Scripts\activate
python start.py
```

### Method 2: Using uvicorn directly
```cmd
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
```

### Method 3: Using batch file (Windows)
```cmd
cd backend
start_server.bat
```

## 🔍 Testing Your Installation

### Quick Test
```cmd
cd backend
python quick_test.py
```

### Server Test
```cmd
cd backend
python test_server.py
```

### API Test (Browser)
Open `backend/test_api.html` in your browser after starting the server.

## 📱 Accessing the System

### 1. API Server
- **URL:** http://127.0.0.1:8000
- **Should show:** JSON response with HMS information

### 2. API Documentation
- **URL:** http://127.0.0.1:8000/docs
- **Should show:** Interactive API documentation

### 3. Frontend Application
- **File:** Open `frontend/index.html` in your browser
- **Should show:** HMS dashboard

## ❌ Common Issues & Solutions

### Issue: "Module not found" errors
**Solution:**
```cmd
cd backend
venv\Scripts\activate
pip install -r requirements-minimal.txt
```

### Issue: "Database connection failed"
**Solutions:**
1. **Check MySQL is running** (XAMPP, MySQL Workbench, etc.)
2. **Verify credentials in .env file:**
   ```
   DATABASE_URL=mysql+pymysql://root:@localhost:3306/hms
   ```
3. **Test connection:**
   ```cmd
   python -c "from app.database import test_connection; print(test_connection())"
   ```

### Issue: "Port 8000 already in use"
**Solutions:**
1. **Kill existing process:**
   ```cmd
   netstat -ano | findstr :8000
   taskkill /PID <PID_NUMBER> /F
   ```
2. **Use different port:**
   ```cmd
   python -m uvicorn app.main:app --port 8001
   ```

### Issue: "Virtual environment not activated"
**Solution:**
```cmd
cd backend
venv\Scripts\activate
# You should see (venv) in your prompt
```

### Issue: "Frontend not loading data"
**Solutions:**
1. **Check API server is running** at http://127.0.0.1:8000
2. **Verify CORS settings** in main.py
3. **Check browser console** for errors (F12)

## 🧪 Step-by-Step Diagnosis

### 1. Test Python Environment
```cmd
python --version
# Should show Python 3.8+
```

### 2. Test Virtual Environment
```cmd
cd backend
venv\Scripts\activate
python -c "import sys; print(sys.prefix)"
# Should show path to venv
```

### 3. Test Package Installation
```cmd
python -c "import fastapi, sqlalchemy, pymysql; print('✅ Packages OK')"
```

### 4. Test Database Connection
```cmd
python -c "from app.database import test_connection; print('DB:', test_connection())"
```

### 5. Test App Loading
```cmd
python -c "from app.main import app; print('✅ App loads')"
```

### 6. Test Server Start
```cmd
python start.py
# Should show server starting messages
```

## 🌐 Network & Firewall Issues

### Windows Firewall
If Windows blocks the connection:
1. Allow Python through Windows Firewall
2. Or temporarily disable firewall for testing

### Antivirus Software
Some antivirus programs block local servers:
1. Add Python to antivirus exceptions
2. Or temporarily disable real-time protection

## 📞 Quick Fixes

### Reset Everything
```cmd
cd backend
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements-minimal.txt
python init_database.py
python start.py
```

### Use SQLite (if MySQL issues)
Edit `.env` file:
```
DATABASE_URL=sqlite:///./hms.db
```

### Minimal Test Server
```cmd
cd backend
python -c "
from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def root(): return {'message': 'HMS Test Server'}
import uvicorn
uvicorn.run(app, host='127.0.0.1', port=8000)
"
```

## ✅ Success Indicators

You know it's working when:
- ✅ http://127.0.0.1:8000 shows HMS API information
- ✅ http://127.0.0.1:8000/docs shows interactive documentation
- ✅ `frontend/index.html` loads and shows dashboard
- ✅ You can login with admin/admin123

## 🆘 Still Need Help?

1. **Run full diagnosis:**
   ```cmd
   cd backend
   python quick_test.py
   python test_server.py
   ```

2. **Check logs** in the terminal where you started the server

3. **Verify all files** are in the correct locations:
   ```
   backend/
   ├── app/
   │   ├── main.py
   │   ├── database.py
   │   └── ...
   ├── start.py
   └── requirements-minimal.txt
   ```

**Your HMS should be working perfectly! 🏥✨**