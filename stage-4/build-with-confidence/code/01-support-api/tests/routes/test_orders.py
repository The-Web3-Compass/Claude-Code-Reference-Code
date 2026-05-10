from app import create_app


def test_get_order_happy_path() -> None:
    app = create_app()
    client = app.test_client()

    res = client.get("/orders/ord_456")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    assert payload["data"]["id"] == "ord_456"


def test_get_order_not_found() -> None:
    app = create_app()
    client = app.test_client()

    res = client.get("/orders/does_not_exist")
    assert res.status_code == 404
    payload = res.get_json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "order_not_found"
