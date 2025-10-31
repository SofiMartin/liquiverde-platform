"""
Servicio de base de datos usando MongoDB.
"""
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from typing import List, Dict, Optional
from datetime import datetime
from app.config import settings

logger = logging.getLogger(__name__)

client: Optional[AsyncIOMotorClient] = None
db = None

async def init_db():
    """Inicializa la conexión a MongoDB"""
    global client, db
    
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        
        await db.products.create_index("barcode")
        await db.products.create_index("category")
        await db.products.create_index("store")
        await db.products.create_index("name")
        
        await db.shopping_lists.create_index("created_at")
        await db.stores.create_index([("location.latitude", 1), ("location.longitude", 1)])
        
        logger.info(f"MongoDB connected successfully to {settings.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise

async def close_db():
    """Cierra la conexión a MongoDB"""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")

class ProductDB:
    """Operaciones de base de datos para productos usando MongoDB"""
    
    @staticmethod
    async def create(product: Dict) -> str:
        """Crea un nuevo producto"""
        product_id = product.get('id', f"prod_{datetime.utcnow().timestamp()}")
        product['_id'] = product_id
        product['id'] = product_id
        product['created_at'] = datetime.utcnow()
        product['updated_at'] = datetime.utcnow()
        
        await db.products.insert_one(product)
        return product_id
    
    @staticmethod
    async def get_by_id(product_id: str) -> Optional[Dict]:
        """Obtiene un producto por ID"""
        product = await db.products.find_one({"_id": product_id})
        if product:
            product.pop('_id', None)
        return product
    
    @staticmethod
    async def get_by_barcode(barcode: str) -> Optional[Dict]:
        """Obtiene un producto por código de barras"""
        product = await db.products.find_one({"barcode": barcode})
        if product:
            product.pop('_id', None)
        return product
    
    @staticmethod
    async def search(query: str = "", category: Optional[str] = None,
                    max_price: Optional[float] = None, store: Optional[str] = None,
                    limit: int = 50) -> List[Dict]:
        """Busca productos"""
        filter_query = {}
        
        if query:
            filter_query["$or"] = [
                {"name": {"$regex": query, "$options": "i"}},
                {"brand": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        
        if category:
            filter_query["category"] = category
        
        if max_price:
            filter_query["price"] = {"$lte": max_price}
        
        if store:
            filter_query["store"] = store
        
        cursor = db.products.find(filter_query).limit(limit)
        products = await cursor.to_list(length=limit)
        
        for product in products:
            product.pop('_id', None)
        
        return products
    
    @staticmethod
    async def get_all(limit: int = 100) -> List[Dict]:
        """Obtiene todos los productos"""
        cursor = db.products.find().limit(limit)
        products = await cursor.to_list(length=limit)
        
        for product in products:
            product.pop('_id', None)
        
        return products
    
    @staticmethod
    async def get_by_category(category: str) -> List[Dict]:
        """Obtiene productos por categoría"""
        cursor = db.products.find({"category": category})
        products = await cursor.to_list(length=None)
        
        for product in products:
            product.pop('_id', None)
        
        return products
    
    @staticmethod
    async def update(product_id: str, updates: Dict) -> bool:
        """Actualiza un producto"""
        updates['updated_at'] = datetime.utcnow()
        result = await db.products.update_one(
            {"_id": product_id},
            {"$set": updates}
        )
        return result.modified_count > 0

class ShoppingListDB:
    """Operaciones de base de datos para listas de compras usando MongoDB"""
    
    @staticmethod
    async def create(shopping_list: Dict) -> str:
        """Crea una nueva lista de compras"""
        list_id = shopping_list.get('id', f"list_{datetime.utcnow().timestamp()}")
        shopping_list['_id'] = list_id
        shopping_list['id'] = list_id
        shopping_list['created_at'] = datetime.utcnow()
        shopping_list['updated_at'] = datetime.utcnow()
        
        await db.shopping_lists.insert_one(shopping_list)
        return list_id
    
    @staticmethod
    async def get_by_id(list_id: str) -> Optional[Dict]:
        """Obtiene una lista por ID"""
        shopping_list = await db.shopping_lists.find_one({"_id": list_id})
        if shopping_list:
            shopping_list.pop('_id', None)
        return shopping_list
    
    @staticmethod
    async def get_all(limit: int = 50) -> List[Dict]:
        """Obtiene todas las listas"""
        cursor = db.shopping_lists.find().sort("created_at", -1).limit(limit)
        lists = await cursor.to_list(length=limit)
        
        for shopping_list in lists:
            shopping_list.pop('_id', None)
        
        return lists

class StoreDB:
    """Operaciones de base de datos para tiendas usando MongoDB"""
    
    @staticmethod
    async def create(store: Dict) -> str:
        """Crea una nueva tienda"""
        store_id = store.get('id', f"store_{datetime.utcnow().timestamp()}")
        store['_id'] = store_id
        store['id'] = store_id
        store['created_at'] = datetime.utcnow()
        
        await db.stores.insert_one(store)
        return store_id
    
    @staticmethod
    async def get_all() -> List[Dict]:
        """Obtiene todas las tiendas"""
        cursor = db.stores.find()
        stores = await cursor.to_list(length=None)
        
        for store in stores:
            store.pop('_id', None)
        
        return stores
    
    @staticmethod
    async def get_nearby(latitude: float, longitude: float, radius_km: float = 10) -> List[Dict]:
        """Obtiene tiendas cercanas usando geoespacial de MongoDB"""
        radius_radians = radius_km / 6371
        
        cursor = db.stores.find({
            "location": {
                "$geoWithin": {
                    "$centerSphere": [[longitude, latitude], radius_radians]
                }
            }
        })
        
        stores = await cursor.to_list(length=None)
        
        for store in stores:
            store.pop('_id', None)
        
        return stores
