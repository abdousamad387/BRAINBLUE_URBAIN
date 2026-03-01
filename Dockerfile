# BRAINBLUE URBAIN - Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Variables d'environnement
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH

# Copier requirements
COPY requirements.txt .

# Installer dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier code
COPY . .

# Créer utilisateur non-root
RUN useradd -m -u 1000 brainblue && chown -R brainblue:brainblue /app
USER brainblue

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Lancer l'app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
