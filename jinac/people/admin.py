import csv
from io import StringIO
from django.http import HttpResponse
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from martor.widgets import AdminMartorWidget
from jinac.people.models import Journalist, JournalistStatus, Attorney, Prosecutor, Judge, Plaintiff, \
    JOURNALIST_STATUS_CHOICES
from jinac.cases.models import CaseJournalist, CaseDocument, CaseIndictment, CaseNote, WorkPosition, Case, \
    TrialDocument


@admin.register(Attorney, Judge)
class JurisdictionAdmin(admin.ModelAdmin):
    pass


@admin.register(Prosecutor)
class ProsecutorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'indictment_cases_count',
        'indictment_cases',
        'trials_count',
        'trials',
    )
    actions = ['download']

    def indictment_cases_count(self, obj):
        return obj.case_set.count()
    indictment_cases_count.short_description = _('indictment prosecutor')

    def indictment_cases(self, obj):
        return '; '.join([c.__str__() for c in obj.case_set.all()])
    indictment_cases.short_description = _('indictment prosecutor')

    def trials_count(self, obj):
        return obj.trial_set.values_list('case').distinct().count()
    trials_count.short_description = _('trial prosecutor')

    def trials(self, obj):
        case_ids = obj.trial_set.values_list('case').distinct()
        return '; '.join([c.__str__() for c in Case.objects.filter(id__in=case_ids)])
    trials.short_description = _('trial prosecutor')

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for obj in qs:
            writer.writerow([
                obj.name, self.indictment_cases_count(obj), self.indictment_cases(obj),
                self.trials_count(obj), self.trials(obj),
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="savcilar.csv"'
        return response
    download.short_description = _('Download')


@admin.register(Plaintiff)
class PlaintiffAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cases_count',
        'cases',
    )
    actions = ['download']

    def cases_count(self, obj):
        return obj.case_set.count()
    cases_count.short_description = _('cases')

    def cases(self, obj):
        return '; '.join([c.__str__() for c in obj.case_set.all()])
    cases.short_description = _('cases')

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for obj in qs:
            writer.writerow([obj.name, self.cases_count(obj), self.cases(obj)])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="davacilar.csv"'
        return response
    download.short_description = _('Download')


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


class TrialDocumentInline(admin.TabularInline):
    model = TrialDocument
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


class JournalistStatusFilter(SimpleListFilter):
    title = _('journalist status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return JOURNALIST_STATUS_CHOICES

    def queryset(self, request, qs):
        if self.value():
            ids = []
            for j in qs.all():
                status = j.current_status()
                if status:
                    if status.status == int(self.value()):
                        ids.append(j.id)
            qs = qs.filter(id__in=ids)
        return qs


class JournalistPositionFilter(SimpleListFilter):
    title = _('journalist position')
    parameter_name = 'position'

    def lookups(self, request, model_admin):
        return [(p.id, p.position) for p in WorkPosition.objects.all()]

    def queryset(self, request, qs):
        if self.value():
            ids = [cj.journalist.id for cj in CaseJournalist.objects.filter(position__id=self.value())]
            qs = qs.filter(id__in=ids)
        return qs


@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    list_display = ['name', 'institutions', 'get_current_status', 'reporter', 'added', 'modified', 'publish']
    search_fields = ('name',)
    list_editable = ('publish',)
    list_filter = (
        'publish',
        PhotoFilter,
        ShortBioFilter,
        JournalistStatusFilter,
        JournalistPositionFilter,
        'gender',
    )
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        StatusInline,
        CaseInline,
        CaseIndictmentInline,
        CaseNoteInline,
        CaseDocumentInline,
        TrialDocumentInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    actions = ['download']

    def get_current_status(self, obj):
        current_status = obj.current_status()
        if current_status:
            return current_status.get_status_display()
    get_current_status.short_description = _('status')

    def institutions(self, obj):
        institutions = []
        for case_journalist in obj.casejournalist_set.all():
            institution = []
            if case_journalist.institution:
                institution.append(case_journalist.institution.name)
            if case_journalist.position:
                institution.append(case_journalist.position.position)
            if institution:
                institutions.append(' - '.join(institution))
        return '; '.join(institutions)
    institutions.short_description = _('institutions')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            fields.remove('publish')
        return fields

    def save_model(self, request, obj, form, change):
        obj.reporter = request.user
        super().save_model(request, obj, form, change)

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for obj in qs:
            writer.writerow([
                obj.name, self.institutions(obj), self.get_current_status(obj),
                obj.reporter, obj.added, obj.modified,
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="gazeteciler.csv"'
        return response
    download.short_description = _('Download')
