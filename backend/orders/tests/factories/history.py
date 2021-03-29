import json

import factory
from pytest_factoryboy import register

from orders.controllers import get_snapshot


@register
class EventFactory(factory.django.DjangoModelFactory):
    """
    Event Factory
    """

    class Meta:
        model = "orders.Event"

    @factory.lazy_attribute
    def snapshot(self):
        snapshot = get_snapshot(self.order)
        return json.dumps(snapshot)
