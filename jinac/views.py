import os
import json
import uuid
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import translate_url
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.forms import ModelForm
from django.db.models import Max, F, Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from martor.utils import LazyEncoder
from captcha.fields import ReCaptchaField
from jinac.cases.models import Case, Trial
from jinac.news.models import Carousel, News, Info, Feed
from jinac.people.models import Journalist, JournalistStatus
from jinac.articles.models import Article
from jinac.contact.models import Message


class ContactForm(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Message
        fields = ['name', 'email', 'message']


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stats = JournalistStatus.objects.filter(journalist__publish=True).filter(
            end_date__isnull=True
        ).annotate(current_status=F('status')).annotate(
            last_date=Max('start_date')
        ).filter(start_date=F('last_date'))
        context.update({
            'cases': Case.objects.filter(publish=True),
            'carousel': Carousel.objects.filter(publish=True),
            'news': News.objects.filter(publish=True)[:3],
            'upcoming_trials': Trial.objects.filter(time_next__gte=timezone.now()).order_by('time_next'),
            'info': {i.slug: i.value for i in Info.objects.all()},
            'stats': {
                'prosecuted': Journalist.objects.filter(publish=True).count(),
                'jailed': stats.filter(end_date__isnull=True).filter(
                    current_status__in=[3, 4, 8]  # [2, 3, 4, 8]
                ).count(),
                'pending_trial': stats.filter(end_date__isnull=True).filter(
                    current_status__in=[1]  # [5, 6, 7]
                ).count(),
            },
            'feed': Feed.objects.all()[:5],
            'trials': Trial.objects.filter(publish=True).filter(case__publish=True).order_by('-modified')[:5],
            'pending_trial': Trial.objects.filter(publish=True).filter(case__publish=True).order_by('-modified')[:5],
            'contact_form': ContactForm(),
        })
        return context


class SearchResultView(TemplateView):
    template_name = 'search_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        q = self.request.GET.get('q')
        context.update({
            'articles': q and Article.objects.filter(
                Q(title__icontains=q) | Q(subtitle__icontains=q) | Q(summary__icontains=q)
            ).distinct(),
            'journalists': q and Journalist.objects.filter(
                Q(name__icontains=q) | Q(short_bio__icontains=q) | Q(short_bio_en__icontains=q) |
                Q(bio__icontains=q) | Q(bio_en__icontains=q)
            ).distinct(),
            'cases': q and Case.objects.filter(
                Q(name__icontains=q) | Q(name_en__icontains=q) | Q(summary__icontains=q) | Q(summary_en__icontains=q) |
                Q(casenote__note__icontains=q) | Q(casenote__note_en__icontains=q) |
                Q(trial__trialnote__note__icontains=q) |
                Q(journalists__name=q)
            ).distinct(),
            'q': q,
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
    captcha = ReCaptchaField()

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


@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))