@echo off
title Cooin Platform - Cloudflare Tunnels
color 0A
echo.
echo ========================================
echo   Cooin Platform - Cloudflare Tunnels
echo ========================================
echo.

REM Check if cloudflared is installed
where cloudflared >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] cloudflared not found!
    echo.
    echo Please install cloudflared first:
    echo   winget install cloudflare.cloudflared
    echo.
    echo Or download from:
    echo   https://github.com/cloudflare/cloudflared/releases/latest
    echo.
    pause
    exit /b 1
)

echo [INFO] Checking services...
echo.

REM Check if backend is running on port 8000
netstat -an | findstr ":8000" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Backend not detected on port 8000
    echo           Please start backend first:
    echo           cd cooin-backend
    echo           python start_dev.py
    echo.
)

REM Check if frontend is running on port 8083
netstat -an | findstr ":8083" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Frontend not detected on port 8083
    echo           Please start frontend first:
    echo           cd cooin-frontend
    echo           npx expo start --web --port 8083
    echo.
)

REM Check if config files exist
if exist cloudflare-config.yml (
    echo [OPTION 1] Named tunnels detected
    echo            Starting persistent tunnels...
    echo.

    start "Cooin Backend Tunnel" cloudflared tunnel --config cloudflare-config.yml run cooin-backend
    timeout /t 2 /nobreak > nul
    start "Cooin Frontend Tunnel" cloudflared tunnel --config cloudflare-frontend-config.yml run cooin-frontend

    echo.
    echo [SUCCESS] Named tunnels started!
    echo           Check your configured URLs in Cloudflare dashboard
    echo.
) else (
    echo [OPTION 2] No named tunnels configured
    echo            Starting quick tunnels...
    echo            (URLs will be displayed in each terminal)
    echo.

    start "Cooin Backend Tunnel" cmd /k "echo Backend Tunnel Starting... && cloudflared tunnel --url http://localhost:8000"
    timeout /t 2 /nobreak > nul
    start "Cooin Frontend Tunnel" cmd /k "echo Frontend Tunnel Starting... && cloudflared tunnel --url http://localhost:8083"

    echo.
    echo [SUCCESS] Quick tunnels started!
    echo.
    echo IMPORTANT:
    echo   1. Check the terminal windows for your public URLs
    echo   2. Copy the backend URL
    echo   3. Update cooin-frontend/src/constants/config.ts with backend URL
    echo   4. Add frontend URL to cooin-backend/.env CORS origins
    echo   5. Restart both backend and frontend
    echo.
)

echo ========================================
echo   Tunnels Running
echo ========================================
echo.
echo To stop tunnels:
echo   - Close the tunnel terminal windows
echo   - Or run: taskkill /F /IM cloudflared.exe
echo.
echo For persistent tunnels, see:
echo   CLOUDFLARE-TUNNEL-SETUP.md
echo.

pause
