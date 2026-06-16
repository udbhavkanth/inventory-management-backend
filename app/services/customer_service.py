from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order
from app.schemas.customer import CustomerCreate


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    """Create and persist a customer."""
    full_name = payload.full_name.strip()
    phone = payload.phone.strip()
    if not full_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Customer full_name cannot be empty",
        )
    if not phone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Customer phone cannot be empty",
        )

    customer = Customer(
        full_name=full_name,
        email=str(payload.email).lower(),
        phone=phone,
    )
    db.add(customer)
    try:
        db.commit()
        db.refresh(customer)
        return customer
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer email already exists",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        ) from exc


def get_customers(db: Session, skip: int = 0, limit: int = 10) -> list[Customer]:
    """Fetch customers with pagination."""
    statement = select(Customer).order_by(Customer.created_at.desc(), Customer.id).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def get_customer_by_id(db: Session, customer_id: UUID) -> Customer:
    """Fetch customer by id or raise 404."""
    customer = db.scalar(select(Customer).where(Customer.id == customer_id))
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


def delete_customer(db: Session, customer_id: UUID) -> None:
    """Delete customer if they have no existing orders."""
    customer = get_customer_by_id(db, customer_id)
    has_orders = db.scalar(select(Order.id).where(Order.customer_id == customer_id).limit(1))
    if has_orders is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer has existing orders",
        )

    try:
        db.delete(customer)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        ) from exc
