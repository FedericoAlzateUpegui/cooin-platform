@echo off
REM Cooin App - Ngrok Tunnel Starter
REM This script starts ngrok tunnels for both frontend and backend

echo.
echo ========================================
echo   Cooin App - Starting Ngrok Tunnels
echo ========================================
echo.

REM Check if ngrok is installed
where ngrok >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ngrok is not installed or not in PATH
    echo.
    echo Please install ngrok:
    echo 1. Download from https://ngrok.com/download
    echo 2. Extract ngrok.exe to a folder
    echo 3. Add the folder to your PATH or copy ngrok.exe to C:\Windows\System32
    echo.
    pause
    exit /b 1
)

REM Check if ngrok.yml exists
if not exist "ngrok.yml" (
    echo [ERROR] ngrok.yml configuration file not found
    echo.
    echo Expected location: %CD%\ngrok.yml
    echo.
    pause
    exit /b 1
)

REM Check if auth token is set
findstr /C:"YOUR_NGROK_AUTH_TOKEN_HERE" ngrok.yml >nul
if %ERRORLEVEL% EQU 0 (
    echo [WARNING] Ngrok auth token not configured!
    echo.
    echo Please update ngrok.yml with your auth token:
    echo 1. Go to https://dashboard.ngrok.com/get-started/your-authtoken
    echo 2. Copy your auth token
    echo 3. Edit ngrok.yml and replace YOUR_NGROK_AUTH_TOKEN_HERE
    echo.
    echo Press any key to continue anyway (will use free plan)...
    pause >nul
    echo.
)

echo [1/3] Starting ngrok tunnels
echo.
echo Frontend: http://localhost:8083
echo Backend:  http://localhost:8000
echo.

REM Start ngrok with the config file
ngrok start --all --config=ngrok.yml

REM If ngrok exits, show message
echo.
echo ========================================
echo   Ngrok tunnels stopped
echo ========================================
echo.
pause
