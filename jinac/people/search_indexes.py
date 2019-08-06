from haystack import indexes
from unidecode import unidecode
from jinac.people.models import Journalist


class JournalistIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Journalist

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publish=True)

    def prepare(self, obj):
        prepared = super().prepare(obj)
        prepared['text'] += '\n' + unidecode(prepared['text'])
        return prepared
