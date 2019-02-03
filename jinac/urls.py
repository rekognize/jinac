from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('admin/', admin.site.urls),
]


admin.site.index_title = _('Press in Arrest')
admin.site.site_header = _('Press in Arrest Administration')
admin.site.site_title = _('Press in Arrest Management')
