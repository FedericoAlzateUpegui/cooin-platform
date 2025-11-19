# Cooin Web App - Production Security Deployment Guide

**Version**: 1.0
**Last Updated**: 2025-11-19 (Session 15)
**Status**: Ready for Implementation

---

## 🎯 Overview

This guide provides step-by-step instructions for securely deploying the Cooin application to production. Follow ALL steps in order before going live.

### Prerequisites
- ✅ Application tested in staging environment
- ✅ All features working correctly
- ✅ Database backup strategy in place
- ✅ SSL certificate obtained
- ✅ Domain name configured

---

## 📋 Pre-Deployment Checklist (Complete ALL Items)

### Phase 1: Environment Configuration (1-2 hours)

#### Step 1: Generate Production Secrets

```bash
# 1. Generate new SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy output and save it securely (password manager)

# 2. Generate strong database password
python -c "import secrets; print(secrets.token_urlsafe(24))"
# Copy output

# 3. Generate Redis password (if using remote Redis)
python -c "import secrets; print(secrets.token_urlsafe(24))"
# Copy output
```

**Save these securely!** You'll need them for the `.env` file.

---

#### Step 2: Create Production `.env` File

**Location**: `cooin-backend/.env` (on production server)

```env
# ============================================================================
# CRITICAL PRODUCTION SETTINGS
# ============================================================================

# ⚠️  MUST CHANGE - Use generated secret from Step 1
SECRET_KEY=<YOUR_GENERATED_SECRET_KEY_HERE>

# ⚠️  MUST SET TO FALSE
DEBUG=False

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# PostgreSQL (recommended for production)
DATABASE_URL=postgresql://cooin_user:<STRONG_PASSWORD>@db-host:5432/cooin_prod
DATABASE_HOSTNAME=db-host.your-provider.com
DATABASE_PORT=5432
DATABASE_NAME=cooin_prod
DATABASE_USERNAME=cooin_user
DATABASE_PASSWORD=<STRONG_DB_PASSWORD>

# ============================================================================
# SECURITY
# ============================================================================

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUNDS=12

# ============================================================================
# CORS - PRODUCTION DOMAINS ONLY
# ============================================================================

# ⚠️  CRITICAL: Only include your actual production domain(s)
BACKEND_CORS_ORIGINS=["https://app.cooin.com","https://www.cooin.com"]

# ============================================================================
# REDIS CONFIGURATION
# ============================================================================

# With password (recommended)
REDIS_URL=redis://:< REDIS_PASSWORD>@redis-host:6379/0

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.your-provider.com
SMTP_USER=noreply@cooin.com
SMTP_PASSWORD=<SMTP_APP_PASSWORD>
FRONTEND_URL=https://app.cooin.com

# ============================================================================
# SESSION & COOKIE SECURITY
# ============================================================================

# ⚠️  MUST be True (requires HTTPS)
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=lax

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL=WARNING  # Production: WARNING or ERROR
LOG_FORMAT=json

# ============================================================================
# RATE LIMITING
# ============================================================================

RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# ============================================================================
# FILE UPLOADS
# ============================================================================

MAX_UPLOAD_SIZE=5242880
UPLOAD_FOLDER=/var/www/cooin/uploads/
```

---

#### Step 3: Verify `.env` Security

```bash
# On production server

# 1. Check file permissions (should be readable only by app user)
chmod 600 .env
chown cooin-user:cooin-group .env

# 2. Verify .env is NOT in git
git status
# Should NOT show .env file

# 3. Verify .gitignore includes .env
cat .gitignore | grep ".env"
# Should show: .env
```

---

### Phase 2: Enable Security Middleware (30 minutes)

#### Step 4: Enable All Security Middleware

**File**: `cooin-backend/app/main.py`

**Find** (lines 65-74):
```python
# TEMPORARILY DISABLED FOR TESTING - Security middleware stack
# app.add_middleware(SecurityHeadersMiddleware)
# app.add_middleware(RequestLoggingMiddleware)
# app.add_middleware(APISecurityMiddleware)
# app.add_middleware(RequestValidationMiddleware)
# app.add_middleware(DDoSProtectionMiddleware)
# app.add_middleware(RateLimitMiddleware)
```

**Replace with**:
```python
# Production Security Middleware Stack - ENABLED
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(APISecurityMiddleware)
app.add_middleware(RequestValidationMiddleware)
app.add_middleware(DDoSProtectionMiddleware)
app.add_middleware(RateLimitMiddleware)

# Trusted Host Middleware - Production domains only
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["app.cooin.com", "www.cooin.com", "api.cooin.com"]
)
```

