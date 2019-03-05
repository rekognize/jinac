from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from polymorphic.models import PolymorphicModel


class Person(PolymorphicModel):
    name = models.CharField(_('name'), max_length=100)
    gender = models.CharField(
        _('gender'), max_length=2, blank=True, null=True,
        choices=(
            ('m', _('male')),
            ('f', _('female')),
        )
    )
    bio = models.TextField(_('biography'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        ordering = ('name',)


class Journalist(Person):
    slug = models.SlugField()
    photo = models.ImageField(_('photo'), blank=True, null=True)
    publish = models.BooleanField(_('publish'), default=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('journalist_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('journalist')
        verbose_name_plural = _('journalists')


class JournalistStatus(models.Model):
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalist'), on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(_('status'), choices=(
        (1, _('not detained')),
        (2, _('detained')),
        (3, _('imprisoned')),
        (4, _('convicted')),
        (5, _('fugitive')),
    ))
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    case = models.ForeignKey('cases.Case', verbose_name=_('case'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('journalist status')
        verbose_name_plural = _('journalist status')


class Attorney(Person):
    type = models.PositiveSmallIntegerField(
        _('type'), default=1,
        choices=(
            (1, _('defence')),
            (2, _('prosecution')),
        )
    )

    class Meta:
        verbose_name = _('attorney')
        verbose_name_plural = _('attorneys')


class Judge(Person):

    class Meta:
        verbose_name = _('judge')
        verbose_name_plural = _('judges')


class Prosecutor(Person):

    class Meta:
        verbose_name = _('prosecutor')
        verbose_name_plural = _('prosecutors')


class Plaintiff(Person):

    class Meta:
        verbose_name = _('plaintiff')
        verbose_name_plural = _('plaintiffs')
