from django.views.generic import ListView, DetailView
from jinac.infographics.models import Infographic


class InfographicListView(ListView):
    model = Infographic

    def get_queryset(self):
        qs = super().get_queryset().filter(publish=True)
        if self.request.LANGUAGE_CODE == 'en':
            qs = qs.filter(lang='en')
        else:
            qs = qs.filter(lang='tr')
        return qs


class InfographicDetailView(DetailView):
    model = Infographic

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)
