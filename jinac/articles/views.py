from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views.generic import ListView, DetailView, TemplateView
from jinac.articles.models import Article


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        qs = super().get_queryset().filter(publish=True)
        qs = qs.exclude(about_page=True)
        if self.kwargs.get('report'):
            qs = qs.filter(type='r')
        else:
            qs = qs.filter(type='a')
        if self.request.LANGUAGE_CODE == 'en':
            qs = qs.filter(lang='en')
        else:
            qs = qs.filter(lang='tr')
        return qs


class ArticleDetailView(DetailView):
    model = Article

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish=True)

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if article.type == 'r' and not self.kwargs.get('report'):
            return redirect('report_detail', slug=article.slug)
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        if article.lang != get_language() and article.translation:
            return article.translation
        return article


class AboutView(TemplateView):
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(publish=True).filter(about_page=True)
        if self.request.LANGUAGE_CODE == 'en':
            articles = articles.filter(lang='en')
        else:
            articles = articles.filter(lang='tr')
        context.update({
            'article': articles.first()
        })
        return context
