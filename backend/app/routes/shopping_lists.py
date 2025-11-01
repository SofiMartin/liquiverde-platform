"""
Endpoints para gestión de listas de compras.
"""
from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict
import logging

from app.models.shopping_list import (
    ShoppingList, OptimizedShoppingList, ShoppingListItem, 
    OptimizationCriteria, ShoppingAnalysis
)
from app.services.database import ProductDB, ShoppingListDB
from app.algorithms.knapsack import MultiObjectiveKnapsack
from app.algorithms.product_substitution import ProductSubstitutionEngine
from app.algorithms.sustainability_scoring import SustainabilityScorer

router = APIRouter()
logger = logging.getLogger(__name__)

substitution_engine = ProductSubstitutionEngine()
scorer = SustainabilityScorer()

@router.post("/", response_model=ShoppingList)
async def create_shopping_list(shopping_list: ShoppingList):
    """
    Crea una nueva lista de compras.
    """
    list_dict = shopping_list.dict(exclude_none=True)
    list_id = await ShoppingListDB.create(list_dict)
    list_dict['id'] = list_id
    
    return list_dict

@router.get("/{list_id}", response_model=ShoppingList)
async def get_shopping_list(list_id: str):
    """
    Obtiene una lista de compras por ID.
    """
    shopping_list = await ShoppingListDB.get_by_id(list_id)
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    return shopping_list

@router.get("/")
async def list_shopping_lists(limit: int = 50):
    """
    Lista todas las listas de compras.
    """
    lists = await ShoppingListDB.get_all(limit=limit)
    return lists

@router.post("/{list_id}/optimize")
async def optimize_shopping_list(
    list_id: str,
    criteria: OptimizationCriteria = Body(...)
):
    """
    Optimiza una lista de compras usando algoritmo de mochila multi-objetivo.
    """
    # Obtener lista original
    shopping_list = await ShoppingListDB.get_by_id(list_id)
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    # Obtener productos
    products = []
    quantities = []
    essential_indices = []
    
    for idx, item in enumerate(shopping_list['items']):
        product = await ProductDB.get_by_id(item['product_id'])
        
        if not product:
            logger.warning(f"Product {item['product_id']} not found, skipping")
            continue
        
        product['category_avg_price'] = product['price'] * 1.1
        product['priority'] = item.get('priority', 1)
        
        products.append(product)
        quantities.append(item['quantity'])
        
        if item.get('is_essential', False):
            essential_indices.append(idx)
    
    if not products:
        raise HTTPException(status_code=400, detail="No valid products in list")
    
    knapsack = MultiObjectiveKnapsack(
        max_budget=criteria.max_budget,
        sustainability_weight=0.35 if criteria.prioritize_sustainability else 0.2,
        savings_weight=0.35 if criteria.prioritize_savings else 0.2,
        priority_weight=0.3
    )
    
    if essential_indices:
        optimized_quantities, stats = knapsack.optimize_with_essentials(
            products, quantities, essential_indices
        )
    else:
        optimized_quantities, stats = knapsack.optimize(products, quantities)
    
    optimized_items = []
    total_carbon = 0
    
    for i, qty in enumerate(optimized_quantities):
        if qty > 0:
            product = products[i]
            optimized_items.append({
                "product": product,
                "quantity": qty,
                "subtotal": product['price'] * qty
            })
            
            if product.get('sustainability_score'):
                total_carbon += product['sustainability_score'].get('carbon_footprint', 0) * qty
    
    original_cost = sum(products[i]['price'] * quantities[i] for i in range(len(products)))
    estimated_savings = original_cost - stats['total_cost']
    
    substitutions = []
    if criteria.prioritize_sustainability:
        all_products = ProductDB.get_all(limit=200)
        
        for item in optimized_items:
            product = item['product']
            category_products = [p for p in all_products if p.get('category') == product.get('category')]
            
            subs = substitution_engine.find_substitutes(
                product,
                category_products,
                max_price_increase=0.15,
                min_sustainability_improvement=10.0
            )
            
            if subs:
                substitutions.append({
                    "original": product['name'],
                    "substitute": subs[0]['product']['name'],
                    "reason": subs[0]['reason'],
                    "savings": subs[0]['savings'],
                    "sustainability_improvement": subs[0]['sustainability_improvement']
                })
    
    result = {
        "original_list": shopping_list,
        "optimized_items": optimized_items,
        "total_cost": stats['total_cost'],
        "estimated_savings": round(estimated_savings, 2),
        "total_environmental_score": stats.get('average_sustainability', 0),
        "total_carbon_footprint": round(total_carbon, 3),
        "substitutions_made": substitutions[:5],  # Top 5
        "optimization_stats": stats
    }
    
    return result

