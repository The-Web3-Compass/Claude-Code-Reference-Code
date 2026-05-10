from flask import Blueprint

from app.errors import AppError
from app.responses import json_error, json_ok
from app.services.customer_service import get_customer

bp = Blueprint("customers", __name__)


@bp.get("/<customer_id>")
def get_customer_route(customer_id: str):
    try:
        customer = get_customer(customer_id)
        return json_ok({"id": customer.id, "email": customer.email})
    except AppError as e:
        return json_error(e.code, e.message, status=e.status)
