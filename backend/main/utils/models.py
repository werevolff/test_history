from django.db import models
from django.utils.translation import ugettext_lazy as _


class ModelTrackingCreated(models.Model):
    """
    Model, tracking created datetime
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(_("created"), auto_now_add=True, blank=True)
