import csv
from io import StringIO
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from jinac.institutions.models import Institution, Observer


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    actions = ['download']

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for obj in qs:
            writer.writerow([obj.name])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="kurumlar.csv"'
        return response
    download.short_description = _('Download')


@admin.register(Observer)
class ObserverAdmin(admin.ModelAdmin):
    actions = ['download']

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for obj in qs:
            writer.writerow([obj.name])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="gozlemciler.csv"'
        return response
    download.short_description = _('Download')
