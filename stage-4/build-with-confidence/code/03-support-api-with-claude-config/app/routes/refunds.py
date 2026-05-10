from flask import Blueprint

from app.responses import json_ok

bp = Blueprint("refunds", __name__)


@bp.get("/health")
def refunds_healthcheck():
    return json_ok({"status": "ok"})
