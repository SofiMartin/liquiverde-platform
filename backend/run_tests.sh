#!/bin/bash

echo "🧪 Ejecutando tests de LiquiVerde Platform..."
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar tests con cobertura
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

echo ""
echo "✅ Tests completados!"
echo "📊 Reporte de cobertura generado en: htmlcov/index.html"
