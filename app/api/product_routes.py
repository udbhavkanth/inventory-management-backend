from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import (
    create_product,
    delete_product,
    get_product_by_id,
    get_products,
    update_product,
)

router = APIRouter()


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(payload: ProductCreate, db: Session = Depends(get_db)) -> ProductResponse:
    """Create a product with an auto-generated SKU."""
    return create_product(db, payload)


@router.get("", response_model=list[ProductResponse])
def list_products_endpoint(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[ProductResponse]:
    """List products with pagination."""
    return get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: UUID, db: Session = Depends(get_db)) -> ProductResponse:
    """Get one product by id."""
    return get_product_by_id(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: UUID,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
) -> ProductResponse:
    """Update mutable product fields."""
    return update_product(db, product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_product_endpoint(product_id: UUID, db: Session = Depends(get_db)) -> Response:
    """Delete a product by id."""
    delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
