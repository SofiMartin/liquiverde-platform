# Documentación de Algoritmos - LiquiVerde

Este documento explica en detalle los algoritmos implementados en la plataforma.

## 1. Algoritmo de Mochila Multi-objetivo

### Descripción
Implementa una variante del problema de la mochila (0/1 Knapsack) que optimiza múltiples objetivos simultáneamente: presupuesto, sostenibilidad y prioridad de productos.

### Ubicación
`backend/app/algorithms/knapsack.py`

### Complejidad
- **Temporal**: O(n × W × Q) donde:
  - n = número de productos
  - W = presupuesto en centavos
  - Q = cantidad máxima por producto
- **Espacial**: O(n × W)

### Funcionamiento

#### 1. Cálculo de Valor Multi-objetivo
```python
value = (sustainability_score × w1) + (savings_score × w2) + (priority × w3)
```

Donde:
- `sustainability_score`: Puntuación de sostenibilidad normalizada (0-1)
- `savings_score`: Ahorro vs precio promedio de categoría (0-1)
- `priority`: Prioridad del producto normalizada (0-1)
- `w1, w2, w3`: Pesos configurables (default: 0.3, 0.4, 0.3)

#### 2. Programación Dinámica
```
dp[i][w] = valor máximo usando productos 1..i con presupuesto w

Para cada producto i y presupuesto w:
  Para cada cantidad q de 1 a cantidad_deseada:
    Si costo(i, q) <= w:
      dp[i][w] = max(dp[i][w], dp[i-1][w-costo(i,q)] + valor(i) × q)
```

#### 3. Reconstrucción de Solución
Se recorre la tabla DP en reversa para determinar qué productos y cantidades fueron seleccionados.

### Casos Especiales

#### Productos Esenciales
```python
def optimize_with_essentials(products, quantities, essential_indices):
    # 1. Calcular costo de esenciales
    essential_cost = sum(price[i] × qty[i] for i in essential_indices)
    
    # 2. Si excede presupuesto, reducir proporcionalmente
    if essential_cost > budget:
        factor = budget / essential_cost
        return reduced_essentials
    
    # 3. Optimizar no-esenciales con presupuesto restante
    remaining_budget = budget - essential_cost
    optimize(non_essential_products, remaining_budget)
```

### Ejemplo de Uso
```python
knapsack = MultiObjectiveKnapsack(
    max_budget=50000,
    sustainability_weight=0.35,
    savings_weight=0.35,
    priority_weight=0.30
)

quantities, stats = knapsack.optimize(products, desired_quantities)
```

---

## 2. Sistema de Scoring de Sostenibilidad

### Descripción
Calcula puntuaciones multi-dimensionales para evaluar la sostenibilidad de productos en tres aspectos: económico, ambiental y social.

### Ubicación
`backend/app/algorithms/sustainability_scoring.py`

### Dimensiones de Evaluación

#### A. Score Económico (0-100)

**Factores considerados**:
1. **Relación precio/calidad** (±30 puntos)
   ```
   ratio = precio_producto / precio_promedio_categoria
   
   Si ratio < 0.8:  +30 puntos (muy barato)
   Si ratio < 1.0:  +20 puntos (barato)
   Si ratio < 1.2:  +10 puntos (justo)
   Si ratio < 1.5:  -10 puntos (caro)
   Si ratio >= 1.5: -20 puntos (muy caro)
   ```

2. **Valor nutricional** (+10 puntos)
   - Alto en proteína (>10g) o fibra (>5g)

3. **Compra a granel** (+10 puntos máx)
   - Bonus proporcional a cantidad

**Score base**: 50 puntos

#### B. Score Ambiental (0-100)

**1. Huella de Carbono**

Factores de emisión por categoría (kg CO₂/kg):
```python
CARBON_FACTORS = {
    "meat": 27.0,      # Carne roja
    "poultry": 6.9,    # Aves
    "dairy": 13.5,     # Lácteos
    "fish": 6.0,       # Pescado
    "vegetables": 2.0, # Verduras
    "fruits": 1.1,     # Frutas
    "grains": 2.5,     # Granos
    "legumes": 0.9,    # Legumbres
}
```

Cálculo:
```python
carbon_footprint = carbon_factor × peso_kg + transporte_carbon

# Transporte
transport_carbon = (distancia_km / 1000) × 0.1 × peso_kg
```

