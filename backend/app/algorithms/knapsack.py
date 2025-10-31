"""
Algoritmo de Mochila Multi-objetivo para optimización de lista de compras.
Optimiza simultáneamente: presupuesto, sostenibilidad y prioridad de productos.
"""
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class MultiObjectiveKnapsack:
    """
    Implementa un algoritmo de mochila multi-objetivo usando programación dinámica
    con ponderación de objetivos múltiples.
    """
    
    def __init__(self, max_budget: float, sustainability_weight: float = 0.3, 
                 savings_weight: float = 0.4, priority_weight: float = 0.3):
        """
        Args:
            max_budget: Presupuesto máximo disponible
            sustainability_weight: Peso para sostenibilidad (0-1)
            savings_weight: Peso para ahorros (0-1)
            priority_weight: Peso para prioridad (0-1)
        """
        self.max_budget = max_budget
        self.sustainability_weight = sustainability_weight
        self.savings_weight = savings_weight
        self.priority_weight = priority_weight
        
    def calculate_item_value(self, product: Dict) -> float:
        """
        Calcula el valor multi-objetivo de un producto.
        
        Formula:
        value = (sustainability_score * w1) + (savings_score * w2) + (priority * w3)
        """
        sustainability_score = product.get('sustainability_score', 50) / 100.0
        
        # Calcular ahorro basado en precio vs precio promedio de categoría
        avg_price = product.get('category_avg_price', product['price'])
        savings_score = max(0, (avg_price - product['price']) / avg_price) if avg_price > 0 else 0
        
        # Normalizar prioridad (1-5 -> 0-1)
        priority_score = product.get('priority', 1) / 5.0
        
        # Valor multi-objetivo
        value = (
            sustainability_score * self.sustainability_weight +
            savings_score * self.savings_weight +
            priority_score * self.priority_weight
        )
        
        return value * 100  # Escalar para mejor precisión
    
    def optimize(self, products: List[Dict], quantities: List[int]) -> Tuple[List[int], Dict]:
        """
        Optimiza la selección de productos usando mochila multi-objetivo.
        
        Args:
            products: Lista de productos con precio, sostenibilidad, etc.
            quantities: Cantidades deseadas de cada producto
            
        Returns:
            Tuple de (cantidades_optimizadas, estadísticas)
        """
        n = len(products)
        if n == 0:
            return [], {"total_cost": 0, "total_value": 0, "items_selected": 0}
        
        # Convertir presupuesto a centavos para evitar problemas de punto flotante
        budget_cents = int(self.max_budget * 100)
        
        # Calcular valores y costos
        values = [self.calculate_item_value(p) for p in products]
        prices_cents = [int(p['price'] * 100) for p in products]
        
        logger.info(f"Optimizing {n} products with budget ${self.max_budget}")
        
        # Programación dinámica con cantidades
        # dp[i][w] = (valor_máximo, items_seleccionados)
        dp = [[0 for _ in range(budget_cents + 1)] for _ in range(n + 1)]
        
        # Llenar tabla DP
        for i in range(1, n + 1):
            for w in range(budget_cents + 1):
                # No incluir el producto
                dp[i][w] = dp[i-1][w]
                
                # Intentar incluir el producto (hasta la cantidad deseada)
                max_qty = quantities[i-1]
                for qty in range(1, max_qty + 1):
                    cost = prices_cents[i-1] * qty
                    if cost <= w:
                        value = dp[i-1][w-cost] + values[i-1] * qty
                        if value > dp[i][w]:
                            dp[i][w] = value
        
        # Reconstruir solución
        selected_quantities = [0] * n
        w = budget_cents
        total_value = dp[n][w]
        
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                # Este producto fue seleccionado
                for qty in range(quantities[i-1], 0, -1):
                    cost = prices_cents[i-1] * qty
                    if w >= cost and dp[i][w] == dp[i-1][w-cost] + values[i-1] * qty:
                        selected_quantities[i-1] = qty
                        w -= cost
                        break
        
        # Calcular estadísticas
        total_cost = sum(selected_quantities[i] * products[i]['price'] for i in range(n))
        items_selected = sum(1 for q in selected_quantities if q > 0)
        total_items = sum(selected_quantities)
        
        avg_sustainability = 0
        if items_selected > 0:
            total_sustainability = sum(
                selected_quantities[i] * products[i].get('sustainability_score', 50)
                for i in range(n)
            )
            avg_sustainability = total_sustainability / total_items
        
        stats = {
            "total_cost": round(total_cost, 2),
            "total_value": round(total_value, 2),
            "items_selected": items_selected,
            "total_items": total_items,
            "budget_used_percent": round((total_cost / self.max_budget) * 100, 2),
            "average_sustainability": round(avg_sustainability, 2),
            "budget_remaining": round(self.max_budget - total_cost, 2)
        }
        
        logger.info(f"Optimization complete: {items_selected} items, ${total_cost:.2f} spent")
        
        return selected_quantities, stats
    
    def optimize_with_essentials(self, products: List[Dict], quantities: List[int], 
                                 essential_indices: List[int]) -> Tuple[List[int], Dict]:
        """
        Optimiza asegurando que los productos esenciales sean incluidos.
        
        Args:
            products: Lista de productos
            quantities: Cantidades deseadas
            essential_indices: Índices de productos esenciales
            
        Returns:
            Tuple de (cantidades_optimizadas, estadísticas)
        """
        # Calcular costo de esenciales
        essential_cost = sum(
            products[i]['price'] * quantities[i] 
            for i in essential_indices
        )
        
        if essential_cost > self.max_budget:
            logger.warning(f"Essential items cost ${essential_cost:.2f} exceeds budget ${self.max_budget:.2f}")
            # Retornar solo esenciales con cantidades reducidas proporcionalmente
            factor = self.max_budget / essential_cost
            selected = [0] * len(products)
            for i in essential_indices:
                selected[i] = max(1, int(quantities[i] * factor))
            
            total_cost = sum(selected[i] * products[i]['price'] for i in range(len(products)))
            return selected, {
                "total_cost": round(total_cost, 2),
                "items_selected": len(essential_indices),
                "warning": "Budget insufficient for all essentials"
            }
        
        # Inicializar con esenciales
        selected_quantities = [0] * len(products)
        for i in essential_indices:
            selected_quantities[i] = quantities[i]
        
        # Optimizar productos no esenciales con presupuesto restante
        remaining_budget = self.max_budget - essential_cost
        
        if remaining_budget > 0:
            non_essential_products = [
                p for i, p in enumerate(products) if i not in essential_indices
            ]
            non_essential_quantities = [
                q for i, q in enumerate(quantities) if i not in essential_indices
            ]
            
            if non_essential_products:
                temp_knapsack = MultiObjectiveKnapsack(
                    remaining_budget,
                    self.sustainability_weight,
                    self.savings_weight,
                    self.priority_weight
                )
                
                optimized_non_essential, _ = temp_knapsack.optimize(
                    non_essential_products,
                    non_essential_quantities
                )
                
                # Combinar resultados
                non_essential_idx = 0
                for i in range(len(products)):
                    if i not in essential_indices:
                        selected_quantities[i] = optimized_non_essential[non_essential_idx]
                        non_essential_idx += 1
        
        # Calcular estadísticas finales
        total_cost = sum(selected_quantities[i] * products[i]['price'] for i in range(len(products)))
        items_selected = sum(1 for q in selected_quantities if q > 0)
        
        stats = {
            "total_cost": round(total_cost, 2),
            "items_selected": items_selected,
            "essentials_included": len(essential_indices),
            "budget_remaining": round(self.max_budget - total_cost, 2)
        }
        
        return selected_quantities, stats
