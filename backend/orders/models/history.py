from django.db import models
from django.utils.translation import ugettext_lazy as _

from main.utils.models import ModelTrackingCreated


class Event(ModelTrackingCreated):
    """
    Events
    """

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ("-created",)

    class TypeChoices(models.TextChoices):
        CREATED = "created", _("created")
        UPDATED = "updated", _("updated")
        TRANSITION = "transition", _("transition")

    event_type = models.CharField(
        _("event type"), max_length=10, choices=TypeChoices.choices
    )
    subtype = models.CharField(
        _("subtype"), max_length=255, choices=TypeChoices.choices
    )
    user = models.ForeignKey(
        "auth.User",
        verbose_name=_("user"),
        related_name="events",
        on_delete=models.PROTECT,
    )
    order = models.ForeignKey(
        "orders.Order",
        verbose_name=_("order"),
        related_name="events",
        on_delete=models.CASCADE,
    )
    snapshot = models.JSONField(_("snapshot"))
    difference = models.JSONField(_("difference"), blank=True, null=True)