@router.post("/analyze")
async def analyze_shopping_list(items: List[Dict] = Body(...)):
    """
    Analiza una lista de compras y proporciona insights.
    """
    if not items:
        raise HTTPException(status_code=400, detail="Empty shopping list")
    
    total_cost = 0
    total_carbon = 0
    sustainability_scores = []
    category_costs = {}
    
    products_data = []
    
    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        
        product = ProductDB.get_by_id(product_id)
        
        if not product:
            continue
        
        products_data.append(product)
        
        cost = product['price'] * quantity
        total_cost += cost
        
        # Acumular por categoría
        category = product.get('category', 'other')
        category_costs[category] = category_costs.get(category, 0) + cost
        
        # Sostenibilidad
        if product.get('sustainability_score'):
            sustainability_scores.append(product['sustainability_score']['overall_score'])
            total_carbon += product['sustainability_score'].get('carbon_footprint', 0) * quantity
    
    avg_sustainability = sum(sustainability_scores) / len(sustainability_scores) if sustainability_scores else 0
    
    # Generar recomendaciones
    recommendations = []
    
    if avg_sustainability < 50:
        recommendations.append("Considera productos con mejor puntuación de sostenibilidad")
    
    if total_carbon > 20:
        recommendations.append("Tu lista tiene alta huella de carbono. Considera productos locales")
    
    high_cost_categories = sorted(category_costs.items(), key=lambda x: x[1], reverse=True)[:3]
    if high_cost_categories:
        recommendations.append(f"Categorías de mayor gasto: {', '.join([c[0] for c in high_cost_categories])}")
    
    # Calcular ahorros potenciales con sustituciones
    all_products = ProductDB.get_all(limit=200)
    potential_savings = 0
    
    for product in products_data[:5]:  # Analizar top 5 productos
        category_products = [p for p in all_products if p.get('category') == product.get('category')]
        subs = substitution_engine.find_substitutes(product, category_products)
        
        if subs and subs[0]['savings'] > 0:
            potential_savings += subs[0]['savings']
    
    return {
        "total_items": len(items),
        "total_cost": round(total_cost, 2),
        "average_sustainability_score": round(avg_sustainability, 2),
        "total_carbon_footprint": round(total_carbon, 3),
        "category_breakdown": category_costs,
        "potential_savings": round(potential_savings, 2),
        "recommendations": recommendations
    }

@router.post("/quick-optimize")
async def quick_optimize(
    product_ids: List[str] = Body(...),
    max_budget: float = Body(...),
    prioritize_sustainability: bool = Body(True)
):
    """
    Optimización rápida sin crear lista persistente.
    """
    products = []
    quantities = []
    
    for product_id in product_ids:
        product = await ProductDB.get_by_id(product_id)
        
        if product:
            product['category_avg_price'] = product['price'] * 1.1
            product['priority'] = 3  # Prioridad media por defecto
            products.append(product)
            quantities.append(1)
    
    if not products:
        raise HTTPException(status_code=400, detail="No valid products provided")
    
    knapsack = MultiObjectiveKnapsack(
        max_budget=max_budget,
        sustainability_weight=0.4 if prioritize_sustainability else 0.2,
        savings_weight=0.3,
        priority_weight=0.3
    )
    
    optimized_quantities, stats = knapsack.optimize(products, quantities)
    
    selected_products = []
    for i, qty in enumerate(optimized_quantities):
        if qty > 0:
            selected_products.append({
                "product": products[i],
                "quantity": qty,
                "subtotal": products[i]['price'] * qty
            })
    
    return {
        "selected_products": selected_products,
        "stats": stats
    }
