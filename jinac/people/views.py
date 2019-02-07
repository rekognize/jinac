from django.views.generic import ListView
from jinac.people.models import Journalist


class JournalistListView(ListView):
    model = Journalist

