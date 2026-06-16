from contextlib import asynccontextmanager

from fastapi import FastAPI

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

app.include_router(router)
app.include_router(product_router, prefix="/products", tags=["Products"])
