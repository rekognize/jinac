from django.shortcuts import render
from django.views.generic import ListView, DetailView
from jinac.cases.models import Case, Trial


class CaseListView(ListView):
    model = Case


class CaseDetailView(DetailView):
    model = Case


class TrialDetailView(DetailView):
    model = Trial
