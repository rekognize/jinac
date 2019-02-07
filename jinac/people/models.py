from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic.models import PolymorphicModel


class Person(PolymorphicModel):
    name = models.CharField(_('name'), max_length=100)
    photo = models.ImageField(_('photo'), blank=True, null=True)
    gender = models.CharField(
        _('gender'), max_length=2, blank=True, null=True,
        choices=(
            ('m', _('male')),
            ('f', _('female')),
        )
    )
    bio = models.TextField(_('biography'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')


class Journalist(Person):
    status = models.PositiveSmallIntegerField(
        _('status'), blank=True, null=True,
        choices=(
            (1, _('convict')),
            (2, _('detained')),
            (3, _('fugitive')),
        )
    )
    status_change_date = models.DateField(_('status change date'), blank=True, null=True)

    class Meta:
        verbose_name = _('journalist')
        verbose_name_plural = _('journalists')


class Attorney(Person):
    type = models.PositiveSmallIntegerField(
        _('type'),
        choices=(
            (1, _('defence')),
            (2, _('prosecution')),
        )
    )

    class Meta:
        verbose_name = _('attorney')
        verbose_name_plural = _('attorneys')


class Judge(Person):

    class Meta:
        verbose_name = _('judge')
        verbose_name_plural = _('judges')


class Prosecutor(Person):

    class Meta:
        verbose_name = _('prosecutor')
        verbose_name_plural = _('prosecutors')

