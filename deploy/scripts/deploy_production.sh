#!/bin/bash

cd "$(dirname "$0")/../.."

echo "🚀 Starting local environment..."

# Start Docker services
cd deploy/local
docker-compose up -d
cd ../..

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
sleep 3

# Setup Django
python -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt

export DJANGO_ENV=local
python manage.py migrate
python manage.py collectstatic --noinput

echo "✅ Local environment ready!"
echo ""
echo "Run these in separate terminals:"
echo "  1. python manage.py runserver"
echo "  2. celery -A core worker -l info"
