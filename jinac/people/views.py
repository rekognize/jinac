from django.views.generic import ListView, DetailView
from jinac.people.models import Journalist


class JournalistListView(ListView):
    model = Journalist

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)


class JournalistDetailView(DetailView):
    model = Journalist

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)
