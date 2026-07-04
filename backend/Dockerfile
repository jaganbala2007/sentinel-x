# =============================================
# Sentinel-X Backend — Dockerfile
# =============================================
# Multi-stage build for a minimal production image.
# Stage 1: Build dependencies
# Stage 2: Runtime-only image

# --- Stage 1: Builder ---
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Runtime ---
FROM python:3.11-slim AS runtime

# Create non-root user for security
RUN useradd -m -r sentinelx
USER sentinelx

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/sentinelx/.local

# Copy application source
COPY --chown=sentinelx:sentinelx . .

# Expose application port
EXPOSE 8080

# Health check for Kubernetes / Docker Compose
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Production startup command
CMD ["/home/sentinelx/.local/bin/uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "8080", \
     "--workers", "4", "--log-level", "info"]
