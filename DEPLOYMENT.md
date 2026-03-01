# 🚀 BRAINBLUE URBAIN - Deployment Guide

## Déploiement en Production

Guide complet pour déployer BRAINBLUE URBAIN en environnement de production.

---

## 1. Déploiement avec Docker Compose (Recommandé)

### Prérequis
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum
- 20GB stockage
- Domaine avec certificat SSL

### Étapes

#### 1.1 Configuration
```bash
# Cloner le repository
git clone https://github.com/brainblue/urbain.git
cd BRAINBLUE_URBAIN

# Créer fichier .env production
cat > .env.production << 'EOF'
ENVIRONMENT=production
FLASK_ENV=production
DEBUG=False
TESTING=False

# Database (utiliser service managé en prod)
DATABASE_URL=postgresql://brainblue_user:very_strong_password_here@postgres:5432/brainblue_urbain

# Redis
REDIS_URL=redis://redis:6379/0

# Sécurité (générer des clés cryptographiques fortes)
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# CORS (domaine réel)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Sentry (monitoring)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project

# Email
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your-sendgrid-key

# Logging
LOG_LEVEL=WARNING
EOF

# Copier fichier de production
cp .env.production .env
```

#### 1.2 Préparation SSL
```bash
# Générer certificats SSL (Let's Encrypt recommandé)
mkdir -p ssl

# Avec Certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copier certificats
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem
sudo chown $USER:$USER ./ssl/*
```

#### 1.3 Lancer les services
```bash
# Build images
docker-compose build

# Lancer en détaché
docker-compose up -d

# Vérifier santé
docker-compose ps
docker-compose logs -f

# Initialiser la base de données
docker-compose exec backend python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Base de données initialisée !')
"
```

#### 1.4 Vérifier le déploiement
```bash
# Health check
curl -k https://yourdomain.com/api/health

# Logs
docker-compose logs -f backend

# Accéder à Nginx stats
# http://yourdomain.com:8080/nginx_status
```

---

## 2. Déploiement AWS

### Architecture AWS
```
┌─────────────┐
│   CloudFront │ (CDN, SSL)
└──────┬──────┘
       │
┌──────▼──────────────────┐
│  Application Load       │
│  Balancer (ALB)         │
└──────┬──────────────────┘
       │
   ┌───┼───┐
   │       │
┌──▼──┐ ┌─▼───┐
│ ECS │ │ ECS │ (Auto-scaling)
│ Fargate
└──────┘ └─────┘
   │       │
   └───┬───┘
       │
    ┌──▼─────────────┐
    │  RDS PostgreSQL │ (Managed)
    │  + PostGIS      │
    └─────────────────┘
       │
    ┌──▼─────────────┐
    │ ElastiCache    │ (Redis)
    │ Redis          │
    └────────────────┘
```

### Déploiement ECS

```bash
# 1. Créer cluster ECS
aws ecs create-cluster --cluster-name brainblue-prod

# 2. Créer registre ECR
aws ecr create-repository --repository-name brainblue/backend
aws ecr create-repository --repository-name brainblue/frontend

# 3. Build et push images
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker build -t brainblue/backend ./backend
docker tag brainblue/backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/brainblue/backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/brainblue/backend:latest

# 4. Créer RDS instance
aws rds create-db-instance \
  --db-instance-identifier brainblue-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 15.3 \
  --master-username brainblue_admin \
  --master-user-password 'StrongPassword123!' \
  --allocated-storage 100 \
  --storage-type gp3 \
  --backup-retention-period 30

# 5. Créer ElastiCache Redis
aws elasticache create-cache-cluster \
  --cache-cluster-id brainblue-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1

# 6. Créer task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 7. Créer service ECS
aws ecs create-service \
  --cluster brainblue-prod \
  --service-name brainblue-backend \
  --task-definition brainblue-backend:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=backend,containerPort=5000
```

---

## 3. Déploiement Google Cloud

### Cloud Run + Cloud SQL

```bash
# 1. Authentifier
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Créer Cloud SQL instance
gcloud sql instances create brainblue-db \
  --database-version=POSTGRES_15 \
  --tier=db-custom-2-8192 \
  --region=us-central1

# 3. Créer database
gcloud sql databases create brainblue_urbain --instance=brainblue-db

# 4. Build et push image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/brainblue-backend ./backend

# 5. Deploy sur Cloud Run
gcloud run deploy brainblue-backend \
  --image gcr.io/YOUR_PROJECT_ID/brainblue-backend \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 120 \
  --set-env-vars DATABASE_URL=postgresql://...,REDIS_URL=...

# 6. Configurer Cloud Storage (pour uploads)
gsutil mb gs://brainblue-uploads
gsutil iam ch serviceAccount:YOUR_SA@appspot.gserviceaccount.com:objectEditor gs://brainblue-uploads

# 7. Configurer Cloud CDN
gcloud compute backend-services create brainblue-backend \
  --protocol HTTP \
  --enable-cdn \
  --global
```

---

## 4. Déploiement Kubernetes

### K8s Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: brainblue-backend
  namespace: prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: brainblue-backend
  template:
    metadata:
      labels:
        app: brainblue-backend
    spec:
      containers:
      - name: backend
        image: gcr.io/project/brainblue-backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: connection-string
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 20
          periodSeconds: 5

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: brainblue-backend
  namespace: prod
