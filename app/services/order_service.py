from collections import defaultdict
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate


def create_order(db: Session, payload: OrderCreate) -> Order:
    """Create an order atomically and reduce inventory."""
    try:
        customer = db.scalar(select(Customer).where(Customer.id == payload.customer_id))
        if customer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        quantity_by_product: dict[UUID, int] = defaultdict(int)
        for item in payload.items:
            quantity_by_product[item.product_id] += item.quantity

        product_ids = list(quantity_by_product.keys())
        products = db.scalars(
            select(Product).where(Product.id.in_(product_ids)).with_for_update()
        ).all()
        products_by_id = {product.id: product for product in products}

        for product_id, requested_quantity in quantity_by_product.items():
            product = products_by_id.get(product_id)
            if product is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            if requested_quantity > product.stock_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient inventory for product",
                )

        total_amount = Decimal("0")
        order_items: list[OrderItem] = []

        for item in payload.items:
            product = products_by_id[item.product_id]
            line_total = product.price * item.quantity
            total_amount += line_total
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )
            )

        for product_id, requested_quantity in quantity_by_product.items():
            products_by_id[product_id].stock_quantity -= requested_quantity

        order = Order(customer_id=payload.customer_id, total_amount=total_amount, items=order_items)
        db.add(order)
        db.commit()
        db.refresh(order, attribute_names=["items"])
        return order
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        ) from exc


def get_orders(db: Session, skip: int = 0, limit: int = 10) -> list[Order]:
    """Fetch orders with pagination."""
    statement = (
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc(), Order.id)
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def get_order_by_id(db: Session, order_id: UUID) -> Order:
    """Fetch one order by id or raise 404."""
    statement = select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    order = db.scalar(statement)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


def delete_order(db: Session, order_id: UUID) -> None:
    """Cancel an order by restoring stock and deleting it."""
    try:
        order = get_order_by_id(db, order_id)

        quantity_by_product: dict[UUID, int] = defaultdict(int)
        for item in order.items:
            quantity_by_product[item.product_id] += item.quantity

        product_ids = list(quantity_by_product.keys())
        if product_ids:
            products = db.scalars(
                select(Product).where(Product.id.in_(product_ids)).with_for_update()
            ).all()
            products_by_id = {product.id: product for product in products}
            for product_id, restored_quantity in quantity_by_product.items():
                product = products_by_id.get(product_id)
                if product is not None:
                    product.stock_quantity += restored_quantity

        db.delete(order)
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        ) from exc
