@echo off
REM ===================================================
REM Cooin Services Health Check (Windows)
REM ===================================================
REM This script checks the status of all required services
REM ===================================================

echo.
echo ========================================
echo   Cooin Platform - Services Check
echo ========================================
echo.

REM Check Docker
echo [1/5] Checking Docker...
docker info >nul 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Docker is running
) else (
    echo   [ERROR] Docker is not running
    echo   Please start Docker Desktop
)
echo.

REM Check Redis Container
echo [2/5] Checking Redis container...
docker ps --filter "name=redis" --format "{{.Names}}" | findstr "redis" >nul 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Redis container is running
    docker ps --filter "name=redis" --format "   Container: {{.Names}} - Status: {{.Status}}"
) else (
    echo   [ERROR] Redis container not found
    echo   Run: docker-compose up -d redis
)
echo.

REM Check Backend Server
echo [3/5] Checking Backend Server...
curl -s http://localhost:8000/health >nul 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Backend server is running at http://localhost:8000
) else (
    echo   [OFFLINE] Backend server not responding
    echo   Run: start-backend.bat or start-all.bat
)
echo.

REM Check Frontend Server
echo [4/5] Checking Frontend Server...
curl -s http://localhost:8083 >nul 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Frontend server is running at http://localhost:8083
) else (
    echo   [OFFLINE] Frontend server not responding
    echo   Run: start-frontend.bat or start-all.bat
)
echo.

REM Check Python Virtual Environment
echo [5/5] Checking Python Virtual Environment...
if exist "cooin-backend\venv\Scripts\python.exe" (
    echo   [OK] Virtual environment found
    "cooin-backend\venv\Scripts\python.exe" --version
) else (
    echo   [ERROR] Virtual environment not found
    echo   Run: cd cooin-backend ^&^& python -m venv venv
)
echo.

REM Check Cloudflared
where cloudflared >nul 2>nul
if %errorlevel% equ 0 (
    echo   [OPTIONAL] Cloudflared is installed
    cloudflared --version
) else (
    echo   [INFO] Cloudflared not installed (optional)
    echo   Install: winget install cloudflare.cloudflared
)

echo.
echo ========================================
echo   Check Complete
echo ========================================
echo.
pause
