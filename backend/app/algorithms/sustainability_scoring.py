"""
Sistema de Scoring de Sostenibilidad (económico, ambiental, social)
Calcula puntuaciones multi-dimensionales para productos.
"""
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class SustainabilityScorer:
    """
    Calcula puntuaciones de sostenibilidad en tres dimensiones:
    - Económica: relación calidad-precio, ahorros
    - Ambiental: huella de carbono, packaging, origen
    - Social: comercio justo, condiciones laborales, local
    """
    
    # Factores de emisión de CO2 por categoría (kg CO2 por kg de producto)
    CARBON_FACTORS = {
        "meat": 27.0,
        "dairy": 13.5,
        "fish": 6.0,
        "vegetables": 2.0,
        "fruits": 1.1,
        "grains": 2.5,
        "legumes": 0.9,
        "beverages": 1.5,
        "snacks": 3.0,
        "default": 3.5
    }
    
    # Distancias promedio por región (km)
    TRANSPORT_DISTANCES = {
        "local": 50,
        "national": 500,
        "south_america": 2000,
        "north_america": 5000,
        "europe": 10000,
        "asia": 12000,
        "default": 8000
    }
    
    def __init__(self):
        self.weights = {
            "economic": 0.33,
            "environmental": 0.34,
            "social": 0.33
        }
    
    def calculate_economic_score(self, product: Dict, category_avg_price: Optional[float] = None) -> float:
        """
        Calcula puntuación económica basada en:
        - Relación precio/calidad
        - Comparación con promedio de categoría
        - Valor nutricional (si aplica)
        
        Returns:
            Score de 0-100
        """
        score = 50.0  # Base score
        
        price = product.get('price', 0)
        if price <= 0:
            return 50.0
        
        # Comparar con promedio de categoría
        if category_avg_price and category_avg_price > 0:
            price_ratio = price / category_avg_price
            if price_ratio < 0.8:
                score += 30  # Muy barato
            elif price_ratio < 1.0:
                score += 20  # Barato
            elif price_ratio < 1.2:
                score += 10  # Precio justo
            elif price_ratio < 1.5:
                score -= 10  # Caro
            else:
                score -= 20  # Muy caro
        
        # Bonus por valor nutricional
        nutritional_info = product.get('nutritional_info', {})
        if nutritional_info:
            protein = nutritional_info.get('proteins', 0)
            fiber = nutritional_info.get('fiber', 0)
            
            # Alto en proteína o fibra = mejor valor
            if protein > 10 or fiber > 5:
                score += 10
        
        # Bonus por cantidad/tamaño
        quantity = product.get('quantity', 1.0)
        if quantity > 1.0:
            score += min(10, quantity * 2)  # Bonus por compra a granel
        
        return max(0, min(100, score))
    
    def calculate_environmental_score(self, product: Dict) -> tuple[float, float]:
        """
        Calcula puntuación ambiental basada en:
        - Huella de carbono
        - Origen y transporte
        - Packaging
        - Certificaciones orgánicas
        
        Returns:
            Tuple de (score 0-100, carbon_footprint en kg CO2)
        """
        score = 50.0
        
        # Determinar categoría para cálculo de carbono
        category = product.get('category', 'default').lower()
        carbon_factor = self.CARBON_FACTORS.get(category, self.CARBON_FACTORS['default'])
        
        # Calcular huella de carbono base
        weight = product.get('quantity', 1.0)
        if product.get('unit') == 'kg':
            weight_kg = weight
        elif product.get('unit') == 'l':
            weight_kg = weight * 1.0  # Aproximación
        else:
            weight_kg = weight * 0.5  # Aproximación para unidades
        
        carbon_footprint = carbon_factor * weight_kg
        
        # Agregar transporte
        origin = product.get('origin_country', 'unknown').lower()
        transport_distance = self._get_transport_distance(origin)
        transport_carbon = (transport_distance / 1000) * 0.1 * weight_kg  # 0.1 kg CO2 per ton-km
        carbon_footprint += transport_carbon
        
        # Penalizar por huella de carbono
        if carbon_footprint < 1.0:
            score += 30
        elif carbon_footprint < 3.0:
            score += 15
        elif carbon_footprint < 5.0:
            score += 5
        elif carbon_footprint < 10.0:
            score -= 10
        else:
            score -= 25
        
        # Bonus por certificaciones
        labels = product.get('labels', [])
        if 'organic' in [l.lower() for l in labels]:
            score += 15
            carbon_footprint *= 0.9  # Orgánico típicamente tiene menor huella
        
        if 'eco-friendly' in [l.lower() for l in labels]:
            score += 10
        
        # Bonus por origen local
        if origin in ['chile', 'local']:
            score += 20
            carbon_footprint *= 0.7
        
        # Penalizar packaging excesivo (heurística)
        if 'single-use' in product.get('description', '').lower():
            score -= 15
        
        return max(0, min(100, score)), round(carbon_footprint, 3)
    
    def calculate_social_score(self, product: Dict) -> float:
        """
        Calcula puntuación social basada en:
        - Comercio justo
        - Producción local
        - Certificaciones sociales
        - Marca responsable
        
        Returns:
            Score de 0-100
        """
        score = 50.0
        
        labels = [l.lower() for l in product.get('labels', [])]
        
        # Certificaciones sociales
        if 'fair-trade' in labels:
            score += 25
        
        if 'b-corp' in labels:
            score += 20
        
        # Producción local
        origin = product.get('origin_country', '').lower()
        if origin in ['chile', 'local']:
            score += 20
        elif origin in ['argentina', 'peru', 'brazil']:
            score += 10
        
        # Pequeños productores
        if 'small-producer' in labels or 'artesanal' in labels:
            score += 15
        
        # Cooperativas
        if 'cooperative' in labels or 'cooperativa' in labels:
            score += 15
        
        return max(0, min(100, score))
    
    def calculate_overall_score(self, product: Dict, 
                               category_avg_price: Optional[float] = None) -> Dict:
        """
        Calcula todas las puntuaciones de sostenibilidad.
        
        Returns:
            Dict con scores económico, ambiental, social, overall y huella de carbono
        """
        economic_score = self.calculate_economic_score(product, category_avg_price)
        environmental_score, carbon_footprint = self.calculate_environmental_score(product)
        social_score = self.calculate_social_score(product)
        
        # Puntuación general ponderada
        overall_score = (
            economic_score * self.weights['economic'] +
            environmental_score * self.weights['environmental'] +
            social_score * self.weights['social']
        )
        
        result = {
            "economic_score": round(economic_score, 2),
            "environmental_score": round(environmental_score, 2),
            "social_score": round(social_score, 2),
            "overall_score": round(overall_score, 2),
            "carbon_footprint": carbon_footprint
        }
        
        logger.info(f"Sustainability score for {product.get('name', 'unknown')}: {overall_score:.2f}")
        
        return result
    
    def _get_transport_distance(self, origin: str) -> float:
        """Estima distancia de transporte basada en origen"""
        origin = origin.lower()
        
        if 'chile' in origin or 'local' in origin:
            return self.TRANSPORT_DISTANCES['local']
        elif any(country in origin for country in ['argentina', 'peru', 'brazil', 'uruguay']):
            return self.TRANSPORT_DISTANCES['south_america']
        elif any(country in origin for country in ['usa', 'mexico', 'canada']):
            return self.TRANSPORT_DISTANCES['north_america']
        elif any(country in origin for country in ['spain', 'france', 'italy', 'germany']):
            return self.TRANSPORT_DISTANCES['europe']
        elif any(country in origin for country in ['china', 'japan', 'india', 'thailand']):
            return self.TRANSPORT_DISTANCES['asia']
        else:
            return self.TRANSPORT_DISTANCES['default']
    
    def compare_products(self, product1: Dict, product2: Dict) -> Dict:
        """
        Compara dos productos y retorna análisis detallado.
        
        Returns:
            Dict con comparación de scores y recomendación
        """
        score1 = self.calculate_overall_score(product1)
        score2 = self.calculate_overall_score(product2)
        
        better_product = 1 if score1['overall_score'] > score2['overall_score'] else 2
        
        return {
            "product1_scores": score1,
            "product2_scores": score2,
            "better_product": better_product,
            "score_difference": abs(score1['overall_score'] - score2['overall_score']),
            "carbon_difference": abs(score1['carbon_footprint'] - score2['carbon_footprint']),
            "recommendation": self._generate_recommendation(product1, product2, score1, score2)
        }
    
    def _generate_recommendation(self, p1: Dict, p2: Dict, s1: Dict, s2: Dict) -> str:
        """Genera recomendación textual basada en comparación"""
        if s1['overall_score'] > s2['overall_score']:
            better, worse = (p1, s1), (p2, s2)
        else:
            better, worse = (p2, s2), (p1, s1)
        
        diff = better[1]['overall_score'] - worse[1]['overall_score']
        
        if diff > 20:
            return f"{better[0]['name']} es significativamente mejor en sostenibilidad"
        elif diff > 10:
            return f"{better[0]['name']} es mejor opción considerando sostenibilidad"
        else:
            return f"Ambos productos son similares, considera precio y preferencias"
