from django.contrib import admin
from django.contrib.auth.models import Group
from jinac.people.models import Journalist, JournalistStatus, Attorney, Prosecutor, Judge, Plaintiff,\
    JournalistNote, JournalistNoteType, Complainant
from jinac.cases.models import CaseJournalist, CaseDocument


@admin.register(Attorney, Prosecutor, Judge, Plaintiff, JournalistNote, JournalistNoteType, Complainant)
class JurisdictionAdmin(admin.ModelAdmin):
    pass


class CaseInline(admin.TabularInline):
    model = CaseJournalist
    extra = 1


class StatusInline(admin.TabularInline):
    model = JournalistStatus
    extra = 1


class JournalistNoteInline(admin.TabularInline):
    model = JournalistNote
    extra = 1


class CaseDocumentInline(admin.TabularInline):
    model = CaseDocument
    extra = 1


@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    list_display = ['name', 'reporter', 'added', 'modified']
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        StatusInline,
        CaseInline,
        JournalistNoteInline,
        CaseDocumentInline,
    ]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            fields.remove('publish')
        return fields

    def save_model(self, request, obj, form, change):
        obj.reporter = request.user
        super().save_model(request, obj, form, change)
