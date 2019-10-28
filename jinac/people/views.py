from django.db.models import Max, F
from django.views.generic import ListView, DetailView
from jinac.people.models import Journalist

qs = Journalist.objects.all()
class JournalistListView(ListView):
    model = Journalist

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(publish=True).exclude(short_bio__isnull=True).exclude(photo__isnull=True).\
            exclude(short_bio='').exclude(photo='')
        if self.request.LANGUAGE_CODE == 'en':
            qs = qs.exclude(bio_en__isnull=True).exclude(bio_en='')
        if self.request.GET.get('f'):
            qs = qs.filter(name__istartswith=self.request.GET.get('f'))
        if self.request.GET.get('s'):
            status = self.request.GET.get('s')
            qs = qs.filter(
                journaliststatus__end_date__isnull=True
            ).annotate(status=F('journaliststatus__status')).annotate(
                last_date=Max('journaliststatus__start_date')
            ).filter(journaliststatus__start_date=F('last_date'))
            if status == 'jailed':
                qs = qs.filter(status__in=[3, 4, 8])
            elif status == 'prosecuted':
                qs = qs.filter(status__in=[1, 3, 5, 8])
            elif status == 'pending':
                qs = qs.filter(status=1)
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
