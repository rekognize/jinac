from django.contrib import admin
from jinac.people.models import Journalist, Attorney, Prosecutor, Judge
from jinac.cases.models import CaseJournalist


@admin.register(Attorney, Prosecutor, Judge)
class JurisdictionAdmin(admin.ModelAdmin):
    pass


class CaseInline(admin.TabularInline):
    model = CaseJournalist


@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    inlines = [CaseInline]
