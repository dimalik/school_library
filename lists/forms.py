# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

from ajax_select import make_ajax_field

from lists.models import BookList


class BookListCreateForm(ModelForm):
    class Meta:
        model = BookList
        fields = ('title', 'books', 'public', 'description', 'image',)
        
    books  = make_ajax_field(BookList,'books','item',help_text=u"Πληκτρολογήστε για να ξεκινήσει η αναζήτηση.")
    
    


class BookListUpdateForm(ModelForm):
    class Meta:
        model = BookList
        fields = ('title', 'books', 'public',)
        
    books  = make_ajax_field(BookList,'books','item',help_text=u"Πληκτρολογήστε για να ξεκινήσει η αναζήτηση.")
