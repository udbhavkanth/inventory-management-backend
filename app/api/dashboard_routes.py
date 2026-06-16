from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard_summary

router = APIRouter()


@router.get("", response_model=DashboardResponse)
def get_dashboard_endpoint(db: Session = Depends(get_db)) -> DashboardResponse:
    """Return dashboard summary metrics."""
    return get_dashboard_summary(db)
