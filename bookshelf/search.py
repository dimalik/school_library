from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


import simplejson

from haystack.query import SearchQuerySet
from haystack.forms import FacetedSearchForm
from bookshelf.forms import SearchForm
from bookshelf.models import Item, Author, Publisher, Category, Locations

from bookshelf.views import FacetedSearchView



import simplejson
from django.template import loader


def generic_search_function(request_get_dict):
    """
    implements a generic search function to be used both with
    simple and advanced searches. It expects a request.GET 
    dictionary with either query, author, publisher, category,
    year, language, status, tags, location
    
    Returns a dict object containing all the appropriate
    results filtered.
    """
    query = request_get_dict.get('query', '')    
    author = request_get_dict.getlist('author[]', '')
    publisher = request_get_dict.getlist('publisher[]', '')
    category = request_get_dict.get('category', '')
    year = request_get_dict.getlist('year[]', '')
    language = request_get_dict.get('language[]', '')
    status = request_get_dict.get('status', '')
    tags = request_get_dict.get('tags[]', '')
    location = request_get_dict.getlist('location[]', '')
    


    sqs = SearchQuerySet().filter(title=query)
    
    if author:
        sqs = sqs.filter(author__in=author)

    if publisher:
        sqs = sqs.filter(publisher__in=publisher)
        
    if category:
        sqs = sqs.filter(category=category)
        
    if year:
        sqs = sqs.filter(year__in=year)
    
    if language:
        sqs = sqs.filter(language=language)
        
    if location:
        sqs = sqs.filter(location__in=location)
        
    if status:
        if status == 'true':
            sqs = sqs.filter(status=True)
        else:
            sqs = sqs.filter(status=False)
            
    return [Item.objects.get(pk=result.pk) for result in sqs]
    

    
def faceted_search(searchqueryset_obj):
    """
    returns all the objects that occur in the sqs obj and their
    occurences.
    """
    
    results = {}
    
    results['books'] = [Item.objects.get(pk=result.pk) for result in searchqueryset_obj]
    
    def count_occurences(itemlist):
        
        result_dict = {}
        
        for item in itemlist:
            result_dict[item] = itemlist.count(item)
        
        return result_dict    
        
    def get_authors(results):
        
        authors = [author for author in book.author.all() if author.name for book in results]
        
        authors = []
        
        for book in results:
            for author in book.author.all():
                if author.name:
                    authors.append(author)
        
        return count_occurences(authors)
        
    results['authors']     = get_authors(results['books'])        
    results['publishers']  = count_occurences([item.publisher for item in results['books'] if item.publisher.name])
    results['years']       = count_occurences([item.year for item in results['books'] if item.year])
    results['locations']   = count_occurences([item.location for item in results['books'] if item.location])
    results['languages']   = count_occurences([item.language for item in results['books'] if item.language])
    
    return results    
   
  


def advanced_search_view(request):
    if request.method == "GET":
        form = SearchForm()
        return render(request, 'search/advanced.html', {'form': form})
    return HttpResponseRedirect(FacetedSearchView, kwargs={'searchqueryset':'sa'})
    
    
def simple_search_view(request):
    
    """
    search_view implements searching in the database with the
    help of django-haystack.
    
    1. it expects a request.GET['query']
    2. searches the database against that query and returns the results,
       the authors of the results, their categories etc.
    3. if the request is_ajax() that means we have a filter call
    4. search_view receives a request.GET['query'] plus a filter
       the idea is that whatever it receives it sends back with the
       appropriate data filtered
    """
    import pdb
    pdb.set_trace()

    #sqs= generic_search_function(request.GET)
    #context_data = faceted_search(sqs)
        
    if request.is_ajax():
       
        t = loader.get_template('search/search_results/book_results.html')
        html = t.render(RequestContext(request,{'results': sqs}))
        return HttpResponse(simplejson.dumps({'html': html}))
        
    return render_to_response(
                'search/search_results.html',
                {
                'filtered': sqs,
                'sqs': context_data,
                'results': context_data['books'],
                'query': request.GET.get('query',''),
                'author': request.GET.get('author', ''),
                'publisher': request.GET.get('publisher', ''),
                'category' : request.GET.get('category', ''),
                'year' : request.GET.get('year', ''),
                'language' : request.GET.get('language', ''),
                'status' : request.GET.get('status', ''),
                'tags' : request.GET.get('tags', ''),
                'location' : request.GET.get('location', ''),  
                },
                context_instance=RequestContext(request)
                )