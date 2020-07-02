from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as _p
from django.conf import settings
from martor.models import MartorField


class Article(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(_('subtitle'), max_length=200, blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='articles/', blank=True, null=True)
    summary = MartorField(_('summary'), blank=True, null=True)
    lang = models.CharField(_('language'), max_length=5, choices=settings.LANGUAGES)
    translation = models.ForeignKey(
        'self', verbose_name=_('translation'),
        blank=True, null=True, on_delete=models.SET_NULL
    )
    type = models.CharField(max_length=1, choices=(
        ('a', _('analysis')),
        ('r', _('report')),
    ), default='a')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish = models.BooleanField(_('publish'), default=False)
    about_page = models.BooleanField(_('about page'), default=False)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if self.translation:
            if not self.translation.translation:
                self.translation.translation = self
                self.translation.save()
        super().save(**kwargs)

    def get_absolute_url(self):
        if self.type == 'a':
            return reverse('article_detail', kwargs={'slug': self.slug})
        else:
            return reverse('report_detail', kwargs={'slug': self.slug})

    def get_image(self):
        image = self.image
        if not image:
            section = self.section_set.exclude(image__isnull=True).exclude(image='').first()
            if section:
                image = section.image
        return image

    class Meta:
        verbose_name = _p('blog', 'article')
        verbose_name_plural = _p('blog', 'articles')
        ordering = ('-added',)


class Section(models.Model):
    article = models.ForeignKey(Article, verbose_name=_('article'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=200, blank=True, null=True)
    text = MartorField(_('text'), blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='articles/', blank=True, null=True)

    def __str__(self):
        return f'{self.article.title}: {self.title or "-"}'

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        ordering = ('id',)
