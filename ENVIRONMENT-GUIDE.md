# Cooin Web App - Environment Configuration Guide

**Version**: 1.0
**Last Updated**: 2025-11-19 (Session 15)

---

## 🌍 Overview

The Cooin application now supports **environment-aware security configuration**, allowing you to:
- Develop freely without security restrictions
- Deploy to production with full security enabled
- Test in staging with production-like security

---

## 📋 Available Environments

| Environment | Purpose | Security Level | Debug Mode |
|-------------|---------|----------------|------------|
| **development** | Local development | Relaxed | Enabled |
| **staging** | Pre-production testing | Strict | Disabled |
| **production** | Live application | Strict | Disabled |

---

## 🔧 Current Configuration

### Development Mode (Current)

**File**: `cooin-backend/.env`

```env
ENVIRONMENT=development
DEBUG=True
ENABLE_SECURITY_HEADERS=True
ENABLE_RATE_LIMITING=True
ENABLE_DDOS_PROTECTION=True
ENABLE_REQUEST_VALIDATION=True
ENABLE_SECURITY_LOGGING=True
```

**Security Behavior**:
- ✅ Security headers added (relaxed CSP)
- ✅ Rate limiting enabled (high limits: 1000 req/min)
- ✅ DDoS protection enabled (relaxed thresholds)
- ✅ Request validation enabled (logs only)
- ✅ All hosts allowed (TrustedHostMiddleware)
- ✅ API docs accessible at `/api/v1/docs`
- ✅ Detailed error messages

**CORS Allowed**:
- All localhost ports
- Cloudflare tunnels
- Local network IPs

---

## 🚀 Switching Environments

### Option 1: Change Environment Variable (Recommended)

Simply update the `ENVIRONMENT` variable in your `.env` file:

```env
# Development
ENVIRONMENT=development

# Staging
ENVIRONMENT=staging

# Production
ENVIRONMENT=production
```

Then restart the backend:
```cmd
# Stop server (Ctrl+C)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Option 2: Use Separate Environment Files

#### For Development (Default)
```cmd
# Uses .env file
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### For Staging
```cmd
# Create .env.staging first
cp .env.production.template .env.staging
# Edit .env.staging with staging values

# Load staging environment
$env:ENVIRONMENT="staging"  # PowerShell
# OR
set ENVIRONMENT=staging     # CMD

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### For Production
```cmd
# Create .env.production from template
cp .env.production.template .env.production
# Edit .env.production with production values

# Use production environment file
# (Typically handled by deployment platform like Docker, systemd, etc.)
```

---

## 🔐 Security Differences by Environment

### Development Environment

| Feature | Behavior |
|---------|----------|
| Rate Limiting | 1000 requests/minute per IP |
| DDoS Protection | Threshold: 100 req/sec |
| Security Headers | CSP allows unsafe-inline |
| Trusted Hosts | All hosts (*) allowed |
| API Documentation | Visible at /api/v1/docs |
| Error Messages | Detailed stack traces |
| CORS | Multiple origins allowed |
| Session Cookies | Secure=False (HTTP works) |

### Staging Environment

| Feature | Behavior |
|---------|----------|
| Rate Limiting | 100 requests/minute per IP |
| DDoS Protection | Threshold: 50 req/sec |
| Security Headers | Strict CSP |
| Trusted Hosts | staging.cooin.com only |
| API Documentation | Hidden |
| Error Messages | Generic messages |
| CORS | staging.cooin.com only |
| Session Cookies | Secure=True (HTTPS required) |

### Production Environment

| Feature | Behavior |
|---------|----------|
| Rate Limiting | 100 requests/minute per IP |
| DDoS Protection | Threshold: 20 req/sec |
| Security Headers | Strictest CSP |
| Trusted Hosts | app.cooin.com, www.cooin.com |
| API Documentation | Hidden |
| Error Messages | Generic messages |
| CORS | app.cooin.com only |
| Session Cookies | Secure=True (HTTPS required) |

---

## 🧪 Testing Security in Development

Even though security is relaxed in development, you can still test it:

### Test 1: Security Headers
```bash
curl -I http://localhost:8000/health

# Should see headers:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

