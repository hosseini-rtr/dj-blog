from django.db import models
from django.utils.translation import gettext_lazy as _


class Link(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    url = models.URLField()
    label = models.CharField(max_length=30, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
