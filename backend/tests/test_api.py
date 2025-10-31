"""
Tests para los endpoints de la API.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestProductsAPI:
    """Tests para endpoints de productos."""
    
    def test_list_products(self):
        """Test de listado de productos."""
        response = client.get("/api/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_products(self):
        """Test de búsqueda de productos."""
        response = client.get("/api/products/search?query=orgánico")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_scan_product_existing(self):
        """Test de escaneo de producto existente."""
        # Primero obtenemos un producto para tener un barcode válido
        products_response = client.get("/api/products/")
        if products_response.status_code == 200 and len(products_response.json()) > 0:
            barcode = products_response.json()[0].get('barcode')
            if barcode:
                response = client.post(f"/api/products/scan/{barcode}")
                assert response.status_code == 200
                data = response.json()
                assert 'id' in data
                assert 'name' in data
                assert 'sustainability_score' in data
    
    def test_scan_product_not_found(self):
        """Test de escaneo de producto no existente."""
        response = client.post("/api/products/scan/9999999999999")
        
        # Puede ser 404 o 200 si lo busca en API externa
        assert response.status_code in [200, 404]
    
    def test_compare_products(self):
        """Test de comparación de productos."""
        # Obtener dos productos para comparar
        products_response = client.get("/api/products/?limit=2")
        
        if products_response.status_code == 200:
            products = products_response.json()
            if len(products) >= 2:
                product1_id = products[0]['id']
                product2_id = products[1]['id']
                
                response = client.post(
                    f"/api/products/compare?product_id_1={product1_id}&product_id_2={product2_id}"
                )
                
                assert response.status_code == 200
                data = response.json()
                assert 'product1' in data
                assert 'product2' in data
                assert 'comparison' in data


class TestShoppingListsAPI:
    """Tests para endpoints de listas de compras."""
    
    def test_create_shopping_list(self):
        """Test de creación de lista de compras."""
        # Primero obtenemos un producto
        products_response = client.get("/api/products/?limit=1")
        
        if products_response.status_code == 200 and len(products_response.json()) > 0:
            product = products_response.json()[0]
            
            shopping_list = {
                "name": "Test List",
                "items": [
                    {
                        "product_id": product['id'],
                        "quantity": 2,
                        "priority": 3
                    }
                ]
            }
            
            response = client.post("/api/shopping-lists/", json=shopping_list)
            
            assert response.status_code == 200
            data = response.json()
            assert 'id' in data
            assert data['name'] == "Test List"
    
    def test_quick_optimize(self):
        """Test de optimización rápida."""
        # Obtener productos para optimizar
        products_response = client.get("/api/products/?limit=3")
        
        if products_response.status_code == 200 and len(products_response.json()) > 0:
            products = products_response.json()
            product_ids = [p['id'] for p in products[:3]]
            
            optimization_request = {
                "product_ids": product_ids,
                "max_budget": 10000,
                "prioritize_sustainability": True
            }
            
            response = client.post("/api/shopping-lists/quick-optimize", json=optimization_request)
            
            assert response.status_code == 200
            data = response.json()
            assert 'selected_products' in data
            assert 'total_cost' in data
            assert 'total_sustainability' in data


class TestAnalysisAPI:
    """Tests para endpoints de análisis."""
    
    def test_dashboard(self):
        """Test del endpoint de dashboard."""
        response = client.get("/api/analysis/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        assert 'total_products' in data
        assert 'average_sustainability' in data
        assert isinstance(data['total_products'], int)
    
    def test_impact_calculation(self):
        """Test de cálculo de impacto."""
        # Obtener productos para calcular impacto
        products_response = client.get("/api/products/?limit=2")
        
        if products_response.status_code == 200 and len(products_response.json()) > 0:
            products = products_response.json()
            product_ids = [p['id'] for p in products[:2]]
            
            response = client.get(
                f"/api/analysis/impact?product_ids={','.join(product_ids)}"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert 'total_carbon_footprint' in data
            assert 'equivalences' in data


class TestStoresAPI:
    """Tests para endpoints de tiendas."""
    
    def test_list_stores(self):
        """Test de listado de tiendas."""
        response = client.get("/api/stores/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_nearby_stores(self):
        """Test de búsqueda de tiendas cercanas."""
        # Santiago, Chile
        response = client.get(
            "/api/stores/nearby?latitude=-33.4489&longitude=-70.6693&radius_km=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Verificar que tienen distancia calculada
        if len(data) > 0:
            assert 'distance_km' in data[0]
    
    def test_map_data(self):
        """Test de datos para mapa."""
        response = client.get("/api/stores/map-data")
        
        assert response.status_code == 200
        data = response.json()
        assert 'stores' in data
        assert 'center' in data
        assert isinstance(data['stores'], list)


class TestHealthCheck:
    """Tests para endpoints de salud."""
    
    def test_root_endpoint(self):
        """Test del endpoint raíz."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'version' in data
    
    def test_health_endpoint(self):
        """Test del endpoint de health check."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
