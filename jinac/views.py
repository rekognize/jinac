from django.shortcuts import render
from django.views.generic import TemplateView
from jinac.cases.models import Case


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'cases': Case.objects.all(),
        })
        return context
