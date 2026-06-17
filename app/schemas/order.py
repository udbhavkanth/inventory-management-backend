from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.models.order import Order


class OrderItemCreate(BaseModel):
    """Line item payload for order creation."""

    product_id: UUID
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    """Payload for creating an order."""

    customer_id: UUID
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    """Order item response schema."""

    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
    quantity: int
    unit_price: Decimal


class OrderListResponse(BaseModel):
    """Order list response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    customer_name: str
    total_amount: Decimal
    created_at: datetime

    @classmethod
    def from_order(cls, order: Order) -> OrderListResponse:
        if order.customer is None:
            raise ValueError("Order customer relationship must be loaded")
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            customer_name=order.customer.full_name,
            total_amount=order.total_amount,
            created_at=order.created_at,
        )


class OrderDetailResponse(BaseModel):
    """Order detail response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    customer_name: str
    customer_email: str
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemResponse]

    @classmethod
    def from_order(cls, order: Order) -> OrderDetailResponse:
        if order.customer is None:
            raise ValueError("Order customer relationship must be loaded")
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            customer_name=order.customer.full_name,
            customer_email=order.customer.email,
            total_amount=order.total_amount,
            created_at=order.created_at,
            items=[OrderItemResponse.model_validate(item) for item in order.items],
        )
