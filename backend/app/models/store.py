from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import time

class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: str

class StoreHours(BaseModel):
    day: str
    open_time: str
    close_time: str

class Store(BaseModel):
    id: Optional[str] = None
    name: str
    chain: Optional[str] = None
    location: Location
    hours: Optional[List[StoreHours]] = None
    phone: Optional[str] = None
    sustainability_rating: Optional[float] = Field(None, ge=0, le=5)
    average_price_level: Optional[str] = None
    
class RouteOptimization(BaseModel):
    stores: List[Store]
    total_distance: float
    estimated_time: float
    route_order: List[int]
    savings_by_route: float
