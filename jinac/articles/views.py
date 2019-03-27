from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from jinac.articles.models import Article


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)


class ArticleDetailView(DetailView):
    model = Article

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            # TODO: filter by current lang
            'article': Article.objects.filter(publish=True).filter(about_page=True).first()
        })
        return context
