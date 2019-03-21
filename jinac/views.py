from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from jinac.cases.models import Case, Trial
from jinac.news.models import Carousel, News


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'cases': Case.objects.all(),
            'carousel': Carousel.objects.filter(publish=True),
            'news': News.objects.filter(publish=True)[:3],
            'upcoming_trials': Trial.objects.filter(time_next__gte=timezone.now())
        })
        return context
