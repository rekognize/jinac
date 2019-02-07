from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from jinac.views import IndexView
from jinac.cases.views import CaseListView
from jinac.people.views import JournalistListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('davalar/', CaseListView.as_view(), name='case_list'),
    path('gazeteciler/', JournalistListView.as_view(), name='journalist_list'),
]


admin.site.index_title = _('Press in Arrest')
admin.site.site_header = _('Press in Arrest Administration')
admin.site.site_title = _('Press in Arrest Management')
