# Cooin Platform

Peer-to-peer lending/borrowing platform with web, iOS, and mobile apps.

## 🌟 Features

- Multi-language (English/Spanish) | Intelligent matching | JWT auth | Real-time messaging
- Cross-platform (Web/iOS/Mobile) | Advanced security & rate limiting | Redis caching

## 📁 Project Structure

```
cooin-platform/
├── cooin-backend/          # FastAPI backend server
├── cooin-frontend/         # React Native web & mobile app
├── cooin-ios/              # Native iOS Swift app
└── TECH_STACK.md          # Comprehensive technology documentation
```

## 🚀 Quick Start

**Prerequisites**: Python 3.10+, PostgreSQL 14+, Node.js 18+, Redis (optional)

### Backend
```bash
cd cooin-backend
python3 -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with DB credentials + generate SECRET_KEY
createdb cooin_db && alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
**Windows**: If `ModuleNotFoundError`, use full path: `"C:\Users\USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe" -m uvicorn...`

→ `http://localhost:8000` | API docs: `/api/v1/docs` | Health: `/health`

### Frontend
```bash
cd cooin-frontend && npm install
npx expo start --web          # Web: http://localhost:8081
npx expo start --ios          # iOS simulator
npx expo start --android      # Android
```

### iOS Native
```bash
cd cooin-ios/CooinNew && open CooinNew.xcodeproj
```

## 🔧 Configuration

**Backend** (`.env`):
```env
DATABASE_URL=postgresql://username@localhost:5432/cooin_db
SECRET_KEY=<generated-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8081"]
REDIS_URL=redis://localhost:6379/0  # Optional
```

**Frontend** (`src/constants/config.ts`):
```typescript
export const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8000/api/v1',
  TIMEOUT: 10000,
} as const;
```

## 🧪 Testing
```bash
cd cooin-backend && pytest                      # Backend
cd cooin-frontend && npm test                   # Frontend
cd cooin-ios/CooinNew && xcodebuild test ...    # iOS
```

## 🏗️ Tech Stack

**Backend**: FastAPI, PostgreSQL, SQLAlchemy, Redis, JWT, Uvicorn
**Frontend**: React Native, Expo, TypeScript, i18next, Zustand, Axios
**iOS**: Swift, SwiftUI, Combine
→ See [TECH_STACK.md](./TECH_STACK.md) for details

## 🌍 i18n

**Languages**: English, Spanish (275+ keys)
**Add Language**: Create `src/i18n/locales/{code}.json`, copy `en.json` structure, add to `config.ts`

## 📱 Platform Status

| Platform | Status |
|----------|--------|
| Web/Backend/iOS | ✅ Production Ready |
| Android | 🚧 In Development |

## 🔒 Security

Multi-layer middleware (headers, validation, DDoS, rate limiting 100/hr) | JWT (30min access, 7day refresh) | bcrypt | CORS whitelist

**API Docs**: `http://localhost:8000/api/v1/docs` (Swagger) | `/redoc` | `/openapi.json`

## 🐛 Common Issues

**CORS errors**: Add frontend URL to `BACKEND_CORS_ORIGINS` in `.env`
**DB connection**: Verify PostgreSQL running: `pg_ctl status` | `createdb cooin_db`
**Redis**: Optional - falls back to in-memory cache
**ModuleNotFoundError (Windows)**: Multiple Pythons - use full path or venv (see TODO.md)
**Frontend cache**: `rm -rf node_modules && npm install` | `npx expo start --clear`
**Permission denied**: Project in System32 - run `fix-permissions.bat` as admin OR move to user folder

→ See [PERMISSION-FIX.md](./PERMISSION-FIX.md) | [HISTORY.md](./HISTORY.md)

## 🤝 Development

**Git**: Create branch → commit → push → PR | **Always use GitHub Desktop for pushing** (credential issues)

**Services** (separate terminals):
```bash
# 1. Backend: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 2. Frontend: npx expo start --web
# 3. Redis: redis-server (optional)
```

## 🌐 Public Access

### Cloudflare Tunnel (Recommended) ⭐
**Free forever | Unlimited | Persistent URLs | Custom domains | CDN performance**

```bash
# Install: winget install cloudflare.cloudflared (Windows) | brew install cloudflared (Mac)
cloudflared tunnel --url http://localhost:8000   # Backend
cloudflared tunnel --url http://localhost:8083   # Frontend
```
→ [CLOUDFLARE-QUICKSTART.md](./CLOUDFLARE-QUICKSTART.md) | [Full Setup](./CLOUDFLARE-TUNNEL-SETUP.md)

### Ngrok (Alternative)
**2hr sessions | Random URLs**
```bash
ngrok http 8000   # Backend
ngrok http 8083   # Frontend
```
→ [NGROK-QUICKSTART.md](./NGROK-QUICKSTART.md) | [Full Setup](./NGROK-SETUP.md)

## 📊 Status

✅ Backend API | Web/iOS (i18n) | Auth | Matching | Messaging | Cloudflare/Ngrok
🚧 Payment | Admin Dashboard

## 📖 Documentation

**Setup**: [LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md) | [TECH_STACK.md](./TECH_STACK.md)
**Tunnels**: [Cloudflare Quick](./CLOUDFLARE-QUICKSTART.md) | [Cloudflare Full](./CLOUDFLARE-TUNNEL-SETUP.md) | [Ngrok Quick](./NGROK-QUICKSTART.md) | [Ngrok Full](./NGROK-SETUP.md)
**Troubleshooting**: [PERMISSION-FIX.md](./PERMISSION-FIX.md) | [HISTORY.md](./HISTORY.md) | [TODO.md](./TODO.md)
**Contributing**: [DOCUMENTATION_PROCESS.md](./DOCUMENTATION_PROCESS.md) - How to maintain project documentation

---

Proprietary software. Developed with Claude AI.
