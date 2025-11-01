"""
Endpoints para análisis y reportes (BONUS).
"""
from fastapi import APIRouter, Query
from typing import List, Dict
import logging
from datetime import datetime, timedelta

from app.services.database import ProductDB
from app.algorithms.sustainability_scoring import SustainabilityScorer

router = APIRouter()
logger = logging.getLogger(__name__)

scorer = SustainabilityScorer()

@router.get("/dashboard")
async def get_dashboard_stats():
    """
    Obtiene estadísticas para el dashboard principal.
    """
    products = await ProductDB.get_all(limit=500)
    
    if not products:
        return {
            "total_products": 0,
            "average_sustainability": 0,
            "total_carbon_footprint": 0,
            "category_distribution": {},
            "top_sustainable_products": [],
            "top_savings_opportunities": []
        }
    
    total_products = len(products)
    sustainability_scores = []
    carbon_footprints = []
    category_counts = {}
    
    for product in products:
        if product.get('sustainability_score'):
            sustainability_scores.append(product['sustainability_score']['overall_score'])
            carbon_footprints.append(product['sustainability_score'].get('carbon_footprint', 0))
        
        category = product.get('category', 'other')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    avg_sustainability = sum(sustainability_scores) / len(sustainability_scores) if sustainability_scores else 0
    total_carbon = sum(carbon_footprints)
    
    sorted_by_sustainability = sorted(
        [p for p in products if p.get('sustainability_score')],
        key=lambda x: x['sustainability_score']['overall_score'],
        reverse=True
    )
    
    top_sustainable = [
        {
            "id": p['id'],
            "name": p['name'],
            "score": p['sustainability_score']['overall_score'],
            "category": p.get('category')
        }
        for p in sorted_by_sustainability[:10]
    ]
    
    # Oportunidades de ahorro (productos caros que tienen alternativas)
    sorted_by_price = sorted(products, key=lambda x: x['price'], reverse=True)
    
    savings_opportunities = [
        {
            "id": p['id'],
            "name": p['name'],
            "price": p['price'],
            "category": p.get('category')
        }
        for p in sorted_by_price[:10]
    ]
    
    return {
        "total_products": total_products,
        "average_sustainability": round(avg_sustainability, 2),
        "total_carbon_footprint": round(total_carbon, 3),
        "category_distribution": category_counts,
        "top_sustainable_products": top_sustainable,
        "top_savings_opportunities": savings_opportunities
    }

@router.get("/impact")
async def calculate_impact(product_ids: List[str] = Query(...)):
    """
    Calcula el impacto ambiental y económico de una selección de productos.
    """
    products = []
    
    for product_id in product_ids:
        product = await ProductDB.get_by_id(product_id)
        if product:
            products.append(product)
    
    if not products:
        return {
            "total_cost": 0,
            "total_carbon": 0,
            "average_sustainability": 0,
            "impact_breakdown": {}
        }
    
    total_cost = sum(p['price'] for p in products)
    total_carbon = sum(
        p['sustainability_score'].get('carbon_footprint', 0)
        for p in products if p.get('sustainability_score')
    )
    
    sustainability_scores = [
        p['sustainability_score']['overall_score']
        for p in products if p.get('sustainability_score')
    ]
    avg_sustainability = sum(sustainability_scores) / len(sustainability_scores) if sustainability_scores else 0
    
    # Desglose por categoría
    impact_breakdown = {}
    
    for product in products:
        category = product.get('category', 'other')
        
        if category not in impact_breakdown:
            impact_breakdown[category] = {
                "count": 0,
                "cost": 0,
                "carbon": 0
            }
        
        impact_breakdown[category]["count"] += 1
        impact_breakdown[category]["cost"] += product['price']
        
        if product.get('sustainability_score'):
            impact_breakdown[category]["carbon"] += product['sustainability_score'].get('carbon_footprint', 0)
    
    # Equivalencias para hacer el impacto más comprensible
    equivalences = {
        "km_driven": round(total_carbon * 4.5, 1),  # 1 kg CO2 ≈ 4.5 km en auto
        "trees_needed": round(total_carbon / 21, 1),  # 1 árbol absorbe ~21 kg CO2/año
        "days_of_energy": round(total_carbon / 6, 1)  # Consumo promedio hogar ~6 kg CO2/día
    }
    
    return {
        "total_cost": round(total_cost, 2),
        "total_carbon": round(total_carbon, 3),
        "average_sustainability": round(avg_sustainability, 2),
        "impact_breakdown": impact_breakdown,
        "equivalences": equivalences,
        "recommendations": _generate_impact_recommendations(total_carbon, avg_sustainability)
    }