---

#### Step 5: Test Middleware in Staging

```bash
# Start backend with production settings in staging
DEBUG=False python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test each endpoint:
curl -I https://staging.cooin.com/health

# Verify security headers are present:
# - X-Frame-Options: DENY
# - X-Content-Type-Options: nosniff
# - Strict-Transport-Security: max-age=31536000
```

---

### Phase 3: Database Security (1 hour)

#### Step 6: Secure PostgreSQL Database

```sql
-- 1. Create dedicated database user
CREATE USER cooin_user WITH PASSWORD '<STRONG_PASSWORD>';

-- 2. Create production database
CREATE DATABASE cooin_prod OWNER cooin_user;

-- 3. Grant only necessary permissions
GRANT CONNECT ON DATABASE cooin_prod TO cooin_user;
GRANT USAGE ON SCHEMA public TO cooin_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO cooin_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO cooin_user;

-- 4. Enable SSL connections (in postgresql.conf)
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'

-- 5. Restrict connections by IP (in pg_hba.conf)
hostssl cooin_prod cooin_user 10.0.1.0/24 md5
```

#### Step 7: Configure Database Backups

```bash
# Automated daily backup script
#!/bin/bash
# /usr/local/bin/backup-cooin-db.sh

BACKUP_DIR="/var/backups/cooin"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="cooin_prod"
DB_USER="cooin_user"

# Create backup
pg_dump -U $DB_USER -F c -b -v -f "$BACKUP_DIR/cooin_$DATE.backup" $DB_NAME

# Keep only last 7 days
find $BACKUP_DIR -name "cooin_*.backup" -mtime +7 -delete

# Optional: Upload to S3/Cloud Storage
# aws s3 cp "$BACKUP_DIR/cooin_$DATE.backup" s3://cooin-backups/
```

```bash
# Add to crontab (run daily at 2 AM)
crontab -e
0 2 * * * /usr/local/bin/backup-cooin-db.sh
```

---

### Phase 4: Redis Security (30 minutes)

#### Step 8: Secure Redis

**File**: `/etc/redis/redis.conf` (or `redis.conf` in Docker)

```conf
# 1. Bind to internal network only
bind 127.0.0.1 ::1
# OR for Docker internal network:
bind 0.0.0.0
protected-mode yes

# 2. Set strong password
requirepass <YOUR_REDIS_PASSWORD>

# 3. Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
rename-command CONFIG ""

# 4. Enable persistence
appendonly yes
appendfilename "appendonly.aof"

# 5. Set memory limit
maxmemory 256mb
maxmemory-policy allkeys-lru
```

**Update Docker Compose** (`docker-compose.yml`):
```yaml
services:
  redis:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf --requirepass ${REDIS_PASSWORD}
    volumes:
      - ./redis.conf:/usr/local/etc/redis/redis.conf:ro
      - redis-data:/data
    networks:
      - cooin-internal  # Internal network only
```

---

### Phase 5: HTTPS & SSL Configuration (1-2 hours)

#### Step 9: Obtain SSL Certificate

**Option A: Let's Encrypt (Free, Automated)**
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot certonly --nginx -d app.cooin.com -d www.cooin.com
```

**Option B: Cloudflare (Free, Managed)**
- Use Cloudflare's SSL/TLS encryption (Full Strict mode)
- Automatic certificate management
- Built-in DDoS protection

**Option C: Commercial CA**
- Purchase from DigiCert, Comodo, etc.
- Follow CA's verification process

---

#### Step 10: Configure Nginx Reverse Proxy

**File**: `/etc/nginx/sites-available/cooin`

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name app.cooin.com www.cooin.com;

    return 301 https://$server_name$request_uri;
}

# Backend API
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.cooin.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.cooin.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.cooin.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Proxy to FastAPI backend
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # File upload size limit
    client_max_body_size 10M;
}

# Frontend Application
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name app.cooin.com www.cooin.com;

    # SSL Configuration (same as above)
    ssl_certificate /etc/letsencrypt/live/app.cooin.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.cooin.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Frontend static files
    root /var/www/cooin/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers (same as backend)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

**Enable and test**:
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/cooin /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Test SSL
curl -I https://api.cooin.com/health
```

---

### Phase 6: Monitoring & Logging (1 hour)

#### Step 11: Set Up Logging

