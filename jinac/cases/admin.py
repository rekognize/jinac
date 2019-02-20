from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from jinac.cases.models import Indictment, IndictmentType, Case, CaseNote, CaseDocument, ViolationType, TrialViolation,\
    Trial, TrialDocumentType, TrialDocument, TrialNote, NoteType, CaseJournalist, CaseScope, WorkPosition, \
    CaseDocumentType, CaseStatus


@admin.register(Indictment, ViolationType, TrialViolation, TrialDocumentType, TrialDocument, NoteType, IndictmentType,
                CaseScope, WorkPosition, CaseDocumentType)
class CasesAdmin(admin.ModelAdmin):
    pass


# cases

class CaseIndictmentInline(admin.TabularInline):
    model = Indictment
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
        CaseNoteInline,
        CaseIndictmentInline,
        CaseDocumentInline,
        CaseStatusInline,
    ]
    list_display = ['no', 'journalist_names', 'scope', 'court', 'status']
    list_editable = ['scope']
    search_fields = ['journalists__name', 'scope__scope', 'court__city__name']

    def journalist_names(self, obj):
        return ', '.join([j.name for j in obj.journalists.all()])
    journalist_names.short_description = _('journalists')


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
