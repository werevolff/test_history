from hamcrest import assert_that, has_entries
import pytest

from orders.controllers import get_difference, store_event
from orders.models import Event, Order, SavedProduct


@pytest.mark.django_db
def test_get_difference(order_with_untracked_event):
    actual_difference = get_difference(order_with_untracked_event)
    assert_that(
        actual_difference,
        has_entries(
            {
                "root['order_items'][0]['saved_product']['width']": has_entries(
                    {
                        "new_value": "0.000",
                    }
                )
            }
        ),
    )


@pytest.mark.django_db
def test_store_event(order_with_untracked_event, mocker):
    spy = mocker.spy(Event.objects, "create")
    store_event(Event.TypeChoices.UPDATED, order_with_untracked_event)
    spy.assert_called_once()


@pytest.fixture
def order_with_untracked_event(order_with_item, last_event) -> Order:
    SavedProduct.objects.filter(order_item__order=order_with_item).update(width=0)
    order_with_item.refresh_from_db()
    return order_with_item


@pytest.fixture
def last_event(order_with_item, make_order_history) -> Event:
    return order_with_item.events.latest("-created")
