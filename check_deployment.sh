#!/bin/bash
# Diagnostic script to check deployment issues
# Run this on your EC2 server: bash check_deployment.sh

echo "=== Deployment Diagnostic Script ==="
echo ""

cd /home/ubuntu/projects/mcq || exit 1
source venv/bin/activate

echo "1. Checking Python and Django versions..."
python --version
python manage.py --version
echo ""

echo "2. Checking environment variables..."
echo "DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY:+SET}"
echo "DJANGO_DEBUG: ${DJANGO_DEBUG:-NOT SET}"
echo "DJANGO_ALLOWED_HOSTS: ${DJANGO_ALLOWED_HOSTS:-NOT SET}"
echo "DB_ENGINE: ${DB_ENGINE:-NOT SET}"
echo ""

echo "3. Checking database connection..."
python manage.py check --database default 2>&1 || echo "ERROR: Database connection failed!"
echo ""

echo "4. Checking for pending migrations..."
python manage.py showmigrations --plan | grep "\[ \]" || echo "No pending migrations"
echo ""

echo "5. Checking Django configuration..."
python manage.py check 2>&1
echo ""

echo "6. Checking gunicorn service status..."
sudo systemctl status gunicorn_mcq --no-pager -l || echo "ERROR: Service not found or not running!"
echo ""

echo "7. Checking recent gunicorn logs..."
sudo journalctl -u gunicorn_mcq -n 20 --no-pager || echo "No logs found"
echo ""

echo "8. Testing Django application..."
python manage.py shell -c "from django.contrib.auth.models import User; print('Django models working')" 2>&1
echo ""

echo "9. Checking if UserProfile model exists..."
python manage.py shell -c "from quiz_app.models import UserProfile; print('UserProfile model found')" 2>&1 || echo "ERROR: UserProfile model not accessible!"
echo ""

echo "=== Diagnostic Complete ==="

