from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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


class OrderResponse(BaseModel):
    """Order response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemResponse]
