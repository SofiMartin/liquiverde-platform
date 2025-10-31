#!/bin/bash

echo "🌱 Iniciando LiquiVerde Platform (Modo Local)..."

# Iniciar backend
echo "🚀 Iniciando backend..."
cd backend

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias si es necesario
if [ ! -f "venv/installed" ]; then
    echo "📦 Instalando dependencias del backend..."
    pip install -r requirements.txt
    touch venv/installed
fi

# Verificar si existe la base de datos
if [ ! -f "data/liquiverde.db" ]; then
    echo "📊 Inicializando base de datos con datos de ejemplo..."
    python -m app.services.seed_data
fi

# Iniciar backend en segundo plano
echo "✅ Iniciando servidor backend en http://localhost:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Iniciar frontend
echo "🎨 Iniciando frontend..."
cd frontend

# Instalar dependencias si es necesario
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    npm install
fi

# Iniciar frontend
echo "✅ Iniciando servidor frontend en http://localhost:5173"
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ LiquiVerde Platform está ejecutándose!"
echo ""
echo "📍 URLs disponibles:"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend API: http://localhost:8000"
echo "   - Documentación API: http://localhost:8000/docs"
echo ""
echo "🛑 Para detener, presiona Ctrl+C"
echo ""

# Esperar a que el usuario presione Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
