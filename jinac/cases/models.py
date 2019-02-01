from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from jinac.journalists.models import Journalist, Institution
from jinac.jurisdiction.models import Court, Judge, Prosecutor, Attorney, TrialType, DecisionType, PunishmentType, \
    IndictmentType, ViolationType


# cases

class Case(models.Model):
    no = models.CharField(max_length=20)
    name = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateField()
    parent_case = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    court = models.ForeignKey(Court, blank=True, null=True, on_delete=models.SET_NULL)

    reporter = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.no


class Indictment(models.Model):
    type = models.ForeignKey(IndictmentType, on_delete=models.CASCADE)
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
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
    journalists = models.ManyToManyField(Journalist, blank=True)
    date = models.DateField()


# trials

class WitnessType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Witness(models.Model):
    name = models.CharField(max_length=100)
    for_against = models.NullBooleanField()
    type = models.ForeignKey(WitnessType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('witness')
        verbose_name_plural = _('witnesses')


class Trial(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    type = models.ForeignKey(TrialType, blank=True, null=True, on_delete=models.SET_NULL)
    session_no = models.PositiveIntegerField()
    journalist_count = models.PositiveIntegerField()
    defendant_count = models.PositiveIntegerField()
    time = models.DateTimeField()
    prosecutor = models.ForeignKey(Prosecutor, blank=True, null=True, on_delete=models.SET_NULL)
    judge = models.ForeignKey(Judge, blank=True, null=True, on_delete=models.SET_NULL)
    board = models.ManyToManyField(Judge, related_name='board_memberships', blank=True)
    witnesses = models.ManyToManyField(Witness, blank=True)
    observers = models.ManyToManyField(Institution, verbose_name=_('Institutional observers'), blank=True)
    attorneys = models.ManyToManyField(Attorney, blank=True)
    summary = models.TextField(blank=True, null=True)

    reporter = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.case}:{self.session_no}'



class TrialViolation(models.Model):
    trial = models.ForeignKey('Trial', on_delete=models.CASCADE)
    type = models.ForeignKey(ViolationType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)


class TrialDocumentType(models.Model):
    file = models.FileField()
    description = models.TextField(blank=True, null=True)


class TrialDocument(models.Model):
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE)
    file = models.FileField()
    type = models.ForeignKey(TrialDocumentType, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)


class Decision(models.Model):
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE)
    type = models.ForeignKey(DecisionType, blank=True, null=True, on_delete=models.SET_NULL)
    punishment_type = models.ForeignKey(PunishmentType, blank=True, null=True, on_delete=models.SET_NULL)
    punishment_amount = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    journalists = models.ManyToManyField(Journalist, blank=True)
    is_final = models.BooleanField(default=False)
