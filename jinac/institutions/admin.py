from django.contrib import admin
from jinac.institutions.models import Institution, Observer


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    pass


@admin.register(Observer)
class ObserverAdmin(admin.ModelAdmin):
    pass
