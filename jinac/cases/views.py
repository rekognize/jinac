from django.views.generic import ListView, DetailView
from jinac.cases.models import Case, Trial


class CaseListView(ListView):
    model = Case

    def get_queryset(self):
        qs = super().get_queryset().filter(publish=True)
        if self.request.GET.get('f'):
            qs = qs.filter(name__istartswith=self.request.GET.get('f'))
        return qs.filter(publish=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'filter': self.request.GET.get('f')
        })
        return context


class CaseDetailView(DetailView):
    model = Case

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)


class TrialListView(ListView):
    model = Trial

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True).order_by('-time_start')


class TrialDetailView(DetailView):
    model = Trial

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)
