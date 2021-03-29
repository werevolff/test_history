from django.db import models
from django.utils.translation import ugettext_lazy as _

from main.utils.models import ModelTrackingCreated
from orders.mixins import EventCreationHandlerMixin


class Order(EventCreationHandlerMixin, ModelTrackingCreated):
    """
    Order model
    """

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("order")
        ordering = ("-created",)

    class StateChoices(models.TextChoices):
        ACTION_REQUIRED = "action_required", _("action required")
        DRAFT = "draft", _("draft")
        SENT = "sent", _("sent")
        DELIVERED = "delivered", _("delivered")
        CANCELED = "canceled", _("canceled")

    calculate_difference_on_update = True

    state = models.CharField(
        _("state"),
        max_length=15,
        choices=StateChoices.choices,
        default=StateChoices.ACTION_REQUIRED,
    )

    @property
    def order_for_event(self):
        return self

    @property
    def event_type_on_create(self):
        return self.event_model.TypeChoices.CREATED

    @property
    def event_type_on_update(self):
        return self.event_model.TypeChoices.UPDATED


class OrderItem(EventCreationHandlerMixin, models.Model):
    """
    Order item
    """

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        ordering = ("-id",)

    handle_on_create = False
    calculate_difference_on_update = True
    event_subtype_on_update = "order_item_updated"

    order = models.ForeignKey(
        "Order",
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    saved_product = models.OneToOneField(
        "orders.SavedProduct",
        verbose_name=_("saved product"),
        on_delete=models.PROTECT,
        related_name="order_item",
    )

    def __str__(self):
        return self.saved_product.title

    @property
    def product(self) -> int:
        return self.saved_product.product_id

    @property
    def order_for_event(self):
        return self.order

    @property
    def event_type_on_update(self):
        return self.event_model.TypeChoices.UPDATED
