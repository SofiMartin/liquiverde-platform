from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routes import products, shopping_lists, analysis, stores
from app.services.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    logger.info("Starting LiquiVerde Platform...")
    await init_db()
    yield
    logger.info("Shutting down LiquiVerde Platform...")

app = FastAPI(
    title="LiquiVerde - Retail Inteligente",
    description="Plataforma de retail inteligente para compras sostenibles y ahorro",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(shopping_lists.router, prefix="/api/shopping-lists", tags=["Shopping Lists"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(stores.router, prefix="/api/stores", tags=["Stores"])

@app.get("/")
async def root():
    return {
        "message": "LiquiVerde API - Retail Inteligente",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
