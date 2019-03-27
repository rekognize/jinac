from django.shortcuts import render
from django.views.generic import ListView, DetailView
from jinac.cases.models import Case, Trial


class CaseListView(ListView):
    model = Case

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)


class CaseDetailView(DetailView):
    model = Case

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)


class TrialListView(ListView):
    model = Trial

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)


class TrialDetailView(DetailView):
    model = Trial

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)
