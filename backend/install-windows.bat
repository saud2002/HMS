@echo off
echo Installing HMS on Windows...
echo ================================

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing core requirements...
pip install -r requirements-minimal.txt
if errorlevel 1 (
    echo Core installation failed, trying individual packages...
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
)

echo Checking installation...
python -c "import fastapi, sqlalchemy, pymysql; print('Core packages installed successfully!')"
if errorlevel 1 (
    echo Installation verification failed
    pause
    exit /b 1
)

echo ================================
echo Installation completed successfully!
echo.
echo Next steps:
echo 1. Copy .env.example to .env and update database settings
echo 2. Run: python init_database.py
echo 3. Run: python start.py
echo.
pause