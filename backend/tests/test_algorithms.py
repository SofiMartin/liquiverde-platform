"""
Tests para los algoritmos de optimización.
"""
import pytest
from app.algorithms.knapsack import MultiObjectiveKnapsack
from app.algorithms.sustainability_scoring import SustainabilityScorer
from app.algorithms.product_substitution import ProductSubstitutionEngine
from app.algorithms.route_optimization import RouteOptimizer


class TestMultiObjectiveKnapsack:
    """Tests para el algoritmo de mochila multi-objetivo."""
    
    def test_basic_optimization(self):
        """Test de optimización básica con presupuesto."""
        products = [
            {
                'id': '1',
                'name': 'Producto A',
                'price': 1000,
                'sustainability_score': {'overall_score': 80},
                'category_avg_price': 1200,
                'priority': 3
            },
            {
                'id': '2',
                'name': 'Producto B',
                'price': 2000,
                'sustainability_score': {'overall_score': 90},
                'category_avg_price': 2500,
                'priority': 5
            },
            {
                'id': '3',
                'name': 'Producto C',
                'price': 3000,
                'sustainability_score': {'overall_score': 70},
                'category_avg_price': 3200,
                'priority': 2
            }
        ]
        quantities = [1, 1, 1]
        
        knapsack = MultiObjectiveKnapsack(max_budget=4000)
        result = knapsack.optimize(products, quantities)
        
        assert result is not None
        assert 'selected_products' in result
        assert 'total_cost' in result
        assert result['total_cost'] <= 4000
        assert len(result['selected_products']) > 0
    
    def test_essential_products(self):
        """Test que productos esenciales siempre se incluyan."""
        products = [
            {
                'id': '1',
                'name': 'Esencial',
                'price': 1000,
                'sustainability_score': {'overall_score': 80},
                'category_avg_price': 1200,
                'priority': 5
            },
            {
                'id': '2',
                'name': 'Opcional',
                'price': 500,
                'sustainability_score': {'overall_score': 70},
                'category_avg_price': 600,
                'priority': 2
            }
        ]
        quantities = [1, 1]
        essential_indices = [0]
        
        knapsack = MultiObjectiveKnapsack(max_budget=1200)
        result = knapsack.optimize_with_essentials(products, quantities, essential_indices)
        
        assert result is not None
        # El producto esencial debe estar incluido
        selected_ids = [p['id'] for p in result['selected_products']]
        assert '1' in selected_ids
    
    def test_budget_constraint(self):
        """Test que respeta el límite de presupuesto."""
        products = [
            {
                'id': str(i),
                'name': f'Producto {i}',
                'price': 1000,
                'sustainability_score': {'overall_score': 80},
                'category_avg_price': 1200,
                'priority': 3
            }
            for i in range(10)
        ]
        quantities = [1] * 10
        
        knapsack = MultiObjectiveKnapsack(max_budget=5000)
        result = knapsack.optimize(products, quantities)
        
        assert result['total_cost'] <= 5000


class TestSustainabilityScorer:
    """Tests para el sistema de scoring de sostenibilidad."""
    
    def test_economic_score(self):
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
        
        assert 0 <= score <= 100
        assert score > 50  # Debería ser bueno porque está bajo el promedio
    
    def test_environmental_score(self):
        """Test de cálculo de score ambiental."""
        scorer = SustainabilityScorer()
        
        product = {
            'category': 'vegetables',
            'origin_country': 'Chile',
            'labels': ['organic', 'local']
        }
        
        score = scorer.calculate_environmental_score(product)
        
        assert 0 <= score <= 100
        assert score > 70  # Vegetales orgánicos locales deberían tener buen score
    
    def test_social_score(self):
        """Test de cálculo de score social."""
        scorer = SustainabilityScorer()
        
        product = {
            'labels': ['fair-trade', 'local'],
            'origin_country': 'Chile'
        }
        
        score = scorer.calculate_social_score(product)
        
        assert 0 <= score <= 100
        assert score > 60  # Fair trade y local deberían tener buen score
    
    def test_overall_score(self):
        """Test de cálculo de score general."""
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
        
        assert 'economic_score' in result
        assert 'environmental_score' in result
        assert 'social_score' in result
        assert 'overall_score' in result
        assert 'carbon_footprint' in result
        assert 0 <= result['overall_score'] <= 100
    
    def test_carbon_footprint_calculation(self):
        """Test de cálculo de huella de carbono."""
        scorer = SustainabilityScorer()
        
        # Carne debería tener alta huella
        meat_product = {'category': 'meat', 'origin_country': 'Chile'}
        meat_footprint = scorer.estimate_carbon_footprint(meat_product)
        
        # Vegetales deberían tener baja huella
        veg_product = {'category': 'vegetables', 'origin_country': 'Chile'}
        veg_footprint = scorer.estimate_carbon_footprint(veg_product)
        
        assert meat_footprint > veg_footprint
        assert veg_footprint < 5  # Vegetales deberían ser < 5 kg CO2


