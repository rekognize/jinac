from django.db import models
from django.utils.translation import ugettext_lazy as _


class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('institution')
        verbose_name_plural = _('institutions')
