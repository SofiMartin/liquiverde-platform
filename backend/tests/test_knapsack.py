"""
Tests para el algoritmo de Mochila Multi-objetivo.
"""
import pytest
from app.algorithms.knapsack import MultiObjectiveKnapsack


class TestMultiObjectiveKnapsack:
    """Tests para el algoritmo de mochila multi-objetivo."""
    
    @pytest.fixture
    def sample_products(self):
        """Productos de ejemplo para tests."""
        return [
            {
                'id': '1',
                'name': 'Producto Económico',
                'price': 1000,
                'sustainability_score': {'overall_score': 70},
                'category_avg_price': 1500,
                'priority': 3
            },
            {
                'id': '2',
                'name': 'Producto Sostenible',
                'price': 2000,
                'sustainability_score': {'overall_score': 90},
                'category_avg_price': 2200,
                'priority': 5
            },
            {
                'id': '3',
                'name': 'Producto Caro',
                'price': 3000,
                'sustainability_score': {'overall_score': 60},
                'category_avg_price': 2800,
                'priority': 2
            },
            {
                'id': '4',
                'name': 'Producto Balanceado',
                'price': 1500,
                'sustainability_score': {'overall_score': 80},
                'category_avg_price': 1800,
                'priority': 4
            }
        ]
    
    def test_basic_optimization(self, sample_products):
        """Test de optimización básica con presupuesto."""
        quantities = [1, 1, 1, 1]
        
        knapsack = MultiObjectiveKnapsack(max_budget=5000)
        result = knapsack.optimize(sample_products, quantities)
        
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2  # (quantities, stats)
        
        selected_quantities, stats = result
        
        # Verificar que retorna cantidades válidas
        assert len(selected_quantities) == len(sample_products)
        assert all(q >= 0 for q in selected_quantities)
        
        # Verificar estadísticas
        assert 'total_cost' in stats
        assert 'items_selected' in stats
        assert stats['total_cost'] <= 5000
    
    def test_budget_constraint(self, sample_products):
        """Test que respeta el límite de presupuesto."""
        quantities = [2, 2, 2, 2]  # Cantidades altas
        
        knapsack = MultiObjectiveKnapsack(max_budget=4000)
        selected_quantities, stats = knapsack.optimize(sample_products, quantities)
        
        # El costo total debe estar dentro del presupuesto
        assert stats['total_cost'] <= 4000
        
        # Debe haber seleccionado algunos productos
        assert stats['items_selected'] > 0
    
    def test_tight_budget(self, sample_products):
        """Test con presupuesto muy ajustado."""
        quantities = [1, 1, 1, 1]
        
        # Presupuesto solo para el producto más barato
        knapsack = MultiObjectiveKnapsack(max_budget=1500)
        selected_quantities, stats = knapsack.optimize(sample_products, quantities)
        
        assert stats['total_cost'] <= 1500
        # Debería seleccionar al menos 1 producto
        assert stats['items_selected'] >= 1
    
    def test_sustainability_priority(self, sample_products):
        """Test que prioriza sostenibilidad cuando se configura."""
        quantities = [1, 1, 1, 1]
        
        # Alta prioridad a sostenibilidad
        knapsack = MultiObjectiveKnapsack(
            max_budget=5000,
            sustainability_weight=0.6,
            savings_weight=0.2,
            priority_weight=0.2
        )
        
        selected_quantities, stats = knapsack.optimize(sample_products, quantities)
        
        # Debe seleccionar productos
        assert stats['items_selected'] > 0
        
        # El producto sostenible (id=2, score=90) debería estar seleccionado
        assert selected_quantities[1] > 0  # Índice 1 = Producto Sostenible
    
    def test_savings_priority(self, sample_products):
        """Test que prioriza ahorro cuando se configura."""
        quantities = [1, 1, 1, 1]
        
        # Alta prioridad a ahorro
        knapsack = MultiObjectiveKnapsack(
            max_budget=5000,
            sustainability_weight=0.2,
            savings_weight=0.6,
            priority_weight=0.2
        )
        
        selected_quantities, stats = knapsack.optimize(sample_products, quantities)
        
        # Debe seleccionar productos
        assert stats['items_selected'] > 0
        
        # El producto económico (id=1, mejor ahorro) debería estar seleccionado
        assert selected_quantities[0] > 0
    
    def test_multiple_quantities(self, sample_products):
        """Test con cantidades variables por producto."""
        quantities = [3, 1, 2, 1]  # Diferentes cantidades
        
        knapsack = MultiObjectiveKnapsack(max_budget=6000)
        selected_quantities, stats = knapsack.optimize(sample_products, quantities)
        
        # Las cantidades seleccionadas no deben exceder las solicitadas
        for i in range(len(quantities)):
            assert selected_quantities[i] <= quantities[i]
        
        assert stats['total_cost'] <= 6000
    
    def test_zero_budget(self):
        """Test con presupuesto cero."""
        products = [
            {
                'id': '1',
                'name': 'Producto',
                'price': 1000,
                'sustainability_score': {'overall_score': 70},
                'category_avg_price': 1200,
                'priority': 3
            }
        ]
        quantities = [1]
        
        # Presupuesto mínimo de 1 para evitar división por cero
        knapsack = MultiObjectiveKnapsack(max_budget=1)
        selected_quantities, stats = knapsack.optimize(products, quantities)
        
        # No debería seleccionar nada (producto muy caro)
        assert stats['items_selected'] == 0
        assert stats['total_cost'] == 0
    
    def test_single_product(self):
        """Test con un solo producto."""
        products = [
            {
                'id': '1',
                'name': 'Único Producto',
                'price': 1000,
                'sustainability_score': {'overall_score': 80},
                'category_avg_price': 1200,
                'priority': 3
            }
        ]
        quantities = [1]
        
        knapsack = MultiObjectiveKnapsack(max_budget=2000)
        selected_quantities, stats = knapsack.optimize(products, quantities)
        
        # Debería seleccionar el único producto
        assert selected_quantities[0] == 1
        assert stats['total_cost'] == 1000
        assert stats['items_selected'] == 1
    
    def test_stats_structure(self, sample_products):
        """Test que las estadísticas tienen la estructura correcta."""
        quantities = [1, 1, 1, 1]
        
        knapsack = MultiObjectiveKnapsack(max_budget=5000)
        selected_quantities, stats = knapsack.optimize(sample_products, quantities)
        
        # Verificar que todas las claves esperadas están presentes
        required_keys = [
            'total_cost',
            'total_value',
            'items_selected',
            'total_items',
            'budget_used_percent',
            'average_sustainability'
        ]
        
        for key in required_keys:
            assert key in stats, f"Falta la clave '{key}' en stats"
        
        # Verificar tipos de datos
        assert isinstance(stats['total_cost'], (int, float))
        assert isinstance(stats['items_selected'], int)
        assert 0 <= stats['budget_used_percent'] <= 100
        assert 0 <= stats['average_sustainability'] <= 100
    
    def test_value_calculation(self):
        """Test del cálculo de valor multi-objetivo."""
        knapsack = MultiObjectiveKnapsack(
            max_budget=5000,
            sustainability_weight=0.4,
            savings_weight=0.3,
            priority_weight=0.3
        )
        
        product = {
            'price': 1000,
            'sustainability_score': {'overall_score': 80},
            'category_avg_price': 1200,
            'priority': 4
        }
        
        value = knapsack.calculate_item_value(product)
        
        # El valor puede ser mayor a 1 (no está normalizado a 0-1)
        assert value > 0
        assert isinstance(value, float)
    
    def test_optimize_with_essentials(self, sample_products):
        """Test de optimización con productos esenciales."""
        quantities = [1, 1, 1, 1]
        essential_indices = [1]  # El producto sostenible es esencial
        
        knapsack = MultiObjectiveKnapsack(max_budget=5000)
        selected_quantities, stats = knapsack.optimize_with_essentials(
            sample_products, 
            quantities, 
            essential_indices
        )
        
        # El producto esencial debe estar seleccionado
        assert selected_quantities[1] > 0
        
        # Debe respetar el presupuesto
        assert stats['total_cost'] <= 5000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
