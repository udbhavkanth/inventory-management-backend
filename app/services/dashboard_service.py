from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.schemas.dashboard import DashboardResponse

LOW_STOCK_THRESHOLD = 10


def get_dashboard_summary(db: Session) -> DashboardResponse:
    """Fetch dashboard summary statistics using aggregate queries."""
    try:
        total_products = db.scalar(select(func.count(Product.id))) or 0
        total_customers = db.scalar(select(func.count(Customer.id))) or 0
        total_orders = db.scalar(select(func.count(Order.id))) or 0

        low_stock_products = db.scalar(
            select(func.count(Product.id)).where(Product.stock_quantity < LOW_STOCK_THRESHOLD)
        ) or 0

        total_inventory_value = db.scalar(
            select(func.coalesce(func.sum(Product.price * Product.stock_quantity), 0))
        )
        inventory_value = Decimal(total_inventory_value or 0)

        return DashboardResponse(
            total_products=int(total_products),
            total_customers=int(total_customers),
            total_orders=int(total_orders),
            low_stock_products=int(low_stock_products),
            total_inventory_value=inventory_value,
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch dashboard summary",
        ) from exc
