import csv
from io import StringIO
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from jinac.jurisdiction.models import City, Court, Prison
from jinac.cases.models import Case
from jinac.people.models import Journalist


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cases_count', 'cases')
    list_filter = ('type', 'city')
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
            writer.writerow([
                obj.__str__(), self.cases_count(obj), self.cases(obj),
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="mahkemeler.csv"'
        return response
    download.short_description = _('Download')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'court_count', 'cases_count', 'cases')
    actions = ['download']

    def court_count(self, obj):
        return obj.court_set.distinct().count()
    court_count.short_description = _('courts')

    def cases_count(self, obj):
        court_ids = obj.court_set.values_list('id').distinct()
        return Case.objects.filter(court__id__in=court_ids).distinct().count()
    cases_count.short_description = _('cases')

    def cases(self, obj):
        court_ids = obj.court_set.values_list('id').distinct()
        return '; '.join([c.__str__() for c in Case.objects.filter(court__id__in=court_ids)])
    cases.short_description = _('cases')

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for obj in qs:
            writer.writerow([
                obj.name, self.court_count(obj), self.cases_count(obj), self.cases(obj),
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="sehirler.csv"'
        return response
    download.short_description = _('Download')


@admin.register(Prison)
class PrisonAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'journalist_count', 'journalists')
    list_filter = ('type', 'city')
    list_editable = ['city']
    actions = ['download']

    def journalist_count(self, obj):
        journalist_ids = []
        for js in obj.journaliststatus_set.filter(prison=obj):
            current_status = js.journalist.current_status()
            if current_status and js.status == current_status.status:
                journalist_ids.append(js.journalist.id)
                break
        return Journalist.objects.filter(id__in=journalist_ids).distinct().count()
    journalist_count.short_description = _('journalists')

    def journalists(self, obj):
        journalist_ids = []
        for js in obj.journaliststatus_set.filter(prison=obj):
            current_status = js.journalist.current_status()
            if current_status and js.status == current_status.status:
                journalist_ids.append(js.journalist.id)
                break
        return '; '.join([j.name for j in Journalist.objects.filter(id__in=journalist_ids)])
    journalists.short_description = _('journalists')

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for obj in qs:
            writer.writerow([
                obj.name, obj.get_type_display(), obj.city,
                self.journalist_count(obj), self.journalists(obj),
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="cezaevleri.csv"'
        return response
    download.short_description = _('Download')
