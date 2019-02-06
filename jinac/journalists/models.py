from django.db import models
from django.utils.translation import ugettext_lazy as _


class Journalist(models.Model):
    name = models.CharField(_('name'), max_length=100)
    photo = models.ImageField(_('photo'), blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=2, blank=True, null=True, choices=(
        ('m', 'male'),
        ('f', 'female'),
    ))
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('journalist')
        verbose_name_plural = _('journalists')


class Status(models.Model):
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'convict'),
            (2, 'detained'),
            (3, 'fugitive'),
        )
    )
    date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('status')
