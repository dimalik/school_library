from import_export import resources
from bookshelf.models import Item

class ItemResource(resources.ModelResource):
    
    class Meta:
        model = Item
        exclude = ('tags',)