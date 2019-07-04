import csv
from io import StringIO, BytesIO
from django.http import HttpResponse
from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from translations.admin import TranslatableAdmin, TranslationInline
from jinac.cases.models import CaseIndictment, Case, CaseDocument, ViolationType, TrialViolation,\
    Trial, TrialDocumentType, TrialDocument, TrialNote, CaseNoteType, TrialNoteType, CaseJournalist, \
    WorkPosition, CaseDocumentType, CaseStatus, Article, CaseDecision, TrialDecision


@admin.register(ViolationType, TrialViolation, TrialDocumentType, TrialDocument, TrialDecision,
                CaseNoteType, TrialNoteType, WorkPosition, CaseDocumentType, CaseIndictment, Article)
class CasesAdmin(admin.ModelAdmin):
    pass


# cases

class CaseIndictmentInline(admin.TabularInline):
    model = CaseIndictment
    extra = 1


class CaseDecisionInline(admin.TabularInline):
    model = CaseDecision
    extra = 1


class CaseDocumentInline(admin.TabularInline):
    model = CaseDocument
    extra = 1


class CaseJournalistInline(admin.StackedInline):
    model = CaseJournalist
    extra = 1
    filter_horizontal = ['attorneys']


class CaseStatusInline(admin.TabularInline):
    model = CaseStatus
    extra = 1


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    inlines = [
        CaseJournalistInline,
        CaseIndictmentInline,
        CaseDocumentInline,
        CaseDecisionInline,
        CaseStatusInline,
    ]
    list_display = ['name', 'no', 'journalist_names', 'court', 'status', 'reporter', 'added', 'modified']
    search_fields = ['name', 'journalists__name', 'court__city__name']
    readonly_fields = ['reporter']
    filter_horizontal = ['related_cases', 'plaintiff']
    list_filter = ['publish', 'opening_date', 'modified', 'coup_related', 'reporter']
    actions = ['publish', 'download']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def get_actions(self, request):
        actions = super().get_actions(request)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            if 'publish' in actions:
                del actions['publish']
        return actions

    def journalist_names(self, obj):
        return ', '.join([j.name for j in obj.journalists.all().distinct()])
    journalist_names.short_description = _('journalists')

    def publish(self, request, queryset):
        for case in queryset:
            case.publish = True
            case.save()
            case.casedocument_set.update(publish=True)
    publish.short_description = _('Publish')

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for case in qs:
            writer.writerow([case.name, case.no, self.journalist_names(case), case.court, case.status()])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="davalar.csv"'
        return response
    download.short_description = _('Download')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            fields.remove('publish')
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        reporter_group = Group.objects.filter(name='Raportör').first()
        if reporter_group:
            if reporter_group in request.user.groups.all():
                qs = qs.filter(reporter=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.reporter:
            obj.reporter = request.user
        super().save_model(request, obj, form, change)


@admin.register(CaseDecision)
class CaseDecisionAdmin(admin.ModelAdmin):
    list_display = ['case', 'journalist', 'decision_type', 'get_punishment']
    actions = ['download']
    list_filter = ['decision_type']

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for decision in qs:
            writer.writerow([decision.case.name, decision.journalist.name, decision.get_decision_type_display(), decision.get_punishment()])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="kararlar.csv"'
        return response
    download.short_description = _('Download')


# trials

class TrialNoteInline(admin.TabularInline):
    model = TrialNote
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


class TrialDocumentInline(admin.TabularInline):
    model = TrialDocument
    extra = 1


class TrialViolationInline(admin.TabularInline):
    model = TrialViolation
    extra = 1


class TrialDecisionInline(admin.TabularInline):
    model = TrialDecision
    extra = 1


class UpcomingTrialsFilter(SimpleListFilter):
    title = _('upcoming trials')
    parameter_name = 'upcoming'

    def lookups(self, request, model_admin):
        return [
            ('u', _('Upcoming')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'u':
            queryset = queryset.filter(time_next__gte=timezone.now())
        return queryset


class ViolationsFilter(SimpleListFilter):
    title = _('violations')
    parameter_name = 'violation'

    def lookups(self, request, model_admin):
        return [(v.id, v.type) for v in ViolationType.objects.all()]

    def queryset(self, request, qs):
        if self.value():
            ids = [tv.trial.id for tv in TrialViolation.objects.filter(type__id=self.value())]
            qs = qs.filter(id__in=ids)
        return qs


@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    inlines = [
        TrialViolationInline,
        TrialNoteInline,
        TrialDocumentInline,
        TrialDecisionInline,
    ]
    list_display = ['case', 'session_no', 'reporter', 'added', 'modified', 'time_next', 'violations']
    readonly_fields = ['reporter']
    search_fields = ['case__name']
    filter_horizontal = ['observers', 'board']
    list_filter = ['publish', UpcomingTrialsFilter, 'time_start', 'modified', 'reporter', ViolationsFilter]
    actions = ['publish']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def get_actions(self, request):
        actions = super().get_actions(request)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            if 'publish' in actions:
                del actions['publish']
        return actions

    def violations(self, obj):
        return ', '.join([v.type.type for v in obj.trialviolation_set.all()])
    violations.short_description = _('Violations')

    def publish(self, request, queryset):
        for trial in queryset:
            trial.publish = True
            trial.save()
            trial.trialdocument_set.update(publish=True)
    publish.short_description = _('publish')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            fields.remove('publish')
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if 'Raportör' in [g.name for g in request.user.groups.all()]:
            qs = qs.filter(reporter=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.reporter:
            obj.reporter = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        # updates the CaseDecision by the TrialDecision if this is the last trial of the case
        instances = formset.save()
        trial_decisions_modified = False
        for instance in instances:
            if isinstance(instance, TrialDecision):
                trial_decisions_modified = True
                trial = instance.trial
                break
        if not trial_decisions_modified:
            for obj in formset.deleted_objects:
                if isinstance(obj, TrialDecision):
                    trial_decisions_modified = True
                    trial = obj.trial
                    break
        if trial_decisions_modified:
            last_trial = trial.case.trial_set.order_by('session_no').last()
            if trial == last_trial:
                case = trial.case
                case.casedecision_set.all().delete()
                for trial_decision in trial.trialdecision_set.all():
                    case_decision = CaseDecision.objects.create(
                        case=case,
                        journalist=trial_decision.journalist,
                        decision_type=trial_decision.decision_type,
                        punishment_year=trial_decision.punishment_year,
                        punishment_month=trial_decision.punishment_month,
                        punishment_day=trial_decision.punishment_day,
                        punishment_fine=trial_decision.punishment_fine,
                    )
                    case_decision.articles.add(*trial_decision.articles.all())
