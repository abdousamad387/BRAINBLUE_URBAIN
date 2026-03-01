#!/bin/bash
# BRAINBLUE URBAIN - Startup Script
# Initialise et lance l'application complète

set -e

echo "🌊 BRAINBLUE URBAIN - Startup Script"
echo "====================================="

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
LOG_DIR="$PROJECT_DIR/logs"

# Créer répertoire logs
mkdir -p "$LOG_DIR"

# Fonction logs
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Vérifier prérequis
log_info "Vérification des prérequis..."

if ! command -v python3 &> /dev/null; then
    log_error "Python 3 n'est pas installé"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    log_warn "PostgreSQL client pas trouvé (optionnel si DB distante)"
fi

log_info "✓ Python version: $(python3 --version)"

# 2. Charger variables d'environnement
if [ -f "$PROJECT_DIR/.env" ]; then
    log_info "Chargement fichier .env..."
    set -a
    source "$PROJECT_DIR/.env"
    set +a
else
    log_warn "Fichier .env non trouvé, utilisation variables système"
fi

# 3. Préparer Backend
log_info "Préparation Backend..."

cd "$BACKEND_DIR"

# Créer virtual env si inexistant
if [ ! -d "venv" ]; then
    log_info "Création virtual environment Python..."
    python3 -m venv venv
fi

# Activer virtual env
source venv/bin/activate

# Installer dépendances
if [ -f "requirements.txt" ]; then
    log_info "Installation dépendances Python..."
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
fi

# Initialiser base de données
if [ "$INIT_DB" = "true" ] || [ "$1" = "--init-db" ]; then
    log_info "Initialisation base de données..."
    
    # Test connexion DB
    if ! python3 -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; then
        log_error "Impossible de se connecter à la base de données"
        log_info "Vérifiez: DATABASE_URL=$DATABASE_URL"
        exit 1
    fi
    
    # Créer tables
    python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✓ Tables créées")
EOF
    
    # Seed données
    if [ "$SEED_DB" = "true" ]; then
        log_info "Insertion données de démo..."
        python3 << EOF
from app import app
from utils.helpers import DataGenerator
with app.app_context():
    DataGenerator.generate_test_data(app.db)
    print("✓ Données insérées")
EOF
    fi
fi

# 4. Lancer Backend
log_info "Lancement Backend sur port $PORT..."

if [ "$ENVIRONMENT" = "production" ]; then
    log_info "Mode PRODUCTION - Utilisation Gunicorn"
    gunicorn -c gunicorn_config.py app:app 2>&1 | tee "$LOG_DIR/backend.log" &
    BACKEND_PID=$!
else
    log_info "Mode DEVELOPMENT - Utilisation Flask dev server"
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    python3 app.py 2>&1 | tee "$LOG_DIR/backend.log" &
    BACKEND_PID=$!
fi

log_info "Backend lancé avec PID: $BACKEND_PID"

# 5. Lancer Frontend
log_info "Préparation Frontend..."

cd "$FRONTEND_DIR"

if [ "$ENVIRONMENT" = "production" ]; then
    log_info "Lancement serveur static avec Python"
    cd "$FRONTEND_DIR"
    python3 -m http.server 8000 2>&1 | tee "$LOG_DIR/frontend.log" &
    FRONTEND_PID=$!
else
    log_info "Frontend prêt à : http://localhost:8000/index.html"
    python3 -m http.server 8000 2>&1 | tee "$LOG_DIR/frontend.log" &
    FRONTEND_PID=$!
fi

log_info "Frontend lancé avec PID: $FRONTEND_PID"

# 6. Afficher information de démarrage
sleep 2

cat << EOF

${GREEN}╔════════════════════════════════════════╗${NC}
${GREEN}║  BRAINBLUE URBAIN - Démarrage réussi  ║${NC}
${GREEN}╚════════════════════════════════════════╝${NC}

🌊 Application Information:
   Environnement: $ENVIRONMENT
   Backend PID: $BACKEND_PID
   Frontend PID: $FRONTEND_PID

📱 Accès:
   Frontend: http://localhost:8000
   API: http://localhost:${PORT:-5000}/api
   Health: http://localhost:${PORT:-5000}/api/health

📊 Logs:
   Backend: $LOG_DIR/backend.log
   Frontend: $LOG_DIR/frontend.log

🔧 Commandes utiles:
   Arrêter: kill $BACKEND_PID $FRONTEND_PID
   Voir logs: tail -f $LOG_DIR/*.log
   Redémarrer: $0

📖 Documentation: https://docs.brainblue.io
💬 Support: support@brainblue.io

EOF

# 7. Cleanup on exit
trap cleanup EXIT

cleanup() {
    log_info "Arrêt de l'application..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    log_info "Application arrêtée"
}

# Keep script running
log_info "Application en exécution... (Ctrl+C pour arrêter)"
wait
