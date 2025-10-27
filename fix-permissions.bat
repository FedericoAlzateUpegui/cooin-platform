@echo off
REM Cooin App - Fix Permissions Script
REM This script grants the current user full control over the cooin-app folder

echo.
echo ========================================
echo   Fixing Cooin App Folder Permissions
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] This script must be run as Administrator
    echo.
    echo To run as administrator:
    echo 1. Right-click this file: fix-permissions.bat
    echo 2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking current permissions...
echo.
icacls "C:\Windows\System32\cooin-app" | findstr /C:"Usuarios"

echo.
echo [2/3] Granting full control to current user...
echo.

REM Grant full control to the Users group
icacls "C:\Windows\System32\cooin-app" /grant Usuarios:(OI)(CI)F /T

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [3/3] SUCCESS! Permissions updated successfully.
    echo.
    echo You now have full control over the cooin-app folder.
    echo You can now edit files without admin privileges.
    echo.
) else (
    echo.
    echo [ERROR] Failed to update permissions.
    echo.
    echo Please try manual method (see PERMISSION-FIX.md)
    echo.
)

echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Close and reopen VS Code
echo 2. Try editing ngrok.yml again
echo 3. If still having issues, check PERMISSION-FIX.md
echo.
pause
