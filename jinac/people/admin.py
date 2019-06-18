from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from martor.widgets import AdminMartorWidget
from jinac.people.models import Journalist, JournalistStatus, Attorney, Prosecutor, Judge, Plaintiff, Complainant
from jinac.cases.models import CaseJournalist, CaseDocument, CaseIndictment, CaseNote


@admin.register(Attorney, Prosecutor, Judge, Plaintiff, Complainant)
class JurisdictionAdmin(admin.ModelAdmin):
    pass


@admin.register(CaseNote)
class CaseNoteAdmin(admin.ModelAdmin):
    list_display = ['journalist', 'case', 'type', 'time']
    list_editable = ['case', 'type']
    search_fields = ['case__name', 'journalist__name']


class CaseInline(admin.TabularInline):
    model = CaseJournalist
    extra = 1


class StatusInline(admin.TabularInline):
    model = JournalistStatus
    extra = 1


class CaseNoteInline(admin.StackedInline):
    model = CaseNote
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


class CaseIndictmentInline(admin.TabularInline):
    model = CaseIndictment
    extra = 1


class CaseDocumentInline(admin.TabularInline):
    model = CaseDocument
    extra = 1


class PhotoFilter(SimpleListFilter):
    title = _('photo')
    parameter_name = 'photo'

    def lookups(self, request, model_admin):
        return [('y', _('Yes')), ('n', _('No'))]

    def queryset(self, request, qs):
        if self.value() == 'y':
            qs = qs.exclude(photo__isnull=True).exclude(photo='')
        if self.value() == 'n':
            qs = qs.filter(Q(photo__isnull=True) | Q(photo=''))
        return qs


class ShortBioFilter(SimpleListFilter):
    title = _('short bio')
    parameter_name = 'photo'

    def lookups(self, request, model_admin):
        return [('y', _('Yes')), ('n', _('No'))]

    def queryset(self, request, qs):
        if self.value() == 'y':
            qs = qs.exclude(short_bio__isnull=True).exclude(short_bio='')
        if self.value() == 'n':
            qs = qs.filter(Q(short_bio__isnull=True) | Q(short_bio=''))
        return qs


@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    list_display = ['name', 'reporter', 'added', 'modified', 'publish']
    search_fields = ('name',)
    list_editable = ('publish',)
    list_filter = (
        'publish',
        PhotoFilter,
        ShortBioFilter,
    )
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        StatusInline,
        CaseInline,
        CaseIndictmentInline,
        CaseNoteInline,
        CaseDocumentInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            fields.remove('publish')
        return fields

    def save_model(self, request, obj, form, change):
        obj.reporter = request.user
        super().save_model(request, obj, form, change)
