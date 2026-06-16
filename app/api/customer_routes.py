from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import (
    create_customer,
    delete_customer,
    get_customer_by_id,
    get_customers,
)

router = APIRouter()


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer_endpoint(payload: CustomerCreate, db: Session = Depends(get_db)) -> CustomerResponse:
    """Create a customer."""
    return create_customer(db, payload)


@router.get("", response_model=list[CustomerResponse])
def list_customers_endpoint(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    """List customers with pagination."""
    return get_customers(db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_endpoint(customer_id: UUID, db: Session = Depends(get_db)) -> CustomerResponse:
    """Get one customer by id."""
    return get_customer_by_id(db, customer_id)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_customer_endpoint(customer_id: UUID, db: Session = Depends(get_db)) -> Response:
    """Delete customer when they have no orders."""
    delete_customer(db, customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
