from django.contrib import admin
from jinac.journalists.models import Journalist, WorkPosition, Institution, JournalistInstitution


@admin.register(Journalist, WorkPosition, Institution, JournalistInstitution)
class JournalistsAdmin(admin.ModelAdmin):
    pass
