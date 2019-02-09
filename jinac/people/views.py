from django.views.generic import ListView, DetailView
from jinac.people.models import Journalist


class JournalistListView(ListView):
    model = Journalist


class JournalistDetailView(DetailView):
    model = Journalist

