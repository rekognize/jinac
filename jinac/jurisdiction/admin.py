from django.contrib import admin
from jinac.jurisdiction.models import City, Court, CourtType, Attorney, Prosecutor, Judge, TrialType, \
    DecisionType, Prison, PrisonType, PunishmentType, IndictmentType


@admin.register(City, Court, CourtType, Attorney, Prosecutor, Judge, TrialType, DecisionType, Prison, PrisonType,
                PunishmentType, IndictmentType)
class JurisdictionAdmin(admin.ModelAdmin):
    pass
