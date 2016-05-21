#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
# stdlib imports
from django import forms
from django.core.paginator import Paginator, InvalidPage
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render_to_response, render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import six
# 3rdparty imports
from reportlab.pdfgen import canvas
import base64
import random
import simplejson
# app imports
from make_pdf import render_to_pdf
from assignments.models import Assignment
from lists.models import BookList
from djangoratings.views import AddRatingView
from bookshelf.models import Item, Author, Publisher, Category
import unidecode
from watson.views import SearchView as watsSearchView, SearchMixin

from bookshelf.forms import SearchForm, ItemForm

from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.views import FacetedSearchView
from haystack.forms import ModelSearchForm

from haystack.query import EmptySearchQuerySet


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


model_dict = {
    'books'     :   Item,
    'author'    :   Author,
    'publisher' :   Publisher,
    'category'  :   Category,
    }

def get_paginated_res(r, kwd):
    paginator = Paginator(kwd, 15)
    page = r.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    return [items, paginator.page_range]
    
    
class IndexView(TemplateView):
    
    template_name = 'bookshelf/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        books = Item.available_books.all()
        if books:
            try:
                context['books_to_present'] = random.sample(books, 8)
            except ValueError:
                context['books_to_present'] = random.sample(books, len(books))
        return context


def browse_view(request):
    return render_to_response('bookshelf/browse.html', context_instance=RequestContext(request))


def make_pdf_view(request):

    if request.is_ajax() and request.method == "GET":
        item = Item.objects.get(id=request.GET['book_id'])
        x = render_to_pdf('make_pdf.html', {'pagesize': 'A4', 'obj': item})
        return HttpResponse(x)
        
    raise Http404


def bibliography_view(request, slug):
    pass


def book_rate_view(request):
    if request.is_ajax and request.method == "POST":
        params = {
            'content_type_id'   :   ContentType.objects.get(model="item").id,
            'object_id'         :   request.POST['book'],
            'field_name'        :   'rating',
            'score'             :   request.POST['score'],
        }            
        response = AddRatingView()(request, **params)
        response_dict = {}
        response_dict.update({'content': response.content, 'code': response.status_code })
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        raise Http404

## Publishers


class PublisherDetail(DetailView):
    model               = Publisher
    context_object_name = 'ekdoths'

    def get_context_data(self, **kwargs):
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        def get_paginated_res(kwd):
            paginator = Paginator(kwd, 15)
            page = self.request.GET.get('page')
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
    
            return [items, paginator.page_range]
        x = get_paginated_res(Item.objects.filter(publisher__slug=self.kwargs['slug']))
        context['items'] = x[0]
        context['numpages'] = x[1]
        return context
        
    


class PublisherList(ListView):
    model = Publisher
    context_object_name = 'ekdotes'
    paginate_by = 15

## Authors


class AuthorDetail(DetailView):
    model = Author
    context_object_name = 'syggrafeas'
        
        
    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        def get_paginated_res(kwd):
            paginator = Paginator(kwd, 15)
            page = self.request.GET.get('page')
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
    
            return [items, paginator.page_range]
            
        ## San syggrafeas
        as_author = Item.objects.filter(author__slug=self.kwargs['slug'])
        as_editor = Item.objects.filter(editor__slug=self.kwargs['slug'])
        as_translator = Item.objects.filter(translator__slug=self.kwargs['slug'])
        import ipdb; ipdb.set_trace()
        results = list(chain(as_author, as_editor, as_translator))
        x = get_paginated_res(results)
        context['items'] = x[0]
        context['numpages'] = x[1]
        return context


class AuthorList(ListView):
    model = Author
    paginate_by = 15
    context_object_name = 'syggrafeis'

## Books


class ItemDetail(DetailView):
    model = Item
    context_object_name = 'vivlio'

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        context['ergasies'] = Assignment.objects.filter(book__slug=self.kwargs['slug']).order_by('-created_at')
        try:
            context['user_booklists'] = BookList.objects.filter(user=self.request.user) 
        except TypeError:
            pass
        return context


class ItemList(ListView):
    model = Item
    queryset = Item.available_books.all()
    #paginate_by = 15
    context_object_name = 'vivlia'

## Categories


class CategoryList(ListView):
    model = Category
    paginate_by = 15
    context_object_name = 'kathgories'
    
    
def view_alphabetically(request):
    return render(request, 'bookshelf/alphabetically.html')
    

def view_alphabetically_author(request):
    return render(request, 'bookshelf/alphabetically_author.html')
    
def view_publishers(request):
    return render(request, 'bookshelf/alphabetically_publishers.html')
    
def view_publishers_alphabetically(request, letter):
    publishers_filtered = Publisher.objects.filter(name__startswith=letter)
    x = get_paginated_res(request, publishers_filtered)
    return render(request, 'bookshelf/alphabetically_letter_publisher.html', {'items' : x[0], 'numpages': x[1]})

    


def getYears():
    years = sorted([d.values()[0] for d in Item.objects.values('year').distinct() if d.values()[0] != None])
    centuries = [''.join([x, str('00')]) for x in sorted(list(set([str(x)[:2] for x in years])))]
    decades = [''.join([x, str('0')]) for x in sorted(list(set([str(x)[:3] for x in years])))]
    return (years, centuries, decades,)
    
    
def view_by_year(request):
    return render(request, 'bookshelf/year_index.html', {'centuries': getYears()[0], 'decades': getYears()[2]})
    
