# LiquiVerde - Plataforma de Retail Inteligente 🌱

Plataforma full-stack que ayuda a los consumidores a ahorrar dinero mientras toman decisiones de compra sostenibles, optimizando presupuesto e impacto ambiental/social.

## 🎯 Características Principales

### Funcionalidades Obligatorias ✅
- **Escáner de Productos**: Escaneo por código de barras y búsqueda de productos
- **Análisis de Sostenibilidad**: Sistema de scoring multi-dimensional (económico, ambiental, social)
- **Optimización de Listas**: Algoritmo de mochila multi-objetivo para optimizar compras
- **Cálculo de Ahorros**: Estimación de ahorros y comparación de precios
- **Sustitución Inteligente**: Recomendaciones de productos alternativos más sostenibles

### Funcionalidades Bonus 🌟
- **Dashboard de Impacto**: Visualización de métricas de sostenibilidad y ahorros
- **Comparador de Productos**: Comparación detallada entre dos productos
- **Mapa de Tiendas**: Visualización de tiendas cercanas
- **Optimización de Rutas**: Algoritmo para optimizar rutas de compras
- **PWA**: Progressive Web App con manifest.json
- **Dockerización**: Docker y Docker Compose para despliegue fácil

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: FastAPI (Python)
- **Base de Datos**: MongoDB (NoSQL, escalable y flexible)
- **ORM/ODM**: Motor (async MongoDB driver)
- **APIs Externas**:
  - Open Food Facts API (información de productos)
  - OpenStreetMap Nominatim (geocodificación)
  - Overpass API (búsqueda de tiendas)

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Routing**: React Router DOM

### DevOps
- **Containerización**: Docker + Docker Compose
- **Web Server**: Nginx (para frontend en producción)

## 📊 Algoritmos Implementados

### 1. Algoritmo de Mochila Multi-objetivo ✅
**Archivo**: `backend/app/algorithms/knapsack.py`

Optimiza la selección de productos considerando múltiples objetivos:
- **Presupuesto**: Maximiza valor dentro del presupuesto disponible
- **Sostenibilidad**: Prioriza productos con mejor score ambiental
- **Prioridad**: Considera la importancia de cada producto

**Implementación**:
- Programación dinámica con cantidades variables
- Soporte para productos esenciales
- Ponderación configurable de objetivos

**Fórmula de valor**:
```
value = (sustainability_score × w1) + (savings_score × w2) + (priority × w3)
```

### 2. Sistema de Scoring de Sostenibilidad ✅
**Archivo**: `backend/app/algorithms/sustainability_scoring.py`

Calcula puntuaciones en tres dimensiones:

**a) Score Económico (0-100)**:
- Relación precio/calidad
- Comparación con promedio de categoría
- Valor nutricional
- Descuentos por volumen

**b) Score Ambiental (0-100)**:
- Huella de carbono (basada en categoría y origen)
- Distancia de transporte
- Certificaciones orgánicas
- Packaging sostenible

**Factores de emisión por categoría**:
```python
CARBON_FACTORS = {
    "meat": 27.0 kg CO2/kg,
    "dairy": 13.5 kg CO2/kg,
    "vegetables": 2.0 kg CO2/kg,
    "legumes": 0.9 kg CO2/kg,
    ...
}
```

**c) Score Social (0-100)**:
- Comercio justo
- Producción local
- Certificaciones sociales (B-Corp, Fair Trade)
- Pequeños productores

**Score General**:
```
overall = economic × 0.33 + environmental × 0.34 + social × 0.33
```

### 3. Algoritmo de Sustitución Inteligente ✅
**Archivo**: `backend/app/algorithms/product_substitution.py`

Encuentra alternativas mejores basándose en:
- Mejora de sostenibilidad (mínimo configurable)
- Ahorro de precio (máximo incremento permitido)
- Similitud de categoría
- Similitud nutricional

**Score de sustitución**:
```
score = (sustainability_improvement × 0.35) + 
        (price_savings × 0.30) + 
        (category_match × 0.20) + 
        (nutritional_similarity × 0.15)
```

