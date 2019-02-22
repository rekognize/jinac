from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.views.static import serve
from jinac.views import IndexView
from jinac.cases.views import CaseListView, CaseDetailView, TrialDetailView
from jinac.people.views import JournalistListView, JournalistDetailView


urlpatterns = [
    path('yonetim/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),

    path('davalar/', CaseListView.as_view(), name='case_list'),
    path('davalar/<int:pk>/', CaseDetailView.as_view(), name='case_detail'),
    path('davalar/<int:case>/<int:pk>/', TrialDetailView.as_view(), name='trial_detail'),

    path('gazeteciler/', JournalistListView.as_view(), name='journalist_list'),
    path('gazeteciler/<slug:slug>/', JournalistDetailView.as_view(), name='journalist_detail'),
]


if settings.DEBUG:
    urlpatterns += [
        path('media/<path>', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]


admin.site.index_title = _('Press in Arrest')
admin.site.site_header = _('Press in Arrest Administration')
admin.site.site_title = _('Press in Arrest Management')
