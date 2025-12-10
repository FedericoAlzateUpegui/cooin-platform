# 📱 Guía de Instalación de Cooin Web App en Mac


## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener:

- ✅ Una Mac con macOS 10.15 o superior
- ✅ Al menos 5 GB de espacio libre en disco
- ✅ Cuenta de GitHub https://github.com

---

## 🛠️ Instalación de Herramientas

### Paso 1: Instalar Homebrew (Administrador de Paquetes)

Homebrew es como una "tienda de aplicaciones" para desarrolladores en Mac.

**1.1** Abre la aplicación **Terminal** 

**1.2** Copia y pega este comando en la Terminal y presiona Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**1.3** Te pedirá tu contraseña de Mac (no se verá mientras la escribes, es normal)

**1.4** Presiona Enter cuando te lo pida para continuar la instalación

**1.5** Espera 5-10 minutos mientras se instala

**1.6** Verifica que se instaló correctamente:

```bash
brew --version
```

Deberías ver algo como: `Homebrew 4.x.x`

---

### Paso 2: Instalar Git

Git es la herramienta para descargar y gestionar el código del proyecto.

**2.1** En la Terminal, ejecuta:

```bash
brew install git
```

**2.2** Verifica la instalación:

```bash
git --version
```

Deberías ver: `git version 2.x.x`

---

### Paso 3: Instalar Python 3.12

Python es el lenguaje de programación que usa el backend.

**3.1** Instala Python con Homebrew:

```bash
brew install python@3.12
```

**3.2** Verifica la instalación:

```bash
python3 --version
```

Deberías ver: `Python 3.12.1` o superior

---

### Paso 4: Instalar Node.js y npm

Node.js y npm son necesarios para el frontend de la aplicación.

**4.1** Instala Node.js:

```bash
brew install node
```

**4.2** Verifica las instalaciones:

```bash
node --version
npm --version
```

Deberías ver versiones como:
- Node: `v24.7.0` o superior
- npm: `11.5.1` o superior

---

### Paso 5: Instalar PostgreSQL (Base de Datos)

PostgreSQL es la base de datos donde se guarda toda la información.

**5.1** Instala PostgreSQL:

```bash
brew install postgresql@14
```

**5.2** Inicia el servicio de PostgreSQL:

```bash
brew services start postgresql@14
```

**5.3** Verifica que está corriendo:

```bash
psql --version
```

Deberías ver: `psql (PostgreSQL) 14.x`

---

### Paso 6: Instalar Docker Desktop

Docker es necesario para ejecutar Redis (sistema de caché).

**6.1** Descarga Docker Desktop desde:
```
https://www.docker.com/products/docker-desktop/
```

**6.2** Descarga la versión para **Mac con procesador Intel** o **Mac con Apple Silicon** según tu Mac

**6.3** Abre el archivo `.dmg` descargado y arrastra Docker a Aplicaciones

**6.4** Abre Docker Desktop desde Aplicaciones

**6.5** Sigue el asistente de instalación (acepta los permisos que te pida)

**6.6** Espera a que aparezca la "ballena" (ícono de Docker) en la barra superior de tu Mac

**6.7** Verifica la instalación en la Terminal:

```bash
docker --version
```

Deberías ver: `Docker version 25.0.3` o superior

---

## 📥 Clonar el Proyecto desde GitHub

### Paso 7: Descargar el Código del Proyecto

**7.1** Crea una carpeta para tus proyectos (si no la tienes):

```bash
mkdir -p ~/Desktop
cd ~/Desktop
```

**7.2** Clona el repositorio de GitHub: (la rama que estamos utilizando es DEV)

```bash
git clone https://github.com/FedericoAlzateUpegui/cooin-platform.git
```

**7.3** Espera a que se descargue (puede tomar 1-2 minutos)

**7.4** Entra a la carpeta del proyecto:

```bash
cd cooin-platform
```

**7.5** Verifica que todo se descargó:

```bash
ls -la
```

Deberías ver carpetas como:
- `cooin-backend/`
- `cooin-frontend/`
- `cooin-ios/`

---

## 🔧 Configurar el Backend

### Paso 8: Configurar el Entorno Virtual de Python

**8.1** Navega a la carpeta del backend:

```bash
cd ~/Desktop/cooin-platform/cooin-backend
```

**8.2** Crea un entorno virtual:

```bash
python3 -m venv venv
```

**8.3** Activa el entorno virtual:

```bash
source venv/bin/activate
```

