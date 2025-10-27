# Cooin Platform - Collaboration Guide

Welcome to the Cooin Platform! This guide will help partners and developers get started with the project.

## 📦 Repository Access

**Repository URL:** https://github.com/FedericoAlzateUpegui/cooin-platform

### Getting Access

To collaborate on this project, you need to be added as a collaborator:

1. Share your GitHub username with the project owner
2. You'll receive an invitation email from GitHub
3. Accept the invitation to gain access

## 🚀 Quick Start for Developers

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/FedericoAlzateUpegui/cooin-platform.git

# Navigate to project directory
cd cooin-platform
```

### 2. Setup Development Environment

#### Prerequisites
- **Backend**: Python 3.10+, PostgreSQL 14+
- **Frontend**: Node.js 18+, npm or yarn
- **iOS** (optional): Xcode 15+, macOS 13+

#### Backend Setup
```bash
cd cooin-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd cooin-frontend

# Install dependencies
npm install

# Start web app
npx expo start --web
```

### 3. Read the Documentation

- **Main README**: [README.md](./README.md) - Project overview and features
- **Technology Stack**: [TECH_STACK.md](./TECH_STACK.md) - Detailed tech documentation
- **Launch Guide**: [HOW-TO-LAUNCH-WEB-APP.md](./HOW-TO-LAUNCH-WEB-APP.md) - Step-by-step launch instructions
- **Deployment**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Production deployment guide
- **Current Tasks**: [TODO.md](./TODO.md) - Current and planned tasks

## 🔧 Development Workflow

### Branch Strategy

```bash
# Always create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
git add .
git commit -m "Description of changes"

# Push to remote
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Coding Standards

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use ESLint configuration, strict TypeScript
- **Commits**: Write clear, descriptive commit messages
- **Testing**: Write tests for new features

### Pull Request Process

1. Create feature branch from `main`
2. Make your changes
3. Test thoroughly (backend + frontend)
4. Create Pull Request with description:
   - What changed?
   - Why was it changed?
   - How to test it?
5. Wait for code review
6. Address feedback if any
7. Merge after approval

## 🌐 Testing Your Changes Publicly

### Using Ngrok (Quick Testing)

Share your local development with others:

```bash
# Start backend and frontend
# Terminal 1: Backend on port 8000
# Terminal 2: Frontend on port 8083

# Terminal 3: Start ngrok
cd cooin-platform
start-ngrok.bat  # Windows
# Or: ./start-ngrok.sh  # Mac/Linux

# Get public URLs
powershell -ExecutionPolicy Bypass -File .\get-ngrok-urls.ps1
```

See [NGROK-QUICKSTART.md](./NGROK-QUICKSTART.md) for details.

### Deploying to Staging

For longer-term testing, deploy to a staging environment:

- **Frontend**: Use Vercel (see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md))
- **Backend**: Use Heroku, Railway, or similar
- **Database**: Use managed PostgreSQL (Supabase, Neon, etc.)

## 👥 Team Communication

### Where to Discuss

- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code review and discussions
- **GitHub Discussions**: General questions and ideas

### Creating Issues

When reporting bugs or requesting features:

```markdown
## Description
Clear description of the issue or feature

## Steps to Reproduce (for bugs)
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Platform: Web/iOS/Mobile
- Browser/Device: Chrome 120, iPhone 15, etc.
- Version: Latest main branch
```

## 📱 Platform-Specific Notes

### Web App (React Native Web)
- Primary development platform
- Located in `cooin-frontend/`
- Runs on Expo Web
- Full feature parity with mobile

### iOS App (Native Swift)
- Located in `cooin-ios/`
- SwiftUI interface
- Requires Xcode
- Shares API with web/mobile

### Mobile App (React Native)
- Same codebase as web (`cooin-frontend/`)
- Run with `npx expo start`
- Test on iOS/Android simulators or physical devices

## 🔒 Security Guidelines

### DO NOT Commit

- ❌ `.env` files with real credentials
- ❌ API keys or tokens
- ❌ `ngrok.yml` (contains auth token)
- ❌ Private keys or certificates
- ❌ Database dumps with real data

### DO Commit

- ✅ `.env.example` files (with placeholder values)
- ✅ Documentation
- ✅ Code and tests
- ✅ Configuration templates

### Environment Variables

Use `.env.example` as template:

```bash
# Copy example file
cp cooin-backend/.env.example cooin-backend/.env

# Edit with your values
# NEVER commit the real .env file
```

## 🐛 Troubleshooting

### Common Issues

#### "Cannot find module" errors
```bash
# Backend
pip install -r requirements.txt

# Frontend
rm -rf node_modules package-lock.json
npm install
```

#### Database connection errors
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Run migrations: alembic upgrade head
```

#### CORS errors
```bash
# Add your frontend URL to backend .env:
# BACKEND_CORS_ORIGINS=["http://localhost:8083"]
```

#### Port already in use
```bash
# Backend (port 8000)
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -ti:8000 | xargs kill -9

# Frontend (port 8083)
# Similar process for port 8083
```

## 📚 Learning Resources

### Project Documentation
- Main README: Project overview
- TECH_STACK.md: Technology details
- TODO.md: Current and planned work

### External Resources
- **FastAPI**: https://fastapi.tiangolo.com/
- **React Native**: https://reactnative.dev/
- **Expo**: https://docs.expo.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/

## 🎯 Current Development Focus

See [TODO.md](./TODO.md) for detailed task list.

**High Priority:**
- Web deployment and public access
- Partner collaboration setup
- Production environment configuration

**In Progress:**
- Payment integration
- Admin dashboard
- Enhanced analytics

## 📞 Getting Help

1. **Check Documentation**: Read relevant docs first
2. **Search Issues**: Someone may have had the same problem
3. **Ask in Discussions**: General questions
4. **Create Issue**: Bug reports or feature requests
5. **Contact Owner**: Direct message for urgent/private matters

## ✅ Checklist for New Contributors

- [ ] Clone repository
- [ ] Set up development environment
- [ ] Read main README
- [ ] Read TECH_STACK.md
- [ ] Run backend locally
- [ ] Run frontend locally
- [ ] Test basic functionality (register, login)
- [ ] Create a test feature branch
- [ ] Make a small change
- [ ] Create test Pull Request
- [ ] Join team communication channels

---

**Welcome to the Cooin team! We're excited to have you contribute to this platform.**

For questions, open an issue or reach out to the project maintainer.
