from haystack import indexes
from bookshelf.models import Item, Author, Publisher


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    publisher = indexes.CharField(faceted=True, null=True)
    author = indexes.MultiValueField(faceted=True, indexed=True)
    category = indexes.CharField(faceted=True, null=True)
    language = indexes.CharField(model_attr='language', faceted=True, null=True)
    bibcode = indexes.CharField(model_attr='bib_code', null=True)
    crcode = indexes.IntegerField(model_attr='cr_code', null=True)
    status = indexes.BooleanField(model_attr='status', faceted=True, null=True)
    subtitle = indexes.CharField(model_attr='subtitle', null=True)
    year = indexes.IntegerField(model_attr='year', faceted=True, null=True)
    series = indexes.CharField(model_attr='series', null=True)
    location = indexes.CharField(null=True) ## na to ftiaksw

    def get_model(self):
        return Item
		
	def prepare_author(self,obj):
	    if obj.author.all().count():
	        return [author.pk for author in obj.author.all()]
	    return [u"Default"]
        
    def prepare_publisher(self, obj):
        if obj.publisher.name:
            return obj.publisher.name
        return obj.publisher.pk
        
    def prepare_category(self, obj):
        if obj.category.title:
            return obj.category.title
        return obj.category.code
        
    def prepare_location(self, obj):
        return obj.location.title

class AuthorIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	name = indexes.EdgeNgramField(model_attr='name')

	def get_model(self):
		return Author