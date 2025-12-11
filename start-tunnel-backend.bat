@echo off
REM ===================================================
REM Cloudflare Tunnel for Backend (Windows)
REM ===================================================
REM This script creates a Cloudflare tunnel for the
REM backend API server (port 8000)
REM ===================================================

echo.
echo ========================================
echo   Cloudflare Tunnel - Backend
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

echo Starting tunnel for backend (http://localhost:8000)
echo.
echo IMPORTANT: Copy the tunnel URL and update:
echo   1. cooin-frontend\.env - EXPO_PUBLIC_API_URL
echo   2. cooin-backend\.env - BACKEND_CORS_ORIGINS
echo.
echo Press Ctrl+C to stop the tunnel
echo ========================================
echo.

cloudflared tunnel --url http://localhost:8000
