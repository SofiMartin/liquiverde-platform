"""
Algoritmo de Optimización de Rutas de Tiendas (BONUS)
Implementa el problema del viajante (TSP) para optimizar rutas de compras.
"""
import logging
from typing import List, Dict, Tuple
import math

logger = logging.getLogger(__name__)

class RouteOptimizer:
    """
    Optimiza rutas de visita a tiendas usando algoritmo greedy nearest neighbor
    con mejoras locales (2-opt).
    """
    
    def __init__(self, start_location: Tuple[float, float]):
        """
        Args:
            start_location: Tupla (latitud, longitud) del punto de inicio
        """
        self.start_location = start_location
    
    def calculate_distance(self, loc1: Tuple[float, float], 
                          loc2: Tuple[float, float]) -> float:
        """
        Calcula distancia haversine entre dos coordenadas.
        
        Returns:
            Distancia en kilómetros
        """
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        
        # Radio de la Tierra en km
        R = 6371.0
        
        # Convertir a radianes
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Fórmula haversine
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def optimize_route(self, stores: List[Dict]) -> Dict:
        """
        Optimiza la ruta de visita a tiendas.
        
        Args:
            stores: Lista de tiendas con ubicación
            
        Returns:
            Dict con ruta optimizada y estadísticas
        """
        if not stores:
            return {
                "route": [],
                "total_distance": 0,
                "estimated_time": 0,
                "order": []
            }
        
        if len(stores) == 1:
            store = stores[0]
            loc = (store['location']['latitude'], store['location']['longitude'])
            distance = self.calculate_distance(self.start_location, loc) * 2  # Ida y vuelta
            
            return {
                "route": [store],
                "total_distance": round(distance, 2),
                "estimated_time": round(distance / 30 * 60, 0),  # 30 km/h promedio
                "order": [0]
            }
        
        # Algoritmo Nearest Neighbor
        unvisited = list(range(len(stores)))
        route_order = []
        current_location = self.start_location
        total_distance = 0
        
        while unvisited:
            # Encontrar tienda más cercana
            nearest_idx = None
            nearest_distance = float('inf')
            
            for idx in unvisited:
                store = stores[idx]
                store_loc = (store['location']['latitude'], 
                           store['location']['longitude'])
                distance = self.calculate_distance(current_location, store_loc)
                
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_idx = idx
            
            # Visitar tienda más cercana
            route_order.append(nearest_idx)
            unvisited.remove(nearest_idx)
            total_distance += nearest_distance
            
            store = stores[nearest_idx]
            current_location = (store['location']['latitude'],
                              store['location']['longitude'])
        
        # Agregar regreso al inicio
        return_distance = self.calculate_distance(current_location, self.start_location)
        total_distance += return_distance
        
        # Aplicar optimización 2-opt
        route_order, total_distance = self._two_opt_optimization(
            route_order, stores, total_distance
        )
        
        # Construir ruta final
        optimized_route = [stores[i] for i in route_order]
        
        # Estimar tiempo (30 km/h promedio + 15 min por tienda)
        travel_time = (total_distance / 30) * 60  # minutos
        shopping_time = len(stores) * 15  # 15 min por tienda
        total_time = travel_time + shopping_time
        
        logger.info(f"Optimized route for {len(stores)} stores: {total_distance:.2f} km")
        
        return {
            "route": optimized_route,
            "total_distance": round(total_distance, 2),
            "estimated_time": round(total_time, 0),
            "order": route_order,
            "travel_time": round(travel_time, 0),
            "shopping_time": shopping_time
        }
    
    def _two_opt_optimization(self, route: List[int], stores: List[Dict],
                             initial_distance: float) -> Tuple[List[int], float]:
        """
        Aplica optimización 2-opt para mejorar la ruta.
        
        Returns:
            Tuple de (ruta_mejorada, distancia_total)
        """
        improved = True
        best_route = route.copy()
        best_distance = initial_distance
        
        iterations = 0
        max_iterations = 100
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            
            for i in range(1, len(route) - 1):
                for j in range(i + 1, len(route)):
                    # Crear nueva ruta invirtiendo segmento
                    new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
                    
                    # Calcular distancia de nueva ruta
                    new_distance = self._calculate_route_distance(new_route, stores)
                    
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
            
            route = best_route
        
        logger.info(f"2-opt completed in {iterations} iterations")
        return best_route, best_distance
    
    def _calculate_route_distance(self, route: List[int], stores: List[Dict]) -> float:
        """Calcula distancia total de una ruta"""
        total = 0
        current = self.start_location
        
        for idx in route:
            store = stores[idx]
            store_loc = (store['location']['latitude'], 
                        store['location']['longitude'])
            total += self.calculate_distance(current, store_loc)
            current = store_loc
        
        # Agregar regreso
        total += self.calculate_distance(current, self.start_location)
        
        return total
    
    def compare_routes(self, stores: List[Dict], 
                      alternative_orders: List[List[int]]) -> Dict:
        """
        Compara diferentes órdenes de visita a tiendas.
        
        Args:
            stores: Lista de tiendas
            alternative_orders: Lista de órdenes alternativos a comparar
            
        Returns:
            Dict con comparación de rutas
        """
        routes_comparison = []
        
        # Calcular ruta optimizada
        optimized = self.optimize_route(stores)
        
        routes_comparison.append({
            "name": "Optimizada",
            "order": optimized['order'],
            "distance": optimized['total_distance'],
            "time": optimized['estimated_time']
        })
        
        # Calcular rutas alternativas
        for i, order in enumerate(alternative_orders):
            distance = self._calculate_route_distance(order, stores)
            time = (distance / 30) * 60 + len(stores) * 15
            
            routes_comparison.append({
                "name": f"Alternativa {i+1}",
                "order": order,
                "distance": round(distance, 2),
                "time": round(time, 0)
            })
        
        # Encontrar mejor ruta
        best_route = min(routes_comparison, key=lambda x: x['distance'])
        
        return {
            "routes": routes_comparison,
            "best_route": best_route,
            "savings_vs_worst": round(
                max(r['distance'] for r in routes_comparison) - best_route['distance'],
                2
            )
        }
