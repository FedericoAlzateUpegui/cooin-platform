#!/bin/bash

# Cooin Platform - Cloudflare Tunnels Startup Script
# Mac/Linux version

set -e

echo ""
echo "========================================"
echo "  Cooin Platform - Cloudflare Tunnels"
echo "========================================"
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "[ERROR] cloudflared not found!"
    echo ""
    echo "Please install cloudflared first:"
    echo "  Mac: brew install cloudflared"
    echo "  Linux: See CLOUDFLARE-TUNNEL-SETUP.md"
    echo ""
    exit 1
fi

echo "[INFO] Checking services..."
echo ""

# Check if backend is running on port 8000
if ! lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "[WARNING] Backend not detected on port 8000"
    echo "          Please start backend first:"
    echo "          cd cooin-backend"
    echo "          python start_dev.py"
    echo ""
fi

# Check if frontend is running on port 8083
if ! lsof -Pi :8083 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "[WARNING] Frontend not detected on port 8083"
    echo "          Please start frontend first:"
    echo "          cd cooin-frontend"
    echo "          npx expo start --web --port 8083"
    echo ""
fi

# Check if config files exist
if [ -f "cloudflare-config.yml" ]; then
    echo "[OPTION 1] Named tunnels detected"
    echo "           Starting persistent tunnels..."
    echo ""

    # Start backend tunnel in background
    osascript -e 'tell app "Terminal" to do script "cd \"'"$PWD"'\" && cloudflared tunnel --config cloudflare-config.yml run cooin-backend"' &
    sleep 2

    # Start frontend tunnel in background
    osascript -e 'tell app "Terminal" to do script "cd \"'"$PWD"'\" && cloudflared tunnel --config cloudflare-frontend-config.yml run cooin-frontend"' &

    echo ""
    echo "[SUCCESS] Named tunnels started!"
    echo "          Check your configured URLs in Cloudflare dashboard"
    echo ""
else
    echo "[OPTION 2] No named tunnels configured"
    echo "           Starting quick tunnels..."
    echo "           (URLs will be displayed in each terminal)"
    echo ""

    # Start backend quick tunnel
    osascript -e 'tell app "Terminal" to do script "cd \"'"$PWD"'\" && echo \"Backend Tunnel Starting...\" && cloudflared tunnel --url http://localhost:8000"' &
    sleep 2

    # Start frontend quick tunnel
    osascript -e 'tell app "Terminal" to do script "cd \"'"$PWD"'\" && echo \"Frontend Tunnel Starting...\" && cloudflared tunnel --url http://localhost:8083"' &

    echo ""
    echo "[SUCCESS] Quick tunnels started!"
    echo ""
    echo "IMPORTANT:"
    echo "  1. Check the terminal windows for your public URLs"
    echo "  2. Copy the backend URL"
    echo "  3. Update cooin-frontend/src/constants/config.ts with backend URL"
    echo "  4. Add frontend URL to cooin-backend/.env CORS origins"
    echo "  5. Restart both backend and frontend"
    echo ""
fi

echo "========================================"
echo "  Tunnels Running"
echo "========================================"
echo ""
echo "To stop tunnels:"
echo "  - Close the tunnel terminal windows"
echo "  - Or run: pkill cloudflared"
echo ""
echo "For persistent tunnels, see:"
echo "  CLOUDFLARE-TUNNEL-SETUP.md"
echo ""
