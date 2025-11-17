# Redis Setup Guide for Cooin App

This guide provides instructions for setting up Redis for production-grade caching with high scalability.

---

## 🎯 Why Redis?

Redis is essential for scaling Cooin to handle many users:

- **Performance**: Sub-millisecond response times
- **Scalability**: Handles millions of operations per second
- **Reliability**: Persistence options ensure data safety
- **Memory Efficiency**: LRU eviction manages memory automatically
- **Connection Pooling**: Efficient resource management for concurrent users

---

## 📦 Option 1: Docker Setup (Recommended for Production)

### Prerequisites
- Docker Desktop for Windows: https://www.docker.com/products/docker-desktop/

### Installation Steps

1. **Install Docker Desktop**
   ```cmd
   # Download and install from https://www.docker.com/products/docker-desktop/
   # After installation, restart your computer
   ```

2. **Verify Docker Installation**
   ```cmd
   docker --version
   docker-compose --version
   ```

3. **Start Redis**
   ```cmd
   cd C:\Windows\System32\cooin-app
   docker compose up -d redis
   ```

4. **Verify Redis is Running**
   ```cmd
   docker ps
   # Should show cooin-redis container running on port 6379
   ```

5. **Check Redis Health**
   ```cmd
   docker exec -it cooin-redis redis-cli ping
   # Should return: PONG
   ```

6. **View Redis Logs**
   ```cmd
   docker logs cooin-redis
   ```

### Docker Commands Reference

```cmd
# Start Redis
docker compose up -d redis

# Stop Redis
docker compose down redis

# Restart Redis
docker compose restart redis

# View logs
docker logs -f cooin-redis

# Access Redis CLI
docker exec -it cooin-redis redis-cli

# Stop and remove all data
docker compose down -v

# Start with Redis Commander (GUI)
docker compose --profile dev up -d
# Access at: http://localhost:8081
```

---

## 📦 Option 2: Windows Native Installation

### Using Memurai (Redis-compatible for Windows)

Memurai is a Redis-compatible server optimized for Windows:

1. **Download Memurai**
   ```
   https://www.memurai.com/get-memurai
   ```

2. **Install Memurai**
   - Run the installer
   - Choose "Install as Windows Service"
   - Use default port: 6379

3. **Verify Installation**
   ```cmd
   memurai-cli ping
   # Should return: PONG
   ```

4. **Configure Memurai**
   - Config file location: `C:\Program Files\Memurai\memurai.conf`
   - Use the same settings from `redis.conf`

### Using WSL2 + Redis

If you have Windows Subsystem for Linux installed:

```bash
# Update WSL
wsl --update

# Install Redis
wsl
sudo apt update
sudo apt install redis-server

# Start Redis
sudo service redis-server start

# Verify
redis-cli ping
# Should return: PONG
```

---

## 🔧 Configuration

### Redis Configuration File

The `redis.conf` file has been configured with production-ready settings:

```
├── Persistence: RDB + AOF for data durability
├── Memory Management: 256MB max with LRU eviction
├── Connection Limits: 10,000 max clients
├── Performance Tuning: Optimized for web applications
└── Monitoring: Slow log and latency tracking enabled
```

### Key Settings Explained

1. **Persistence**
   ```conf
   save 900 1      # Snapshot every 15 min if 1+ keys changed
   save 300 10     # Snapshot every 5 min if 10+ keys changed
   save 60 10000   # Snapshot every 1 min if 10,000+ keys changed
   appendonly yes  # Enable AOF for maximum durability
   ```

2. **Memory Management**
   ```conf
   maxmemory 256mb           # Limit memory usage
   maxmemory-policy allkeys-lru  # Evict least recently used keys
   ```

3. **Connection Pooling** (configured in `cache.py`)
   - Max 50 connections
   - Connection health checks every 30s
   - Automatic retry on timeout
   - TCP keepalive enabled

---

## 🧪 Testing Redis

### Test 1: Basic Connection

```cmd
cd C:\Windows\System32\cooin-app\cooin-backend
python -m pytest tests/test_redis_connection.py
```

### Test 2: Performance Test

```python
# Create file: test_redis_performance.py
import asyncio
from app.core.cache import init_cache

async def test_performance():
    cache = await init_cache()

    # Write test
    for i in range(1000):
        await cache.set(f"test_key_{i}", f"value_{i}", expire_seconds=60)

    # Read test
    for i in range(1000):
        value = await cache.get(f"test_key_{i}")
        assert value == f"value_{i}"

    stats = await cache.get_stats()
    print(f"Cache Stats: {stats}")

asyncio.run(test_performance())
```

