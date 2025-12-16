@echo off
echo Starting HMS Server...
echo ========================

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1

pause