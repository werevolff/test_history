import pytest

from orders.models import Event
from orders.models import Order


@pytest.fixture
def make_order_history(order_with_item, event_factory) -> None:
    Order.objects.filter(pk=order_with_item.pk).update(state=Order.StateChoices.SENT)
    order_with_item.refresh_from_db()
    event_factory(
        event_type=Event.TypeChoices.TRANSITION,
        order=order_with_item,
        subtype="order state changed",
    )
    order_with_item.refresh_from_db()


@pytest.fixture
def order_with_item(order_factory) -> Order:
    return order_factory(with_order_item=True)
