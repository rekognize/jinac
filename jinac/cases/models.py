from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from translations.models import Translatable
from django.template.defaultfilters import slugify
from martor.models import MartorField
from jinac.jurisdiction.models import Court
from jinac.people.models import Journalist, Judge, Prosecutor, Attorney, Plaintiff, Complainant
from jinac.institutions.models import Institution


# case & trial decision types
DECISION_TYPES = (
    (0, _('acquittal')),
    (1, _('fine')),
    (2, _('imprisonment')),
    (6, _('postponed')),
    (7, _('judgement receded')),
    (8, _('discontinued')),
)


# cases

class Case(models.Model):
    name = models.CharField(_('case name'), max_length=100)
    name_en = models.CharField(_('case name (EN)'), max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    no = models.CharField(_('file number'), max_length=20)
    court = models.ForeignKey(Court, verbose_name=_('court'), on_delete=models.CASCADE)
    filing_date = models.DateField(_('case filing date'), blank=True, null=True)  # iddianame tarihi
    opening_date = models.DateField(_('case opening date'), blank=True, null=True)  # dava acilis tarihi
    defendant_count = models.PositiveIntegerField(_('defendant count'), blank=True, null=True)
    journalist_defendant_count = models.PositiveIntegerField(_('journalist defendant count'), blank=True, null=True)
    coup_related = models.BooleanField(_('coup attempt related'), default=False)
    journalists = models.ManyToManyField(Journalist, through='CaseJournalist')
    plaintiff = models.ManyToManyField(Plaintiff, verbose_name=_('plaintiff'), blank=True)
    complainant = models.ManyToManyField(Complainant, verbose_name=_('complainant'), blank=True)
    prosecutor = models.ForeignKey(Prosecutor, verbose_name=_('indictment prosecutor'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    summary = MartorField(_('case summary'), blank=True, null=True)
    summary_en = MartorField(_('case summary (EN)'), blank=True, null=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    related_cases = models.ManyToManyField('self', verbose_name=_('related cases'), blank=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    publish = models.BooleanField(_('publish'), default=False)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('case_detail', args=[self.id])

    def status(self):
        return self.casestatus_set.last()

    def notes(self):
        return self.casenote_set.filter(type__publish=True).filter(journalist__isnull=True)

    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('cases')
        ordering = ('slug', 'order', '-modified',)


class CaseStatus(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=1, choices=(
        (0, _('local')),
        (1, _('appeal')),
        (2, _('supreme',)),
        (3, _('constitutional')),
        (4, _('ECHR')),
    ))
    date = models.DateField(blank=True, null=True)
    decision = models.PositiveSmallIntegerField(
        choices=(
            (1, _('approved')),
            (2, _('denied')),
        ), blank=True, null=True
    )
    details = models.TextField(_('details'), blank=True, null=True)

    def __str__(self):
        return self.get_status_display()

    class Meta:
        verbose_name = _('case status')
        verbose_name_plural = _('case status')
        ordering = ('date',)


class WorkPosition(models.Model):
    position = models.CharField(_('work position'), max_length=100)

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = _('work position')
        verbose_name_plural = _('work position')


class CaseJournalist(models.Model):
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalists'), on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution,
        verbose_name=_('institution'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    position = models.ForeignKey(
        WorkPosition,
        verbose_name=_('work position'),
        blank=True, null=True, on_delete=models.SET_NULL
    )
    attorneys = models.ManyToManyField(Attorney, verbose_name=_('attorney'), blank=True)

    def __str__(self):
        return f"{self.case.__str__()} - {self.journalist.__str__()}"

    class Meta:
        verbose_name = _('case - journalist relation')
        verbose_name_plural = _('case - journalist relations')


class CaseDecision(models.Model):
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalists'), on_delete=models.CASCADE)
    decision_type = models.PositiveSmallIntegerField(
        _('decision type'), blank=True, null=True,
        choices=DECISION_TYPES
    )
    articles = models.ManyToManyField('Article', verbose_name=_('articles'), blank=True)
    punishment_year = models.PositiveSmallIntegerField(_('year'), blank=True, null=True)
    punishment_month = models.PositiveSmallIntegerField(_('month'), blank=True, null=True)
    punishment_day = models.PositiveSmallIntegerField(_('day'), blank=True, null=True)
    punishment_fine = models.CharField(_('fine'), max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.case.__str__()}'

    def get_punishment(self):
        if self.punishment_fine:
            return f'{self.punishment_fine} TL'
        else:
            punishment = []
            if self.punishment_year:
                punishment.append('%s %s' % (self.punishment_year, _('year')))
            if self.punishment_month:
                punishment.append('%s %s' % (self.punishment_month, _('month')))
            if self.punishment_day:
                punishment.append('%s %s' % (self.punishment_day, _('day')))
            return punishment and ', '.join(punishment) or '-'
    get_punishment.short_description = _('punishment')

    class Meta:
        verbose_name = _('case - decision relation')
        verbose_name_plural = _('case - decision relations')


class Article(models.Model):
    type = models.PositiveSmallIntegerField(choices=(
        (1, _('TCK')),
        (2, _('TMK')),
        (3, _('Constitution')),
    ))
    description = models.TextField(_('article'), blank=True, null=True)
    indictment = models.CharField(_('indictment'), max_length=200, blank=True, null=True)
    no = models.CharField(max_length=20)
    punishment_type = models.PositiveSmallIntegerField(
        _('punishment type'), blank=True, null=True,
        choices=(
            (1, _('fine')),
            (2, _('imprisonment')),
        )
    )

    def __str__(self):
        return f"{self.get_type_display()} {self.no} {self.indictment}"

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class CaseIndictment(models.Model):
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalist'), on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, verbose_name=_('articles'), blank=True)
    details = models.TextField(_('details'), blank=True, null=True)

    def __str__(self):
        return f'{self.case.__str__()}'

    class Meta:
        verbose_name = _('indictment')
        verbose_name_plural = _('indictments')


class CaseDocumentType(models.Model):
    type = models.CharField(_('type'), max_length=50)
    order = models.PositiveSmallIntegerField(_('order'), blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('case document type')
        verbose_name_plural = _('case document types')
        ordering = ('order', 'id')


class CaseDocument(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    file = models.FileField(_('file'), upload_to='documents/')
    type = models.ForeignKey(CaseDocumentType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalist'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    publish = models.BooleanField(_('publish'), default=False)

    class Meta:
        verbose_name = _('case document')
        verbose_name_plural = _('case documents')
        ordering = ('case', 'type')


class CaseNoteType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    type_en = models.CharField(_('type (EN)'), max_length=100, blank=True, null=True)
    publish = models.BooleanField(_('publish'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('case note type')
        verbose_name_plural = _('case note types')
        ordering = ('order', 'id')


class CaseNote(Translatable):
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalist'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    case = models.ForeignKey(Case, verbose_name=_('case'),
                             blank=True, null=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(
        CaseNoteType, verbose_name=_('type'),
        blank=True, null=True, on_delete=models.SET_NULL,
    )
    note = MartorField(_('note'))
    note_en = MartorField(_('note (EN)'), blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type and self.type.type or '-'

    class Meta:
        verbose_name = _('case notes')
        verbose_name_plural = _('case notes')
        ordering = ('case__name', 'type')

    class TranslatableMeta:
        fields = ['note']


# trials

class Trial(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    session_no = models.PositiveIntegerField(_('session'))
    time_announced = models.DateTimeField(_('announced time'))
    time_start = models.DateTimeField(_('start time'), blank=True, null=True)
    time_next = models.DateTimeField(_('next trial time'), blank=True, null=True)
    observers = models.ManyToManyField(Institution, verbose_name=_('institutional observers'), blank=True)
    summary = MartorField(_('case summary'))
    judge = models.ForeignKey(Judge, verbose_name=_('presiding judge'), blank=True, null=True, on_delete=models.SET_NULL)
    board = models.ManyToManyField(Judge, verbose_name=_('board of judges'),
                                   related_name='board_memberships', blank=True)
    prosecutor = models.ForeignKey(Prosecutor, verbose_name=_('trial prosecutor'),
                                   blank=True, null=True, on_delete=models.SET_NULL)

    publish = models.BooleanField(_('publish'), default=False)
    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    def __str__(self):
        standing = "%s. %s" % (self.session_no, _('Standing'))
        return f'{self.case.name}: {standing}'

    def name_en(self):
        standing = "%s. %s" % (self.session_no, _('Standing'))
        return f'{self.case.name_en}: {standing}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        trial = Trial.objects.get(id=self.id)
        case = trial.case
        last_trial = case.trial_set.order_by('session_no').last()
        if trial == last_trial:
            case.summary = trial.summary
            case.save()

    def get_absolute_url(self):
        #return reverse('trial_detail', kwargs={'case': self.case.id, 'pk': self.id})
        return reverse('case_detail', kwargs={'pk': self.case.id})

    def notes(self):
        return self.trialnote_set.filter(type__publish=True)

    class Meta:
        verbose_name = _('trial')
        verbose_name_plural = _('trials')
        ordering = ('time_start',)


class TrialNoteType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    publish = models.BooleanField(_('publish'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('trial note type')
        verbose_name_plural = _('trial note types')
        ordering = ('order', 'id')


class TrialNote(models.Model):
    trial = models.ForeignKey('Trial', verbose_name=_('trial'), on_delete=models.CASCADE)
    type = models.ForeignKey(
        TrialNoteType, verbose_name=_('type'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    note = MartorField(_('note'), blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = _('trial note')
        verbose_name_plural = _('trial notes')
        ordering = ('trial', 'type',)


class ViolationType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    order = models.PositiveSmallIntegerField(_('order'), blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('violation type')
        verbose_name_plural = _('violation types')
        ordering = ('order', 'id')


class TrialViolation(models.Model):
    trial = models.ForeignKey('Trial', verbose_name=_('trial'), on_delete=models.CASCADE)
    type = models.ForeignKey(ViolationType, verbose_name=_('violation type'), on_delete=models.CASCADE)
    details = models.TextField(_('details'), blank=True, null=True)

    class Meta:
        verbose_name = _('right violation')
        verbose_name_plural = _('right violations')
        ordering = ('trial', 'type',)


class TrialDocumentType(models.Model):
    type = models.CharField(_('type'), max_length=50)
    order = models.PositiveSmallIntegerField(_('order'), blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('trial document type')
        verbose_name_plural = _('trial document types')


class TrialDocument(models.Model):
    trial = models.ForeignKey(Trial, verbose_name=_('trial'), on_delete=models.CASCADE)
    file = models.FileField(_('file'), upload_to='documents/')
    type = models.ForeignKey(TrialDocumentType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalist'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    publish = models.BooleanField(_('publish'), default=False)

    class Meta:
        verbose_name = _('trial document')
        verbose_name_plural = _('trial documents')
        ordering = ('trial', 'type',)


class TrialDecision(models.Model):
    trial = models.ForeignKey(Trial, verbose_name=_('trial'), on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalists'), on_delete=models.CASCADE)
    decision_type = models.PositiveSmallIntegerField(
        _('decision type'), blank=True, null=True,
        choices=DECISION_TYPES
    )
    articles = models.ManyToManyField('Article', verbose_name=_('articles'), blank=True)
    punishment_year = models.PositiveSmallIntegerField(_('year'), blank=True, null=True)
    punishment_month = models.PositiveSmallIntegerField(_('month'), blank=True, null=True)
    punishment_day = models.PositiveSmallIntegerField(_('day'), blank=True, null=True)
    punishment_fine = models.CharField(_('fine'), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('trial - decision relation')
        verbose_name_plural = _('trial - decision relations')
