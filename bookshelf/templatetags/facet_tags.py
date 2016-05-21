from django import template

from urllib import urlencode

register = template.Library()


@register.simple_tag
def remove_facet(request, facet_value):
    """"Returns a string that extracts the supplied facet_value's facect from
        the current querystring

        Example:
            {% load facet_tags %}
            {% remove_facet request value %}

        Renders:
            ?q=text&page=N
        or
            ?q=text&page=N&selected_facets=facet2:value
        if additional selected_facets are in the current querystring
    """
    params = []
    for param in request.GET.lists():
        # reconstruct the non-selected_facets params
        if param[0] != 'selected_facets':
            for v in param[1]:
                params.append((param[0], v))
        else:
            for v in param[1]:
                # exclude the selected_facet param that matches the supplied
                # facet_value
                if facet_value != v.split(':')[1]:
                    params.append((param[0], v))
    qs = urlencode(dict([k, v.encode('utf-8')] for k, v in params))

    
    return qs


@register.simple_tag
def faceted_next_prev_querystring(request, page_number):
    """"Returns a string that provides the querystring required to paginate in
        search results while retaining the selected facets

        Example:
            {% load facet_tags %}
            {% faceted_next_prev_querystring request page_number %}

        Renders:
           ?q=text&page=N&selected_facets=facet:value
    """
    q_dict = request.GET.copy()
    q_dict['page'] = page_number
    ans = {}
    for k, v in q_dict.items():
        print type(v)
        if type(v) != int:
            ans[k] = v.encode('utf-8')
        else:
            ans[k] = v

    qs = urlencode(ans)
    
    return qs


@register.filter(name="get_value")
def get_value(obj, original_field):
    obj_ = obj._object
    return getattr(obj_, original_field)
    

@register.filter(name="get_method")
def get_method(obj, original_method):
    obj_ = obj._object
    return getattr(obj_, original_method)()
    

@register.filter(name="get_authors")
def get_authors(obj):
    return obj._object.author.all()
    
    
@register.filter(name="get_publisher_name")
def get_publisher_name(obj):
    return obj._object.publisher.name
    
    
@register.filter(name="get_publisher_url")
def get_publisher_url(obj):
    if obj._object.publisher.name:
        return obj._object.publisher.get_absolute_url()
        
        
@register.filter(name="get_category_name")
def get_category_name(obj):
    return obj._object.category.title
    
    
@register.filter(name="get_category_url")
def get_category_url(obj):
    if obj._object.category.title:
        return obj._object.category.get_absolute_url()