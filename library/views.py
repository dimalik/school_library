#!/usr/bin/python
# -*- coding: utf-8 -*-

# stdlib imports
from django.contrib import auth
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse, HttpResponseRedirect

import random
import datetime
import simplejson

from djangoratings.models import Vote
from userena import views as userena_views

from bookshelf.models import Item
from lists.models import BookList
from assignments.models import Assignment
from transactions.models import Transaction
from reservations.models import Reservation
from presentations.models import InPresentation
from suggestions.models import Suggestion

def my_profile_detail(request, username):
    black_list = ["signup", "",]
    if username in black_list:
        raise Http404    
    reservations = Reservation.objects.filter(user=request.user)
    assignments = Assignment.objects.filter(participants__username=request.user.username)
    booklists = BookList.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    ratings = Vote.objects.filter(user=request.user)

    response = userena_views.profile_detail(
        request,
        username,
        extra_context={
            'reservations': reservations,
            'assignments': assignments,
            'booklists': booklists,
            'transactions': transactions,
            'ratings': ratings,
        }
    )
        
    return response


class HomeView(TemplateView):
    template_name = 'library/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            to_present = InPresentation.objects.filter(display_from__lte=datetime.date.today(), display_until__gte=datetime.date.today())
            to_present = [x.book for x in to_present]
            try:
                context['book_present'] = random.sample(to_present, 5)
            except ValueError:
                context['book_present'] = random.sample(to_present, len(to_present))
        except ValueError:
            pass
        try:
            to_suggest = Suggestion.objects.filter(display_from__lte=datetime.date.today(), display_until__gte=datetime.date.today())
            to_suggest = [x.book for x in to_suggest]
            try:
                context['in_suggestions'] = random.sample(to_suggest, 10)
            except ValueError:
                context['in_suggestions'] = random.sample(to_suggest, len(to_suggest))
        except ValueError:
            pass
        context['books'] = Item.available_books.all().order_by("-rating_score")[:5]
        context['lists'] = BookList.objects.all()[:5]
        context['assignments'] = Assignment.objects.all()[:5]

        return context


class AboutView(TemplateView):
    template_name = 'library/about.html'
    

def timeline_view(request):
    return render(request, 'library/timeline.html')


class ContactView(TemplateView):
    template_name = 'library/contact.html'


class HelpView(TemplateView):
    template_name = 'library/help.html'
    
def help_search(request):
    return render(request, 'library/help/search.html')
    
def help_browse(request):
    return render(request, 'library/help/browse.html')

def help_lists(request):
    return render(request, 'library/help/lists.html')

def help_reservations(request):
    return render(request, 'library/help/reservations.html')
