#!/bin/bash

cd "$(dirname "$0")/../local"

echo "🚀 Building and starting all services..."
docker-compose up -d --build

# echo "⏳ Waiting for services..."
# sleep 5

# echo "🔧 Running migrations..."
# docker-compose exec web python manage.py migrate

# echo "📦 Collecting static files..."
# docker-compose exec web python manage.py collectstatic --noinput

# echo ""
# echo "✅ All services running!"
# echo ""
# echo "🌐 Django: http://localhost:8000"
# echo ""
# echo "Useful commands:"
# echo "  View logs:     cd deploy/local && docker-compose logs -f"
# echo "  Stop all:      cd deploy/local && docker-compose down"
# echo "  Restart:       cd deploy/local && docker-compose restart"
# echo "  Shell:         cd deploy/local && docker-compose exec web python manage.py shell"
