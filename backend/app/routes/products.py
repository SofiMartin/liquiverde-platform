"""
Endpoints para gestión de productos.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from app.models.product import Product, ProductSearch, ProductSubstitution
from app.services.database import ProductDB
from app.services.external_apis import OpenFoodFactsAPI, PriceEstimator
from app.algorithms.sustainability_scoring import SustainabilityScorer
from app.algorithms.product_substitution import ProductSubstitutionEngine

router = APIRouter()
logger = logging.getLogger(__name__)

scorer = SustainabilityScorer()
substitution_engine = ProductSubstitutionEngine()

@router.post("/scan/{barcode}", response_model=Product)
async def scan_product(barcode: str):
    """
    Escanea un producto por código de barras.
    Busca primero en BD local, luego en Open Food Facts.
    """
    product = await ProductDB.get_by_barcode(barcode)
    
    if product:
        logger.info(f"Product found in local DB: {barcode}")
        return product
    
    logger.info(f"Fetching product from OpenFoodFacts: {barcode}")
    product_data = await OpenFoodFactsAPI.get_product_by_barcode(barcode)
    
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if 'price' not in product_data or not product_data['price']:
        product_data['price'] = PriceEstimator.estimate_price(product_data)
    
    category_avg = PriceEstimator.get_category_average(product_data.get('category', 'default'))
    sustainability_score = scorer.calculate_overall_score(product_data, category_avg)
    product_data['sustainability_score'] = sustainability_score
    
    product_id = await ProductDB.create(product_data)
    product_data['id'] = product_id
    
    return product_data

@router.get("/search", response_model=List[Product])
async def search_products(
    query: str = Query("", description="Search term"),
    category: Optional[str] = Query(None, description="Category filter"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    store: Optional[str] = Query(None, description="Store filter"),
    limit: int = Query(50, le=100, description="Result limit")
):
    """
    Busca productos en la base de datos local.
    """
    products = await ProductDB.search(
        query=query,
        category=category,
        max_price=max_price,
        store=store,
        limit=limit
    )
    
    return products

@router.get("/search/external")
async def search_external_products(
    query: str = Query(..., description="Search term"),
    country: str = Query("chile", description="Country filter"),
    category: Optional[str] = Query(None, description="Category filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, le=50, description="Page size")
):
    """
    Busca productos en Open Food Facts API.
    """
    products = await OpenFoodFactsAPI.search_products(
        query=query,
        country=country,
        category=category,
        page=page,
        page_size=page_size
    )
    
    # Agregar precios estimados y scores
    for product in products:
        if 'price' not in product or not product['price']:
            product['price'] = PriceEstimator.estimate_price(product)
        
        category_avg = PriceEstimator.get_category_average(product.get('category', 'default'))
        product['sustainability_score'] = scorer.calculate_overall_score(product, category_avg)
    
    return products

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Obtiene un producto por ID.
    """
    product = await ProductDB.get_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.post("/", response_model=Product)
async def create_product(product: Product):
    """
    Crea un nuevo producto manualmente.
    """
    product_dict = product.dict(exclude_none=True)
    
    # Calcular score de sostenibilidad si no está presente
    if not product_dict.get('sustainability_score'):
        category_avg = PriceEstimator.get_category_average(product_dict.get('category', 'default'))
        sustainability_score = scorer.calculate_overall_score(product_dict, category_avg)
        product_dict['sustainability_score'] = sustainability_score
    
    product_id = await ProductDB.create(product_dict)
    product_dict['id'] = product_id
    
    return product_dict

@router.get("/category/{category}", response_model=List[Product])
async def get_products_by_category(category: str, limit: int = Query(50, le=100)):
    """
    Obtiene productos por categoría.
    """
    products = await ProductDB.get_by_category(category)
    return products[:limit]

@router.post("/{product_id}/substitutes")
async def find_product_substitutes(
    product_id: str,
    max_price_increase: float = Query(0.1, description="Max price increase (10% default)"),
    min_sustainability_improvement: float = Query(5.0, description="Min sustainability improvement")
):
    """
    Encuentra productos sustitutos para un producto dado.
    """
    # Obtener producto original
    original_product = await ProductDB.get_by_id(product_id)
    
    if not original_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Obtener productos de la misma categoría como candidatos
    category = original_product.get('category')
    candidate_products = await ProductDB.get_by_category(category)
    
    # Encontrar sustitutos
    substitutes = substitution_engine.find_substitutes(
        original_product,
        candidate_products,
        max_price_increase=max_price_increase,
        min_sustainability_improvement=min_sustainability_improvement
    )
    
    return {
        "original_product": original_product,
        "substitutes": substitutes[:10],  # Top 10
        "total_found": len(substitutes)
    }

@router.post("/compare")
async def compare_products(product_id_1: str, product_id_2: str):
    """
    Compara dos productos en términos de sostenibilidad y precio.
    """
    product1 = await ProductDB.get_by_id(product_id_1)
    product2 = await ProductDB.get_by_id(product_id_2)
    
    if not product1 or not product2:
        raise HTTPException(status_code=404, detail="One or both products not found")
    
    comparison = scorer.compare_products(product1, product2)
    
    return {
        "product1": product1,
        "product2": product2,
        "comparison": comparison
    }

@router.get("/")
async def list_products(limit: int = Query(100, le=200)):
    """
    Lista todos los productos.
    """
    products = await ProductDB.get_all(limit=limit)
    return products
