@echo off
REM ===================================================
REM Cooin Frontend Startup Script (Windows)
REM ===================================================
REM This script starts the React Native web app using
REM Expo with a clear cache on port 8083
REM ===================================================

echo.
echo ========================================
echo   Starting Cooin Frontend (Web)
echo ========================================
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
    echo WARNING: node_modules not found!
    echo Installing dependencies...
    echo.
    call npm install
    echo.
)

echo [1/1] Starting Expo web server on port 8083...
echo.
echo Frontend URL: http://localhost:8083
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Expo web with clear cache
npx expo start --web --port 8083 --clear
