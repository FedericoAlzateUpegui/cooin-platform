@echo off
REM ===================================================
REM Cooin Backend Startup Script (Windows)
REM ===================================================
REM This script activates the virtual environment and
REM starts the FastAPI backend server with auto-reload
REM ===================================================

echo.
echo ========================================
echo   Starting Cooin Backend Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\pip.exe install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and start server
echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/2] Starting FastAPI server on http://localhost:8000
echo.
echo API Documentation: http://localhost:8000/api/v1/docs
echo Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start uvicorn with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
