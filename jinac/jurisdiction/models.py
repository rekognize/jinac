from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class Court(models.Model):
    city = models.ForeignKey(City, verbose_name=_('city'), blank=True, null=True, on_delete=models.SET_NULL)
    no = models.PositiveSmallIntegerField(_('number'), blank=True, null=True)
    type = models.PositiveSmallIntegerField(
        _('type'), default=1,
        choices=(
            (1, _('penal court')),
            (2, _('criminal court')),
            (3, _('court of appeal')),
            (4, _('supreme court')),
            (5, _('constitutional court')),
            (6, _('ECHR')),
        )
    )

    def __str__(self):
        if self.no:  # agir ceza & asliye hukuk
            return f'{self.city} {self.no}. {self.get_type_display()}'
        elif self.city:
            return f'{self.city} {self.get_type_display()}'
        else:
            return self.type

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
