@echo off
echo 🏥 Starting Complete HMS System
echo ================================

echo 1. Starting Backend Server...
cd backend
start "HMS Backend" cmd /k "venv\Scripts\activate && python start.py"

echo 2. Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 3. Opening Frontend...
cd ..
start "" "frontend\index.html"

echo 4. Opening API Documentation...
timeout /t 2 /nobreak > nul
start "" "http://127.0.0.1:8000/docs"

echo ================================
echo 🎉 HMS System Started!
echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: Opened in browser
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Login: admin / admin123
echo.
echo Press any key to exit...
pause > nul