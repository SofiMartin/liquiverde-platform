"""
Tests simplificados para los algoritmos (sin dependencias de BD).
"""
import pytest
from app.algorithms.sustainability_scoring import SustainabilityScorer


class TestSustainabilityScorer:
    """Tests para el sistema de scoring de sostenibilidad."""
    
    def test_economic_score_calculation(self):
        """Test de cálculo de score económico."""
        scorer = SustainabilityScorer()
        
        product = {
            'price': 1000,
            'nutritional_info': {
                'proteins': 20,
                'fiber': 5
            }
        }
        category_avg = 1500
        
        score = scorer.calculate_economic_score(product, category_avg)
        
        assert isinstance(score, (int, float))
        assert 0 <= score <= 100
        # Producto más barato que el promedio debería tener buen score
        assert score > 50
    
    def test_environmental_score_organic_local(self):
        """Test de score ambiental para productos orgánicos locales."""
        scorer = SustainabilityScorer()
        
        product = {
            'category': 'vegetables',
            'origin_country': 'Chile',
            'labels': ['organic', 'local']
        }
        
        result = scorer.calculate_environmental_score(product)
        
        # El método retorna una tupla (score, carbon_footprint)
        if isinstance(result, tuple):
            score = result[0]
        else:
            score = result
            
        assert isinstance(score, (int, float))
        assert 0 <= score <= 100
        # Vegetales orgánicos locales deberían tener alto score
        assert score >= 70
    
    def test_social_score_fair_trade(self):
        """Test de score social para productos fair trade."""
        scorer = SustainabilityScorer()
        
        product = {
            'labels': ['fair-trade', 'local'],
            'origin_country': 'Chile'
        }
        
        score = scorer.calculate_social_score(product)
        
        assert isinstance(score, (int, float))
        assert 0 <= score <= 100
        # Fair trade y local deberían tener buen score
        assert score >= 60
    
    def test_overall_score_structure(self):
        """Test de estructura del score general."""
        scorer = SustainabilityScorer()
        
        product = {
            'price': 1000,
            'category': 'vegetables',
            'origin_country': 'Chile',
            'labels': ['organic', 'local'],
            'nutritional_info': {
                'proteins': 5,
                'fiber': 8
            }
        }
        category_avg = 1500
        
        result = scorer.calculate_overall_score(product, category_avg)
        
        # Verificar estructura
        assert isinstance(result, dict)
        assert 'economic_score' in result
        assert 'environmental_score' in result
        assert 'social_score' in result
        assert 'overall_score' in result
        assert 'carbon_footprint' in result
        
        # Verificar rangos
        assert 0 <= result['overall_score'] <= 100
        assert result['carbon_footprint'] >= 0
    
    def test_carbon_footprint_by_category(self):
        """Test de huella de carbono por categoría."""
        scorer = SustainabilityScorer()
        
        # Carne debería tener alta huella
        meat_product = {'category': 'meat', 'origin_country': 'Chile'}
        meat_result = scorer.calculate_environmental_score(meat_product)
        meat_score = meat_result[0] if isinstance(meat_result, tuple) else meat_result
        
        # Vegetales deberían tener baja huella
        veg_product = {'category': 'vegetables', 'origin_country': 'Chile'}
        veg_result = scorer.calculate_environmental_score(veg_product)
        veg_score = veg_result[0] if isinstance(veg_result, tuple) else veg_result
        
        # Vegetales deberían tener mejor score (menor huella)
        assert veg_score > meat_score
    
    def test_comparison_better_product(self):
        """Test de comparación entre productos."""
        scorer = SustainabilityScorer()
        
        product1 = {
            'name': 'Producto Normal',
            'price': 2000,
            'category': 'vegetables',
            'sustainability_score': {'overall_score': 60, 'carbon_footprint': 3.0}
        }
        
        product2 = {
            'name': 'Producto Sostenible',
            'price': 1800,
            'category': 'vegetables',
            'sustainability_score': {'overall_score': 85, 'carbon_footprint': 1.5}
        }
        
        comparison = scorer.compare_products(product1, product2)
        
        assert isinstance(comparison, dict)
        assert 'better_product' in comparison
        assert 'recommendation' in comparison
        # El producto 2 debería ser mejor (puede ser 2 o 'product2')
        assert comparison['better_product'] in [2, 'product2']


class TestAlgorithmIntegration:
    """Tests de integración básicos."""
    
    def test_scorer_initialization(self):
        """Test que el scorer se inicializa correctamente."""
        scorer = SustainabilityScorer()
        assert scorer is not None
    
    def test_score_ranges(self):
        """Test que todos los scores están en rango válido."""
        scorer = SustainabilityScorer()
        
        test_product = {
            'price': 1500,
            'category': 'legumes',
            'origin_country': 'Chile',
            'labels': ['organic'],
            'nutritional_info': {'proteins': 25, 'fiber': 15}
        }
        
        result = scorer.calculate_overall_score(test_product, 2000)
        
        # Todos los scores deben estar entre 0 y 100
        assert 0 <= result['economic_score'] <= 100
        assert 0 <= result['environmental_score'] <= 100
        assert 0 <= result['social_score'] <= 100
        assert 0 <= result['overall_score'] <= 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
