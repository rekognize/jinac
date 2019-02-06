from django.contrib import admin
from jinac.journalists.models import Journalist
from jinac.cases.models import Trial, Case


class TrialInline(admin.TabularInline):
    model = Trial


class CaseInline(admin.TabularInline):
    model = Case


@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    inlines = [
#        CaseInline
    ]
