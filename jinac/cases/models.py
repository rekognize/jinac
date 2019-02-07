from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from jinac.jurisdiction.models import Court
from jinac.people.models import Journalist, Judge, Prosecutor, Attorney
from jinac.institutions.models import Institution


class NoteType(models.Model):
    type = models.CharField(_('type'), max_length=100)

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
    no = models.CharField(_('number'), max_length=20)
    name = models.CharField(_('name'), max_length=250, blank=True, null=True)
    parent_case = models.ForeignKey('self', verbose_name=_('parent case'),
                                    blank=True, null=True, on_delete=models.SET_NULL)
    court = models.ForeignKey(Court, verbose_name=_('court'),
                              blank=True, null=True, on_delete=models.SET_NULL)
    defendant_count = models.PositiveIntegerField(_('defendant count'), blank=True, null=True)
    scope = models.ForeignKey(CaseScope, verbose_name=_('case scope'), blank=True, null=True, on_delete=models.SET_NULL)
    journalists = models.ManyToManyField(Journalist, through='CaseJournalist')
    prosecutor = models.ForeignKey(Prosecutor, verbose_name=_('prosecutor'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    judge = models.ForeignKey(Judge, verbose_name=_('judge'), blank=True, null=True, on_delete=models.SET_NULL)
    board = models.ManyToManyField(Judge, verbose_name=_('board of judges'),
                                   related_name='board_memberships', blank=True)
    defendant_attorneys = models.ManyToManyField(Attorney, verbose_name=_('defendant attorneys'), blank=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('modified time'), auto_now=True)

    def __str__(self):
        return self.no

    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('cases')


class CaseJournalist(models.Model):
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    journalist = models.ForeignKey(Journalist, verbose_name=_('journalists'), on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution,
        verbose_name=_('institution'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    position = models.PositiveSmallIntegerField(
        _('position'), blank=True, null=True,
        choices=(
            (1, _('reporter')),
            (2, _('editor')),
        )
    )

    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('cases')


class IndictmentType(models.Model):
    definition = models.CharField(_('definition'), max_length=200)

    def __str__(self):
        return self.definition

    class Meta:
        verbose_name = _('indictment type')
        verbose_name_plural = _('indictment types')


class Indictment(models.Model):
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    type = models.ForeignKey(
        IndictmentType, verbose_name=_('indictment type'),
        blank=True, null=True, on_delete=models.SET_NULL
    )
    details = models.TextField(_('details'), blank=True, null=True)
    requested_punishment_type = models.PositiveSmallIntegerField(
        _('requested punishment type'),
        blank=True, null=True,
        choices=(
            (1, 'imprisonment'),
            (2, 'fine'),
        )
    )
    requested_punishment_amount = models.CharField(
        _('requested punishment amount'),
        max_length=100, blank=True, null=True
    )
    date = models.DateField(_('date'))

    class Meta:
        verbose_name = _('indictment')
        verbose_name_plural = _('indictments')


class CaseDocumentType(models.Model):
    file = models.FileField(_('file'))
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('case document type')
        verbose_name_plural = _('case document types')


class CaseDocument(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    file = models.FileField(_('file'))
    type = models.ForeignKey(CaseDocumentType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('case document')
        verbose_name_plural = _('case documents')


class CaseNote(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    note = models.TextField(_('note'))
    type = models.ForeignKey(
        NoteType, verbose_name=_('type'),
        blank=True, null=True, on_delete=models.SET_NULL,
    )
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
    time = models.DateTimeField(_('time'))
    observers = models.ManyToManyField(Institution, verbose_name=_('institutional observers'), blank=True)
    summary = models.TextField(_('summary'), blank=True, null=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)
    modified = models.DateTimeField(_('added time'), auto_now=True)

    def __str__(self):
        return f'{self.case}:{self.session_no}'

    class Meta:
        verbose_name = _('trial')
        verbose_name_plural = _('trials')


class TrialNote(models.Model):
    trial = models.ForeignKey('Trial', verbose_name=_('trial'), on_delete=models.CASCADE)
    note = models.TextField(_('note'))
    type = models.ForeignKey(
        NoteType, verbose_name=_('type'),
        blank=True, null=True, on_delete=models.SET_NULL,
    )
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
    file = models.FileField(_('file'))
    description = models.TextField(_('description'), blank=True, null=True)

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


class Decision(models.Model):
    trial = models.ForeignKey(Trial, verbose_name=_('trial'), on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(
        _('decision type'), blank=True, null=True,
        choices=(
            (1, _('interlocutory')),
            (2, _('definitive')),
        )
    )
    punishment_type = models.PositiveSmallIntegerField(
        _('decision type'),
        blank=True, null=True,
        choices=(
            (1, 'imprisonment'),
            (2, 'fine'),
            (3, 'probation'),
        )
    )
    punishment_amount = models.CharField(_('punishment amount'), max_length=100, blank=True, null=True)
    date = models.DateField(_('date'))
    journalists = models.ManyToManyField(Journalist, verbose_name=_('journalists'), blank=True)

    class Meta:
        verbose_name = _('decision')
        verbose_name_plural = _('decisions')
