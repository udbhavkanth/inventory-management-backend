from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DashboardResponse(BaseModel):
    """Dashboard summary response schema."""

    model_config = ConfigDict(from_attributes=True)

    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products: int
    total_inventory_value: Decimal