**Option A: Local File Logging**
```python
# Update app/main.py logging configuration
logging.basicConfig(
    level=logging.WARNING,  # Production: WARNING or ERROR only
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/var/log/cooin/app.log"),
        logging.StreamHandler()  # Also log to console
    ]
)
```

**Option B: Centralized Logging (Recommended)**
- CloudWatch (AWS)
- Datadog
- Loggly
- Papertrail

#### Step 12: Set Up Monitoring

**Health Check Monitoring**:
```bash
# Simple uptime monitoring with cron
#!/bin/bash
# /usr/local/bin/health-check.sh

HEALTH_URL="https://api.cooin.com/health"
ALERT_EMAIL="ops@cooin.com"

if ! curl -sf $HEALTH_URL > /dev/null; then
    echo "API health check failed!" | mail -s "ALERT: Cooin API Down" $ALERT_EMAIL
fi
```

**Recommended Monitoring Services**:
- UptimeRobot (free, basic)
- Pingdom
- Datadog
- New Relic

---

## 🧪 Post-Deployment Testing

### Step 13: Security Testing Checklist

```bash
# 1. Test HTTPS enforcement
curl -I http://api.cooin.com/health
# Should redirect to https://

# 2. Test security headers
curl -I https://api.cooin.com/health
# Verify: X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security

# 3. Test rate limiting
for i in {1..150}; do curl https://api.cooin.com/health; done
# Should start returning 429 Too Many Requests

# 4. Test CORS
curl -H "Origin: https://evil.com" -I https://api.cooin.com/api/v1/users
# Should NOT allow cross-origin request

# 5. Test authentication
curl https://api.cooin.com/api/v1/users/me
# Should return 401 Unauthorized without token

# 6. Verify API docs are disabled
curl https://api.cooin.com/api/v1/docs
# Should return 404 (docs disabled in production)
```

### Step 14: SSL/TLS Testing

Visit: https://www.ssllabs.com/ssltest/
- Enter: `api.cooin.com`
- Target grade: **A or A+**

---

## 🔐 Security Maintenance

### Daily
- [ ] Monitor error logs for anomalies
- [ ] Check failed login attempts
- [ ] Review rate limit violations

### Weekly
- [ ] Review access logs
- [ ] Check database backup status
- [ ] Monitor disk space/resources

### Monthly
- [ ] Update dependencies (`pip list --outdated`)
- [ ] Review security advisories
- [ ] Rotate non-critical API keys
- [ ] Test backup restoration

### Quarterly
- [ ] Rotate SECRET_KEY (coordinate with active users)
- [ ] Update SSL certificates (if manual)
- [ ] Security penetration testing
- [ ] Review and update firewall rules

---

## 🚨 Incident Response Plan

### If Security Breach Detected:

1. **Immediate Actions** (0-1 hour)
   - [ ] Take affected systems offline
   - [ ] Notify security team
   - [ ] Preserve logs and evidence

2. **Investigation** (1-4 hours)
   - [ ] Identify breach vector
   - [ ] Assess data exposure
   - [ ] Document timeline

3. **Remediation** (4-24 hours)
   - [ ] Patch vulnerability
   - [ ] Rotate all secrets
   - [ ] Force password reset for affected users
   - [ ] Restore from clean backup if needed

4. **Communication** (24-48 hours)
   - [ ] Notify affected users
   - [ ] Comply with breach notification laws
   - [ ] Update security documentation

5. **Post-Incident** (1-2 weeks)
   - [ ] Conduct post-mortem
   - [ ] Implement preventive measures
   - [ ] Update incident response plan

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [PostgreSQL Security Checklist](https://www.postgresql.org/docs/current/security-checklist.html)

---

## ✅ Final Pre-Launch Checklist

- [ ] All secrets generated and stored securely
- [ ] DEBUG=False in production .env
- [ ] All security middleware enabled
- [ ] HTTPS configured and tested
- [ ] SSL certificate valid and trusted
- [ ] CORS limited to production domains only
- [ ] Database user has minimal permissions
- [ ] Database backups automated and tested
- [ ] Redis password set and commands disabled
- [ ] Rate limiting active and tested
- [ ] Security headers present on all responses
- [ ] API docs disabled (DEBUG=False)
- [ ] Monitoring and alerting configured
- [ ] Log rotation configured
- [ ] Incident response plan documented
- [ ] Team trained on security procedures

---

**Document Version**: 1.0
**Last Updated**: 2025-11-19
**Next Review**: Before production deployment
