# stdlib imports
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from bookshelf.views import ItemDetail, PublisherDetail, AuthorDetail, CategoryDetail, IndexView, FacetedSearchCustomView, SearchView, SearchBookshelf

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

from bookshelf.forms import ItemSearchForm, FacetedSearchForm


from djangoratings.views import AddRatingFromModel


#sqs = SearchQuerySet().facet('language').facet('status').facet('publisher').facet('category').facet('location')


urlpatterns = patterns(
    'bookshelf.views',
    url(r'^$', IndexView.as_view(), name='bookshelf_index_view'),
    
    url(r'^books/$', 'view_alphabetically', name='bookshelf_alphabetically_view'),
    url(r'^books/(?P<letter>\D{1})/$', 'view_alphabetically_letter', name='bookshelf_alphabetically_letter_view'),
    url(r'^authors/$', 'view_alphabetically_author', name='bookshelf_authorlist_view'),
    url(r'^authors/(?P<name>[\w-]+)/$', 'view_alphabetically_letter_author', name='bookshelf_alphabetically_letter_author_view'),
    url(r'^years/$', 'view_by_year', name='bookshelf_year_view'),
    url(r'^years/(?P<decade>\d{4})/$', 'view_by_year_year', name='bookshelf_year_view_year'),
    url(r'^categories/$', 'view_category', name='bookshelf_categorylist_view'),
    url(r'^categories/(?P<code>\d{3})/$', 'view_category_filter', name='bookshelf_category_filter_view'),
    url(r'^publishers/$', 'view_publishers', name='bookshelf_publisher_view'),
    url(r'^publishers/(?P<letter>\D{1})/$', 'view_publishers_alphabetically', name='bookshelf_publisher_alphabetically_view'),
    


    url(r'^book/(?P<slug>[\w-]+)/', ItemDetail.as_view(), name='bookshelf_itemdetail_view'),
    url(r'^author/(?P<slug>[\w-]+)/$', AuthorDetail.as_view(), name='bookshelf_authordetail_view'),
    url(r'^category/(?P<slug>[\w-]+)/$', CategoryDetail.as_view(), name='bookshelf_categorydetail_view'),
    url(r'^publisher/(?P<slug>[\w-]+)/$', PublisherDetail.as_view(), name='bookshelf_publisherdetail_view'),

    url(r'^browse/$', 'browse_view', name='bookshelf_browse_view'),
    url(r'^make_pdf/$', 'make_pdf_view', name="bookshelf_pdf_view"),
    url(r'^book_rate/$', 'book_rate_view', name='bookshelf_book_rate_view'),
    url(r'^bibliography/$', 'bibliography_view', name="bookshelf_bibliography_view"),
    
)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

sqs = SearchQuerySet()
facet_list = ('language', 'status', 'publisher', 'category', 'location',)
for facet in facet_list:
    sqs = sqs.facet(facet)

# urlpatterns += patterns('haystack.views',
#     url(r'^search/$',
#         FacetedSearchCustomView(form_class=FacetedSearchForm, searchqueryset=sqs),
#         name='bookshelf_search_view',
#     ),
# )+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns(
    'haystack.views',
    url(r"^search/", SearchBookshelf.as_view(), name='bookshelf_search_view'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += patterns(
    'bookshelf.search',
    url(r'^search/advanced/$', search_view_factory(
        view_class=SearchView,
        template='search/advanced_search.html',
        form_class=ItemSearchForm
    ), name='bookshelf_advanced_search_view'),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
