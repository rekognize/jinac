from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from jinac.jurisdiction.models import Court
from jinac.people.models import Journalist, Judge, Prosecutor, Attorney, Plaintiff
from jinac.institutions.models import Institution


class NoteType(models.Model):
    type = models.CharField(_('type'), max_length=100)
    publish = models.BooleanField(_('publish'), default=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('note type')
        verbose_name_plural = _('note types')


# cases

class CaseScope(models.Model):
    scope = models.CharField(_('scope'), max_length=200)  # feto, pkk, kck, ...

    def __str__(self):
        return self.scope

    class Meta:
        verbose_name = _('case scope')
        verbose_name_plural = _('case scope')


class Case(models.Model):
    no = models.CharField(_('file number'), max_length=20)
    court = models.ForeignKey(Court, verbose_name=_('court'), on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=100, blank=True, null=True)
    filing_date = models.DateField(_('case filing date'), blank=True, null=True)  # iddianame tarihi
    opening_date = models.DateField(_('case opening date'), blank=True, null=True)  # dava acilis tarihi
    defendant_count = models.PositiveIntegerField(_('defendant count'), blank=True, null=True)
    scope = models.ForeignKey(CaseScope, verbose_name=_('case scope'),
                              blank=True, null=True, on_delete=models.SET_NULL)
    coup_related = models.BooleanField(_('coup attempt related'), default=False)
    journalists = models.ManyToManyField(Journalist, through='CaseJournalist')
    plaintiff = models.ForeignKey(Plaintiff, verbose_name=_('plaintiff'),
                                  blank=True, null=True, on_delete=models.SET_NULL)
    prosecutor = models.ForeignKey(Prosecutor, verbose_name=_('prosecutor'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    judge = models.ForeignKey(Judge, verbose_name=_('presiding judge'), blank=True, null=True, on_delete=models.SET_NULL)
    board = models.ManyToManyField(Judge, verbose_name=_('board of judges'),
                                   related_name='board_memberships', blank=True)
    defendant_attorneys = models.ManyToManyField(Attorney, verbose_name=_('defendant attorneys'), blank=True)

    related_cases = models.ManyToManyField('self', verbose_name=_('related cases'), blank=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    def __str__(self):
        return f"{self.court} / {self.no}"

    def get_absolute_url(self):
        return reverse('case_detail', args=[self.id])

    def status(self):
        return self.casestatus_set.last()

    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('cases')


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
    decision_type = models.PositiveSmallIntegerField(
        _('decision type'), blank=True, null=True,
        choices=(
            (0, _('acquittal')),
            (1, _('fine')),
            (2, _('imprisonment')),
        )
    )
    punishment_amount = models.CharField(_('punishment amount'), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('case - journalist relation')
        verbose_name_plural = _('case - journalist relations')


class Indictment(models.Model):
    category = models.PositiveSmallIntegerField(verbose_name=_('category'), blank=True, null=True)
    definition = models.CharField(_('type'), max_length=200)

    def __str__(self):
        return self.definition

    class Meta:
        verbose_name = _('indictment type')
        verbose_name_plural = _('indictment types')


class Article(models.Model):
    type = models.PositiveSmallIntegerField(choices=(
        (1, _('TCK')),
        (2, _('TMK')),
        (3, _('Constitution')),
    ))
    no = models.CharField(max_length=20)
    punishment_type = models.PositiveSmallIntegerField(
        _('punishment type'), blank=True, null=True,
        choices=(
            (1, _('fine')),
            (2, _('imprisonment')),
        )
    )
    punishment_amount_min = models.CharField(_('minimum punishment due'), max_length=100, blank=True, null=True)
    punishment_amount_max = models.CharField(_('maximum punishment due'), max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_display()} {self.no}"

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class CaseIndictment(models.Model):
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    indictment = models.ForeignKey(
        Indictment, verbose_name=_('indictment type'),
        blank=True, null=True, on_delete=models.SET_NULL
    )
    articles = models.ManyToManyField(Article, verbose_name=_('articles'))
    details = models.TextField(_('details'), blank=True, null=True)

    def __str__(self):
        return self.type.type

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
    file = models.FileField(_('file'))
    type = models.ForeignKey(CaseDocumentType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(_('description'), blank=True, null=True)
    publish = models.BooleanField(_('publish'), default=True)

    class Meta:
        verbose_name = _('case document')
        verbose_name_plural = _('case documents')


class CaseNote(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    type = models.ForeignKey(
        NoteType, verbose_name=_('type'),
        blank=True, null=True, on_delete=models.SET_NULL,
    )
    note = models.TextField(_('note'))
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')


# trials

class Trial(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    session_no = models.PositiveIntegerField(_('session'))
    time_announced = models.DateTimeField(_('announced time'))
    time_start = models.DateTimeField(_('start time'), blank=True, null=True)
    observers = models.ManyToManyField(Institution, verbose_name=_('institutional observers'), blank=True)
    summary = models.TextField(_('summary'), blank=True, null=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('added time'), auto_now=True)

    def __str__(self):
        return f'{self.case}:{self.session_no}'

    def get_absolute_url(self):
        return reverse('trial_detail', kwargs={'case': self.case.id, 'pk': self.id})

    class Meta:
        verbose_name = _('trial')
        verbose_name_plural = _('trials')


class TrialNote(models.Model):
    trial = models.ForeignKey('Trial', verbose_name=_('trial'), on_delete=models.CASCADE)
    type = models.ForeignKey(
        NoteType, verbose_name=_('type'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    note = models.TextField(_('note'), blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')


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

    class Meta:
        verbose_name = _('trial document type')
        verbose_name_plural = _('trial document types')


class TrialDocument(models.Model):
    trial = models.ForeignKey(Trial, verbose_name=_('trial'), on_delete=models.CASCADE)
    file = models.FileField(_('file'))
    type = models.ForeignKey(TrialDocumentType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('trial document')
        verbose_name_plural = _('trial documents')
