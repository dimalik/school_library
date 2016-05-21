# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from lists.models import BookList
from lists.views import BookListCreate, BookListDetail, BookListList, BookListUpdate, BookListDelete

urlpatterns = patterns(
	'lists.views',
	## listviews
	
	url(r'^$', BookListList.as_view(
							queryset = BookList.objects.order_by('-created_at')[:20],
							title = u'τελευταίες λίστες',
							), name='lists_recent_lists'), # recent
	url(r'^all/$', BookListList.as_view(
							queryset = BookList.objects.all().order_by('-created_at'),
							title = u'όλες οι λίστες',
							), name='lists_all_lists'), # all
	url(r'^userlists/$', BookListList.as_view(
							queryset = BookList.objects.filter(user__is_staff=False).order_by('-created_at'),
							title = u'οι λίστες των μαθητών μας',
							), name='lists_user_lists'), # user
	url(r'^suggested/$', BookListList.as_view(
							queryset = BookList.objects.filter(user__is_staff=True).order_by('-created_at'),
							title = u'προτεινόμενες λίστες βιβλίων',
							), name='lists_suggested_lists'), # suggested
	
	## listactions
	
	url(r'^add-book/$', 'add_book_view', name = 'lists_add_book'),
    url(r'^create/$', login_required(BookListCreate.as_view(title=u"δημιουργία νέας λίστας")), name = 'lists_create_list'),
	url(r'^(?P<slug>[\w-]+)/$', BookListDetail.as_view(), name = 'lists_view_list'),
	url(r'^(?P<slug>[\w-]+)/edit/$', BookListUpdate.as_view(title=u"επεξεργασία λίστας"), name = 'lists_edit_list'),
	url(r'^(?P<slug>[\w-]+)/delete/$', BookListDelete.as_view(), name = 'lists_delete_list'),
    

)