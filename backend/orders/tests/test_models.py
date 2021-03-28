import pytest


@pytest.mark.django_db
def test_models(order_item):
    assert order_item.id
