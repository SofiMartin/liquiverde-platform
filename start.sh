#!/bin/bash

echo "🌱 Iniciando LiquiVerde Platform..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

echo "✅ Docker y Docker Compose encontrados"

# Construir y ejecutar contenedores
echo "🔨 Construyendo contenedores..."
docker-compose up --build -d

echo ""
echo "✅ LiquiVerde Platform está ejecutándose!"
echo ""
echo "📍 URLs disponibles:"
echo "   - Frontend: http://localhost"
echo "   - Backend API: http://localhost:8000"
echo "   - Documentación API: http://localhost:8000/docs"
echo ""
echo "📊 Para ver los logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Para detener:"
echo "   docker-compose down"
echo ""