Verás que tu línea de comando ahora empieza con `(venv)`

**8.4** Actualiza pip (instalador de Python):

```bash
pip install --upgrade pip
```

---

### Paso 9: Instalar Dependencias del Backend

**9.1** Instala todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

**9.2** Espera 5-10 minutos mientras se instalan todas las dependencias

**9.3** Verifica que se instalaron:

```bash
pip list
```

Deberías ver una lista larga con paquetes como:
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- etc.

---

### Paso 10: Configurar Variables de Entorno

⚠️ **IMPORTANTE**: es delicado y aveces complejo, tener cuidado.

**10.1** Verifica que tienes el archivo de ejemplo:

```bash
ls -la | grep .env.example
```

Deberías ver: `.env.example`

si no lo ves en la ruta cooin-platform/
  └── cooin-backend/
      └── .env.example
    hay archivos que aveces se ocultan si es el caso: cmd +  shift + .(punto)

**10.2** Edita el archivo `.env`:

```bash
nano .env
```

**10.3** Busca y modifica SOLO estas 2 líneas importantes:

**Línea 1 - DATABASE_URL:**
```
# ENCUENTRA (línea 9):
DATABASE_URL=postgresql://your_username@localhost:5432/cooin_db

# CÁMBIALA POR (reemplaza "tu_usuario" con tu nombre de usuario de Mac):
DATABASE_URL=postgresql://tu_usuario@localhost:5432/cooin_db
```

Para saber tu usuario de Mac, abre otra terminal y ejecuta:
```bash
whoami
```
Usa ese nombre en lugar de **"tu_usuario"**

**Línea 2 - SECRET_KEY:**
```
# ENCUENTRA (línea 25):
SECRET_KEY=your-secret-key-here-replace-me-with-generated-key

# Genera una clave segura en otra terminal:
python3 -c "import secrets; print(secrets.token_urlsafe(64))"

# Copia TODO el resultado y reemplázalo en SECRET_KEY=
```

**10.5** verificar
- `REDIS_URL=redis://localhost:6379/0`
- BACKEND_CORS_ORIGINS=["http://localhost:8083"]`
- DEBUG=true`

**10.6** Guarda el archivo en nano:
- Presiona `Ctrl + X`
- Presiona `Y` (para confirmar)
- Presiona `Enter`

**10.7** Verifica que tu `.env` tiene las configuraciones correctas:

```bash
cat .env | grep DATABASE_URL
cat .env | grep SECRET_KEY | head -1
```

**🔒 SEGURIDAD:**
- ⚠️ **NUNCA** compartas tu archivo `.env` con nadie
- ⚠️ **NUNCA** lo subas a GitHub
- ⚠️ El `SECRET_KEY` debe ser único para tu instalación


---

## 📦 Configurar el Frontend

### Paso 11: Instalar Dependencias del Frontend

**11.1** Abre una **NUEVA TERMINAL** (Cmd+T para nueva pestaña)

**11.2** Navega a la carpeta del frontend:

```bash
cd ~/Desktop/cooin-platform/cooin-frontend
```

**11.3** Instala las dependencias de npm:

```bash
npm install
```

**11.4** Espera 10-15 minutos (¡sí, tarda bastante! ☕)

Verás mensajes como:
- `added X packages`
- `found 0 vulnerabilities`

**11.5** Verifica que se instaló todo:

```bash
ls -la node_modules | wc -l
```

Deberías ver un número grande (más de 1000)

---

## 🗄️ Configurar la Base de Datos

### Paso 12: Crear la Base de Datos

**12.1** Abre una **NUEVA TERMINAL**

**12.2** Crea la base de datos de Cooin:

```bash
createdb cooin_db
```

**12.3** Verifica que se creó:

```bash
psql -l | grep cooin
```

Deberías ver `cooin_db` en la lista

---

### Paso 13: Ejecutar las Migraciones

Las migraciones crean todas las tablas necesarias en la base de datos.

**13.1** Ve a la carpeta del backend:

```bash
cd ~/Desktop/cooin-platform/cooin-backend
```

**13.2** Activa el entorno virtual (si no lo está):

```bash
source venv/bin/activate
```

**13.3** Ejecuta las migraciones:

```bash
alembic upgrade head
```

**13.4** Verás mensajes como:
```
INFO  [alembic.runtime.migration] Running upgrade -> xxx
INFO  [alembic.runtime.migration] Running upgrade xxx -> yyy
```

**13.5** Verifica que se crearon las tablas:

