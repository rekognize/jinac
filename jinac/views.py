from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import translate_url
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.forms import ModelForm
from jinac.cases.models import Case, Trial
from jinac.news.models import Carousel, News, Info, Feed
from jinac.contact.models import Message


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'cases': Case.objects.filter(publish=True),
            'carousel': Carousel.objects.filter(publish=True),
            'news': News.objects.filter(publish=True)[:3],
            'upcoming_trials': Trial.objects.filter(time_next__gte=timezone.now()).order_by('time_next'),
            'info': {i.slug: i.value for i in Info.objects.all()},
            'feed': Feed.objects.all()[:5],
            'trials': Trial.objects.filter(publish=True).filter(case__publish=True).order_by('-modified')[:5]
        })
        return context


def set_language(request):
    next_page = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(next_page) if next_page else HttpResponseRedirect('/')
    lang_code = request.GET.get('lang')
    next_trans = translate_url(next_page, lang_code)
    if next_trans != next_page:
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


class ContactForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']


def contact_message(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            return render(request, 'contact/done.html')
    else:
        form = ContactForm()
    return render(
        request,
        'contact/form.html',
        {
            'form': form,
        }
    )
