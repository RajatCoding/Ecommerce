#!/bin/sh

# Wait for the PostgreSQL database to be ready
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Run database migrations
python manage.py migrate

# Execute the command passed to the script
exec "$@"
