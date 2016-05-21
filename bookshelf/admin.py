# -*- coding: utf-8 -*-

# stdlib imports
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.core.urlresolvers import reverse

import reversion
from import_export.admin import ImportExportMixin
# app imports
from bookshelf.forms import ItemForm
from bookshelf.models import Publisher, Author, Item, Category, Name, Locations

from merge import *

# def to_presentations(self, request, queryset):
#     for book in queryset:
#         book.in_presentation = not book.in_presentation
#         book.save()
# to_presentations.short_description = u"Προσθαφαίρεση στις βιβλιοπαρουσιάσεις"
#         
# def to_suggestions(self, request, queryset):
#     for book in queryset:
#         book.in_suggestions = not book.in_suggestions
#         book.save()
# to_suggestions.short_description = u"Προσθαφαίρεση στις προτάσεις"

def merge(self, request, queryset):
    main = queryset[0]
    temp = queryset[1:]
    
    tail = []
    for x in temp: tail.append(x)

    merge_model_objects(main, tail)
    
merge.short_description = u"Συγχώνευση επιλεγμένων εγγραφών"



class NameInline(admin.StackedInline):
    model = Name

class BookAdmin(reversion.VersionAdmin, ImportExportMixin, admin.ModelAdmin):
    list_display = ('machine_name', 'get_authors', 'year', 'category', 'cr_code', 'bib_code', 'status', 'num_copies', 'num_available_copies',)
    suit_form_tabs = (('general', u'Βασικά Στοιχεία'), ('internal', u'Στοιχεία Βιβλιοθήκης'),
                     ('other', u'Λοιπά Στοιχεία'))

    fieldsets = (
                                    (u'Βασικά Στοιχεία', {
                                    'classes': ('suit-tab suit-tab-general',),
                            'fields': ('title', 'subtitle', 'machine_name', 'author', 'publisher', 'year', 'language', 'category',),
                            'description': u"<p>Πρέπει να υπάρχει είτε συγγραφέας είτε επιμελητής</p>",
                            }),
                            (u'Στοιχεία Βιβλιοθήκης', {
                            'classes': ('suit-tab suit-tab-internal',),
                            'description': u"Ταξιθετικά στοιχεία -για εσωτερική χρήση",
                            'fields': ('bib_code', 'num_copies', 'cr_code', 'status', 'num_available_copies', 'published', 'isbn',)
                            }),
                            (u'Λοιπά Στοιχεία', {
                            'classes': ('suit-tab suit-tab-other',),
                            'fields': ('editor', 'notes', 'foto', 'volume',
                            'issue', 'translator', 'edition', 'series', 'ser_num',
                            'tags', 'num_pages', 'location')
                            }),
                            )

    search_fields = ('title', 'author__name', 'editor__name', 'translator__name', 'publisher__name', 'category__code', 'location__title', 'year', 'bib_code', )
    list_filter = ('status', 'published',)
    filter_horizontal = ('author', 'translator', 'editor',)
    form = ItemForm
    actions = [merge,]

from django.utils.safestring import mark_safe

class AuthorAdmin(reversion.VersionAdmin, ImportExportMixin, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'get_books_count', 'view_books',)
    
    def view_books(self, obj):
        return mark_safe(u'<a href="http://127.0.0.1:8000/admin/bookshelf/item/?q={0}"><i class="icon-search"></i></a>'.format(obj.name))
    view_books.short_description = u'Φιλτράρισμα'
    fieldsets = (
                            (None, {
                            'fields': ('name', 'fotografia', 'bio', ),
                            },
                            ),
                            )
    inlines = [NameInline, ]
    actions = [merge]


class PublisherAdmin(reversion.VersionAdmin, ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'get_books_count', 'view_books',)
    def view_books(self, obj):
        return mark_safe(u'<a href="http://127.0.0.1:8000/admin/bookshelf/item/?q={0}"><i class="icon-search"></i></a>'.format(obj.name))
    view_books.short_description = u'Φιλτράρισμα'
    fieldsets = (
                            (None, {
                            'fields': ('name', 'address', 'description', ),
                            },
                            ),
                            )
    actions = [merge]


class CategoryAdmin(reversion.VersionAdmin, ImportExportMixin, admin.ModelAdmin):
    list_display = ('code', 'title', 'get_books_count', 'view_books',)
    def view_books(self, obj):
        return mark_safe(u'<a href="http://127.0.0.1:8000/admin/bookshelf/item/?q={0}"><i class="icon-search"></i></a>'.format(obj.code))
    view_books.short_description = u'Φιλτράρισμα'
    fieldsets = (
                            (None, {
                            'fields': ('code', 'title', 'description',),
                            },
                            ),
                            )
    actions = [merge]
    
class LocationAdmin(reversion.VersionAdmin, ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'get_books_count', 'view_books',)
    def view_books(self, obj):
        return mark_safe(u'<a href="http://127.0.0.1:8000/admin/bookshelf/item/?q={0}"><i class="icon-search"></i></a>'.format(obj.title))
    view_books.short_description = u'Φιλτράρισμα'
    fieldsets = (
                            (None, {
                            'fields': ('title',),
                            },
                            ),
                            )                                 

admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Item, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Locations, LocationAdmin)
