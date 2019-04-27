from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from martor.models import MartorField
from jinac.articles.models import Article
from jinac.cases.models import Case, Trial


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
    text = MartorField(_('text'))
    link = models.URLField(_('link'), blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(_('publish'), default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')
        ordering = ('-added',)


class Info(models.Model):
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField()
    value = models.CharField(_('value'), max_length=50)

    def __str__(self):
        return f"{self.name}: {self.value}"

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).replace('-', '_')
        return super().save(**kwargs)

    class Meta:
        verbose_name = _('Info')
        verbose_name_plural = _('Info')


class Feed(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feed')
        ordering = ('-time',)


@receiver([post_save], sender=Article)
@receiver([post_save], sender=Trial)
def add_to_feed(sender, instance, created, **kwargs):
    if created:
        Feed.objects.create(
            object=instance
        )