spec:
  selector:
    app: brainblue-backend
  ports:
  - port: 80
    targetPort: 5000
    protocol: TCP
  type: LoadBalancer

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: brainblue-ingress
  namespace: prod
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - yourdomain.com
    secretName: brainblue-tls
  rules:
  - host: yourdomain.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: brainblue-backend
            port:
              number: 80
```

### Déployer sur K8s
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml

# Vérifier déploiement
kubectl get pods -n prod
kubectl logs -f deployment/brainblue-backend -n prod
```

---

## 5. Monitoring & Maintenance

### Monitoring avec Prometheus + Grafana

```bash
# 1. Installer Prometheus
docker-compose -f monitoring-compose.yml up -d

# 2. Configurer scrape
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'brainblue-api'
    static_configs:
      - targets: ['localhost:5000']

  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']

# 3. Accéder à Grafana
# http://localhost:3000 (admin/admin)
```

### Alertes
```yaml
# alerts.yml
groups:
- name: brainblue
  rules:
  - alert: HighErrorRate
    expr: rate(http_errors_total[5m]) > 0.05
    for: 5m
    annotations:
      summary: "High error rate detected"

  - alert: DBConnectionFailure
    expr: pg_up == 0
    for: 1m
    annotations:
      summary: "Database is down"

  - alert: HighMemoryUsage
    expr: container_memory_usage_bytes / 1073741824 > 3.5
    for: 5m
    annotations:
      summary: "High memory usage"
```

---

## 6. Backup & Disaster Recovery

### Backup Automatique
```bash
# Database backup
BACKUP_DIR="/backups/postgres"
mkdir -p $BACKUP_DIR

# Backup daily
pg_dump -h localhost -U brainblue_user brainblue_urbain | \
  gzip > $BACKUP_DIR/db_$(date +%Y%m%d_%H%M%S).sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/ s3://brainblue-backups/ --recursive

# Retention: 30 jours
find $BACKUP_DIR -mtime +30 -delete
```

### Restore depuis Backup
```bash
# Télécharger backup
aws s3 cp s3://brainblue-backups/db_20241201.sql.gz .

# Restore
gunzip -c db_20241201.sql.gz | \
  psql -h localhost -U brainblue_user brainblue_urbain
```

---

## 7. Performance Tuning

### Database Optimization
```sql
-- Vacuum & Analyze
VACUUM ANALYZE;

-- Index tuning
EXPLAIN ANALYZE SELECT * FROM water_networks WHERE city = 'dakar';

-- Connection pooling
-- Utiliser PgBouncer pour pooling connections
pgbouncer -d -c /etc/pgbouncer/pgbouncer.ini
```

### Cache Optimization
```python
# Redis expiration
from redis import Redis
r = Redis.from_url(REDIS_URL)

# Cache API responses (1 hour)
@app.route('/api/statistics/<city>')
@cache.cached(timeout=3600)
def get_statistics(city):
    return generate_stats(city)

# Clear cache on update
@app.route('/api/water/networks/<id>', methods=['PUT'])
def update_network(id):
    # Update logic
    cache.delete_pattern('api_statistics_*')
    return OK
```

---

## 8. Scaling

### Horizontal Scaling
```bash
# Pod auto-scaling avec K8s
kubectl autoscale deployment brainblue-backend --min=2 --max=10 --cpu-percent=80

# Ou avec Docker Swarm
docker service create --name brainblue \
  --replicas 3 \
  --mount type=volume,source=postgres_data,target=/var/lib/postgresql/data \
  brainblue/app:latest
```

### Vertical Scaling
- Augmenter CPU/RAM des pods
- Optimiser la taille des conteneurs
- Utiliser des ressources managées (RDS instead of self-managed)

---

## 9. Checklist Production

- [ ] Certificat SSL/TLS configuré
- [ ] Variables d'environnement sécurisées
- [ ] Database backup automatique
- [ ] Monitoring et logging en place
- [ ] Rate limiting activé
- [ ] CORS configuré correctement
- [ ] Health checks en place
- [ ] Auto-scaling configuré
- [ ] Disaster recovery plan écrit
- [ ] Documentation maintenance écrite
- [ ] Tests de charge réalisés
- [ ] Security audit complété
- [ ] GDPR/Privacy compliance validé
- [ ] Performance metrics baseline établi

---

## 10. Troubleshooting

### "502 Bad Gateway"
```bash
# Vérifier backend
docker-compose logs backend

# Vérifier connexion DB
psql -h localhost -U brainblue_user -c "SELECT 1"

# Redémarrer services
docker-compose restart backend
```

### "High Latency"
```bash
# Profiler code
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_PROFILER_ENABLED'] = True

# Check slow queries
EXPLAIN ANALYZE SELECT ...;

# Monitor CPU/Memory
docker stats
```

### "Out of Disk"
```bash
# Purger logs
docker system prune -a

# Nettoyer volumes
docker volume prune

# Archive old data
pg_dump ... | gzip > backup.sql.gz
```

---

**Production Ready! 🎉** - BRAINBLUE URBAIN est prêt pour la mise en production.

Pour plus d'aide: support@brainblue.io
