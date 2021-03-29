from __future__ import annotations

"""
I wanted to use signals to track events, but the signal provides a very loose mechanism for 
handling type arguments. The controller here looks more applicable in my opinion.
"""

import json
from typing import Any, Dict, Optional, TYPE_CHECKING

from deepdiff import DeepDiff

from orders.models import Event
from orders.serializers.orders import OrderSerializer


if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from orders.models import Order


def store_event(
    event_type: str,
    order: Order,
    user: Optional[User] = None,
    subtype: Optional[str] = None,
    calculate_difference: bool = False,
) -> Event:
    """
    Saves the event in the database.

    If you pass the argument calculate_difference, the difference between the
    previous and the current snapshot will be saved
    """
    difference_dict = get_difference(order) if calculate_difference else None
    difference = json.dumps(difference_dict) if difference_dict else None
    return Event.objects.create(
        event_type=event_type,
        subtype=subtype,
        user=user,
        order=order,
        difference=difference,
        snapshot=get_json_snapshot(order),
    )


def get_difference(order: Order) -> Optional[Dict[str, Any]]:
    """
    Returns the difference between the last snapshot and the current order
    In case there were no previous snapshots, None will be returned.
    """
    current_snapshot = get_snapshot(order)
    difference = None
    previous_event = order.events.order_by("-created").first()
    previous_snapshot = json.loads(previous_event.snapshot)
    if previous_event:
        diff = DeepDiff(previous_snapshot, current_snapshot, ignore_order=True)
        difference = diff.to_dict().get("values_changed")
    return difference


def get_json_snapshot(order: Order) -> str:
    """
    Gets the snapshot and converts it into JSON string
    """
    snapshot_dict = get_snapshot(order)
    return json.dumps(snapshot_dict)


def get_snapshot(order: Order) -> Dict[str, Any]:
    """
    Creates a snapshot of the order
    """
    serializer = OrderSerializer(order)
    # DRF returns OrderedDict for each relation. We have to get the dict recursively
    return json.loads(json.dumps(serializer.data))
