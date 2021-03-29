from http import HTTPStatus

from hamcrest import any_of, assert_that, only_contains, has_entries, instance_of, none
import pytest
from pytest_drf import APIViewTest
from pytest_lambda import lambda_fixture, static_fixture
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.usefixtures("make_order_history")
class TestEventViewSet(APIViewTest):

    url = static_fixture(reverse("api_v1:orders:event-list"))
    data = lambda_fixture(lambda order_with_item: {"order": order_with_item.pk, "limit": 10, "offset": 0})

    def test_response(self, order_with_item, json, response):
        # I use the direct status_code check because the DRF test is just an
        # abstraction for checking what the REST Framework returns. If I stop
        # using the tool, there will be less rewriting left for me.
        # For pytest_drf, we can use the Returns200 mixin to test the response code.
        assert response.status_code == HTTPStatus.OK
        assert json["count"] == order_with_item.events.count() > 0
        assert_that(
            json["results"],
            only_contains(
                has_entries({
                    "id": instance_of(int),
                    "event_type": instance_of(str),
                    "subtype": any_of(instance_of(str), none()),
                    "user": none(),
                    "difference": any_of(instance_of(str), none()),
                })
            )
        )
