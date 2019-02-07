from django.contrib import admin
from jinac.institutions.models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    pass
