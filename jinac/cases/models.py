from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from jinac.journalists.models import Journalist, Institution
from jinac.jurisdiction.models import Court, Judge, Prosecutor, Attorney, TrialType, DecisionType, PunishmentType, \
    IndictmentType, ViolationType


# cases

class Case(models.Model):
    no = models.CharField(_('number'), max_length=20)
    name = models.CharField(_('name'), max_length=250, blank=True, null=True)
    start_date = models.DateField(_('start date'))
    parent_case = models.ForeignKey('self', verbose_name=_('parent case'),
                                    blank=True, null=True, on_delete=models.SET_NULL)
    court = models.ForeignKey(Court, verbose_name=_('court'),
                              blank=True, null=True, on_delete=models.SET_NULL)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)

    def __str__(self):
        return self.no

    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('case')


class Indictment(models.Model):
    type = models.ForeignKey(IndictmentType, verbose_name=_('type'), on_delete=models.CASCADE)
    case = models.ForeignKey('Case', verbose_name=_('case'), on_delete=models.CASCADE)
    requested_punishment_type = models.ForeignKey(
        PunishmentType,
        verbose_name=_('requested punishment type'),
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    requested_punishment_amount = models.CharField(
        _('requested punishment amount'),
        max_length=100,
        blank=True, null=True
    )
    journalists = models.ManyToManyField(Journalist, verbose_name=_('journalists'), blank=True)
    date = models.DateField(_('date'))

    class Meta:
        verbose_name = _('indictment')
        verbose_name_plural = _('indictments')


# trials

class Trial(models.Model):
    case = models.ForeignKey(Case, verbose_name=_('case'), on_delete=models.CASCADE)
    type = models.ForeignKey(TrialType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    session_no = models.PositiveIntegerField(_('session'))
    journalist_count = models.PositiveIntegerField(_('journalist count'))
    defendant_count = models.PositiveIntegerField(_('defendant count'))
    time = models.DateTimeField(_('time'))
    prosecutor = models.ForeignKey(Prosecutor, verbose_name=_('prosecutor'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    judge = models.ForeignKey(Judge, verbose_name=_('judge'), blank=True, null=True, on_delete=models.SET_NULL)
    board = models.ManyToManyField(Judge, verbose_name=_('board of judges'),
                                   related_name='board_memberships', blank=True)
    observers = models.ManyToManyField(Institution, verbose_name=_('institutional observers'), blank=True)
    attorneys = models.ManyToManyField(Attorney, verbose_name=_('attorney'), blank=True)
    summary = models.TextField(_('summary'), blank=True, null=True)

    reporter = models.ForeignKey(User, verbose_name=_('reporter'), blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(_('added time'), auto_now_add=True)

    def __str__(self):
        return f'{self.case}:{self.session_no}'

    class Meta:
        verbose_name = _('trial')
        verbose_name_plural = _('trials')


class Note(models.Model):
    note = models.TextField(_('note'))

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')


class TrialViolation(models.Model):
    trial = models.ForeignKey('Trial', verbose_name=_('trial'), on_delete=models.CASCADE)
    type = models.ForeignKey(ViolationType, verbose_name=_('violation type'), on_delete=models.CASCADE)
    description = models.TextField(_('description'), blank=True, null=True)

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
    type = models.ForeignKey(DecisionType, verbose_name=_('type'), blank=True, null=True, on_delete=models.SET_NULL)
    punishment_type = models.ForeignKey(PunishmentType, verbose_name=_('punishment type'), blank=True, null=True, on_delete=models.SET_NULL)
    punishment_amount = models.CharField(_('punishment amount'), max_length=100, blank=True, null=True)
    date = models.DateField(_('date'))
    journalists = models.ManyToManyField(Journalist, verbose_name=_('journalists'), blank=True)
    is_final = models.BooleanField(_('is final decision'), default=False)

    class Meta:
        verbose_name = _('decision')
        verbose_name_plural = _('decisions')