```bash
psql -d cooin_db -c "\dt"
```

Deberías ver tablas como:
- `users`
- `user_profiles`
- `connections`
- `messages`
- `ratings`
- etc. (total: 12 tablas)

---

## 🐳 Configurar Docker y Redis

### Paso 14: Iniciar Redis con Docker

**14.1** Asegúrate de que Docker Desktop esté corriendo (ícono de ballena en la barra superior)

**14.2** Ve a la carpeta raíz del proyecto:

```bash
cd ~/Desktop/cooin-platform
```

**14.3** Inicia el contenedor de Redis:

```bash
docker-compose up -d redis
```

**14.4** Verás:
```
[+] Running 1/1
✔ Container cooin-redis  Started
```

**14.5** Verifica que Redis está corriendo:

```bash
docker ps
```

Deberías ver una línea con `cooin-redis` y estado `healthy`

**14.6** Prueba la conexión a Redis:

```bash
docker exec cooin-redis redis-cli PING
```

Debería responder: `PONG`

---

## 🚀 Iniciar la Aplicación



### Paso 15: Iniciar el Backend

**15.1** En una terminal, ve a la carpeta del backend:

```bash
cd ~/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
```

**15.2** Inicia el servidor:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**15.3** Verás mensajes como:
```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**15.4** ✅ ¡Backend corriendo! Déjalo abierto y NO cierres esta terminal.

---

### Paso 16: Iniciar el Frontend

**16.1** Abre una **NUEVA TERMINAL** (Cmd+T)

**16.2** Ve a la carpeta del frontend:

```bash
cd ~/Desktop/cooin-platform/cooin-frontend
```

**16.3** Inicia el servidor web:

```bash
npx expo start --web --port 8083
```

**16.4** Espera 1-2 minutos. Verás:
```
Starting Metro Bundler
› Metro waiting on exp://...
› Scan the QR code above with Expo Go (Android) or the Camera app (iOS)

› Press a │ open Android
› Press i │ open iOS simulator
› Press w │ open web

› Press r │ reload app
› Press m │ toggle menu
› Press ? │ show all commands

Logs for your project will appear below.
```

**16.5** Automáticamente se abrirá tu navegador en `http://localhost:8083`

**16.6** ✅ ¡Frontend corriendo! Déjalo abierto y NO cierres esta terminal.

---

## ✅ Verificar que Todo Funciona

### Paso 17: Verificación Completa

**17.1** Abre tu navegador y ve a estas URLs:

**Frontend (Aplicación Web):**
```
http://localhost:8083
```
Deberías ver la pantalla de login/registro de Cooin

**Backend API:**
```
http://localhost:8000/health
```
Deberías ver:
```json
{"status":"healthy","timestamp":1234567890,"version":"1.0.0"}
```

**Documentación de la API:**
```
http://localhost:8000/api/v1/docs
```
Deberías ver Swagger UI con todos los endpoints de la API

**17.2** Verifica Redis en la terminal:

```bash
docker ps
```

Debes ver `cooin-redis` con estado `healthy`

---

## 🛑 Cómo Detener la Aplicación

Cuando termines de usar la aplicación:

### Detener Frontend
En la terminal del frontend, presiona: **Ctrl + C**

### Detener Backend
En la terminal del backend, presiona: **Ctrl + C**

### Detener Redis
```bash
cd ~/Desktop/cooin-platform
docker-compose down
```

### Detener Docker Desktop (opcional)
Haz clic en el ícono de la ballena → **Quit Docker Desktop**

---

## 🔄 Cómo Iniciar la Aplicación Después

La próxima vez que quieras usar la aplicación:

### Terminal 1 - Docker & Redis:
```bash
open -a Docker
# Espera 30 segundos a que Docker inicie
cd ~/Desktop/cooin-platform
docker-compose up -d redis
```
tambien puedes simplemente abrir la aplicacion de docker y luego en la terminal iniciar Redis 


### Terminal 2 - Backend:
```bash
cd ~/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 3 - Frontend:
```bash
cd ~/Desktop/cooin-platform/cooin-frontend
npx expo start --web --port 8083
```

---

## 🔧 Solución de Problemas

### Problema: "command not found: brew"

**Solución:**
```bash
# Reinstala Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### Problema: "Cannot connect to Docker daemon"

**Solución:**
1. Abre Docker Desktop manualmente
2. Espera a que aparezca el ícono de la ballena en la barra superior
3. Intenta de nuevo

---

