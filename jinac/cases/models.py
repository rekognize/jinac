from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from translations.models import Translatable
from jinac.jurisdiction.models import Court
from jinac.people.models import Journalist, Judge, Prosecutor, Attorney, Plaintiff
from jinac.institutions.models import Institution


# cases

class Case(models.Model):
    name = models.CharField(_('case name'), max_length=100)
    no = models.CharField(_('file number'), max_length=20)
    court = models.ForeignKey(Court, verbose_name=_('court'), on_delete=models.CASCADE)
    filing_date = models.DateField(_('case filing date'), blank=True, null=True)  # iddianame tarihi
    opening_date = models.DateField(_('case opening date'), blank=True, null=True)  # dava acilis tarihi
    defendant_count = models.PositiveIntegerField(_('defendant count'), blank=True, null=True)
    journalist_defendant_count = models.PositiveIntegerField(_('journalist defendant count'), blank=True, null=True)
    coup_related = models.BooleanField(_('coup attempt related'), default=False)
    journalists = models.ManyToManyField(Journalist, through='CaseJournalist')
    plaintiff = models.ManyToManyField(Plaintiff, verbose_name=_('plaintiff'), blank=True)
    prosecutor = models.ForeignKey(Prosecutor, verbose_name=_('indictment prosecutor'),
                                   blank=True, null=True, on_delete=models.SET_NULL)

    related_cases = models.ManyToManyField('self', verbose_name=_('related cases'), blank=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    publish = models.BooleanField(_('publish'), default=False)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('case_detail', args=[self.id])

    def status(self):
        return self.casestatus_set.last()

    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('cases')
        ordering = ('-modified',)


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
    attorneys = models.ManyToManyField(Attorney, verbose_name=_('attorney'))

    class Meta:
        verbose_name = _('case - journalist relation')
        verbose_name_plural = _('case - journalist relations')


class CaseDecision(models.Model):
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalists'), on_delete=models.CASCADE)
    decision_type = models.PositiveSmallIntegerField(
        _('decision type'), blank=True, null=True,
        choices=(
            (0, _('acquittal')),
            (1, _('fine')),
            (2, _('imprisonment')),
            (6, _('postponed')),
            (7, _('judgement receded')),
        )
    )
    articles = models.ManyToManyField('Article', verbose_name=_('articles'), blank=True)
    punishment_year = models.PositiveSmallIntegerField(_('year'), blank=True, null=True)
    punishment_month = models.PositiveSmallIntegerField(_('month'), blank=True, null=True)
    punishment_day = models.PositiveSmallIntegerField(_('day'), blank=True, null=True)
    punishment_fine = models.CharField(_('fine'), max_length=100, blank=True, null=True)

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

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('case document type')
        verbose_name_plural = _('case document types')


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


class CaseNoteType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    publish = models.BooleanField(_('publish'), default=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('case note type')
        verbose_name_plural = _('case note types')


class CaseNote(Translatable):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    type = models.ForeignKey(
        CaseNoteType, verbose_name=_('type'),
        blank=True, null=True, on_delete=models.SET_NULL,
    )
    note = models.TextField(_('note'))
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = _('case note')
        verbose_name_plural = _('case notes')

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
    summary = models.TextField(_('summary'), blank=True, null=True)
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
        return f'{self.case}: {self.session_no}'

    def get_absolute_url(self):
        return reverse('trial_detail', kwargs={'case': self.case.id, 'pk': self.id})

    class Meta:
        verbose_name = _('trial')
        verbose_name_plural = _('trials')
        ordering = ('time_start',)


class TrialNoteType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    publish = models.BooleanField(_('publish'), default=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('trial note type')
        verbose_name_plural = _('trial note types')


class TrialNote(models.Model):
    trial = models.ForeignKey('Trial', verbose_name=_('trial'), on_delete=models.CASCADE)
    type = models.ForeignKey(
        TrialNoteType, verbose_name=_('type'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    note = models.TextField(_('note'), blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = _('trial note')
        verbose_name_plural = _('trial notes')


class ViolationType(models.Model):
    type = models.CharField(_('type'), max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('violation type')
        verbose_name_plural = _('violation types')


class TrialViolation(models.Model):
    trial = models.ForeignKey('Trial', verbose_name=_('trial'), on_delete=models.CASCADE)
    type = models.ForeignKey(ViolationType, verbose_name=_('violation type'), on_delete=models.CASCADE)
    details = models.TextField(_('details'), blank=True, null=True)

    class Meta:
        verbose_name = _('right violation')
        verbose_name_plural = _('right violations')


class TrialDocumentType(models.Model):
    type = models.CharField(_('type'), max_length=50)

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
