from django.shortcuts import render
from django.views.generic import ListView
from jinac.cases.models import Case


class CaseListView(ListView):
    model = Case

