# 🚀 BRAINBLUE URBAIN - Quick Start Guide

Welcome! This guide will help you get BRAINBLUE URBAIN up and running in minutes.

## Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.9+, PostgreSQL 13+, Redis (local installation)
- Git
- At least 4GB RAM, 5GB disk space

## ⚡ Quick Start (Docker - Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/BRAINBLUE.git
cd BRAINBLUE
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed (defaults work for local development)
```

### 3. Start the Application

```bash
# Option A: Using Make (Recommended)
make setup

# Option B: Using Docker Compose directly
docker-compose up -d
docker-compose exec backend python migrate.py upgrade
docker-compose exec backend python seeds.py
```

### 4. Access the Application

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost (or http://localhost:8000) | N/A |
| **API Docs** | http://localhost:5000/api/docs | N/A |
| **Backend** | http://localhost:5000 | N/A |
| **PgAdmin** | http://localhost:5050 | admin@brainblue.local / admin_change_me |
| **Monitoring** | http://localhost:3000 | admin / admin_change_me (if prometheus enabled) |

### 5. Verify Everything Works

```bash
# Check all services are running
docker-compose ps

# Test the API
curl http://localhost:5000/api/health

# View logs
make logs
```

## 📖 Local Installation (Without Docker)

### 1. Prerequisites

```bash
# macOS / Linux
brew install postgresql redis python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11 postgresql postgresql-contrib redis-server

# Windows
# Download and install from:
# - Python: https://www.python.org/downloads/
# - PostgreSQL: https://www.postgresql.org/download/
# - Redis: https://github.com/microsoftarchive/redis/releases
```

### 2. Setup Python Environment

```bash
cd BRAINBLUE
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb brainblue_urbain
psql brainblue_urbain < backend/database/init.sql

# Create user (if not created by init.sql)
createuser -P brainblue_user
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your local PostgreSQL credentials
```

### 5. Run the Application

```bash
# Terminal 1: Start Flask backend
cd backend
python app.py

# Terminal 2: Start frontend (in project root)
cd frontend
python -m http.server 8000

# Terminal 3: Start Redis (if not running as service)
redis-server
```

Access at: http://localhost:8000

## 🔧 Common Commands

```bash
# Development
make up              # Start all services
make down            # Stop all services
make logs            # View logs
make shell           # Open backend shell
make test            # Run tests
make lint            # Check code quality

# Database
make db-migrate      # Run migrations
make db-seed         # Seed initial data
make db-reset        # Reset database (⚠️ deletes data)

# Production
make docker-build    # Build production images
make docker-push     # Push to registry
```

See `Makefile` for all available commands.

## 🐛 Troubleshooting

### "Port already in use"

```bash
# Find process using port 5000
lsof -i :5000

# Or use different port
docker-compose -f docker-compose.yml up -d -p 5001:5000
```

### "PostgreSQL connection refused"

```bash
# Restart PostgreSQL service
docker-compose restart postgres

# Check logs
docker-compose logs postgres

# Ensure .env DATABASE_URL is correct
cat .env | grep DATABASE_URL
```

### "Redis timeout"

```bash
# Restart Redis
docker-compose restart redis

# Check Redis is running
docker-compose exec redis redis-cli ping
```

### "Frontend not loading"

```bash
# Check if frontend service is running
docker-compose ps frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up frontend
```

### All services crash

```bash
# Clean up and restart fresh
make clean
make setup
```

## 📚 Next Steps

1. **Read Full Documentation:** [README_DEPLOYMENT.md](README_DEPLOYMENT.md)
2. **API Reference:** http://localhost:5000/api/docs
3. **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Configuration:** [.env.example](.env.example)

## 🤝 Getting Help

- 📖 Documentation: [README_DEPLOYMENT.md](README_DEPLOYMENT.md)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/yourusername/BRAINBLUE/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/BRAINBLUE/discussions)
- 📧 Contact: contact@brainblue.sn

## 🎓 Learning Resources

### For Beginners
- [Docker Introduction](https://docs.docker.com/get-started/)
- [Flask Tutorial](https://flask.palletsprojects.com/tutorial/)
- [PostgreSQL Getting Started](https://www.postgresql.org/docs/current/intro.html)

### For Experienced Developers
- [API Architecture](docs/architecture.md)
- [ML Models Overview](docs/models.md)
- [Deployment Guide](docs/deployment.md)

## ✅ Verification Checklist

After starting the application, verify:

- [ ] Frontend loads without errors
- [ ] Dashboard displays with data
- [ ] Map loads with markers
- [ ] API health check passes: `curl http://localhost:5000/api/health`
- [ ] Database is connected
- [ ] Redis is running
- [ ] All services show in `docker-compose ps`

## 🚀 Deploy to Production

See [README_DEPLOYMENT.md](README_DEPLOYMENT.md#production-deployment) for detailed production deployment steps.

```bash
# Quick production setup
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

**Ready to explore? Start with the frontend at http://localhost:3000 (Docker) or http://localhost:8000 (Local)! 🎉**
