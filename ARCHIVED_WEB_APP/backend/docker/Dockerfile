# Multi-stage Docker build for Cooin Backend API
# Production-ready configuration with security best practices

# Stage 1: Base Python image with system dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash cooin

# Stage 2: Dependencies installation
FROM base as dependencies

# Set work directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application build
FROM dependencies as builder

# Copy application code
COPY . .

# Remove development/test files
RUN rm -rf tests/ \
    test_*.py \
    *.md \
    .git/ \
    .gitignore \
    __pycache__/

# Stage 4: Production image
FROM base as production

# Install only runtime dependencies
WORKDIR /app

# Copy Python packages from builder
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application from builder
COPY --from=builder --chown=cooin:cooin /app .

# Create necessary directories
RUN mkdir -p /app/uploads /app/logs && \
    chown -R cooin:cooin /app

# Switch to non-root user
USER cooin

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Expose port
EXPOSE 8000

# Production command with Gunicorn
CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]