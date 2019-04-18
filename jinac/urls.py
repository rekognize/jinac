from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from jinac.views import IndexView, set_language
from jinac.cases.views import CaseListView, CaseDetailView, TrialListView, TrialDetailView
from jinac.people.views import JournalistListView, JournalistDetailView
from jinac.articles.views import ArticleListView, ArticleDetailView, AboutView


urlpatterns = [

    path('yonetim/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),

    path('davalar/', CaseListView.as_view(), name='case_list'),
    path('davalar/<int:pk>/', CaseDetailView.as_view(), name='case_detail'),
    path('davalar/raporlar/', TrialListView.as_view(), name='trial_list'),
    path('davalar/<int:case>/<int:pk>/', TrialDetailView.as_view(), name='trial_detail'),

    path('gazeteciler/', JournalistListView.as_view(), name='journalist_list'),
    path('gazeteciler/<slug:slug>/', JournalistDetailView.as_view(), name='journalist_detail'),

    path('analizler/', ArticleListView.as_view(), name='article_list'),
    path('analizler/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('ne-yapiyoruz/', AboutView.as_view(), name='about'),

    path('lang/', set_language, name='set_lang'),

    path(r'tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = _('Press in Arrest')
admin.site.site_header = _('Press in Arrest Administration')
admin.site.site_title = _('Press in Arrest Management')
