from fastapi import APIRouter

from app.schemas.health import HealthResponse, RootResponse

router = APIRouter()


@router.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    """Return API status message."""
    return RootResponse(message="Inventory Management API Running")


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return application health status."""
    return HealthResponse(status="healthy")
