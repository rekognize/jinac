from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class CourtType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Court(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(CourtType, blank=True, null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Attorney(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Prosecutor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Judge(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TrialType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class IndictmentType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('indictment')
        verbose_name_plural = _('indictments')


class PunishmentType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class PrisonType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Prison(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(PrisonType, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class DecisionType(models.Model):
    type = models.CharField(max_length=100)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return self.type


class ViolationType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('violation')
        verbose_name_plural = _('violations')
