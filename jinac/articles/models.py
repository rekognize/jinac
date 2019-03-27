from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Article(models.Model):
    title = models.CharField(_('title'), max_length=200)
    subtitle = models.CharField(_('subtitle'), max_length=200, blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='articles/', blank=True, null=True)
    summary = models.TextField(_('summary'))
    lang = models.CharField(_('language'), max_length=5, choices=settings.LANGUAGES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish = models.BooleanField(_('publish'), default=False)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class Section(models.Model):
    article = models.ForeignKey(Article, verbose_name=_('article'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=200)
    text = models.TextField(_('text'), blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='articles/', blank=True, null=True)

    def __str__(self):
        return f'{self.article.title}: {self.title}'

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        ordering = ('id',)
