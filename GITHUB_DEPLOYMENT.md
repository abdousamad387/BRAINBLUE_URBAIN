# 📦 BRAINBLUE URBAIN - GitHub Deployment & Setup Guide

## Overview

This guide covers deploying the complete BRAINBLUE URBAIN application to GitHub and various production environments.

## Prerequisites

- Git installed and configured
- GitHub account and repository created (named "BRAINBLUE")
- SSH key added to GitHub (optional but recommended)
- Docker installed (for Docker deployments)
- Heroku/AWS/DigitalOcean account (for respective deployments)

## 1. GitHub Repository Setup

### 1.1 Initialize Git Repository

```bash
cd BRAINBLUE
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 1.2 Add Remote Repository

```bash
# Using HTTPS (requires authentication)
git remote add origin https://github.com/yourusername/BRAINBLUE.git

# OR using SSH (if you've configured SSH keys)
git remote add origin git@github.com:yourusername/BRAINBLUE.git

# Verify remote
git remote -v
```

### 1.3 Create Initial Commit

```bash
# Stage all files
git add .

# Commit with meaningful message
git commit -m "feat: Initial commit - BRAINBLUE URBAIN Complete Application

- Full-stack GIS platform for urban water management
- Frontend: HTML5/CSS3/JavaScript with responsive design
- Backend: Flask with 35+ API endpoints
- Database: PostgreSQL with PostGIS for geospatial data
- ML Models: 4 trained prediction models (87-89% accuracy)
- Admin Panel: Complete user management and monitoring
- Docker: Production-ready containerization
- CI/CD: GitHub Actions pipeline configured"
```

### 1.4 Push to GitHub

```bash
# Create main branch
git branch -M main

# Push to GitHub
git push -u origin main

# Verify
git branch -v
git log --oneline -5
```

### 1.5 Configure GitHub Settings

Go to https://github.com/yourusername/BRAINBLUE/settings

#### Branch Protection

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch:
   - ✅ Require status checks to pass
   - ✅ Require code reviews before merging
   - ✅ Dismiss stale reviews
   - ✅ Require branches to be up to date

#### Secrets Configuration

Go to **Settings** → **Secrets and variables** → **Actions**

Add these secrets for CI/CD:

```
DATABASE_URL              # Your production database URL
REDIS_URL                 # Your production Redis URL
SECRET_KEY                # Flask secret key (generate: openssl rand -base64 32)
JWT_SECRET_KEY            # JWT secret (generate: openssl rand -base64 32)
DOCKER_REGISTRY_URL       # Your Docker registry (e.g., ghcr.io)
DOCKER_USERNAME           # Docker registry username
DOCKER_PASSWORD           # Docker registry password (use token)
SLACK_WEBHOOK             # Optional: For notifications
```

#### Pages Configuration (Optional)

For automated documentation:

1. Go to **Settings** → **Pages**
2. Set source to `gh-pages` branch
3. Choose theme (if desired)

## 2. Docker Deployment

### 2.1 Build Docker Images

```bash
# Build images locally first
docker-compose build

# Or build production images
docker build -t brainblue:latest .
```

### 2.2 Run Locally with Docker

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Verify application
curl http://localhost:5000/api/health
```

### 2.3 Push to Docker Registry

```bash
# Login to Docker Hub or your registry
docker login

# Tag images
docker tag brainblue:latest yourusername/brainblue:latest
docker tag brainblue:latest yourusername/brainblue:v1.0.0

# Push to registry
docker push yourusername/brainblue:latest
docker push yourusername/brainblue:v1.0.0
```

## 3. Production Deployment Options

### 3.1 Heroku Deployment

#### Setup

```bash
# Install Heroku CLI
# macOS: brew tap heroku/brew && brew install heroku
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create brainblue-urbain --region eu

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0

# Add Redis addon
heroku addons:create heroku-redis:premium-0
```

#### Configure Environment

```bash
# Set environment variables
heroku config:set \
  FLASK_ENV=production \
  SECRET_KEY=$(openssl rand -base64 32) \
  JWT_SECRET_KEY=$(openssl rand -base64 32) \
  DATABASE_POOL_SIZE=15 \
  MAX_CONNECTIONS=50
```

#### Deploy

```bash
# Push code to Heroku
git push heroku main

# Run migrations
heroku run python backend/migrate.py upgrade

# Seed database
heroku run python backend/seeds.py

# View logs
heroku logs --tail
```

**App URL**: https://brainblue-urbain.herokuapp.com

### 3.2 AWS Deployment

#### EC2 Deployment

```bash
# 1. Launch EC2 instance
# AMI: Ubuntu 22.04 LTS
# Instance Type: t3.medium (min)
# Storage: 30GB (min)

# 2. Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Install dependencies
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv postgresql-client redis-tools docker.io docker-compose

# 4. Clone repository
git clone https://github.com/yourusername/BRAINBLUE.git
cd BRAINBLUE

# 5. Configure environment
cp .env.example .env
nano .env  # Edit with production values

# 6. Start with Docker Compose
docker-compose up -d

# 7. Setup domain and SSL
# Use Route 53 for DNS
# Use AWS Certificate Manager for SSL
```

#### RDS & ElastiCache Setup

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier brainblue-prod \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password $(openssl rand -base64 32)

# Create ElastiCache Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id brainblue-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

### 3.3 DigitalOcean Deployment

#### App Platform