Distancias de transporte:
- Local: 50 km
- Nacional: 500 km
- Sudamérica: 2,000 km
- Norteamérica: 5,000 km
- Europa: 10,000 km
- Asia: 12,000 km

**Puntuación por huella**:
```
Si carbon < 1 kg:   +30 puntos
Si carbon < 3 kg:   +15 puntos
Si carbon < 5 kg:   +5 puntos
Si carbon < 10 kg:  -10 puntos
Si carbon >= 10 kg: -25 puntos
```

**2. Certificaciones** (+25 puntos máx)
- Orgánico: +15 puntos, -10% huella
- Eco-friendly: +10 puntos
- Origen local: +20 puntos, -30% huella

**Score base**: 50 puntos

#### C. Score Social (0-100)

**Certificaciones y prácticas**:
- Fair Trade: +25 puntos
- B-Corp: +20 puntos
- Origen local (Chile): +20 puntos
- Origen regional (Sudamérica): +10 puntos
- Pequeño productor: +15 puntos
- Cooperativa: +15 puntos

**Score base**: 50 puntos

### Score General

```python
overall_score = (economic × 0.33) + (environmental × 0.34) + (social × 0.33)
```

### Equivalencias de Impacto

Para hacer el impacto más comprensible:
```python
equivalences = {
    "km_driven": carbon_kg × 4.5,        # km en auto
    "trees_needed": carbon_kg / 21,       # árboles/año
    "days_of_energy": carbon_kg / 6       # días de energía hogar
}
```

---

## 3. Algoritmo de Sustitución Inteligente

### Descripción
Encuentra productos alternativos que mejoran sostenibilidad y/o precio manteniendo similitud funcional.

### Ubicación
`backend/app/algorithms/product_substitution.py`

### Proceso de Sustitución

#### 1. Filtrado de Candidatos
```python
# Restricciones
max_price_increase = 10%  # Máximo incremento de precio
min_sustainability_improvement = 5.0  # Mínima mejora requerida

# Filtros aplicados
if price_increase > max_price_increase:
    skip
if sustainability_improvement < min_sustainability_improvement:
    skip
```

#### 2. Cálculo de Score de Sustitución

```python
score = (sustainability_improvement × 0.35) + 
        (price_savings × 0.30) + 
        (category_match × 0.20) + 
        (nutritional_similarity × 0.15)
```

**Componentes**:

a) **Mejora de Sostenibilidad** (0-35 puntos)
```python
improvement = candidate_score - original_score
normalized = min(100, max(0, improvement))
component = normalized × 0.35
```

b) **Ahorro de Precio** (0-30 puntos)
```python
savings_percent = ((original_price - candidate_price) / original_price) × 100
normalized = min(100, max(0, savings_percent × 5))  # 20% ahorro = 100 puntos
component = normalized × 0.30
```

c) **Similitud de Categoría** (0-20 puntos)
```python
if same_category:
    score = 100
elif related_category:
    score = 70
else:
    score = 30
```

Categorías relacionadas:
```python
related = {
    'meat': ['poultry', 'fish'],
    'dairy': ['cheese', 'yogurt', 'milk'],
    'vegetables': ['fruits', 'legumes'],
}
```

d) **Similitud Nutricional** (0-15 puntos)
```python
for metric in ['energy_kcal', 'proteins', 'carbs', 'fats']:
    diff = abs(val1 - val2) / max(val1, val2)
    similarity = (1 - diff) × 100

avg_similarity = sum(similarities) / len(similarities)
```

#### 3. Generación de Razón

```python
reasons = []
if sustainability_improvement > 20:
    reasons.append("Mejora significativa en sostenibilidad")
if savings_percent > 15:
    reasons.append("Ahorro considerable")
if 'organic' in labels:
    reasons.append("Producto orgánico")
if origin == 'local':
    reasons.append("Producción local")

reason = " | ".join(reasons)
```

### Sustitución en Lote

```python
def batch_substitute(products, candidate_pool):
    substitutions = []
    
    for product in products:
        substitutes = find_substitutes(product, candidate_pool)
        if substitutes:
            best = substitutes[0]  # Mayor score
            substitutions.append(best)
    
    # Ordenar por impacto combinado
    substitutions.sort(
        key=lambda x: x['sustainability_improvement'] + (x['savings'] × 10),
        reverse=True
    )
    
    return substitutions
```

---

## 4. Optimización de Rutas (TSP)

### Descripción
Optimiza el orden de visita a múltiples tiendas minimizando distancia total recorrida.

