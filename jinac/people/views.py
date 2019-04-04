from django.views.generic import ListView, DetailView
from jinac.people.models import Journalist


class JournalistListView(ListView):
    model = Journalist

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(publish=True).exclude(short_bio__isnull=True).exclude(photo__isnull=True).\
            exclude(short_bio='').exclude(photo='')
        if self.request.GET.get('f'):
            qs = qs.filter(name__istartswith=self.request.GET.get('f'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'filter': self.request.GET.get('f')
        })
        return context


class JournalistDetailView(DetailView):
    model = Journalist

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)
