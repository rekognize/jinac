from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class Court(models.Model):
    name = models.CharField(_('name'), max_length=50)
    type = models.PositiveSmallIntegerField(
        _('type'), blank=True, null=True,
        choices=(
            (1, _('penal court')),
            (2, _('criminal court')),
            (3, _('court of appeal')),
            (4, _('supreme court')),
            (5, _('constitutional court')),
            (6, _('ECHR')),
        )
    )
    city = models.ForeignKey(City, verbose_name=_('city'), blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('court')
        verbose_name_plural = _('courts')


class Prison(models.Model):
    name = models.CharField(_('name'), max_length=200)
    type = models.CharField(
        _('type'), max_length=1, blank=True, null=True,
        choices=(
            ('e', _('Type E')),
            ('f', _('Type F')),
        )
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('prison')
        verbose_name_plural = _('prisons')
