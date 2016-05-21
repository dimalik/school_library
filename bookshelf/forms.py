# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from ajax_select import make_ajax_field

from bookshelf.models import Item, Author, Publisher, Category, Locations
from bookshelf.declarations import *

from haystack.forms import SearchForm
from haystack.forms import ModelSearchForm

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

        group  = make_ajax_field(Item,'author','author',help_text=None)
        
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        # self.initial['cr_code']= Item.objects.order_by('-cr_code')[0].cr_code + 1

    def clean(self):
        """
        Checks that there exists either the author or the editor
        """
        author = self.cleaned_data.get('author')
        editor = self.cleaned_data.get('editor')
        if not author and not editor:
            raise ValidationError(u"Πρέπει να υπάρχει τουλάχιστον ένας συγγραφέας ή ένας επιμελητής έκδοσης")
        return self.cleaned_data
        
        
        
class FacetedSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super(FacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(FacetedSearchForm, self).search()
        

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        return sqs



class MySearchForm(SearchForm):

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()
            
        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs


class ItemSearchForm(MySearchForm):
    
    types = [forms.IntegerField, forms.CharField, forms.ModelChoiceField]
    
    year = forms.IntegerField(required=False,label=YEAR)
    publisher = forms.CharField(required=False,label=PUBLISHER)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label=CATEGORY,required=False)
    issue = forms.IntegerField(required=False, label=ISSUE)
    editor = forms.CharField(required=False, label=EDITOR)
    series = forms.CharField(required=False, label=SERIES)
    volume = forms.IntegerField(required=False, label=VOLUME)
    ser_num = forms.IntegerField(required=False, label=SER_NUM)
    edition = forms.IntegerField(required=False, label=EDITION)
    subtitle = forms.CharField(required=False, label=SUBTITLE)
    proelefsi = forms.CharField(required=False, label=u'Προέλευση')
    num_pages = forms.IntegerField(required=False,label=PAG_NUM)
    translator = forms.CharField(required=False, label=u'Μεταφραστής')
    location = forms.ModelChoiceField(queryset=Locations.objects.all(), required=False, label=u"Τοποθεσία")
    status = forms.BooleanField(required=False, label=AVAILABLE)
    cr_code = forms.IntegerField(required=False, label=CR_CODE)
    bib_code = forms.CharField(required=False, label=BIB_CODE)
    num_copies = forms.IntegerField(required=False, label=NUM_COPIES)
    num_available_copies = forms.IntegerField(required=False, label=u"Αριθμός διαθέσιμων βιβλίων")
    isbn = forms.IntegerField(required=False)
    
    
    
    
    
    def search(self):
        FIELDS = ['year', 'publisher', 'category', 'issue', 'editor', 'series', 'volume', 'ser_num',
                  'edition', 'subtitle', 'proelefsi', 'num_pages', 'translator', 'location',]
        sqs = super(ItemSearchForm, self).search()
        if not sqs:
            pass ## do something else with the data we have
        
        if not self.is_valid():
            return self.no_query_found()
            
        for field in FIELDS:
            if self.cleaned_data[field]:
                d = {field: self.cleaned_data[field]}
                sqs = sqs.filter(**d)
        
            
        return sqs
