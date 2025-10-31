"""
Servicios de integración con APIs externas.
"""
import httpx
import logging
from typing import Optional, Dict, List
from app.config import settings

logger = logging.getLogger(__name__)

class OpenFoodFactsAPI:
    """Cliente para Open Food Facts API"""
    
    BASE_URL = "https://world.openfoodfacts.org/api/v2"
    
    @staticmethod
    async def get_product_by_barcode(barcode: str) -> Optional[Dict]:
        """
        Obtiene información de producto por código de barras.
        
        Args:
            barcode: Código de barras del producto
            
        Returns:
            Dict con información del producto o None si no se encuentra
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{OpenFoodFactsAPI.BASE_URL}/product/{barcode}.json"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('status') == 1 and data.get('product'):
                        return OpenFoodFactsAPI._parse_product(data['product'])
                
                logger.warning(f"Product not found for barcode: {barcode}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching product from OpenFoodFacts: {e}")
            return None
    
    @staticmethod
    async def search_products(query: str, country: str = "chile", 
                             category: Optional[str] = None,
                             page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        Busca productos en Open Food Facts.
        
        Args:
            query: Término de búsqueda
            country: País para filtrar
            category: Categoría opcional
            page: Número de página
            page_size: Tamaño de página
            
        Returns:
            Lista de productos encontrados
        """
        try:
            params = {
                "search_terms": query,
                "countries": country,
                "page": page,
                "page_size": page_size,
                "json": 1
            }
            
            if category:
                params["categories"] = category
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{OpenFoodFactsAPI.BASE_URL}/search",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    products = data.get('products', [])
                    
                    return [OpenFoodFactsAPI._parse_product(p) for p in products]
                
                return []
                
        except Exception as e:
            logger.error(f"Error searching products in OpenFoodFacts: {e}")
            return []
    
    @staticmethod
    def _parse_product(product_data: Dict) -> Dict:
        """Parsea datos de producto de Open Food Facts a nuestro formato"""
        
        # Extraer información nutricional
        nutriments = product_data.get('nutriments', {})
        nutritional_info = {
            "energy_kcal": nutriments.get('energy-kcal_100g'),
            "proteins": nutriments.get('proteins_100g'),
            "carbohydrates": nutriments.get('carbohydrates_100g'),
            "fats": nutriments.get('fat_100g'),
            "fiber": nutriments.get('fiber_100g'),
            "sodium": nutriments.get('sodium_100g')
        }
        
        # Extraer etiquetas
        labels = []
        if product_data.get('labels_tags'):
            labels = [label.replace('en:', '').replace('-', ' ').title() 
                     for label in product_data['labels_tags']]
        
        # Determinar categoría
        category = "food"
        if product_data.get('categories_tags'):
            category_tag = product_data['categories_tags'][0] if product_data['categories_tags'] else "food"
            category = category_tag.replace('en:', '').split(':')[-1]
        
        return {
            "barcode": product_data.get('code'),
            "name": product_data.get('product_name', 'Unknown Product'),
            "brand": product_data.get('brands'),
            "category": category,
            "image_url": product_data.get('image_url'),
            "description": product_data.get('generic_name'),
            "nutritional_info": nutritional_info,
            "ingredients": product_data.get('ingredients_text_en', '').split(', ') if product_data.get('ingredients_text_en') else None,
            "allergens": product_data.get('allergens_tags', []),
            "labels": labels,
            "origin_country": product_data.get('countries', '').split(',')[0].strip() if product_data.get('countries') else None,
            "quantity": product_data.get('quantity'),
        }

