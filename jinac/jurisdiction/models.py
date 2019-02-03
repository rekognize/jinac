from django.db import models
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')


class CourtType(models.Model):
    type = models.CharField(_('type'), max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('court type')
        verbose_name_plural = _('court types')


class Court(models.Model):
    name = models.CharField(_('name'), max_length=50)
    type = models.ForeignKey(CourtType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, verbose_name=_('location'), blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('court')
        verbose_name_plural = _('courts')


class Attorney(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('attorney')
        verbose_name_plural = _('attorneys')


class Prosecutor(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('prosecutor')
        verbose_name_plural = _('prosecutors')


class Judge(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('judge')
        verbose_name_plural = _('judges')


class TrialType(models.Model):
    type = models.CharField(_('type'), max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('trial type')
        verbose_name_plural = _('trial types')


class IndictmentType(models.Model):
    type = models.CharField(_('type'), max_length=200)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('indictment type')
        verbose_name_plural = _('indictment types')


class PunishmentType(models.Model):
    type = models.CharField(_('type'), max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('punishment type')
        verbose_name_plural = _('punishment types')


class PrisonType(models.Model):
    type = models.CharField(_('type'), max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('prison type')
        verbose_name_plural = _('prison types')


class Prison(models.Model):
    name = models.CharField(_('name'), max_length=200)
    type = models.ForeignKey(PrisonType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('prison')
        verbose_name_plural = _('prisons')


class DecisionType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('decision type')
        verbose_name_plural = _('decision types')


class ViolationType(models.Model):
    type = models.CharField(_('type'), max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('violation type')
        verbose_name_plural = _('violation types')
