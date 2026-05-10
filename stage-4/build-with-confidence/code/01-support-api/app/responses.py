from typing import Any

from flask import Response, jsonify


def json_ok(data: dict[str, Any], *, status: int = 200) -> Response:
    return jsonify({"ok": True, "data": data}), status


def json_error(code: str, message: str, *, status: int = 400) -> Response:
    return jsonify({"ok": False, "error": {"code": code, "message": message}}), status