### 4. Optimización de Rutas (BONUS) ✅
**Archivo**: `backend/app/algorithms/route_optimization.py`

Implementa el problema del viajante (TSP):
- **Algoritmo Greedy**: Nearest Neighbor para solución inicial
- **Optimización 2-opt**: Mejora local de la ruta
- **Cálculo de distancia**: Fórmula Haversine para coordenadas geográficas

## 🚀 Instalación y Ejecución

### Opción 1: Docker (Recomendado)

```bash
# Clonar repositorio
git clone <repository-url>
cd liquiverde-platform

# Construir y ejecutar con Docker Compose
docker-compose up --build

# La aplicación estará disponible en:
# - Frontend: http://localhost
# - Backend API: http://localhost:8000
# - MongoDB: localhost:27017
# - Documentación API: http://localhost:8000/docs

# Para poblar la base de datos con datos de ejemplo:
docker-compose exec backend python -m app.services.seed_data
```

### Opción 2: Ejecución Local

#### Backend

```bash
# Asegúrate de tener MongoDB instalado y ejecutándose
# En Ubuntu/Debian: sudo systemctl start mongod
# En macOS con Homebrew: brew services start mongodb-community
# O usa Docker: docker run -d -p 27017:27017 --name mongodb mongo:7.0

cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env
# Editar .env y configurar MONGODB_URL si es necesario

# Inicializar base de datos con datos de ejemplo
python -m app.services.seed_data

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# La aplicación estará en http://localhost:5173
```

## 📁 Estructura del Proyecto

```
liquiverde-platform/
├── backend/
│   ├── app/
│   │   ├── algorithms/          # Algoritmos de optimización
│   │   │   ├── knapsack.py
│   │   │   ├── sustainability_scoring.py
│   │   │   ├── product_substitution.py
│   │   │   └── route_optimization.py
│   │   ├── models/              # Modelos de datos (Pydantic)
│   │   │   ├── product.py
│   │   │   ├── shopping_list.py
│   │   │   └── store.py
│   │   ├── routes/              # Endpoints API
│   │   │   ├── products.py
│   │   │   ├── shopping_lists.py
│   │   │   ├── analysis.py
│   │   │   └── stores.py
│   │   ├── services/            # Servicios externos y DB
│   │   │   ├── database.py      # MongoDB con Motor
│   │   │   ├── external_apis.py
│   │   │   └── seed_data.py
│   │   ├── config.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Scanner.jsx
│   │   │   ├── ShoppingList.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ProductComparison.jsx
│   │   │   └── StoreMap.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── public/
│   │   └── manifest.json        # PWA manifest
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 📡 API Endpoints

### Productos
- `POST /api/products/scan/{barcode}` - Escanear producto por código de barras
- `GET /api/products/search` - Buscar productos
- `GET /api/products/{id}` - Obtener producto por ID
- `POST /api/products/{id}/substitutes` - Encontrar sustitutos
- `POST /api/products/compare` - Comparar dos productos

### Listas de Compras
- `POST /api/shopping-lists/` - Crear lista
- `POST /api/shopping-lists/{id}/optimize` - Optimizar lista
- `POST /api/shopping-lists/analyze` - Analizar lista
- `POST /api/shopping-lists/quick-optimize` - Optimización rápida

### Análisis
- `GET /api/analysis/dashboard` - Estadísticas del dashboard
- `GET /api/analysis/impact` - Calcular impacto ambiental
- `GET /api/analysis/trends` - Tendencias de sostenibilidad
- `GET /api/analysis/savings-report` - Reporte de ahorros

### Tiendas
- `GET /api/stores/` - Listar tiendas
- `GET /api/stores/nearby` - Tiendas cercanas
- `POST /api/stores/optimize-route` - Optimizar ruta
- `GET /api/stores/map-data` - Datos para mapa

## 📊 Dataset de Ejemplo

El proyecto incluye un dataset de 15 productos de ejemplo en categorías:
- Carnes y proteínas
- Lácteos
- Frutas y verduras
- Granos y legumbres
- Bebidas
- Snacks

Y 5 tiendas de ejemplo en Santiago, Chile.

Para cargar los datos:
```bash
cd backend
python -m app.services.seed_data
```

## 🧪 Uso de IA

Este proyecto fue desarrollado con asistencia de IA para:

### Desarrollo de Algoritmos
- **Algoritmo de Mochila Multi-objetivo**: Implementación de programación dinámica con múltiples criterios de optimización
- **Sistema de Scoring**: Diseño de fórmulas y factores de ponderación para sostenibilidad
- **Algoritmo de Sustitución**: Lógica de comparación y scoring de productos alternativos
- **Optimización de Rutas**: Implementación de TSP con Nearest Neighbor y 2-opt

### Arquitectura y Estructura
- Diseño de la estructura de carpetas y organización del código
- Definición de modelos de datos con Pydantic
- Configuración de FastAPI con routers y middleware
- Estructura de componentes React con React Router

### Implementación de Features
- Integración con APIs externas (Open Food Facts, OpenStreetMap)
- Sistema de base de datos con SQLite
- Interfaz de usuario con React y TailwindCSS
- Dockerización y configuración de despliegue

### Documentación
- Generación de este README con instrucciones detalladas
- Documentación de algoritmos y fórmulas
- Comentarios en código para explicar lógica compleja

## 🎨 Características de UX/UI

- **Diseño Responsivo**: Funciona en desktop y móvil
- **Navegación Intuitiva**: Menú claro con iconos descriptivos
- **Feedback Visual**: Indicadores de carga y estados
- **Código de Colores**: Verde para sostenibilidad, rojo/amarillo para alertas
- **PWA Ready**: Manifest.json configurado para instalación

## 🔧 Configuración de Variables de Entorno

Crear archivo `.env` en `backend/`:

```env
# APIs Externas (opcional)
USDA_API_KEY=your_key_here
CARBON_API_KEY=your_key_here

# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=liquiverde

# Aplicación
DEBUG=True
SECRET_KEY=change-in-production
```

## 📈 Métricas de Sostenibilidad

El sistema calcula:
- **Huella de Carbono**: kg CO₂ por producto
- **Score de Sostenibilidad**: 0-100 en tres dimensiones
- **Ahorros Estimados**: Comparación con precios promedio
- **Equivalencias**: km en auto, árboles necesarios, días de energía

## 🚀 Despliegue en Producción

### Opciones Gratuitas
- **Backend**: Railway, Render, Fly.io
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Base de Datos**: Railway (PostgreSQL), Supabase

### Pasos para Despliegue
1. Configurar variables de entorno en la plataforma
2. Conectar repositorio Git
3. La plataforma detectará Dockerfile y construirá automáticamente
4. Configurar dominio personalizado (opcional)

## 🧪 Testing

### Backend Tests

El proyecto incluye tests completos para algoritmos y endpoints de la API.

```bash
cd backend

# Instalar dependencias de testing (si no están instaladas)
pip install pytest pytest-asyncio pytest-cov

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests con cobertura
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

# O usar el script incluido
./run_tests.sh

# Ejecutar solo tests de algoritmos
pytest tests/test_algorithms_simple.py -v

# Ejecutar solo tests de API
pytest tests/test_api.py -v
```

**Tests Incluidos:**
- ✅ **Algoritmos**: 10+ tests para scoring de sostenibilidad
- ✅ **API Endpoints**: 15+ tests para productos, listas, análisis y tiendas
- ✅ **Integración**: Tests end-to-end de flujos completos

### Frontend Tests

```bash
cd frontend
npm test
```

## 📝 Licencia

Este proyecto fue creado como parte de un desafío técnico.

## 👥 Contribuciones

Para contribuir:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para preguntas o problemas, abre un issue en el repositorio.

---

**Desarrollado con 💚 para un futuro más sostenible**
