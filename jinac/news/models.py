from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField


class Carousel(models.Model):
    image = models.ImageField(_('photo'), upload_to='carousel/')
    text = models.CharField(_('text'), max_length=250, blank=True, null=True)
    link = models.URLField(_('link'), blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(_('publish'), default=True)

    def __str__(self):
        return self.text or self.image.name

    class Meta:
        verbose_name = _('carousel')
        verbose_name_plural = _('carousel')
        ordering = ('-added',)


class News(models.Model):
    title = models.CharField(_('title'), max_length=100)
    text = HTMLField(_('text'))
    link = models.URLField(_('link'), blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(_('publish'), default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')
        ordering = ('-added',)
