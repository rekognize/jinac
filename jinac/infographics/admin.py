from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from jinac.infographics.models import Infographic
from martor.widgets import AdminMartorWidget
from martor.models import MartorField


@admin.register(Infographic)
class InfographicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'user', 'added', 'modified', 'lang', 'publish']
    search_fields = ['title', 'user', 'description']
    exclude = ['user']
    list_filter = ['publish', 'added', 'modified', 'user', 'lang']
    formfield_overrides = {
        MartorField: {'widget': AdminMartorWidget},
    }

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        is_reporter = request.user.groups.filter(name='Raportör').first()
        if is_reporter:
            fields.remove('publish')
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        reporter_group = Group.objects.filter(name='Raportör').first()
        if reporter_group:
            if reporter_group in request.user.groups.all():
                qs = qs.filter(reporter=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
