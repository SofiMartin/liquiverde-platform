#!/bin/bash
set -e

echo "Building frontend with API URL: $VITE_API_URL"

# Si no está definida, usar el valor de producción
if [ -z "$VITE_API_URL" ]; then
  export VITE_API_URL="https://liquiverde-platform.onrender.com/api"
  echo "Using default API URL: $VITE_API_URL"
fi

npm install
npm run build

# Copiar _redirects al dist
cp public/_redirects dist/

echo "Build complete!"
