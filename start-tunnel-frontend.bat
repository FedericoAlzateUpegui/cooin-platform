@echo off
REM ===================================================
REM Cloudflare Tunnel for Frontend (Windows)
REM ===================================================
REM This script creates a Cloudflare tunnel for the
REM frontend web app (port 8083)
REM ===================================================

echo.
echo ========================================
echo   Cloudflare Tunnel - Frontend
echo ========================================
echo.

REM Check if cloudflared is installed
where cloudflared >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: cloudflared not found!
    echo.
    echo To install, run:
    echo   winget install cloudflare.cloudflared
    echo.
    echo Or download from:
    echo   https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
    echo.
    pause
    exit /b 1
)

echo Starting tunnel for frontend (http://localhost:8083)
echo.
echo IMPORTANT: Share this URL with partners to access the app
echo.
echo Press Ctrl+C to stop the tunnel
echo ========================================
echo.

cloudflared tunnel --url http://localhost:8083
