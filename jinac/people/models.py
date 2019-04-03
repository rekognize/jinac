from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from jinac.jurisdiction.models import Prison


class Person(PolymorphicModel):
    name = models.CharField(_('name'), max_length=100)
    gender = models.CharField(
        _('gender'), max_length=2, blank=True, null=True,
        choices=(
            ('m', _('male')),
            ('f', _('female')),
        )
    )
    short_bio = models.TextField(_('short bio'), blank=True, null=True)
    bio = models.TextField(_('biography'), blank=True, null=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        ordering = ('name',)


class Journalist(Person):
    slug = models.SlugField(unique=True)
    photo = models.ImageField(_('photo'), upload_to='journalists/', blank=True, null=True)
    publish = models.BooleanField(_('publish'), default=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('journalist_detail', kwargs={'slug': self.slug})

    def current_status(self):
        return self.journaliststatus_set.order_by('start_date').last()

    def get_related_docs(self):
        # return related case and trial documents
        from jinac.cases.models import CaseDocument, Trial, TrialDocument
        documents = {}
        journo_case_docs = self.casedocument_set.filter(publish=True)
        if journo_case_docs:
            documents['journo_case_docs'] = journo_case_docs
        journo_trial_docs = self.trialdocument_set.filter(publish=True)
        if journo_trial_docs:
            documents['journo_trial_docs'] = journo_trial_docs
        case_ids = [cj.case.id for cj in self.casejournalist_set.all()]
        case_docs = CaseDocument.objects.filter(
            case__id__in=case_ids).filter(journalist__isnull=True).filter(publish=True)
        if case_docs:
            documents['case_docs'] = case_docs
        trials = Trial.objects.filter(case__in=case_ids)
        trial_docs = TrialDocument.objects.filter(trial__in=trials).filter(journalist__isnull=True).filter(publish=True)
        if trial_docs:
            documents['trial_docs'] = trial_docs
        return documents

    class Meta:
        verbose_name = _('journalist')
        verbose_name_plural = _('journalists')
        ordering = ('name',)


class JournalistStatus(models.Model):
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalist'), on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(_('status'), choices=(
        (1, _('Not detained')),
        (2, _('Detained')),
        (3, _('Imprisoned')),
        (4, _('Convicted')),
        (5, _('Fugitive')),
        (6, _('Postponed')),
        (7, _('Judgement receded')),
    ))
    prison = models.ForeignKey(Prison, verbose_name=_('prison'), blank=True, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    case = models.ForeignKey('cases.Case', verbose_name=_('case'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('journalist status')
        verbose_name_plural = _('journalist status')
        ordering = ('-start_date',)


class JournalistNoteType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    publish = models.BooleanField(_('publish'), default=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('case note type')
        verbose_name_plural = _('case note types')


class JournalistNote(models.Model):
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalist'), on_delete=models.CASCADE)
    type = models.ForeignKey(
        JournalistNoteType, verbose_name=_('type'),
        blank=True, null=True, on_delete=models.SET_NULL,
    )
    note = models.TextField(_('note'))
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = _('journalist note')
        verbose_name_plural = _('journalist notes')
        ordering = ('time',)

    class TranslatableMeta:
        fields = ['note']


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
        ordering = ('name',)


class Judge(Person):

    class Meta:
        verbose_name = _('judge')
        verbose_name_plural = _('judges')
        ordering = ('name',)


class Prosecutor(Person):

    class Meta:
        verbose_name = _('prosecutor')
        verbose_name_plural = _('prosecutors')
        ordering = ('name',)


class Plaintiff(Person):

    class Meta:
        verbose_name = _('plaintiff')
        verbose_name_plural = _('plaintiffs')
        ordering = ('name',)


class Complainant(Person):

    class Meta:
        verbose_name = _('complainant')
        verbose_name_plural = _('complainants')
        ordering = ('name',)
