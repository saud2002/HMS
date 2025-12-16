# 🪟 HMS Windows Setup Guide

Quick setup guide for Windows users having installation issues.

## 🚀 Quick Start (Windows)

### Step 1: Install Core Requirements Only

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
```

### Step 2: Install Minimal Dependencies

```cmd
pip install -r requirements-minimal.txt
```

If that fails, install packages individually:

```cmd
pip install fastapi==0.115.6
pip install uvicorn[standard]==0.34.0
pip install sqlalchemy==2.0.36
pip install pymysql==1.1.1
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.18
pip install pydantic==2.10.3
pip install pydantic-settings==2.6.1
pip install python-dotenv==1.0.1
```

### Step 3: Configure Database

1. **Create .env file:**
   ```cmd
   copy .env.example .env
   ```

2. **Edit .env file** with your database settings:
   ```
   DATABASE_URL=mysql+pymysql://root:@localhost:3306/hms
   ```

### Step 4: Initialize Database

```cmd
python init_database.py
```

### Step 5: Start Application

```cmd
python start.py
```

## 🔧 Alternative Installation Methods

### Method 1: Use Batch Script
```cmd
install-windows.bat
```

### Method 2: Manual Installation
If you're still having issues, try installing without optional dependencies:

```cmd
pip install fastapi uvicorn sqlalchemy pymysql python-jose passlib pydantic python-dotenv
```

## 🗄️ Database Setup

### Option 1: Use XAMPP
1. Download and install XAMPP
2. Start Apache and MySQL
3. Create database `hms` in phpMyAdmin
4. Update .env file with connection details

### Option 2: Use MySQL Workbench
1. Install MySQL Server and Workbench
2. Create database `hms`
3. Update .env file

### Option 3: Use SQLite (for testing)
Update your .env file:
```
DATABASE_URL=sqlite:///./hms.db
```

## 🚨 Common Issues & Solutions

### Issue: Pillow Installation Fails
**Solution:** Skip Pillow for now - it's only needed for advanced PDF features
```cmd
# Install without Pillow
pip install -r requirements-minimal.txt
```

### Issue: Cryptography Installation Fails
**Solution:** Install Microsoft Visual C++ Build Tools or use pre-compiled wheels
```cmd
pip install --only-binary=cryptography cryptography
```

### Issue: MySQL Connection Fails
**Solutions:**
1. Check if MySQL is running
2. Verify credentials in .env file
3. Try using 127.0.0.1 instead of localhost
4. Use SQLite for testing: `DATABASE_URL=sqlite:///./hms.db`

### Issue: Port 8000 Already in Use
**Solution:** Use a different port
```cmd
python -c "from app.main import app; import uvicorn; uvicorn.run(app, port=8001)"
```

## 🎯 Minimal Working Setup

If you just want to test the system quickly:

1. **Install only core packages:**
   ```cmd
   pip install fastapi uvicorn sqlalchemy pymysql pydantic python-dotenv
   ```

2. **Use SQLite database:**
   Create `.env` file:
   ```
   DATABASE_URL=sqlite:///./hms.db
   SECRET_KEY=test-secret-key
   ```

3. **Initialize and run:**
   ```cmd
   python init_database.py
   python start.py
   ```

## 📱 Access Your Application

Once running:
- **API Documentation:** http://localhost:8000/docs
- **Frontend:** Open `frontend/index.html` in your browser
- **Login:** username: `admin`, password: `admin123`

## 💡 Tips for Windows Users

1. **Use Command Prompt or PowerShell** (not Git Bash for Python commands)
2. **Run as Administrator** if you get permission errors
3. **Disable antivirus temporarily** during installation if it blocks downloads
4. **Use Python 3.8-3.11** for better compatibility (avoid 3.12+)

## 🆘 Still Having Issues?

1. **Check Python version:** `python --version` (should be 3.8+)
2. **Update pip:** `python -m pip install --upgrade pip`
3. **Clear pip cache:** `pip cache purge`
4. **Try virtual environment:** Always use venv to avoid conflicts

## 📞 Quick Test

Test if your installation works:
```cmd
python -c "import fastapi, sqlalchemy, pymysql; print('✅ Core packages working!')"
```

If this works, you're ready to run the HMS system! 🎉