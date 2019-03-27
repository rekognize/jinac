from django.apps import AppConfig
from django.utils.translation import pgettext_lazy as _


class ArticlesConfig(AppConfig):
    name = 'jinac.articles'
    verbose_name = _('blog', 'articles')
