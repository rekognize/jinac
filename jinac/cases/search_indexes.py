from haystack import indexes
from unidecode import unidecode
from jinac.cases.models import Case


class CaseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    name_en = indexes.CharField(model_attr='name_en', null=True)
    summary = indexes.CharField(model_attr='summary', null=True)
    summary_en = indexes.CharField(model_attr='summary', null=True)

    def get_model(self):
        return Case

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publish=True)

    def prepare(self, obj):
        prepared = super().prepare(obj)
        prepared['text'] += '\n' + unidecode(prepared['text'])
        return prepared
