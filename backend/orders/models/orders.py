from django.db import models
from django.utils.translation import ugettext_lazy as _


class Order(models.Model):
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

    state = models.CharField(
        _("state"),
        max_length=15,
        choices=StateChoices.choices,
        default=StateChoices.ACTION_REQUIRED,
    )
    created = models.DateTimeField(_("created"), auto_now_add=True, blank=True)


class OrderItem(models.Model):
    """
    Order item
    """

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        ordering = ("-id",)

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
    def product(self):
        return self.saved_product.product
