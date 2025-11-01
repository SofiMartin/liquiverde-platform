"""
Algoritmo de Sustitución Inteligente de Productos
Encuentra alternativas mejores basadas en múltiples criterios.
"""
import logging
from typing import List, Dict, Optional, Tuple
from app.algorithms.sustainability_scoring import SustainabilityScorer

logger = logging.getLogger(__name__)

class ProductSubstitutionEngine:
    """
    Motor de sustitución inteligente que encuentra alternativas mejores
    basándose en sostenibilidad, precio y similitud de producto.
    """
    
    def __init__(self):
        self.scorer = SustainabilityScorer()
        
        self.weights = {
            "sustainability_improvement": 0.35,
            "price_savings": 0.30,
            "category_match": 0.20,
            "nutritional_similarity": 0.15
        }
    
    def find_substitutes(self, original_product: Dict, candidate_products: List[Dict],
                        max_price_increase: float = 0.1,
                        min_sustainability_improvement: float = 5.0) -> List[Dict]:
        """
        Encuentra productos sustitutos para un producto original.
        
        Args:
            original_product: Producto a sustituir
            candidate_products: Lista de productos candidatos
            max_price_increase: Máximo incremento de precio permitido (porcentaje)
            min_sustainability_improvement: Mínima mejora en sostenibilidad requerida
            
        Returns:
            Lista de sustitutos ordenados por score
        """
        if not candidate_products:
            return []
        
        original_score = self.scorer.calculate_overall_score(original_product)
        original_price = original_product.get('price', 0)
        
        substitutes = []
        
        for candidate in candidate_products:
            if candidate.get('id') == original_product.get('id'):
                continue
            
            candidate_price = candidate.get('price', 0)
            price_diff_percent = ((candidate_price - original_price) / original_price * 100) if original_price > 0 else 0
            
            if price_diff_percent > max_price_increase:
                continue
            
            candidate_score = self.scorer.calculate_overall_score(candidate)
            
            sustainability_improvement = candidate_score['overall_score'] - original_score['overall_score']
            
            if sustainability_improvement < min_sustainability_improvement:
                continue
            
            substitution_score = self._calculate_substitution_score(
                original_product, candidate,
                original_score, candidate_score
            )
            
            savings = original_price - candidate_price
            savings_percent = (savings / original_price * 100) if original_price > 0 else 0
            
            substitutes.append({
                "product": candidate,
                "substitution_score": substitution_score,
                "sustainability_improvement": sustainability_improvement,
                "savings": savings,
                "savings_percent": savings_percent,
                "carbon_reduction": original_score['carbon_footprint'] - candidate_score['carbon_footprint'],
                "reason": self._generate_substitution_reason(
                    original_product, candidate,
                    sustainability_improvement, savings_percent
                ),
                "original_score": original_score,
                "substitute_score": candidate_score
            })
        
        substitutes.sort(key=lambda x: x['substitution_score'], reverse=True)
        
        logger.info(f"Found {len(substitutes)} substitutes for {original_product.get('name', 'unknown')}")
        
        return substitutes
    
    def _calculate_substitution_score(self, original: Dict, candidate: Dict,
                                     original_score: Dict, candidate_score: Dict) -> float:
        """
        Calcula score de sustitución basado en múltiples factores.
        
        Returns:
            Score de 0-100
        """
        score = 0.0
        
        sustainability_improvement = candidate_score['overall_score'] - original_score['overall_score']
        sustainability_component = min(100, max(0, sustainability_improvement)) * self.weights['sustainability_improvement']
        score += sustainability_component
        
        original_price = original.get('price', 0)
        candidate_price = candidate.get('price', 0)
        
        if original_price > 0:
            savings_percent = ((original_price - candidate_price) / original_price) * 100
            price_component = min(100, max(0, savings_percent * 5)) * self.weights['price_savings']
            score += price_component
        
        category_match = self._calculate_category_similarity(original, candidate)
        score += category_match * self.weights['category_match']
        
        nutritional_similarity = self._calculate_nutritional_similarity(original, candidate)
        score += nutritional_similarity * self.weights['nutritional_similarity']
        
        return round(score, 2)
    
    def _calculate_category_similarity(self, product1: Dict, product2: Dict) -> float:
        """
        Calcula similitud de categoría entre dos productos.
        
        Returns:
            Score de 0-100
        """
        cat1 = product1.get('category', '').lower()
        cat2 = product2.get('category', '').lower()
        
        if cat1 == cat2:
            return 100.0
        
        related_categories = {
            'meat': ['poultry', 'fish'],
            'dairy': ['cheese', 'yogurt', 'milk'],
            'vegetables': ['fruits', 'legumes'],
            'snacks': ['sweets', 'cookies'],
        }
        
        for main_cat, related in related_categories.items():
            if cat1 == main_cat and cat2 in related:
                return 70.0
            if cat2 == main_cat and cat1 in related:
                return 70.0
        
        return 30.0
    
    def _calculate_nutritional_similarity(self, product1: Dict, product2: Dict) -> float:
        """
        Calcula similitud nutricional entre dos productos.
        
        Returns:
            Score de 0-100
        """
        nutr1 = product1.get('nutritional_info', {})
        nutr2 = product2.get('nutritional_info', {})
        
        if not nutr1 or not nutr2:
            return 50.0
        
        metrics = ['energy_kcal', 'proteins', 'carbohydrates', 'fats']
        similarities = []
        
        for metric in metrics:
            val1 = nutr1.get(metric, 0)
            val2 = nutr2.get(metric, 0)
            
            if val1 == 0 and val2 == 0:
                similarities.append(100)
            elif val1 == 0 or val2 == 0:
                similarities.append(0)
            else:
                diff = abs(val1 - val2) / max(val1, val2)
                similarity = max(0, (1 - diff) * 100)
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 50.0
    
    def _generate_substitution_reason(self, original: Dict, substitute: Dict,
                                     sustainability_improvement: float,
                                     savings_percent: float) -> str:
        """
        Genera razón textual para la sustitución.
        """
        reasons = []
        
        if sustainability_improvement > 20:
            reasons.append(f"Mejora significativa en sostenibilidad (+{sustainability_improvement:.1f} puntos)")
        elif sustainability_improvement > 10:
            reasons.append(f"Mayor sostenibilidad (+{sustainability_improvement:.1f} puntos)")
        
        if savings_percent > 15:
            reasons.append(f"Ahorro considerable ({savings_percent:.1f}%)")
        elif savings_percent > 5:
            reasons.append(f"Ahorro de {savings_percent:.1f}%")
        elif savings_percent < -5:
            reasons.append(f"Inversión en sostenibilidad (+{abs(savings_percent):.1f}%)")
        
        substitute_labels = [l.lower() for l in substitute.get('labels', [])]
        if 'organic' in substitute_labels:
            reasons.append("Producto orgánico")
        if 'fair-trade' in substitute_labels:
            reasons.append("Comercio justo")
        
        if substitute.get('origin_country', '').lower() in ['chile', 'local']:
            reasons.append("Producción local")
        
        if not reasons:
            reasons.append("Alternativa más sostenible")
        
        return " | ".join(reasons)
    
    def batch_substitute(self, products: List[Dict], candidate_pool: List[Dict],
                        max_substitutions: Optional[int] = None) -> Dict:
        """
        Realiza sustituciones en lote para una lista de productos.
        
        Args:
            products: Lista de productos a analizar
            candidate_pool: Pool de productos candidatos
            max_substitutions: Máximo número de sustituciones a realizar
            
        Returns:
            Dict con productos originales, sustitutos y estadísticas
        """
        substitutions = []
        total_savings = 0
        total_carbon_reduction = 0
        
        for product in products:
            substitutes = self.find_substitutes(product, candidate_pool)
            
            if substitutes:
                best_substitute = substitutes[0]
                
                substitutions.append({
                    "original": product,
                    "substitute": best_substitute['product'],
                    "reason": best_substitute['reason'],
                    "savings": best_substitute['savings'],
                    "sustainability_improvement": best_substitute['sustainability_improvement'],
                    "carbon_reduction": best_substitute['carbon_reduction']
                })
                
                total_savings += best_substitute['savings']
                total_carbon_reduction += best_substitute['carbon_reduction']
        
        if max_substitutions and len(substitutions) > max_substitutions:
            substitutions.sort(
                key=lambda x: x['sustainability_improvement'] + (x['savings'] * 10),
                reverse=True
            )
            substitutions = substitutions[:max_substitutions]
        
        return {
            "substitutions": substitutions,
            "total_substitutions": len(substitutions),
            "total_savings": round(total_savings, 2),
            "total_carbon_reduction": round(total_carbon_reduction, 3),
            "average_sustainability_improvement": round(
                sum(s['sustainability_improvement'] for s in substitutions) / len(substitutions), 2
            ) if substitutions else 0
        }
