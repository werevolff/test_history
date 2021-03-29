import pytest
from hamcrest import (
    assert_that,
    has_entries,
    contains_exactly,
    instance_of,
    matches_regexp,
)

from orders.serializers.orders import OrderSerializer


@pytest.mark.django_db
def test_order_serializer(order_factory):
    """
    Test OrderSerializer
    """
    order = order_factory(with_order_item=True)
    serializer = OrderSerializer(order)
    assert_that(
        serializer.data,
        has_entries(
            {
                "id": instance_of(int),
                "created": instance_of(str),
                "state": instance_of(str),
                "order_items": contains_exactly(
                    has_entries(
                        {
                            "id": instance_of(int),
                            "saved_product_id": instance_of(int),
                            "product": instance_of(int),
                            "saved_product": has_entries(
                                {
                                    "id": instance_of(int),
                                    "product_id": instance_of(int),
                                    "title": instance_of(str),
                                    "width": matches_regexp(r"\d+\.\d{2}"),
                                    "height": matches_regexp(r"\d+\.\d{2}"),
                                    "length": matches_regexp(r"\d+\.\d{2}"),
                                    "weight": matches_regexp(r"\d+\.\d{2}"),
                                    "retail_price": matches_regexp(r"\d+\.\d{2}"),
                                }
                            ),
                        }
                    ),
                ),
            }
        ),
    )
