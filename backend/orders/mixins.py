from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from django.apps import apps
from django.utils.functional import cached_property

if TYPE_CHECKING:
    from orders.models import Order


class EventCreationHandlerMixin:

    calculate_difference_on_create = False
    calculate_difference_on_update = False
    event_subtype_on_create: Optional[str] = None
    event_subtype_on_update: Optional[str] = None
    handle_on_create = True
    handle_on_update = True

    @cached_property
    def event_model(self):
        return apps.get_model("orders", "Event")

    @property
    def order_for_event(self) -> Order:
        raise NotImplementedError

    @property
    def event_type_on_create(self) -> str:
        raise NotImplementedError

    @property
    def event_type_on_update(self) -> Optional[str]:
        raise NotImplementedError
