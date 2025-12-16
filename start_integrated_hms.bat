@echo off
echo 🏥 Starting Integrated HMS System
echo ====================================

echo Activating virtual environment...
cd backend
call venv\Scripts\activate

echo Starting integrated server...
echo.
echo 🌐 HMS will open at: http://127.0.0.1:8000
echo 🔑 Login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo ====================================

python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1

pause