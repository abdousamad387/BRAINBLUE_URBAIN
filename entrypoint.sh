#!/bin/bash
# BRAINBLUE URBAIN - Docker Entrypoint
# This script initializes and starts the Flask application

set -e

echo "=================================="
echo "BRAINBLUE URBAIN - Initialization"
echo "=================================="

# Wait for database
echo "🔄 Waiting for PostgreSQL..."
until PGPASSWORD=$DB_PASSWORD psql -h postgres -U $DB_USER -d $DB_NAME -c "SELECT 1" 2>/dev/null; do
  echo "⏳ PostgreSQL is unavailable - retrying..."
  sleep 2
done
echo "✅ PostgreSQL is up"

# Wait for Redis
echo "🔄 Waiting for Redis..."
until redis-cli -h redis -p 6379 ping >/dev/null 2>&1; do
  echo "⏳ Redis is unavailable - retrying..."
  sleep 2
done
echo "✅ Redis is up"

# Apply database migrations
echo "🔄 Running database migrations..."
cd /app/backend
if [ -f "migrate.py" ]; then
    python migrate.py upgrade || echo "⚠️ No migrations to apply"
else
    echo "⚠️ No migration script found"
fi

# Initialize database seeds if needed
if [ -f "seeds.py" ]; then
    echo "🔄 Seeding database..."
    python seeds.py || echo "⚠️ Database already seeded or seeding failed"
else
    echo "⚠️ No seed script found"
fi

# Collect static files (if needed)
if [ -d "static" ]; then
    echo "🔄 Collecting static files..."
    # Custom static collection logic here if needed
fi

echo "✅ Initialization complete"
echo "🚀 Starting Flask application..."

# Start Flask in production mode
exec gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 0.0.0.0:5000 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 120 \
    --keep-alive 5 \
    app:app
