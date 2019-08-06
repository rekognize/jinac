from haystack import indexes
from unidecode import unidecode
from jinac.articles.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publish=True)

    def prepare(self, obj):
        prepared = super().prepare(obj)
        prepared['text'] += '\n' + unidecode(prepared['text'])
        return prepared