### Problema: "Port 8000 already in use"

**Solución:**
```bash
# Encuentra qué está usando el puerto
lsof -i :8000

# Mata el proceso (usa el PID de arriba)
kill -9 <PID>

# O mata todos los procesos en ese puerto
lsof -ti :8000 | xargs kill -9
```

---

### Problema: "Port 8083 already in use"

**Solución:**
```bash
# Mata el proceso
lsof -ti :8083 | xargs kill -9

# O usa otro puerto
npx expo start --web --port 8084
```

---

### Problema: "Module not found" en el frontend

**Solución:**
```bash
cd ~/Desktop/cooin-platform/cooin-frontend
rm -rf node_modules package-lock.json
npm install
npx expo start --web --port 8083 --clear
```

---

### Problema: "database 'cooin_db' does not exist"

**Solución:**
```bash
# Crea la base de datos
createdb cooin_db

# Ejecuta las migraciones
cd ~/Desktop/cooin-platform/cooin-backend
source venv/bin/activate
alembic upgrade head
```

---

### Problema: "psql: command not found"

**Solución:**
```bash
# Agrega PostgreSQL al PATH
echo 'export PATH="/usr/local/opt/postgresql@14/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verifica
psql --version
```

---

### Problema: Frontend muestra "Cannot connect to server"

**Solución:**
1. Verifica que el backend esté corriendo en otra terminal
2. Ve a: http://localhost:8000/health
3. Si no funciona, reinicia el backend
4. Limpia la caché del frontend:
```bash
npx expo start --web --port 8083 --clear
```

---

## 📚 Comandos Útiles

### Comandos de Git
```bash
# Ver cambios en el código
git status

# Descargar últimos cambios
git pull origin main

# Ver historial de cambios
git log --oneline -10
```

### Comandos de PostgreSQL
```bash
# Conectarse a la base de datos
psql -d cooin_db

# Dentro de psql:
\dt              # Ver todas las tablas
\d users         # Ver estructura de tabla users
SELECT * FROM users LIMIT 5;   # Ver primeros 5 usuarios
\q               # Salir
```

### Comandos de Docker
```bash
# Ver contenedores corriendo
docker ps

# Ver logs de Redis
docker logs cooin-redis

# Reiniciar Redis
docker restart cooin-redis

# Detener todos los contenedores
docker-compose down
```

### Comandos de Python/Backend
```bash
# Ver paquetes instalados
pip list

# Actualizar un paquete
pip install --upgrade <nombre-paquete>

# Ver versión de Python
python3 --version
```

### Comandos de Node/Frontend
```bash
# Ver paquetes instalados
npm list --depth=0

# Actualizar paquetes
npm update

# Limpiar caché
npm cache clean --force
```

---

## 📊 Estructura del Proyecto

```
cooin-platform/
├── cooin-backend/           # Backend (FastAPI + Python)
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   ├── models/         # Modelos de base de datos
│   │   ├── schemas/        # Validaciones
│   │   ├── services/       # Lógica de negocio
│   │   └── main.py         # Punto de entrada
│   ├── venv/               # Entorno virtual de Python
│   ├── requirements.txt    # Dependencias de Python
│   └── .env                # Variables de entorno
│
├── cooin-frontend/          # Frontend (React Native Web)
│   ├── src/
│   │   ├── screens/        # Pantallas de la app
│   │   ├── components/     # Componentes reutilizables
│   │   ├── services/       # Llamadas a la API
│   │   └── store/          # Estado global
│   ├── node_modules/       # Dependencias de npm
│   └── package.json        # Dependencias del proyecto
│
├── cooin-ios/               # App nativa iOS
├── docker-compose.yml       # Configuración de Docker
└── README.md               # Documentación general
```

---


## ✅ Checklist de Instalación Completa

Marca cada paso cuando lo completes:

- [ ] Homebrew instalado
- [ ] Git instalado
- [ ] Python 3.12 instalado
- [ ] Node.js y npm instalados
- [ ] PostgreSQL instalado e iniciado
- [ ] Docker Desktop instalado e iniciado
- [ ] Proyecto clonado desde GitHub
- [ ] Entorno virtual de Python creado
- [ ] Dependencias del backend instaladas
- [ ] Archivo .env configurado
- [ ] Dependencias del frontend instaladas
- [ ] Base de datos creada
- [ ] Migraciones ejecutadas
- [ ] Redis corriendo en Docker
- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 8083
- [ ] Primer usuario creado exitosamente

---