```bash
# 1. Create DigitalOcean account and get API token
doctl auth init

# 2. Create app specification file
cat > app.yaml << 'EOF'
name: brainblue-urbain
services:
  - name: api
    source:
      type: git
      repo: https://github.com/yourusername/BRAINBLUE.git
    build_command: pip install -r requirements.txt
    run_command: gunicorn -w 4 -b 0.0.0.0:8080 backend.app:app
    http_port: 8080
    envs:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        scope: RUN_AND_BUILD_TIME
        value: ${db.connection_string}
    health_check:
      http_path: /api/health

databases:
  - name: postgres
    engine: PG
    version: "15"
    production: true
  - name: redis
    engine: REDIS
    version: "7"
EOF

# 3. Create and deploy app
doctl apps create --spec app.yaml

# 4. View deployment status
doctl apps list
```

#### Droplet Deployment

```bash
# 1. Create Droplet
# Size: Basic $6/month (1GB RAM) - minimum
# OS: Ubuntu 22.04
# Add SSH key for easy access

# 2. SSH into droplet
ssh root@your-droplet-ip

# 3. Setup server
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone and deploy
git clone https://github.com/yourusername/BRAINBLUE.git
cd BRAINBLUE
cp .env.example .env
nano .env  # Configure for production

docker-compose up -d

# 5. Setup reverse proxy with nginx
# or use the included nginx configuration
```

## 4. GitHub Actions CI/CD

The `.github/workflows/ci-cd.yml` file is already configured for:

- ✅ Testing (pytest with coverage)
- ✅ Linting (flake8, pylint, black)
- ✅ Security scanning (bandit, safety)
- ✅ Docker image building
- ✅ Automatic deployment (on main push)

### Workflow Triggers

- **Push to main**: Run tests, build Docker image, deploy
- **Pull requests**: Run tests and linting
- **Schedule**: Daily security scans (optional)

## 5. Database Setup

### PostgreSQL with PostGIS

```sql
-- Create database
CREATE DATABASE brainblue_urbain;

-- Create user
CREATE USER brainblue_user WITH PASSWORD 'secure_password_change_me';

-- Grant privileges
ALTER ROLE brainblue_user WITH CREATEDB CREATEROLE;
GRANT ALL PRIVILEGES ON DATABASE brainblue_urbain TO brainblue_user;

-- Connect to database
\c brainblue_urbain

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Verify
SELECT PostGIS_version();
```

### Run Migrations

```bash
# Local
python backend/migrate.py upgrade

# Docker
docker-compose exec backend python backend/migrate.py upgrade

# Heroku
heroku run python backend/migrate.py upgrade

# Remote SSH
ssh user@server.com "cd BRAINBLUE && python backend/migrate.py upgrade"
```

## 6. SSL/HTTPS Setup

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Verify
sudo certbot certificates
```

### Update Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of configuration
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## 7. Monitoring & Logging

### Application Monitoring

```bash
# View logs
docker-compose logs -f backend

# Health check
curl http://localhost:5000/api/health

# Metrics (if enabled)
curl http://localhost:9090  # Prometheus
curl http://localhost:3000  # Grafana
```

### Error Tracking (Optional)

```python
# Install and configure Sentry
pip install sentry-sdk flask-sentry

# Add to Flask app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    environment="production"
)
```

## 8. Backup Strategy

### Database Backups

```bash
# Automatic backup (cron)
0 2 * * * pg_dump -h localhost -U brainblue_user brainblue_urbain > /backups/db_$(date +\%Y\%m\%d).sql

# Manual backup
pg_dump -h localhost -U brainblue_user brainblue_urbain > backup.sql

# Restore
psql -h localhost -U brainblue_user brainblue_urbain < backup.sql
```

### Docker Volume Backups

```bash
# Backup volumes
docker-compose exec postgres pg_dump -U brainblue_user brainblue_urbain > backup.sql

# Backup Redis
docker-compose exec redis redis-cli BGSAVE
docker cp brainblue-redis:/data/dump.rdb ./redis-backup.rdb
```

## 9. Performance Optimization

### Caching

```python
# Configure Redis caching
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = os.getenv('REDIS_URL')
CACHE_DEFAULT_TIMEOUT = 3600
```

### Database Optimization

```bash
# Analyze query performance
EXPLAIN ANALYZE SELECT * FROM water_networks WHERE city_id = 1;

# Create indexes
CREATE INDEX idx_networks_city ON water_networks(city_id);
CREATE INDEX idx_predictions_network ON predictions(network_id);
```

### Static Asset Optimization

- Files are served with long cache headers (1 year)
- Gzip compression enabled
- CDN can be added for global distribution

## 10. Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

**Redis Timeout**
```bash
# Check Redis is running
docker-compose exec redis redis-cli ping

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

**Docker Build Fails**
```bash
# Clean build (no cache)
docker-compose build --no-cache

# Check Docker resources
docker system df

# Prune unused images
docker system prune -a
```

**Permission Denied (Linux)**
```bash
# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or use sudo
sudo docker-compose up
```

## 11. Maintenance Tasks

### Regular Backups
- Daily: Database backups
- Weekly: Full system snapshots
- Monthly: Off-site archive

### Updates
```bash
# Update Python packages
pip install -r requirements.txt --upgrade

# Update Docker images
docker-compose pull
docker-compose up -d

# Update system
sudo apt-get update && sudo apt-get upgrade -y
```

### Security
- Monthly: Dependency vulnerability scan
- Monthly: Security updates review
- Quarterly: Code audit

## 12. Support & Resources

- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Heroku Devcenter](https://devcenter.heroku.com/)
- [AWS Documentation](https://docs.aws.amazon.com/)

---

**🚀 Your BRAINBLUE URBAIN application is now ready for production deployment!**

For additional help, check [CONTRIBUTING.md](CONTRIBUTING.md) or create an issue on GitHub.
