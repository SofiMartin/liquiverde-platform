"""
Script para poblar la base de datos MongoDB con datos de ejemplo.
"""
import asyncio
import logging
from app.services.database import init_db, ProductDB, StoreDB
from app.algorithms.sustainability_scoring import SustainabilityScorer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scorer = SustainabilityScorer()

# Dataset de productos
SAMPLE_PRODUCTS = [
    {
        "barcode": "7804123456789",
        "name": "Pechuga de Pollo Orgánica",
        "brand": "Agrosuper",
        "category": "poultry",
        "price": 4500,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Jumbo",
        "description": "Pechuga de pollo orgánico, sin antibióticos",
        "nutritional_info": {
            "energy_kcal": 165,
            "proteins": 31,
            "carbohydrates": 0,
            "fats": 3.6,
            "fiber": 0,
            "sodium": 0.074
        },
        "labels": ["organic", "antibiotic-free"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456790",
        "name": "Carne Molida Premium",
        "brand": "PF",
        "category": "meat",
        "price": 6800,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Jumbo",
        "description": "Carne molida de res, 90% magra",
        "nutritional_info": {
            "energy_kcal": 250,
            "proteins": 26,
            "carbohydrates": 0,
            "fats": 17,
            "fiber": 0,
            "sodium": 0.075
        },
        "labels": [],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456791",
        "name": "Leche Descremada Orgánica",
        "brand": "Colun",
        "category": "dairy",
        "price": 1200,
        "unit": "l",
        "quantity": 1.0,
        "store": "Lider",
        "description": "Leche descremada orgánica certificada",
        "nutritional_info": {
            "energy_kcal": 35,
            "proteins": 3.4,
            "carbohydrates": 5,
            "fats": 0.1,
            "fiber": 0,
            "sodium": 0.044
        },
        "labels": ["organic"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456792",
        "name": "Yogurt Natural",
        "brand": "Nestlé",
        "category": "dairy",
        "price": 890,
        "unit": "unit",
        "quantity": 1.0,
        "store": "Lider",
        "description": "Yogurt natural sin azúcar añadida",
        "nutritional_info": {
            "energy_kcal": 59,
            "proteins": 3.5,
            "carbohydrates": 4.7,
            "fats": 3.3,
            "fiber": 0,
            "sodium": 0.046
        },
        "labels": [],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456793",
        "name": "Manzanas Orgánicas",
        "brand": "Frutas del Huerto",
        "category": "fruits",
        "price": 2500,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Santa Isabel",
        "description": "Manzanas rojas orgánicas de temporada",
        "nutritional_info": {
            "energy_kcal": 52,
            "proteins": 0.3,
            "carbohydrates": 14,
            "fats": 0.2,
            "fiber": 2.4,
            "sodium": 0.001
        },
        "labels": ["organic", "local"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456794",
        "name": "Tomates Cherry",
        "brand": "Hortifrut",
        "category": "vegetables",
        "price": 1800,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Santa Isabel",
        "description": "Tomates cherry frescos",
        "nutritional_info": {
            "energy_kcal": 18,
            "proteins": 0.9,
            "carbohydrates": 3.9,
            "fats": 0.2,
            "fiber": 1.2,
            "sodium": 0.005
        },
        "labels": ["local"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456795",
        "name": "Espinaca Orgánica",
        "brand": "Verde Vivo",
        "category": "vegetables",
        "price": 2200,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Jumbo",
        "description": "Espinaca fresca orgánica",
        "nutritional_info": {
            "energy_kcal": 23,
            "proteins": 2.9,
            "carbohydrates": 3.6,
            "fats": 0.4,
            "fiber": 2.2,
            "sodium": 0.079
        },
        "labels": ["organic", "local"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456796",
        "name": "Arroz Integral Orgánico",
        "brand": "Tucapel",
        "category": "grains",
        "price": 1500,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Lider",
        "description": "Arroz integral de grano largo",
        "nutritional_info": {
            "energy_kcal": 370,
            "proteins": 7.9,
            "carbohydrates": 77.2,
            "fats": 2.9,
            "fiber": 3.5,
            "sodium": 0.005
        },
        "labels": ["organic"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456797",
        "name": "Lentejas Orgánicas",
        "brand": "Grano de Oro",
        "category": "legumes",
        "price": 1200,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Santa Isabel",
        "description": "Lentejas orgánicas certificadas",
        "nutritional_info": {
            "energy_kcal": 352,
            "proteins": 25.8,
            "carbohydrates": 60.1,
            "fats": 1.1,
            "fiber": 10.7,
            "sodium": 0.006
        },
        "labels": ["organic", "local"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456798",
        "name": "Quinoa Real",
        "brand": "Andes Organics",
        "category": "grains",
        "price": 3500,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Jumbo",
        "description": "Quinoa real boliviana orgánica",
        "nutritional_info": {
            "energy_kcal": 368,
            "proteins": 14.1,
            "carbohydrates": 64.2,
            "fats": 6.1,
            "fiber": 7,
            "sodium": 0.005
        },
        "labels": ["organic", "fair-trade"],
        "origin_country": "Bolivia"
    },
    {
        "barcode": "7804123456799",
        "name": "Jugo de Naranja Natural",
        "brand": "Watts",
        "category": "beverages",
        "price": 1800,
        "unit": "l",
        "quantity": 1.0,
        "store": "Lider",
        "description": "Jugo de naranja 100% natural",
        "nutritional_info": {
            "energy_kcal": 45,
            "proteins": 0.7,
            "carbohydrates": 10.4,
            "fats": 0.2,
            "fiber": 0.2,
            "sodium": 0.001
        },
        "labels": ["no-added-sugar"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456800",
        "name": "Mix de Frutos Secos",
        "brand": "Nuts & Co",
        "category": "snacks",
        "price": 3200,
        "unit": "kg",
        "quantity": 0.5,
        "store": "Jumbo",
        "description": "Mix de almendras, nueces y pasas",
        "nutritional_info": {
            "energy_kcal": 607,
            "proteins": 20,
            "carbohydrates": 20,
            "fats": 52,
            "fiber": 7,
            "sodium": 0.01
        },
        "labels": ["organic"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456801",
        "name": "Pan Integral Artesanal",
        "brand": "Panadería del Barrio",
        "category": "bread",
        "price": 2500,
        "unit": "unit",
        "quantity": 1.0,
        "store": "Local",
        "description": "Pan integral con semillas",
        "nutritional_info": {
            "energy_kcal": 247,
            "proteins": 9,
            "carbohydrates": 41,
            "fats": 4.2,
            "fiber": 6.5,
            "sodium": 0.5
        },
        "labels": ["artesanal", "local"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456802",
        "name": "Aceite de Oliva Extra Virgen",
        "brand": "Olivos del Sur",
        "category": "oil",
        "price": 5500,
        "unit": "l",
        "quantity": 1.0,
        "store": "Jumbo",
        "description": "Aceite de oliva extra virgen primera presión",
        "nutritional_info": {
            "energy_kcal": 884,
            "proteins": 0,
            "carbohydrates": 0,
            "fats": 100,
            "fiber": 0,
            "sodium": 0.002
        },
        "labels": ["organic", "local"],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456803",
        "name": "Pasta Integral",
        "brand": "Carozzi",
        "category": "pasta",
        "price": 1400,
        "unit": "kg",
        "quantity": 0.5,
        "store": "Lider",
        "description": "Pasta de trigo integral",
        "nutritional_info": {
            "energy_kcal": 348,
            "proteins": 13,
            "carbohydrates": 70,
            "fats": 2.5,
            "fiber": 9,
            "sodium": 0.006
        },
        "labels": [],
        "origin_country": "Chile"
    },
    {
        "barcode": "7804123456804",
        "name": "Salmón Fresco",
        "brand": "AquaChile",
        "category": "fish",
        "price": 8900,
        "unit": "kg",
        "quantity": 1.0,
        "store": "Jumbo",
        "description": "Salmón del Atlántico fresco",
        "nutritional_info": {
            "energy_kcal": 208,
            "proteins": 20,
            "carbohydrates": 0,
            "fats": 13,
            "fiber": 0,
            "sodium": 0.059
        },
        "labels": [],
        "origin_country": "Chile"
    },
]

SAMPLE_STORES = [
    {
        "name": "Jumbo Kennedy",
        "chain": "Jumbo",
        "location": {
            "type": "Point",
            "coordinates": [-70.6040, -33.4172],  # [longitude, latitude] para MongoDB
            "latitude": -33.4172,
            "longitude": -70.6040,
            "address": "Av. Kennedy 9001, Las Condes, Santiago"
        },
        "phone": "+56 2 2630 5000",
        "sustainability_rating": 4.2,
        "average_price_level": "high"
    },
    {
        "name": "Lider Express Providencia",
        "chain": "Lider",
        "location": {
            "type": "Point",
            "coordinates": [-70.6100, -33.4250],
            "latitude": -33.4250,
            "longitude": -70.6100,
            "address": "Av. Providencia 2330, Providencia, Santiago"
        },
        "phone": "+56 2 2600 4000",
        "sustainability_rating": 3.8,
        "average_price_level": "medium"
    },
    {
        "name": "Santa Isabel Ñuñoa",
        "chain": "Santa Isabel",
        "location": {
            "type": "Point",
            "coordinates": [-70.5980, -33.4569],
            "latitude": -33.4569,
            "longitude": -70.5980,
            "address": "Av. Irarrázaval 3520, Ñuñoa, Santiago"
        },
        "phone": "+56 2 2630 6000",
        "sustainability_rating": 3.5,
        "average_price_level": "medium"
    },
    {
        "name": "Jumbo Bilbao",
        "chain": "Jumbo",
        "location": {
            "type": "Point",
            "coordinates": [-70.6200, -33.4378],
            "latitude": -33.4378,
            "longitude": -70.6200,
            "address": "Av. Bilbao 2750, Providencia, Santiago"
        },
        "phone": "+56 2 2630 5100",
        "sustainability_rating": 4.0,
        "average_price_level": "high"
    },
    {
        "name": "Lider Maipú",
        "chain": "Lider",
        "location": {
            "type": "Point",
            "coordinates": [-70.7600, -33.5100],
            "latitude": -33.5100,
            "longitude": -70.7600,
            "address": "Av. Américo Vespucio 1501, Maipú, Santiago"
        },
        "phone": "+56 2 2600 4100",
        "sustainability_rating": 3.6,
        "average_price_level": "low"
    },
]

async def seed_database():
    """Puebla la base de datos con datos de ejemplo"""
    logger.info("Initializing MongoDB connection...")
    await init_db()
    
    logger.info("Seeding products...")
    for product_data in SAMPLE_PRODUCTS:
        # Calcular score de sostenibilidad
        category_avg = 2000  # Precio promedio simplificado
        
        sustainability_score = scorer.calculate_overall_score(product_data, category_avg)
        product_data['sustainability_score'] = sustainability_score
        
        try:
            product_id = await ProductDB.create(product_data)
            logger.info(f"Created product: {product_data['name']} (ID: {product_id})")
        except Exception as e:
            logger.error(f"Error creating product {product_data['name']}: {e}")
    
    logger.info("Seeding stores...")
    for store_data in SAMPLE_STORES:
        try:
            store_id = await StoreDB.create(store_data)
            logger.info(f"Created store: {store_data['name']} (ID: {store_id})")
        except Exception as e:
            logger.error(f"Error creating store {store_data['name']}: {e}")
    
    logger.info("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_database())
