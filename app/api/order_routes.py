from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order, delete_order, get_order_by_id, get_orders

router = APIRouter()


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_endpoint(payload: OrderCreate, db: Session = Depends(get_db)) -> OrderResponse:
    """Create an order and reduce inventory."""
    return create_order(db, payload)


@router.get("", response_model=list[OrderResponse])
def list_orders_endpoint(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[OrderResponse]:
    """List orders with pagination."""
    return get_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_endpoint(order_id: UUID, db: Session = Depends(get_db)) -> OrderResponse:
    """Get one order by id."""
    return get_order_by_id(db, order_id)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_order_endpoint(order_id: UUID, db: Session = Depends(get_db)) -> Response:
    """Cancel an order by deleting it and restoring inventory."""
    delete_order(db, order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
