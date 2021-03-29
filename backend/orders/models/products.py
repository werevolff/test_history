from django.db import models
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    """
    Product model
    """

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ("-id",)

    title = models.CharField(_("title"), max_length=1000)

    def __str__(self):
        return self.title


class SavedProduct(models.Model):
    """
    Stock item
    """

    class Meta:
        verbose_name = _("saved product")
        verbose_name_plural = _("saved products")
        ordering = ("-id",)

    product = models.ForeignKey(
        "Product",
        verbose_name=_("product"),
        on_delete=models.PROTECT,
        related_name="saved_products",
    )
    width = models.DecimalField(_("width"), max_digits=15, decimal_places=3)
    height = models.DecimalField(_("height"), max_digits=15, decimal_places=3)
    length = models.DecimalField(_("length"), max_digits=15, decimal_places=3)
    weight = models.DecimalField(_("weight"), max_digits=15, decimal_places=3)
    retail_price = models.DecimalField(
        _("retail_price"), max_digits=15, decimal_places=3
    )

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self.product.title
