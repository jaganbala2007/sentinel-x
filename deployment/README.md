# Sentinel-X Deployment Guide

Full-stack deployment using Docker Compose or Kubernetes.

## Quick Start (Docker Compose)

```bash
git clone https://github.com/jaganbala2007/sentinel-x.git
cd sentinel-x

docker-compose -f deployment/docker-compose.yml up -d

# Services started:
# Frontend:  http://localhost:8000
# Backend:   http://localhost:8080
# API Docs:  http://localhost:8080/docs
```

## Services

| Service | Image | Port | Purpose |
|---|---|---|---|
| `backend` | Custom FastAPI | 8080 | REST + WebSocket API |
| `postgres` | postgres:16-alpine | 5432 | Persistent database |
| `redis` | redis:7-alpine | 6379 | Telemetry cache |
| `mqtt` | eclipse-mosquitto:2 | 1883 | IoT sensor broker |
| `nginx` | nginx:1.27-alpine | 8000 | Frontend + reverse proxy |

## Configuration

Copy and edit environment variables:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env — change all CHANGE_ME values
```

## Production Checklist

- [ ] Set strong `SECRET_KEY` (`openssl rand -hex 32`)
- [ ] Change PostgreSQL password from `sentinel` to a strong value
- [ ] Enable TLS/HTTPS on Nginx (add SSL certificate)
- [ ] Set `DEBUG=false` in backend `.env`
- [ ] Configure Mosquitto ACL lists for sensor authentication
- [ ] Restrict CORS `ALLOWED_ORIGINS` to your domain only
- [ ] Set up PostgreSQL backups (pg_dump cron)
- [ ] Configure Redis persistence (`appendonly yes`)
- [ ] Set up monitoring (Prometheus + Grafana)

## Useful Commands

```bash
# Check all service health
docker-compose -f deployment/docker-compose.yml ps

# View backend logs
docker-compose -f deployment/docker-compose.yml logs -f backend

# Restart a service
docker-compose -f deployment/docker-compose.yml restart backend

# Stop all services
docker-compose -f deployment/docker-compose.yml down

# Stop and remove volumes (⚠️ deletes data)
docker-compose -f deployment/docker-compose.yml down -v
```

## GitHub Pages (Frontend Only)

Deploy the frontend simulation to GitHub Pages:

1. Go to repository **Settings → Pages**
2. Set Source: **Deploy from branch**
3. Branch: `main`, Folder: `/frontend/src`
4. URL: `https://jaganbala2007.github.io/sentinel-x/`

Or use the automated workflow (`.github/workflows/pages.yml`).