class TestProductSubstitutionEngine:
    """Tests para el motor de sustitución de productos."""
    
    def test_find_substitutes(self):
        """Test de búsqueda de sustitutos."""
        engine = ProductSubstitutionEngine()
        
        original = {
            'id': '1',
            'name': 'Producto Original',
            'price': 2000,
            'category': 'vegetables',
            'sustainability_score': {'overall_score': 60, 'carbon_footprint': 3.0},
            'nutritional_info': {'proteins': 5, 'carbohydrates': 20}
        }
        
        candidates = [
            {
                'id': '2',
                'name': 'Alternativa 1',
                'price': 1800,
                'category': 'vegetables',
                'sustainability_score': {'overall_score': 80, 'carbon_footprint': 2.0},
                'nutritional_info': {'proteins': 6, 'carbohydrates': 22}
            },
            {
                'id': '3',
                'name': 'Alternativa 2',
                'price': 2500,
                'category': 'vegetables',
                'sustainability_score': {'overall_score': 85, 'carbon_footprint': 1.5},
                'nutritional_info': {'proteins': 5, 'carbohydrates': 19}
            }
        ]
        
        substitutes = engine.find_substitutes(
            original,
            candidates,
            max_price_increase=0.2,
            min_sustainability_improvement=10
        )
        
        assert len(substitutes) > 0
        # Todos los sustitutos deberían tener mejor sostenibilidad
        for sub in substitutes:
            assert sub['sustainability_improvement'] >= 10
    
    def test_substitution_score(self):
        """Test de cálculo de score de sustitución."""
        engine = ProductSubstitutionEngine()
        
        original = {
            'price': 1000,
            'category': 'vegetables',
            'sustainability_score': {'overall_score': 60},
            'nutritional_info': {'proteins': 5, 'fiber': 3}
        }
        
        substitute = {
            'price': 900,
            'category': 'vegetables',
            'sustainability_score': {'overall_score': 80},
            'nutritional_info': {'proteins': 6, 'fiber': 4}
        }
        
        score = engine.calculate_substitution_score(original, substitute)
        
        assert 0 <= score <= 100
        assert score > 50  # Debería ser bueno: más sostenible y más barato


class TestRouteOptimizer:
    """Tests para el optimizador de rutas."""
    
    def test_distance_calculation(self):
        """Test de cálculo de distancia Haversine."""
        optimizer = RouteOptimizer((-33.4489, -70.6693))  # Santiago
        
        # Distancia a Valparaíso (aprox 120 km)
        valpo = (-33.0472, -71.6127)
        distance = optimizer.calculate_distance((-33.4489, -70.6693), valpo)
        
        assert 100 < distance < 150  # Debería estar en este rango
    
    def test_nearest_neighbor(self):
        """Test del algoritmo Nearest Neighbor."""
        stores = [
            {'id': '1', 'location': {'latitude': -33.4489, 'longitude': -70.6693}},
            {'id': '2', 'location': {'latitude': -33.4372, 'longitude': -70.6506}},
            {'id': '3', 'location': {'latitude': -33.4569, 'longitude': -70.6483}}
        ]
        
        optimizer = RouteOptimizer((-33.4489, -70.6693))
        route = optimizer.nearest_neighbor(stores)
        
        assert len(route) == len(stores)
        assert 'order' in route
        assert 'total_distance' in route
        assert route['total_distance'] > 0
    
    def test_optimize_route(self):
        """Test de optimización completa de ruta."""
        stores = [
            {'id': '1', 'name': 'Store 1', 'location': {'latitude': -33.4489, 'longitude': -70.6693}},
            {'id': '2', 'name': 'Store 2', 'location': {'latitude': -33.4372, 'longitude': -70.6506}},
            {'id': '3', 'name': 'Store 3', 'location': {'latitude': -33.4569, 'longitude': -70.6483}}
        ]
        
        optimizer = RouteOptimizer((-33.4489, -70.6693))
        result = optimizer.optimize_route(stores)
        
        assert 'optimized_route' in result
        assert 'total_distance' in result
        assert 'estimated_time' in result
        assert len(result['optimized_route']) == len(stores)
        
        # Verificar que todos los stores están en la ruta
        route_ids = [s['id'] for s in result['optimized_route']]
        for store in stores:
            assert store['id'] in route_ids


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