class NominatimAPI:
    """Cliente para Nominatim (OpenStreetMap) API"""
    
    BASE_URL = "https://nominatim.openstreetmap.org"
    
    @staticmethod
    async def geocode_address(address: str) -> Optional[Dict]:
        """
        Convierte dirección a coordenadas.
        
        Args:
            address: Dirección a geocodificar
            
        Returns:
            Dict con latitud, longitud y dirección formateada
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{NominatimAPI.BASE_URL}/search",
                    params={
                        "q": address,
                        "format": "json",
                        "limit": 1
                    },
                    headers={"User-Agent": "LiquiVerde/1.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data:
                        result = data[0]
                        return {
                            "latitude": float(result['lat']),
                            "longitude": float(result['lon']),
                            "address": result['display_name']
                        }
                
                return None
                
        except Exception as e:
            logger.error(f"Error geocoding address: {e}")
            return None
    
    @staticmethod
    async def reverse_geocode(latitude: float, longitude: float) -> Optional[str]:
        """
        Convierte coordenadas a dirección.
        
        Args:
            latitude: Latitud
            longitude: Longitud
            
        Returns:
            Dirección formateada
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{NominatimAPI.BASE_URL}/reverse",
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "format": "json"
                    },
                    headers={"User-Agent": "LiquiVerde/1.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('display_name')
                
                return None
                
        except Exception as e:
            logger.error(f"Error reverse geocoding: {e}")
            return None
    
    @staticmethod
    async def search_nearby_stores(latitude: float, longitude: float, 
                                   radius: int = 5000) -> List[Dict]:
        """
        Busca tiendas cercanas usando Overpass API.
        
        Args:
            latitude: Latitud
            longitude: Longitud
            radius: Radio de búsqueda en metros
            
        Returns:
            Lista de tiendas encontradas
        """
        try:
            # Usar Overpass API para buscar supermercados
            overpass_url = "https://overpass-api.de/api/interpreter"
            
            query = f"""
            [out:json];
            (
              node["shop"="supermarket"](around:{radius},{latitude},{longitude});
              node["shop"="convenience"](around:{radius},{latitude},{longitude});
            );
            out body;
            """
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    overpass_url,
                    data={"data": query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    stores = []
                    
                    for element in data.get('elements', []):
                        if element.get('tags'):
                            tags = element['tags']
                            stores.append({
                                "name": tags.get('name', 'Tienda sin nombre'),
                                "latitude": element['lat'],
                                "longitude": element['lon'],
                                "address": tags.get('addr:street', '') + ' ' + tags.get('addr:housenumber', ''),
                                "phone": tags.get('phone'),
                                "chain": tags.get('brand')
                            })
                    
                    return stores
                
                return []
                
        except Exception as e:
            logger.error(f"Error searching nearby stores: {e}")
            return []

class PriceEstimator:
    """
    Estimador de precios para productos sin precio conocido.
    Usa promedios de categoría y heurísticas.
    """
    
    # Precios promedio por categoría en Chile (CLP)
    CATEGORY_PRICES = {
        "meat": 8000,
        "poultry": 5000,
        "fish": 7000,
        "dairy": 2000,
        "cheese": 4000,
        "vegetables": 1500,
        "fruits": 2000,
        "grains": 1200,
        "legumes": 1000,
        "beverages": 1500,
        "snacks": 2500,
        "bread": 1800,
        "pasta": 1200,
        "rice": 1000,
        "oil": 3000,
        "default": 2000
    }
    
    @staticmethod
    def estimate_price(product: Dict) -> float:
        """
        Estima precio de un producto basado en categoría y características.
        
        Args:
            product: Dict con información del producto
            
        Returns:
            Precio estimado en CLP
        """
        category = product.get('category', 'default').lower()
        base_price = PriceEstimator.CATEGORY_PRICES.get(
            category, 
            PriceEstimator.CATEGORY_PRICES['default']
        )
        
        # Ajustar por marca
        brand = product.get('brand', '').lower()
        if brand and any(premium in brand for premium in ['premium', 'gourmet', 'organic']):
            base_price *= 1.5
        
        # Ajustar por etiquetas
        labels = [l.lower() for l in product.get('labels', [])]
        if 'organic' in labels:
            base_price *= 1.3
        if 'fair-trade' in labels:
            base_price *= 1.2
        
        # Ajustar por cantidad
        quantity = product.get('quantity', 1.0)
        if quantity > 1.0:
            # Descuento por volumen
            base_price *= (1 + (quantity - 1) * 0.8)
        
        return round(base_price, 0)
    
    @staticmethod
    def get_category_average(category: str) -> float:
        """Obtiene precio promedio de una categoría"""
        return PriceEstimator.CATEGORY_PRICES.get(
            category.lower(),
            PriceEstimator.CATEGORY_PRICES['default']
        )
