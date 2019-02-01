from django.contrib import admin
from jinac.jurisdiction.models import Location, Court, CourtType, Attorney, Prosecutor, Judge, TrialType, \
    DecisionType, Prison, PrisonType, PunishmentType, IndictmentType


@admin.register(Location, Court, CourtType, Attorney, Prosecutor, Judge, TrialType, DecisionType, Prison, PrisonType,
                PunishmentType, IndictmentType)
class JurisdictionAdmin(admin.ModelAdmin):
    pass