### Test 3: Manual CLI Test

```cmd
# Connect to Redis
docker exec -it cooin-redis redis-cli
# OR: memurai-cli
# OR: redis-cli (if WSL)

# Test commands
SET test_key "Hello Cooin"
GET test_key
EXPIRE test_key 60
TTL test_key
INFO stats
```

---

## 📊 Monitoring

### Redis Commander (GUI Tool)

Included in docker-compose for development:

```cmd
# Start with Redis Commander
docker compose --profile dev up -d

# Access GUI
http://localhost:8081
```

Features:
- View all keys
- Monitor memory usage
- Execute commands
- Real-time statistics

### CLI Monitoring

```cmd
# Monitor commands in real-time
docker exec -it cooin-redis redis-cli MONITOR

# Get server info
docker exec -it cooin-redis redis-cli INFO

# Check memory usage
docker exec -it cooin-redis redis-cli INFO memory

# View slow queries
docker exec -it cooin-redis redis-cli SLOWLOG GET 10
```

---

## 🚀 Production Deployment

### For Cloud Deployment (AWS, Azure, GCP)

1. **AWS ElastiCache for Redis**
   ```
   - Managed Redis service
   - Automatic backups
   - Multi-AZ replication
   - Auto-scaling
   ```

2. **Azure Cache for Redis**
   ```
   - Fully managed Redis
   - 99.9% SLA
   - Built-in monitoring
   - Geo-replication
   ```

3. **Google Cloud Memorystore**
   ```
   - Managed Redis
   - High availability
   - Automatic failover
   - VPC integration
   ```

### Configuration for Production

Update `.env` or environment variables:

```env
# For managed Redis services
REDIS_URL=redis://username:password@redis-host:6379/0

# With SSL/TLS
REDIS_URL=rediss://username:password@redis-host:6380/0

# For Redis Cluster
REDIS_CLUSTER_NODES=redis1:6379,redis2:6379,redis3:6379
```

---

## 🔐 Security Recommendations

### 1. Enable Authentication

Edit `redis.conf`:
```conf
requirepass your_very_secure_password_here_min_32_characters
```

Update `.env`:
```env
REDIS_URL=redis://:your_very_secure_password_here_min_32_characters@localhost:6379/0
```

### 2. Network Security

```conf
# Bind to specific interface (production)
bind 127.0.0.1

# Or for Docker networking
bind 0.0.0.0
protected-mode yes
```

### 3. Disable Dangerous Commands

```conf
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG ""
```

---

## 🐛 Troubleshooting

### Issue: Connection Refused

**Solution:**
```cmd
# Check if Redis is running
docker ps | grep redis
# OR: netstat -ano | findstr :6379

# Restart Redis
docker compose restart redis

# Check logs
docker logs cooin-redis
```

### Issue: Memory Errors

**Solution:**
```cmd
# Check memory usage
docker exec -it cooin-redis redis-cli INFO memory

# Clear cache if needed
docker exec -it cooin-redis redis-cli FLUSHDB

# Or adjust maxmemory in redis.conf
```

### Issue: Slow Performance

**Solution:**
```cmd
# Check slow queries
docker exec -it cooin-redis redis-cli SLOWLOG GET 10

# Monitor latency
docker exec -it cooin-redis redis-cli --latency

# Check if persistence is causing issues
# Disable AOF temporarily for testing
docker exec -it cooin-redis redis-cli CONFIG SET appendonly no
```

---

## 📈 Scaling for High Traffic

### Vertical Scaling (Single Instance)

Increase Docker resources in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 2G  # Increase from 512M
      cpus: '2.0'  # Increase from 0.5
```

Update Redis config:
```conf
maxmemory 1gb  # Increase from 256mb
```

### Horizontal Scaling (Redis Cluster)

For millions of users, consider Redis Cluster:

1. Multiple Redis nodes
2. Data sharding across nodes
3. Automatic failover
4. Load balancing

---

## 📝 Next Steps

1. **Choose your installation method** (Docker recommended)
2. **Start Redis** using the commands above
3. **Test the connection** with the backend
4. **Monitor performance** using Redis Commander
5. **Configure security** for production

---

## 🔗 Resources

- Redis Documentation: https://redis.io/documentation
- Docker Documentation: https://docs.docker.com/
- Redis Best Practices: https://redis.io/topics/best-practices
- Memurai: https://www.memurai.com/
- Redis Commander: https://github.com/joeferner/redis-commander

---

**Last Updated**: 2025-11-17 (Session 14)
