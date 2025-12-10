#!/bin/bash
# Script para iniciar el frontend limpiamente

echo "🧹 Limpiando procesos antiguos..."
pkill -9 -f "expo start" 2>/dev/null || true
pkill -9 -f "jest-worker" 2>/dev/null || true
pkill -9 -f "metro" 2>/dev/null || true

echo "🗑️  Limpiando cachés..."
cd /Users/mariajimenez/Desktop/cooin-platform/cooin-frontend
rm -rf .expo
rm -rf node_modules/.cache

echo "🚀 Iniciando frontend..."
npx expo start --web --port 8083
