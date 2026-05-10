import pytest

from app.errors import AppError
from app.services.order_service import get_order


def test_get_order_raises_when_missing_id() -> None:
    with pytest.raises(AppError) as exc:
        get_order("")

    assert exc.value.code == "invalid_order_id"


def test_get_order_raises_when_not_found() -> None:
    with pytest.raises(AppError) as exc:
        get_order("nope")

    assert exc.value.status == 404