### Test 2: Rate Limiting
```bash
# Development allows high rate, but still tracks
for i in {1..10}; do curl http://localhost:8000/health; done

# Won't hit limit in dev, but logs activity
```

### Test 3: CORS
```bash
# From allowed origin (should work)
curl -H "Origin: http://localhost:8083" http://localhost:8000/api/v1/users

# From disallowed origin (should work in dev, fail in prod)
curl -H "Origin: https://evil.com" http://localhost:8000/api/v1/users
```

---

## 🔄 Deployment Checklist

### Before Deploying to Production

- [ ] Copy `.env.production.template` to `.env.production`
- [ ] Generate new `SECRET_KEY`
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Update `DATABASE_URL` to production database
- [ ] Set strong `DATABASE_PASSWORD`
- [ ] Update `BACKEND_CORS_ORIGINS` to production domain only
- [ ] Configure `REDIS_URL` with password
- [ ] Set production `SMTP_*` credentials
- [ ] Verify `SESSION_COOKIE_SECURE=True`
- [ ] Obtain SSL certificate
- [ ] Configure reverse proxy (nginx/Caddy)
- [ ] Test all endpoints
- [ ] Run security scan

---

## 🛠️ Troubleshooting

### Issue: "Security middleware not loading"

**Check**:
```bash
# Verify environment variable is set
python -c "from app.core.config import settings; print(f'Environment: {settings.ENVIRONMENT}')"
```

**Solution**: Restart the backend after changing `.env`

---

### Issue: "Rate limiting too strict in development"

**Solution**: Temporarily disable in `.env`:
```env
ENABLE_RATE_LIMITING=False
```

---

### Issue: "CORS blocking requests in development"

**Solution**: Add your frontend URL to `BACKEND_CORS_ORIGINS` in `.env`:
```env
BACKEND_CORS_ORIGINS=["http://localhost:8083","http://localhost:3000","YOUR_URL_HERE"]
```

---

### Issue: "Can't access API docs"

**Check**: Ensure `DEBUG=True` in development:
```env
DEBUG=True
ENVIRONMENT=development
```

API docs should be at: http://localhost:8000/api/v1/docs

---

## 📊 Monitoring Security Status

### Check Current Environment
```bash
curl http://localhost:8000/health | jq

# Response includes environment info (in development only)
```

### View Security Logs
```bash
# Check backend logs for security events
tail -f cooin-backend/logs/security.log

# Look for:
# - Rate limit violations
# - Suspicious request patterns
# - Failed authentication attempts
```

---

## 🔒 Security Best Practices

### Development
- ✅ Keep security middleware enabled (relaxed settings)
- ✅ Test with realistic data
- ✅ Don't commit `.env` files
- ✅ Use `.env.example` for team sharing

### Staging
- ✅ Mirror production configuration
- ✅ Test deployment procedures
- ✅ Verify security headers
- ✅ Test rate limiting thresholds

### Production
- ✅ All security features enabled
- ✅ Monitor security logs daily
- ✅ Keep secrets in secure vault
- ✅ Regular security audits
- ✅ Automated backups
- ✅ Incident response plan ready

---

## 📚 Additional Resources

- [SECURITY-AUDIT.md](./SECURITY-AUDIT.md) - Complete security assessment
- [PRODUCTION-SECURITY-GUIDE.md](./PRODUCTION-SECURITY-GUIDE.md) - Deployment guide
- [.env.example](./cooin-backend/.env.example) - Environment template
- [.env.production.template](./cooin-backend/.env.production.template) - Production template

---

## ❓ FAQ

**Q: Will security slow down my development?**
A: No! Security middleware is configured to be relaxed in development mode with high limits and permissive settings.

**Q: Can I disable specific security features?**
A: Yes! Set any `ENABLE_*` flag to `False` in your `.env` file.

**Q: How do I test production-like security locally?**
A: Set `ENVIRONMENT=staging` in your `.env` file and restart the backend.

**Q: What happens if I forget to change to production mode?**
A: The application will run in development mode with relaxed security. Always verify `ENVIRONMENT=production` before deploying!

**Q: Can I switch environments without restarting?**
A: No, you must restart the backend for environment changes to take effect.

---

**Last Updated**: 2025-11-19 (Session 15)
**Maintained By**: Development Team
**Review Cycle**: Per deployment