def view_by_year_year(request, decade):
    years_filtered = Item.objects.filter(year__startswith=str(decade)[:3]).order_by('year')
    dec = ''.join([str(decade[:3]), '0'])
    x = get_paginated_res(request, years_filtered)
    return render(request, 'bookshelf/year_decade.html', {'items' : x[0], 'numpages': x[1],'centuries': getYears()[0], 'decades': getYears()[2], 'dec': dec})

    
    
    
def view_alphabetically_letter_author(request, name):
    authors_filtered = Author.objects.filter(name__startswith=name).order_by('name')
    x = get_paginated_res(request, authors_filtered)
    return render(request, 'bookshelf/alphabetically_letter_author.html', {'items' : x[0], 'numpages': x[1]})

    
    
    
def view_alphabetically_letter(request, letter):
    books_filtered = Item.objects.filter(title__startswith=letter).order_by('title')
    x = get_paginated_res(request, books_filtered)
    return render(request, 'bookshelf/alphabetically_letter.html', {'items' : x[0], 'numpages': x[1]})
    
    
def view_category_filter(request, code):
    literature = u"ΕΜ ΕΔ ΕΠ ΕΘ ΞΜ ΞΔ ΞΠ ΞΘ L ΒΞ ΒΕ".split()
    code_sw = code.rstrip("00")
    categories_filtered = Category.objects.filter(code__startswith=code_sw).order_by('code')
    extra = []
    if code_sw == "8":
        for item in literature:
            extra.append(Category.objects.filter(code__startswith=item)[0])
    ans = list(chain(categories_filtered, extra))
    return render(request, 'bookshelf/view_categories.html', {'items' : ans})
    
    
def view_category(request):
    return render(request, 'bookshelf/category_list.html')


class CategoryDetail(DetailView):
    model = Category
    context_object_name = 'kathgoria'
    
    

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        def get_paginated_res(kwd):
            paginator = Paginator(kwd, 15)
            page = self.request.GET.get('page')
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
    
            return [items, paginator.page_range]
        x = get_paginated_res(Item.objects.filter(category__slug=self.kwargs['slug']).order_by('title'))
        context['items'] = x[0]
        context['numpages'] = x[1]
        return context


class SearchBookshelf(watsSearchView):
    template_name = 'watson/res.html'
    
    def get_context_data(self, **kwargs):
        """Generates context variables."""
        context = super(SearchMixin, self).get_context_data(**kwargs)
        context["query"] = self.query
        def get_paginated_res(kwd):
            paginator = Paginator(kwd, 15)
            page = self.request.GET.get('page')
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
            
    
            return [items, paginator.page_range]
        x = [x.object for x in context['search_results']]
        x = get_paginated_res(x)
        context['items'] = x[0]
        context['numpages'] = x[1]
        # Process extra context.
        for key, value in six.iteritems(self.get_extra_context()):
            if callable(value):
                value = value()
            context[key] = value
        return context
    
    
class FacetedSearchCustomView(FacetedSearchView):
    """Overrides various default methods to allow for additional context, smoother
       UX for faceting
    """

    def build_page(self):
        """
        Paginates the results appropriately.

        Overriden to redirect to page 1 if a page_no is not found
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        paginator = Paginator(self.results, self.results_per_page)
        try:
            page = paginator.page(page_no)
        except InvalidPage:
            # Redirect to page 1 of the
            path = self.request.path
            qs = self.request.GET.copy()
            qs['page'] = 1
            url = '%s?%s' % (path, qs.urlencode())
            return redirect(url)

        return paginator, page

    def clean_filters(self):
        """Returns a list of tuples (filter, value) of applied facets"""
        filters = []
        # get distinct facets
        facets = list(set(self.form.selected_facets))
        for facet in facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)
            field = field.replace('_', ' ').replace('exact', '').title()
            filters.append((field, value))
        return filters

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.

        Overriding to allow the redirect to pass through from overriden build_page
        """
        try:
            (paginator, page) = self.build_page()
        except ValueError:
            return self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
            'numpages': range(1, paginator.num_pages + 1)
        }

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()
        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))

    def extra_context(self):
        extra = super(FacetedSearchCustomView, self).extra_context()
        extra['filters'] = self.clean_filters()
        if self.results == []:
            extra['facets'] = self.form.search().facet_counts()
        else:
            extra['facets'] = self.results.facet_counts()

        model_type = self.request.path.split('/')[1].rstrip('s')
        extra['model_type'] = None if model_type == "search" else model_type

        if model_type in ['package', 'project']:
            extra['facets'] = self.clean_facets(extra['facets'])
            extra['model_create'] = '%s_create' % model_type
        return extra

    def clean_facets(self, facets):
        """
        A helper function to deal with the fact that taxonomy gets is shared
        between two different models.
        """
        taxonomy_facets = facets.get('fields', {}).get('taxonomy')
        has_taxonomy = any([facet[1] for facet in taxonomy_facets])
        if has_taxonomy:
            return facets
        facets.get('fields', {}).pop('taxonomy')
        return facets
        
        
        
        
class SearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None, searchqueryset=None, context_class=RequestContext, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.context_class = context_class
        self.searchqueryset = searchqueryset

        if form_class is None:
            self.form_class = ModelSearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
            'numpages': range(1, paginator.num_pages + 1)
        }

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        #return render_to_response(self.template, context, context_instance=self.context_class(self.request))
        if self.query:
            return render_to_response('search/search.html', context, context_instance=self.context_class(self.request))
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
        