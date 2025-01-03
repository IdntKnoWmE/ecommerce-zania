#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database to be ready..."
# You can use a utility like `wait-for-it` or `dockerize` here to ensure DB readiness.

# Run migrations
#python manage.py migrate

# Collect static files for production
#RUN python manage.py collectstatic --noinput

# Start the application
exec gunicorn ecom.wsgi:application --bind 0.0.0.0:8000
