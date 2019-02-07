from django.contrib import admin
from jinac.cases.models import Indictment, IndictmentType, Case, CaseNote, CaseDocument, ViolationType, TrialViolation,\
    Trial, TrialDocumentType, TrialDocument, TrialNote, NoteType, CaseJournalist, CaseScope


@admin.register(Indictment, ViolationType, TrialViolation, TrialDocumentType, TrialDocument, NoteType, IndictmentType,
                CaseScope)
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


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    inlines = [
        CaseJournalistInline,
        CaseNoteInline,
        CaseIndictmentInline,
        CaseDocumentInline,
    ]


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
