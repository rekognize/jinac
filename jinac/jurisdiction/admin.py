from django.contrib import admin
from jinac.jurisdiction.models import City, Court, Prison


@admin.register(City, Court, Prison)
class JurisdictionAdmin(admin.ModelAdmin):
    pass
