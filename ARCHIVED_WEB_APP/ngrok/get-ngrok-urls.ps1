# Cooin App - Get Ngrok URLs
# This script retrieves the public URLs from ngrok and optionally updates the frontend config

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cooin App - Ngrok URL Retriever" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ngrok API endpoint (local)
$ngrokApiUrl = "http://localhost:4040/api/tunnels"

try {
    # Query ngrok API
    Write-Host "[1/3] Querying ngrok API..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri $ngrokApiUrl -Method Get -ErrorAction Stop

    # Extract tunnel information
    $tunnels = $response.tunnels

    if ($tunnels.Count -eq 0) {
        Write-Host ""
        Write-Host "[ERROR] No active ngrok tunnels found" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please make sure ngrok is running:" -ForegroundColor Yellow
        Write-Host "  Run: start-ngrok.bat" -ForegroundColor White
        Write-Host ""
        exit 1
    }

    # Find frontend and backend URLs
    $frontendUrl = ""
    $backendUrl = ""

    foreach ($tunnel in $tunnels) {
        $config = $tunnel.config
        $addr = $config.addr
        $publicUrl = $tunnel.public_url

        # Only use https URLs
        if ($publicUrl -like "https://*") {
            if ($addr -like "*:8083") {
                $frontendUrl = $publicUrl
            }
            elseif ($addr -like "*:8000") {
                $backendUrl = $publicUrl
            }
        }
    }

    Write-Host "[2/3] Ngrok tunnels found!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Frontend (Port 8083):" -ForegroundColor Cyan
    Write-Host "  $frontendUrl" -ForegroundColor White
    Write-Host ""
    Write-Host "Backend (Port 8000):" -ForegroundColor Cyan
    Write-Host "  $backendUrl" -ForegroundColor White
    Write-Host ""

    # Ask if user wants to update frontend config
    Write-Host "[3/3] Configuration Update" -ForegroundColor Yellow
    Write-Host ""
    $updateConfig = Read-Host "Update frontend config to use ngrok backend URL? (y/n)"

    if ($updateConfig -eq "y" -or $updateConfig -eq "Y") {
        $configPath = ".\cooin-frontend\src\constants\config.ts"

        if (Test-Path $configPath) {
            # Read the config file
            $configContent = Get-Content $configPath -Raw

            # Create backup
            $backupPath = $configPath + ".backup"
            Copy-Item $configPath $backupPath -Force
            Write-Host ""
            Write-Host "  Backup created: $backupPath" -ForegroundColor Gray

            # Update BASE_URL
            $apiUrl = "$backendUrl/api/v1"
            $configContent = $configContent -replace "BASE_URL:\s*['\`"][^'\`"]*['\`"]", "BASE_URL: '$apiUrl'"

            # Save updated config
            Set-Content $configPath $configContent -NoNewline

            Write-Host "  Config updated: $configPath" -ForegroundColor Green
            Write-Host ""
            Write-Host "  New BASE_URL: $apiUrl" -ForegroundColor White
            Write-Host ""
            Write-Host "[SUCCESS] Frontend will now use ngrok backend!" -ForegroundColor Green
            Write-Host ""
            Write-Host "IMPORTANT:" -ForegroundColor Yellow
            Write-Host "  1. Restart frontend Metro bundler (Ctrl+C then restart)" -ForegroundColor White
            Write-Host "  2. Hard refresh browser (Ctrl+Shift+R)" -ForegroundColor White
        }
        else {
            Write-Host ""
            Write-Host "[ERROR] Config file not found: $configPath" -ForegroundColor Red
        }
    }
    else {
        Write-Host ""
        Write-Host "[INFO] Config not updated. You can manually update:" -ForegroundColor Yellow
        Write-Host "  File: cooin-frontend\src\constants\config.ts" -ForegroundColor White
        Write-Host "  BASE_URL: '$backendUrl/api/v1'" -ForegroundColor White
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Share your public frontend URL:" -ForegroundColor Green
    Write-Host "  $frontendUrl" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "[ERROR] Could not connect to ngrok API" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Make sure ngrok is running (start-ngrok.bat)" -ForegroundColor White
    Write-Host "  2. Check that ngrok web interface is accessible:" -ForegroundColor White
    Write-Host "     http://localhost:4040" -ForegroundColor White
    Write-Host ""
    exit 1
}
