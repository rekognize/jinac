from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from translations.admin import TranslatableAdmin, TranslationInline
from jinac.cases.models import Indictment, CaseIndictment, Case, CaseNote, CaseDocument, ViolationType, TrialViolation,\
    Trial, TrialDocumentType, TrialDocument, TrialNote, CaseNoteType, TrialNoteType, CaseJournalist, CaseScope, \
    WorkPosition, CaseDocumentType, CaseStatus, Article, CaseDecision


@admin.register(Indictment, ViolationType, TrialViolation, TrialDocumentType, TrialDocument,
                CaseNoteType, TrialNoteType, CaseScope, WorkPosition, CaseDocumentType, CaseIndictment, Article)
class CasesAdmin(admin.ModelAdmin):
    pass


# cases

class CaseIndictmentInline(admin.TabularInline):
    model = CaseIndictment
    extra = 1


class CaseCaseDecisionInline(admin.TabularInline):
    model = CaseDecision
    extra = 1


class CaseNoteInline(admin.TabularInline):
    model = CaseNote
    extra = 1


class CaseDocumentInline(admin.TabularInline):
    model = CaseDocument
    extra = 1


class CaseJournalistInline(admin.TabularInline):
    model = CaseJournalist
    extra = 1


class CaseStatusInline(admin.TabularInline):
    model = CaseStatus
    extra = 1


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    inlines = [
        CaseJournalistInline,
        CaseIndictmentInline,
        CaseDocumentInline,
        CaseNoteInline,
        CaseCaseDecisionInline,
        CaseStatusInline,
    ]
    list_display = ['no', 'journalist_names', 'scope', 'court', 'status', 'reporter']
    list_editable = ['scope']
    search_fields = ['journalists__name', 'scope__scope', 'court__city__name']
    exclude = ['reporter']
    filter_horizontal = ['board', 'related_cases']
    list_filter = ['publish', 'opening_date', 'modified', 'scope', 'coup_related', 'reporter']

    def journalist_names(self, obj):
        return ', '.join([j.name for j in obj.journalists.all()])
    journalist_names.short_description = _('journalists')

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
        obj.reporter = request.user
        super().save_model(request, obj, form, change)


# trials

class TrialNoteInline(admin.TabularInline):
    model = TrialNote
    extra = 1


class TrialDocumentInline(admin.TabularInline):
    model = TrialDocument
    extra = 1


class TrialViolationInline(admin.TabularInline):
    model = TrialViolation
    extra = 1


@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    inlines = [
        TrialViolationInline,
        TrialNoteInline,
        TrialDocumentInline,
    ]
    list_display = ['case', 'session_no', 'reporter']
    exclude = ['reporter']
    filter_horizontal = ['observers']
    list_filter = ['publish', 'time_start', 'modified', 'reporter']

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
        obj.reporter = request.user
        super().save_model(request, obj, form, change)
