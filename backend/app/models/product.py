from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class NutritionalInfo(BaseModel):
    energy_kcal: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None

class SustainabilityScore(BaseModel):
    economic_score: float = Field(..., ge=0, le=100, description="Puntuación económica (0-100)")
    environmental_score: float = Field(..., ge=0, le=100, description="Puntuación ambiental (0-100)")
    social_score: float = Field(..., ge=0, le=100, description="Puntuación social (0-100)")
    overall_score: float = Field(..., ge=0, le=100, description="Puntuación general (0-100)")
    carbon_footprint: Optional[float] = Field(None, description="Huella de carbono en kg CO2")

class Product(BaseModel):
    id: Optional[str] = None
    barcode: Optional[str] = None
    name: str
    brand: Optional[str] = None
    category: str
    price: float = Field(..., gt=0)
    unit: str = "unit"  # unit, kg, l, etc.
    quantity: float = 1.0
    store: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    nutritional_info: Optional[NutritionalInfo] = None
    sustainability_score: Optional[SustainabilityScore] = None
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    labels: Optional[List[str]] = None  # organic, fair-trade, etc.
    origin_country: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductSearch(BaseModel):
    query: str
    category: Optional[str] = None
    max_price: Optional[float] = None
    min_sustainability: Optional[float] = None
    store: Optional[str] = None

class ProductSubstitution(BaseModel):
    original_product: Product
    substitute_product: Product
    reason: str
    savings: float
    sustainability_improvement: float