@router.get("/trends")
async def get_sustainability_trends():
    """
    Analiza tendencias de sostenibilidad en el catálogo.
    """
    products = await ProductDB.get_all(limit=500)
    
    # Agrupar por categoría
    category_stats = {}
    
    for product in products:
        category = product.get('category', 'other')
        
        if category not in category_stats:
            category_stats[category] = {
                "count": 0,
                "avg_price": 0,
                "avg_sustainability": 0,
                "avg_carbon": 0,
                "prices": [],
                "sustainability_scores": [],
                "carbon_footprints": []
            }
        
        stats = category_stats[category]
        stats["count"] += 1
        stats["prices"].append(product['price'])
        
        if product.get('sustainability_score'):
            stats["sustainability_scores"].append(product['sustainability_score']['overall_score'])
            stats["carbon_footprints"].append(product['sustainability_score'].get('carbon_footprint', 0))
    
    # Calcular promedios
    for category, stats in category_stats.items():
        if stats["prices"]:
            stats["avg_price"] = round(sum(stats["prices"]) / len(stats["prices"]), 2)
        
        if stats["sustainability_scores"]:
            stats["avg_sustainability"] = round(
                sum(stats["sustainability_scores"]) / len(stats["sustainability_scores"]), 2
            )
        
        if stats["carbon_footprints"]:
            stats["avg_carbon"] = round(
                sum(stats["carbon_footprints"]) / len(stats["carbon_footprints"]), 3
            )
        
        # Limpiar listas temporales
        del stats["prices"]
        del stats["sustainability_scores"]
        del stats["carbon_footprints"]
    
    # Identificar mejores y peores categorías
    categories_by_sustainability = sorted(
        category_stats.items(),
        key=lambda x: x[1]["avg_sustainability"],
        reverse=True
    )
    
    return {
        "category_stats": category_stats,
        "best_categories": [
            {"category": c[0], "score": c[1]["avg_sustainability"]}
            for c in categories_by_sustainability[:5]
        ],
        "worst_categories": [
            {"category": c[0], "score": c[1]["avg_sustainability"]}
            for c in categories_by_sustainability[-5:]
        ]
    }

@router.get("/savings-report")
async def generate_savings_report(product_ids: List[str] = Query(...)):
    """
    Genera reporte de ahorros potenciales para una lista de productos.
    """
    from app.algorithms.product_substitution import ProductSubstitutionEngine
    
    engine = ProductSubstitutionEngine()
    all_products = await ProductDB.get_all(limit=500)
    
    selected_products = []
    for product_id in product_ids:
        product = await ProductDB.get_by_id(product_id)
        if product:
            selected_products.append(product)
    
    if not selected_products:
        return {
            "total_current_cost": 0,
            "total_optimized_cost": 0,
            "total_savings": 0,
            "substitution_details": []
        }
    
    total_current_cost = sum(p['price'] for p in selected_products)
    total_optimized_cost = 0
    substitution_details = []
    
    for product in selected_products:
        category_products = [
            p for p in all_products 
            if p.get('category') == product.get('category') and p['id'] != product['id']
        ]
        
        substitutes = engine.find_substitutes(
            product,
            category_products,
            max_price_increase=0.2,
            min_sustainability_improvement=5.0
        )
        
        if substitutes:
            best_sub = substitutes[0]
            total_optimized_cost += best_sub['product']['price']
            
            substitution_details.append({
                "original": {
                    "id": product['id'],
                    "name": product['name'],
                    "price": product['price']
                },
                "substitute": {
                    "id": best_sub['product']['id'],
                    "name": best_sub['product']['name'],
                    "price": best_sub['product']['price']
                },
                "savings": best_sub['savings'],
                "sustainability_improvement": best_sub['sustainability_improvement'],
                "reason": best_sub['reason']
            })
        else:
            total_optimized_cost += product['price']
    
    total_savings = total_current_cost - total_optimized_cost
    
    return {
        "total_current_cost": round(total_current_cost, 2),
        "total_optimized_cost": round(total_optimized_cost, 2),
        "total_savings": round(total_savings, 2),
        "savings_percentage": round((total_savings / total_current_cost * 100), 2) if total_current_cost > 0 else 0,
        "substitution_details": substitution_details
    }

def _generate_impact_recommendations(carbon: float, sustainability: float) -> List[str]:
    """Genera recomendaciones basadas en impacto"""
    recommendations = []
    
    if carbon > 50:
        recommendations.append("Alta huella de carbono. Considera productos locales y de temporada.")
    elif carbon > 20:
        recommendations.append("Huella de carbono moderada. Puedes mejorar eligiendo productos orgánicos.")
    else:
        recommendations.append("Excelente huella de carbono. ¡Sigue así!")
    
    if sustainability < 40:
        recommendations.append("Baja puntuación de sostenibilidad. Revisa las alternativas sugeridas.")
    elif sustainability < 60:
        recommendations.append("Sostenibilidad moderada. Hay margen de mejora.")
    else:
        recommendations.append("Excelente sostenibilidad. Estás haciendo una diferencia.")
    
    return recommendations
