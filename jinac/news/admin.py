from django.contrib import admin
from jinac.news.models import Carousel, News, Info, Feed
from django.db import models
from martor.widgets import AdminMartorWidget


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['text', 'link', 'added', 'publish']
    list_editable = ['publish']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'added', 'publish']
    list_editable = ['publish']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_editable = ['value']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ['object', 'time']
