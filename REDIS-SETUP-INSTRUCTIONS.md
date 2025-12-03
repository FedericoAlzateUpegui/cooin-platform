# 🔧 Redis Setup Instructions - IMPORTANTE

**Fecha**: 2025-12-03
**Para**: Compañero de desarrollo
**De**: María

---

## 🚨 CAMBIOS CRÍTICOS EN EL CÓDIGO

Se ha **habilitado Redis** en el backend para solucionar problemas de caídas de la app y pérdida de sesiones.

### ⚠️ Antes de hacer `git pull`:

Si haces `git pull` y no tienes Redis configurado, **el backend NO funcionará correctamente**.

---

## 📋 CAMBIOS REALIZADOS

### Archivo modificado: `cooin-backend/app/main.py`

**Líneas 198-205** - Se descomentó la inicialización de Redis:

```python
# ANTES (comentado):
# TEMP FIX: Disable Redis init for now, use in-memory cache
logger.warning("Redis initialization disabled - using in-memory cache only")
# try:
#     await asyncio.wait_for(init_cache(), timeout=5.0)
#     ...

# AHORA (activo):
try:
    await asyncio.wait_for(init_cache(), timeout=5.0)
    logger.info("Cache service initialized successfully with Redis")
except asyncio.TimeoutError:
    logger.warning("Cache initialization timed out (5s), using in-memory cache fallback")
except Exception as e:
    logger.error(f"Cache initialization failed: {e}, using in-memory cache fallback")
```

---

## 🛠️ CONFIGURACIÓN REQUERIDA (Windows)

### Paso 1: Instalar Docker Desktop

1. Descarga Docker Desktop para Windows: https://www.docker.com/products/docker-desktop/
2. Instala y reinicia tu computadora si es necesario
3. Abre Docker Desktop y espera a que inicie completamente (icono de ballena)

### Paso 2: Verificar que Docker funciona

Abre PowerShell o CMD y ejecuta:

```bash
docker --version
```

Deberías ver algo como: `Docker version 25.0.3`

### Paso 3: Iniciar Redis

Navega a la carpeta del proyecto y ejecuta:

```bash
# Cambiar a la carpeta del proyecto
cd C:\ruta\a\tu\proyecto\cooin-platform

# Iniciar Redis con Docker Compose
docker-compose up -d redis

# Verificar que Redis está corriendo
docker ps
```

Deberías ver algo como:

```
CONTAINER ID   IMAGE           STATUS                   PORTS
66679b07e35f   redis:7-alpine  Up 2 minutes (healthy)   0.0.0.0:6379->6379/tcp
```

### Paso 4: Verificar conexión a Redis

```bash
# Probar que Redis responde
docker exec cooin-redis redis-cli ping
```

Debería responder: `PONG`

### Paso 5: Actualizar código con Git

```bash
git pull origin main
```

### Paso 6: Reiniciar Backend

Si ya tenías el backend corriendo, **detenerlo** (Ctrl+C) y volver a iniciarlo:

```bash
cd cooin-backend
python -m venv venv
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Paso 7: Verificar que funcionó

En los logs del backend deberías ver:

```
INFO - Starting up Cooin API...
INFO - Connected to Redis cache server (attempt 1/3)
INFO - Cache service initialized successfully with Redis
```

Si ves esto, **¡está funcionando!** ✅

---

## ❌ SI NO QUIERES CONFIGURAR REDIS (NO RECOMENDADO)

Si por alguna razón NO puedes instalar Docker/Redis en tu máquina, el backend tiene un **fallback automático** a cache en memoria.

**PERO**: Tendrás estos problemas:
- La app puede caerse con múltiples usuarios
- Las sesiones se pierden al reiniciar
- Performance degradado
- Rate limiting no funciona correctamente

Para usar sin Redis, el backend automáticamente detectará que Redis no está disponible y usará memoria.

---

## 🔍 TROUBLESHOOTING

### Problema: "Cannot connect to Redis"

**Solución**:
1. Verifica que Docker Desktop está corriendo (icono de ballena en la barra de tareas)
2. Verifica que el container está corriendo: `docker ps`
3. Si no aparece, inicia Redis: `docker-compose up -d redis`

### Problema: "docker: command not found"

**Solución**:
1. Reinstala Docker Desktop
2. Reinicia tu terminal/PowerShell después de instalar
3. Verifica que Docker Desktop está en el PATH del sistema

### Problema: Backend dice "using in-memory cache fallback"

**Solución**:
Esto significa que Redis NO está conectado. Verifica:
1. `docker ps` - ¿Aparece cooin-redis?
2. `docker logs cooin-redis` - ¿Hay errores?
3. Archivo `.env` - ¿Tiene `REDIS_URL=redis://localhost:6379/0`?

### Problema: Docker Compose no encuentra el archivo

**Solución**:
Verifica que estás en la carpeta raíz del proyecto (`cooin-platform/`) donde está el archivo `docker-compose.yml`

---

## 📊 VERIFICACIÓN FINAL

Para verificar que todo está funcionando correctamente:

```bash
# 1. Redis está corriendo
docker ps | grep redis
# Debe mostrar: cooin-redis ... Up ... 0.0.0.0:6379->6379/tcp

# 2. Backend puede conectarse
# En los logs del backend debes ver:
# INFO - Cache service initialized successfully with Redis

# 3. Redis está almacenando datos
docker exec cooin-redis redis-cli KEYS "*"
# Debe mostrar algunas keys si el backend está activo
```

---

## 🎯 POR QUÉ ESTO ES IMPORTANTE

**Antes** (sin Redis):
- ❌ App se caía con múltiples usuarios
- ❌ Sesiones se perdían al reiniciar backend
- ❌ Performance lento
- ❌ Cache en memoria RAM (se llena rápido)

**Ahora** (con Redis):
- ✅ App estable con múltiples usuarios
- ✅ Sesiones persisten entre reinicios
- ✅ Performance mejorado significativamente
- ✅ Cache persistente y rápido
- ✅ Rate limiting funcional
- ✅ Escalable a producción

---

## 📞 CONTACTO

Si tienes problemas con esta configuración, contacta a María.

**Archivos clave en Git**:
- `cooin-backend/app/main.py` (líneas 198-205) - Cambio principal
- `docker-compose.yml` - Configuración de Redis
- `redis.conf` - Configuración avanzada de Redis
- `.env` - Variable `REDIS_URL`

---

## 🚀 RESUMEN RÁPIDO (TL;DR)

```bash
# 1. Instalar Docker Desktop para Windows
# 2. Abrir terminal en la carpeta del proyecto
cd cooin-platform

# 3. Iniciar Redis
docker-compose up -d redis

# 4. Verificar
docker ps

# 5. Actualizar código
git pull origin main

# 6. Reiniciar backend
cd cooin-backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. Buscar en logs: "Cache service initialized successfully with Redis" ✅
```

---

**Última actualización**: 2025-12-03
**Versión**: 1.0
