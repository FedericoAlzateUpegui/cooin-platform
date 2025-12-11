@echo off
REM ===================================================
REM Cooin All-in-One Startup Script (Windows)
REM ===================================================
REM This script opens 3 terminal windows:
REM   1. Backend Server (port 8000)
REM   2. Frontend Web App (port 8083)
REM   3. Cloudflare Tunnel (backend)
REM ===================================================

echo.
echo ========================================
echo   Cooin Platform - Starting All Services
echo ========================================
echo.

REM Check if Docker is running (Redis)
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Docker is not running!
    echo Redis may not be available.
    echo.
    echo To start Redis:
    echo   1. Open Docker Desktop
    echo   2. Run: docker-compose up -d redis
    echo.
    pause
)

echo Starting services in separate windows...
echo.

REM 1. Start Backend Server
echo [1/3] Starting Backend Server...
start "Cooin Backend" cmd /k "cd /d "%~dp0cooin-backend" && start-backend.bat"
timeout /t 2 /nobreak >nul

REM 2. Start Frontend Web App
echo [2/3] Starting Frontend Web App...
start "Cooin Frontend" cmd /k "cd /d "%~dp0cooin-frontend" && start-frontend.bat"
timeout /t 2 /nobreak >nul

REM 3. Ask user about tunnel
echo [3/3] Cloudflare Tunnel Options:
echo.
echo Do you want to start a Cloudflare tunnel for external access?
echo.
echo   1 = Quick Tunnel (random URL, changes each restart)
echo   2 = Named Tunnel (persistent URL - requires setup)
echo   3 = Skip (local development only)
echo.
set /p TUNNEL_CHOICE="Enter choice (1/2/3): "

if "%TUNNEL_CHOICE%"=="1" (
    echo Starting Quick Tunnel...
    start "Cooin Tunnel - Backend" cmd /k "cd /d "%~dp0" && start-tunnel-backend.bat"
) else if "%TUNNEL_CHOICE%"=="2" (
    echo Starting Named Tunnel...
    echo.
    echo Make sure you completed the setup in SETUP-NAMED-TUNNEL.md
    echo.
    pause
    start "Cooin Named Tunnel" cmd /k "cloudflared tunnel run cooin-backend"
) else (
    echo Skipping tunnel - Local development mode
)

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/api/v1/docs
echo Frontend: http://localhost:8083
echo.
echo Check the opened terminal windows for status.
echo Close terminal windows or press Ctrl+C to stop services.
echo.
echo ========================================
pause
