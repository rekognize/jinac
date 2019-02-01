from django.contrib import admin
from jinac.cases.models import Indictment, Case, ViolationType, TrialViolation, WitnessType, Witness, \
    Trial, TrialDocumentType, TrialDocument, Decision


@admin.register(Indictment, Case, ViolationType, TrialViolation, WitnessType, Witness,
                Trial, TrialDocumentType, TrialDocument, Decision)
class CasesAdmin(admin.ModelAdmin):
    pass
