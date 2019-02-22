from django.contrib import admin
from jinac.people.models import Journalist, JournalistStatus, Attorney, Prosecutor, Judge, Plaintiff
from jinac.cases.models import CaseJournalist


@admin.register(Attorney, Prosecutor, Judge, Plaintiff)
class JurisdictionAdmin(admin.ModelAdmin):
    pass


class CaseInline(admin.TabularInline):
    model = CaseJournalist
    extra = 1


class StatusInline(admin.TabularInline):
    model = JournalistStatus
    extra = 1


@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        StatusInline,
        CaseInline,
    ]
