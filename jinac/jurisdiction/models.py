from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        ordering = ('name',)


class Court(models.Model):
    city = models.ForeignKey(City, verbose_name=_('city'), on_delete=models.CASCADE)
    no = models.PositiveSmallIntegerField(_('number'), blank=True, null=True)
    type = models.PositiveSmallIntegerField(
        _('type'), default=1,
        choices=(
            (0, _('Civil Court')),
            (1, _('Penal Court')),
            (2, _('Criminal Court')),
            (3, _('Court of Appeal')),
            (4, _('Supreme Court')),
            (5, _('Constitutional Court')),
            (6, _('ECHR')),
            (7, _('Commercial Court')),
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
        ordering = ('city',)


class Prison(models.Model):
    city = models.ForeignKey(City, verbose_name=_('city'), on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(_('name'), max_length=200, unique=True)
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
