from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.customer_routes import router as customer_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.order_routes import router as order_router
from app.api.product_routes import router as product_router
from app.api.routes import router
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on application startup."""
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Inventory and Order Management System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
