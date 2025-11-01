#!/bin/bash

echo "Starting LiquiVerde Platform on Railway..."

# Start nginx in background
nginx &

# Start backend
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