### Ubicación
`backend/app/algorithms/route_optimization.py`

### Algoritmos Implementados

#### 1. Cálculo de Distancia (Haversine)

Fórmula para calcular distancia entre dos coordenadas geográficas:

```python
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    
    # Convertir a radianes
    φ1 = radians(lat1)
    φ2 = radians(lat2)
    Δφ = radians(lat2 - lat1)
    Δλ = radians(lon2 - lon1)
    
    # Fórmula haversine
    a = sin²(Δφ/2) + cos(φ1) × cos(φ2) × sin²(Δλ/2)
    c = 2 × atan2(√a, √(1-a))
    
    distance = R × c
    return distance
```

#### 2. Nearest Neighbor (Greedy)

Algoritmo greedy para solución inicial:

```python
def nearest_neighbor(stores, start_location):
    current = start_location
    unvisited = set(range(len(stores)))
    route = []
    total_distance = 0
    
    while unvisited:
        # Encontrar tienda más cercana
        nearest = min(unvisited, 
                     key=lambda i: distance(current, stores[i]))
        
        route.append(nearest)
        total_distance += distance(current, stores[nearest])
        current = stores[nearest]
        unvisited.remove(nearest)
    
    # Regresar al inicio
    total_distance += distance(current, start_location)
    
    return route, total_distance
```

**Complejidad**: O(n²)

#### 3. Optimización 2-opt

Mejora la ruta intercambiando pares de aristas:

```python
def two_opt(route, stores):
    improved = True
    best_route = route
    best_distance = calculate_distance(route)
    
    while improved:
        improved = False
        
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                # Invertir segmento route[i:j+1]
                new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
                new_distance = calculate_distance(new_route)
                
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
        
        route = best_route
    
    return best_route, best_distance
```

**Complejidad**: O(n² × iteraciones)

#### 4. Estimación de Tiempo

```python
def estimate_time(distance_km, num_stores):
    # Tiempo de viaje (30 km/h promedio en ciudad)
    travel_time = (distance_km / 30) × 60  # minutos
    
    # Tiempo de compras (15 min por tienda)
    shopping_time = num_stores × 15
    
    total_time = travel_time + shopping_time
    return total_time
```

### Ejemplo de Uso

```python
optimizer = RouteOptimizer(start_location=(-33.4489, -70.6693))

result = optimizer.optimize_route(stores)

# Resultado:
{
    "route": [store1, store2, store3],
    "total_distance": 12.5,  # km
    "estimated_time": 70,     # minutos
    "order": [0, 2, 1],
    "travel_time": 25,
    "shopping_time": 45
}
```

---

## Consideraciones de Rendimiento

### Optimizaciones Implementadas

1. **Mochila Multi-objetivo**:
   - Uso de centavos para evitar errores de punto flotante
   - Límite de iteraciones en optimización
   - Caché de cálculos de valor

2. **Scoring de Sostenibilidad**:
   - Cálculos pre-computados de factores de carbono
   - Lookup tables para distancias de transporte

3. **Sustitución**:
   - Filtrado temprano de candidatos no viables
   - Límite en número de sustituciones evaluadas

4. **Rutas**:
   - Límite de 100 iteraciones en 2-opt
   - Early stopping si no hay mejoras

### Escalabilidad

- **Productos**: Optimizado para ~1000 productos
- **Listas de compras**: Hasta 100 items por lista
- **Rutas**: Hasta 10 tiendas (TSP es NP-hard)

---

## Testing de Algoritmos

### Casos de Prueba Recomendados

1. **Mochila**:
   - Lista vacía
   - Presupuesto insuficiente
   - Todos productos esenciales
   - Productos con mismo precio

2. **Scoring**:
   - Productos sin información nutricional
   - Productos importados vs locales
   - Productos con múltiples certificaciones

3. **Sustitución**:
   - Sin candidatos disponibles
   - Todos candidatos más caros
   - Categorías no relacionadas

4. **Rutas**:
   - Una sola tienda
   - Tiendas muy cercanas
   - Tiendas muy dispersas

---

## Referencias

- [Knapsack Problem - Wikipedia](https://en.wikipedia.org/wiki/Knapsack_problem)
- [Travelling Salesman Problem - Wikipedia](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
- [Carbon Footprint of Food](https://ourworldindata.org/environmental-impacts-of-food)
- [Haversine Formula](https://en.wikipedia.org/wiki/Haversine_formula)
