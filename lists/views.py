# -*- coding: utf-8 -*-

from lists.models import BookList
from lists.forms import BookListCreateForm, BookListUpdateForm

from bookshelf.models import Item

from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse



from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin

import simplejson



class BookListCreate(LoginRequiredMixin, CreateView):
    model = BookList
    form_class = BookListCreateForm
    title = ''


    def form_valid(self, form):
        user = get_object_or_404(User, username =self.request.user.username)
        form.instance.user = user
        return super(BookListCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lists_all_lists')
        
    def get_context_data(self, **kwargs):
        context                 = super(BookListCreate, self).get_context_data(**kwargs)
        context['title']     = self.title
        
        if self.request.user.is_authenticated():
            context['mylists']     = BookList.objects.filter(user=self.request.user)

        return context

    
class BookListDetail(DetailView):
    model = BookList
    context_object_name = "lista"

    def get_context_data(self, **kwargs):
        context                 = super(BookListDetail, self).get_context_data(**kwargs)
        
        if self.request.user.is_authenticated():
            context['mylists']     = BookList.objects.filter(user=self.request.user)
        
        return context

    
class BookListList(ListView):
    model = BookList
    context_object_name = "listes"
    title = ''
    
    def get_context_data(self, **kwargs):
        context                 = super(BookListList, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            context['mylists']     = BookList.objects.filter(user=self.request.user)
            
        context['title']     = self.title
        
        return context
    

def add_book_view(request):
    book = Item.objects.get(id=request.POST['book'])
    booklist = BookList.objects.get(id=request.POST['list'])
    response_dict = {}
    
    if request.is_ajax() and request.method == "POST":
        if booklist.user == request.user:
            if book in booklist.books.all():
                response_dict.update({'content': u'Το βιβλίο αυτό υπάρχει ήδη στη λίστα σας.', 'code': 500})
                return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
            booklist.books.add(book)
            minima = u'Το βιβλίο %s προστέθηκε στη λίστα %s' % (book.title, booklist.title)
            response_dict.update({'content': minima, 'code': 201})
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
        raise Http404
    raise Http404    
       
class BookListDelete(DeleteView):
    model = BookList
    success_url = reverse_lazy('lists_all_lists')
    
    def get_context_data(self, **kwargs):
        context                 = super(BookListDelete, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            context['mylists']     = BookList.objects.filter(user=self.request.user)
        
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            raise Http404
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
    
    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
                    
        
        self.object = self.get_object()
        if self.object.user != request.user:
            raise Http404
        else:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())

    
class BookListUpdate(UpdateView):
    model = BookList
    form_class = BookListUpdateForm
    title = ''
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            raise Http404
        else:
            self.object = self.get_object()
            return super(BookListUpdate, self).get(request, *args, **kwargs)
            
    def get_context_data(self, **kwargs):
        context                 = super(BookListUpdate, self).get_context_data(**kwargs)
        context['title']     = self.title
        
        if self.request.user.is_authenticated():
            context['mylists']     = BookList.objects.filter(user=self.request.user)

        return context
