from __future__ import annotations

import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orders.models import Order


@pytest.fixture
def order_with_item(order_factory) -> Order:
    return order_factory(with_order_item=True)
