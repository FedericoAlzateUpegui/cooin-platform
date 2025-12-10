# Cooin Platform

Peer-to-peer lending/borrowing platform with web, iOS, and mobile apps.

---

## 🌟 Features

- Multi-language (English/Spanish)
- Intelligent matching
- JWT authentication
- Real-time system notifications
- Cross-platform (Web/iOS/Mobile)
- Advanced security & rate limiting
- Redis caching

---

## 📁 Project Structure

```
cooin-platform/
├── cooin-backend/          # FastAPI backend server
├── cooin-frontend/         # React Native web & mobile app
├── cooin-ios/              # Native iOS Swift app
└── TECH_STACK.md          # Technology documentation
```

---

## 🚀 Quick Start

**Prerequisites**: Python 3.10+, PostgreSQL 14+, Node.js 18+, Docker Desktop (for Redis)

### Docker & Redis
```bash
docker-compose up -d redis  # Start Redis container
docker ps                   # Check status
docker-compose down         # Stop Redis
```
→ See [DOCKER-SETUP-GUIDE.md](./DOCKER-SETUP-GUIDE.md)

### Backend
```bash
cd cooin-backend
python3 -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with DB credentials
createdb cooin_db && alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
→ http://localhost:8000 | API docs: /api/v1/docs

### Frontend
```bash
cd cooin-frontend && npm install
npx expo start --web --port 8083  # Web
npx expo start --ios              # iOS simulator
```
→ http://localhost:8083

### iOS Native
```bash
cd cooin-ios/CooinNew && open CooinNew.xcodeproj
```

---

## 🔧 Configuration

**Backend** (`.env`):
```env
DATABASE_URL=postgresql://username@localhost:5432/cooin_db
SECRET_KEY=<generated-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:8083"]
REDIS_URL=redis://localhost:6379/0
```

**Frontend** (`src/constants/config.ts`):
```typescript
BASE_URL: 'http://127.0.0.1:8000/api/v1'
```

---

## 🏗️ Tech Stack

**Backend**: FastAPI, PostgreSQL, SQLAlchemy, Redis, JWT, Uvicorn
**Frontend**: React Native, Expo, TypeScript, i18next, Zustand, Axios
**iOS**: Swift, SwiftUI, Combine

→ See [TECH_STACK.md](./TECH_STACK.md) for details

---

## 🌍 i18n

**Languages**: English, Spanish (275+ keys)
**Add Language**: Create `src/i18n/locales/{code}.json`, add to `config.ts`

---

## 📱 Platform Status

| Platform | Status |
|----------|--------|
| Web/Backend/iOS | ✅ Production Ready |
| Android | 🚧 In Development |

---

## 🔒 Security

- Multi-layer middleware (headers, validation, DDoS protection, rate limiting 100/hr)
- JWT (30min access, 7day refresh)
- bcrypt password hashing
- CORS whitelist
- Environment-aware security (dev/staging/production)

---

## 🐛 Common Issues

- **CORS errors**: Add frontend URL to `BACKEND_CORS_ORIGINS` in `.env`
- **DB connection**: Verify PostgreSQL running: `pg_ctl status`
- **Redis**: Optional - falls back to in-memory cache
- **ModuleNotFoundError (Windows)**: Use full Python path or venv
- **Frontend cache**: `rm -rf node_modules && npm install`
- **Permission denied**: Project in System32 - move to user folder

→ See [PERMISSION-FIX.md](./PERMISSION-FIX.md) | [HISTORY.md](./HISTORY.md)

---

## 🌐 Public Access

### Cloudflare Tunnel (Recommended) ⭐
**Free | Unlimited | Persistent URLs**

```bash
# Install: winget install cloudflare.cloudflared (Windows) | brew install cloudflared (Mac)
cloudflared tunnel --url http://localhost:8000   # Backend
cloudflared tunnel --url http://localhost:8083   # Frontend
```
→ [CLOUDFLARE-QUICKSTART.md](./CLOUDFLARE-QUICKSTART.md)

---

## 📖 Documentation

**Setup**: [LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md) | [TECH_STACK.md](./TECH_STACK.md)
**Docker/Redis**: [DOCKER-SETUP-GUIDE.md](./DOCKER-SETUP-GUIDE.md)
**Tunnels**: [Cloudflare Quick](./CLOUDFLARE-QUICKSTART.md)
**Troubleshooting**: [PERMISSION-FIX.md](./PERMISSION-FIX.md) | [HISTORY.md](./HISTORY.md) | [TODO.md](./TODO.md)
**Contributing**: [DP.md](./DP.md) - Documentation Process guide

---

Proprietary software. Developed with Claude AI.
