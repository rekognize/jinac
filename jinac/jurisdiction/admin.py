from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from jinac.jurisdiction.models import City, Court, Prison
from jinac.cases.models import Case


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cases_count', 'cases')
    list_filter = ('type', 'city')

    def cases_count(self, obj):
        return obj.case_set.count()
    cases_count.short_description = _('cases')

    def cases(self, obj):
        return '; '.join([c.__str__() for c in obj.case_set.all()])
    cases.short_description = _('cases')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'court_count', 'cases_count', 'cases')

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


@admin.register(Prison)
class PrisonAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    list_filter = ('type',)
