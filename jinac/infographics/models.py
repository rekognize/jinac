from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from martor.models import MartorField


class Infographic(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(_('image'), upload_to='infographics/', blank=True, null=True)
    description = MartorField(_('description'), blank=True, null=True)
    embed_code = models.TextField(_('embed code'))
    lang = models.CharField(_('language'), max_length=5, choices=settings.LANGUAGES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish = models.BooleanField(_('publish'), default=False)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('infographic_detail', kwargs={'slug': self.slug})
