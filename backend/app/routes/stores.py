"""
Endpoints para gestión de tiendas y optimización de rutas.
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Tuple
import logging

from app.models.store import Store, Location, RouteOptimization
from app.services.database import StoreDB
from app.services.external_apis import NominatimAPI
from app.algorithms.route_optimization import RouteOptimizer

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Store)
async def create_store(store: Store):
    """
    Crea una nueva tienda.
    """
    store_dict = store.dict(exclude_none=True)
    store_id = await StoreDB.create(store_dict)
    store_dict['id'] = store_id
    
    return store_dict

@router.get("/")
async def list_stores():
    """
    Lista todas las tiendas.
    """
    stores = await StoreDB.get_all()
    return stores

@router.get("/nearby")
async def get_nearby_stores(
    latitude: float = Query(..., description="User latitude"),
    longitude: float = Query(..., description="User longitude"),
    radius_km: float = Query(10, description="Search radius in km")
):
    """
    Obtiene tiendas cercanas a una ubicación.
    """
    stores = await StoreDB.get_nearby(latitude, longitude, radius_km)
    
    # Calcular distancias
    from app.algorithms.route_optimization import RouteOptimizer
    
    optimizer = RouteOptimizer((latitude, longitude))
    
    for store in stores:
        store_loc = (store['location']['latitude'], store['location']['longitude'])
        distance = optimizer.calculate_distance((latitude, longitude), store_loc)
        store['distance_km'] = round(distance, 2)
    
    stores.sort(key=lambda x: x.get('distance_km', float('inf')))
    
    return stores

@router.post("/search-external")
async def search_external_stores(
    latitude: float = Body(...),
    longitude: float = Body(...),
    radius: int = Body(5000, description="Radius in meters")
):
    """
    Busca tiendas usando OpenStreetMap.
    """
    stores = await NominatimAPI.search_nearby_stores(latitude, longitude, radius)
    
    return {
        "stores": stores,
        "count": len(stores)
    }

@router.post("/geocode")
async def geocode_address(address: str = Body(..., embed=True)):
    """
    Convierte una dirección en coordenadas.
    """
    result = await NominatimAPI.geocode_address(address)
    
    if not result:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return result

@router.post("/optimize-route")
async def optimize_route(
    start_latitude: float = Body(...),
    start_longitude: float = Body(...),
    store_ids: List[str] = Body(...)
):
    """
    Optimiza la ruta para visitar múltiples tiendas.
    """
    if not store_ids:
        raise HTTPException(status_code=400, detail="No stores provided")
    
    # Obtener tiendas
    stores = []
    for store_id in store_ids:
        all_stores = await StoreDB.get_all()
        store = next((s for s in all_stores if s['id'] == store_id), None)
        
        if store:
            stores.append(store)
    
    if not stores:
        raise HTTPException(status_code=404, detail="No valid stores found")
    
    # Optimizar ruta
    optimizer = RouteOptimizer((start_latitude, start_longitude))
    optimized_route = optimizer.optimize_route(stores)
    
    return optimized_route

@router.post("/compare-routes")
async def compare_routes(
    start_latitude: float = Body(...),
    start_longitude: float = Body(...),
    store_ids: List[str] = Body(...),
    alternative_orders: List[List[int]] = Body(default=[])
):
    """
    Compara diferentes órdenes de visita a tiendas.
    """
    # Obtener tiendas
    stores = []
    for store_id in store_ids:
        all_stores = await StoreDB.get_all()
        store = next((s for s in all_stores if s['id'] == store_id), None)
        
        if store:
            stores.append(store)
    
    if not stores:
        raise HTTPException(status_code=404, detail="No valid stores found")
    
    # Si no hay órdenes alternativas, generar algunas
    if not alternative_orders:
        # Orden original
        alternative_orders.append(list(range(len(stores))))
        
        # Orden inverso
        alternative_orders.append(list(range(len(stores)-1, -1, -1)))
    
    optimizer = RouteOptimizer((start_latitude, start_longitude))
    comparison = optimizer.compare_routes(stores, alternative_orders)
    
    return comparison

@router.get("/map-data")
async def get_map_data(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: float = Query(10)
):
    """
    Obtiene datos para renderizar mapa con tiendas.
    """
    if latitude and longitude:
        stores = await StoreDB.get_nearby(latitude, longitude, radius_km)
        center = {"latitude": latitude, "longitude": longitude}
    else:
        stores = await StoreDB.get_all()
        
        # Calcular centro promedio
        if stores:
            avg_lat = sum(s['location']['latitude'] for s in stores) / len(stores)
            avg_lon = sum(s['location']['longitude'] for s in stores) / len(stores)
            center = {"latitude": avg_lat, "longitude": avg_lon}
        else:
            # Santiago, Chile por defecto
            center = {"latitude": -33.4489, "longitude": -70.6693}
    
    # Preparar datos para mapa
    map_markers = []
    
    for store in stores:
        map_markers.append({
            "id": store['id'],
            "name": store['name'],
            "position": {
                "lat": store['location']['latitude'],
                "lng": store['location']['longitude']
            },
            "info": {
                "address": store['location']['address'],
                "chain": store.get('chain'),
                "sustainability_rating": store.get('sustainability_rating')
            }
        })
    
    return {
        "center": center,
        "markers": map_markers,
        "zoom": 12
    }
