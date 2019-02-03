from django.db import models
from django.utils.translation import ugettext_lazy as _


class Journalist(models.Model):
    name = models.CharField(max_length=100)
    institutions = models.ManyToManyField(
        'Institution',
        verbose_name=_('institutions'),
        through='JournalistInstitution', blank=True
    )
    gender = models.CharField(max_length=2, blank=True, null=True, choices=(
        ('m', 'male'),
        ('f', 'female'),
    ))
    has_press_card = models.NullBooleanField(default=None)
    birth_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('journalist')
        verbose_name_plural = _('journalists')


class Status(models.Model):
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('status')


class WorkPosition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('work position')
        verbose_name_plural = _('work positions')


class JournalistInstitution(models.Model):
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, blank=True, null=True)
    started = models.DateField(blank=True, null=True)
    ended = models.DateField(blank=True, null=True)
    position = models.ForeignKey(WorkPosition, blank=True, null=True, on_delete=models.SET_NULL)
    ongoing = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('journalist institution')
        verbose_name_plural = _('journalist institutions')


class Institution(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('institution')
        verbose_name_plural = _('institutions')
