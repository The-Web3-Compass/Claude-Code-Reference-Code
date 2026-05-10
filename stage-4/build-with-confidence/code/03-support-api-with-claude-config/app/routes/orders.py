from flask import Blueprint

from app.errors import AppError
from app.responses import json_error, json_ok
from app.services.order_service import get_order

bp = Blueprint("orders", __name__)


@bp.get("/<order_id>")
def get_order_route(order_id: str):
    try:
        order = get_order(order_id)
        return json_ok({"id": order.id, "customer_id": order.customer_id, "status": order.status})
    except AppError as e:
        return json_error(e.code, e.message, status=e.status)
