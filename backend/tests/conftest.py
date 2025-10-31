"""
Configuración de fixtures para tests.
"""
import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.database import ProductDB, ShoppingListDB, StoreDB


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db():
    """Setup test database."""
    # Usar base de datos de test
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["liquiverde_test"]
    
    # Inicializar conexión
    ProductDB.db = db
    ShoppingListDB.db = db
    StoreDB.db = db
    
    yield db
    
    # Limpiar después de los tests
    await client.drop_database("liquiverde_test")
    client.close()


@pytest.fixture(autouse=True)
async def setup_test_data(test_db):
    """Setup test data before each test."""
    # Limpiar colecciones
    await test_db.products.delete_many({})
    await test_db.shopping_lists.delete_many({})
    await test_db.stores.delete_many({})
    
    # Insertar datos de prueba
    test_products = [
        {
            "id": "test_prod_1",
            "barcode": "1234567890123",
            "name": "Test Product 1",
            "price": 1000,
            "category": "vegetables",
            "sustainability_score": {
                "overall_score": 80,
                "economic_score": 75,
                "environmental_score": 85,
                "social_score": 80,
                "carbon_footprint": 2.0
            },
            "nutritional_info": {
                "proteins": 5,
                "carbohydrates": 20,
                "fats": 1,
                "fiber": 8
            },
            "labels": ["organic", "local"],
            "origin_country": "Chile"
        },
        {
            "id": "test_prod_2",
            "barcode": "1234567890124",
            "name": "Test Product 2",
            "price": 2000,
            "category": "vegetables",
            "sustainability_score": {
                "overall_score": 90,
                "economic_score": 85,
                "environmental_score": 95,
                "social_score": 90,
                "carbon_footprint": 1.5
            },
            "nutritional_info": {
                "proteins": 6,
                "carbohydrates": 22,
                "fats": 1.5,
                "fiber": 10
            },
            "labels": ["organic", "local", "fair-trade"],
            "origin_country": "Chile"
        },
        {
            "id": "test_prod_3",
            "barcode": "1234567890125",
            "name": "Test Product 3",
            "price": 1500,
            "category": "legumes",
            "sustainability_score": {
                "overall_score": 85,
                "economic_score": 80,
                "environmental_score": 90,
                "social_score": 85,
                "carbon_footprint": 0.9
            },
            "nutritional_info": {
                "proteins": 25,
                "carbohydrates": 60,
                "fats": 1,
                "fiber": 15
            },
            "labels": ["organic"],
            "origin_country": "Chile"
        }
    ]
    
    test_stores = [
        {
            "id": "test_store_1",
            "name": "Test Store 1",
            "location": {
                "type": "Point",
                "coordinates": [-70.6693, -33.4489],
                "latitude": -33.4489,
                "longitude": -70.6693,
                "address": "Test Address 1"
            }
        },
        {
            "id": "test_store_2",
            "name": "Test Store 2",
            "location": {
                "type": "Point",
                "coordinates": [-70.6506, -33.4372],
                "latitude": -33.4372,
                "longitude": -70.6506,
                "address": "Test Address 2"
            }
        }
    ]
    
    await test_db.products.insert_many(test_products)
    await test_db.stores.insert_many(test_stores)
    
    yield
    
    # Limpiar después de cada test
    await test_db.products.delete_many({})
    await test_db.shopping_lists.delete_many({})
    await test_db.stores.delete_many({})


@pytest.fixture
def sample_products():
    """Sample products for testing algorithms."""
    return [
        {
            'id': '1',
            'name': 'Producto A',
            'price': 1000,
            'sustainability_score': {'overall_score': 80, 'carbon_footprint': 2.0},
            'category': 'vegetables',
            'category_avg_price': 1200,
            'priority': 3,
            'nutritional_info': {'proteins': 5, 'fiber': 8}
        },
        {
            'id': '2',
            'name': 'Producto B',
            'price': 2000,
            'sustainability_score': {'overall_score': 90, 'carbon_footprint': 1.5},
            'category': 'vegetables',
            'category_avg_price': 2500,
            'priority': 5,
            'nutritional_info': {'proteins': 6, 'fiber': 10}
        },
        {
            'id': '3',
            'name': 'Producto C',
            'price': 3000,
            'sustainability_score': {'overall_score': 70, 'carbon_footprint': 3.0},
            'category': 'meat',
            'category_avg_price': 3200,
            'priority': 2,
            'nutritional_info': {'proteins': 20, 'fiber': 0}
        }
    ]
