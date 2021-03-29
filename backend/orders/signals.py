from typing import Type
from orders.mixins import EventCreationHandlerMixin

from orders.controllers import store_event


def post_save_store_event(
    sender: Type[EventCreationHandlerMixin],
    instance: EventCreationHandlerMixin,
    created: bool,
    *args,
    **kwargs
):
    """
    Store Event after the EventCreationHandlerMixin instance saved
    """
    if created and instance.handle_on_create:
        store_event(
            instance.event_type_on_create,
            instance.order_for_event,
            subtype=instance.event_subtype_on_create,
            calculate_difference=instance.calculate_difference_on_create
        )
    elif not created and instance.handle_on_update:
        store_event(
            instance.event_type_on_update,
            instance.order_for_event,
            subtype=instance.event_subtype_on_update,
            calculate_difference=instance.calculate_difference_on_update
        )
