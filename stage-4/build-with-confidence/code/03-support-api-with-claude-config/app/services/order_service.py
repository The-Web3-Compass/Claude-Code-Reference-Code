from app.errors import AppError
from app.models.order import Order


def get_order(order_id: str) -> Order:
    if not order_id:
        raise AppError("invalid_order_id", "order_id is required", status=400)

    if order_id != "ord_456":
        raise AppError("order_not_found", f"Order {order_id} not found", status=404)

    return Order(id="ord_456", customer_id="cust_123", status="shipped")
