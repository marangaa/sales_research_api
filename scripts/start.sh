#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER
do
  sleep 1
done

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start development server
echo "Starting development server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload