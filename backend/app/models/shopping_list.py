from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from app.models.product import Product

class ShoppingListItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(..., gt=0)
    priority: int = Field(default=1, ge=1, le=5)  # 1=low, 5=high
    is_essential: bool = False

class OptimizationCriteria(BaseModel):
    max_budget: float = Field(..., gt=0)
    prioritize_sustainability: bool = True
    prioritize_savings: bool = True
    min_environmental_score: float = Field(default=0, ge=0, le=100)
    preferred_stores: Optional[List[str]] = None

class ShoppingList(BaseModel):
    id: Optional[str] = None
    name: str
    items: List[ShoppingListItem]
    optimization_criteria: Optional[OptimizationCriteria] = None
    is_optimized: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OptimizedShoppingList(BaseModel):
    original_list: ShoppingList
    optimized_items: List[Dict]  # Products with quantities
    total_cost: float
    estimated_savings: float
    total_environmental_score: float
    total_carbon_footprint: float
    substitutions_made: List[Dict]
    optimization_stats: Dict

class ShoppingAnalysis(BaseModel):
    total_items: int
    total_cost: float
    average_sustainability_score: float
    total_carbon_footprint: float
    category_breakdown: Dict[str, float]
    potential_savings: float
    recommendations: List[str]
