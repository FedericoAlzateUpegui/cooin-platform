# 🚀 Quick Start - Cooin Platform

## Prerequisitos (Mac & Windows)
- Docker Desktop instalado
- Python 3.12
- Node.js 18+

## Inicio Rápido (3 pasos)

### 1️⃣ Iniciar servicios (Redis)
```bash
# En la raíz del proyecto
docker-compose up -d
```

### 2️⃣ Iniciar Backend
```bash
# Terminal 1
cd cooin-backend
source venv/bin/activate  # Mac/Linux
# .\venv\Scripts\activate  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3️⃣ Iniciar Frontend
```bash
# Terminal 2
cd cooin-frontend
npm start
# o usar: ./start-frontend.sh (solo Mac)
```

## ✅ Verificar que todo funciona

- Backend: http://localhost:8000/health
- API Docs: http://localhost:8000/api/v1/docs
- Frontend: http://localhost:8083
- Redis: `docker ps` (debe mostrar cooin-redis healthy)

## 🛑 Detener todo

```bash
# Detener frontend: Ctrl+C en terminal
# Detener backend: Ctrl+C en terminal
# Detener Redis:
docker-compose down
```

## 🔧 Problemas Comunes

### Redis no inicia
```bash
docker-compose down
docker-compose up -d
docker logs cooin-redis
```

### Frontend lento
```bash
# Limpiar caché
cd cooin-frontend
rm -rf .expo node_modules/.cache
npm start
```

### Base de datos desincronizada
```bash
cd cooin-backend
source venv/bin/activate
alembic upgrade head
```

## 📊 Status Check
```bash
# Ver todos los servicios
docker-compose ps
curl http://localhost:8000/health
curl http://localhost:8083
```
