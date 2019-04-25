from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from jinac.articles.models import Article, Section
from martor.widgets import AdminMartorWidget


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['article', 'title']
    search_fields = ['title', 'user', 'summary']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'user', 'added', 'modified', 'lang', 'publish']
    search_fields = ['title', 'user', 'summary']
    exclude = ['user']
    list_filter = ['publish', 'added', 'modified', 'user', 'lang']
    inlines = [SectionInline]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
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
