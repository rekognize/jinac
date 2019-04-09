from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.urls import translate_url
from django.utils.translation import LANGUAGE_SESSION_KEY
from jinac.cases.models import Case, Trial
from jinac.news.models import Carousel, News


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'cases': Case.objects.filter(publish=True),
            'carousel': Carousel.objects.filter(publish=True),
            'news': News.objects.filter(publish=True)[:3],
            'upcoming_trials': Trial.objects.filter(time_next__gte=timezone.now()).order_by('time_next'),
        })
        return context


def set_language(request):
    #next = request.META.get('HTTP_REFERER')
    next = '/'
    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)
    lang_code = request.GET.get('lang')
    next_trans = translate_url(next, lang_code)
    if next_trans != next:
        response = HttpResponseRedirect(next_trans)
    if hasattr(request, 'session'):
        request.session[LANGUAGE_SESSION_KEY] = lang_code
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
    )
    return response
