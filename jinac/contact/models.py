from django.db import models
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    name = models.CharField(_('name'), max_length=50)
    email = models.EmailField(_('email'))
    message = models.TextField(_('message'), blank=True, null=True)
    time = models.DateTimeField(_('time'), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
