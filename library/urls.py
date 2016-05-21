from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from library.views import HomeView, AboutView, ContactView, HelpView

admin.autodiscover()

## Base Views
urlpatterns = patterns(
        'library.views',
        url(r'^$', HomeView.as_view(), name='library_home_view'),
        url(r'^help/$', HelpView.as_view(), name='library_help_view'),
        url(r'^about/$', AboutView.as_view(), name='library_about_view'),
        url(r'^contact/$', ContactView.as_view(), name='library_contact_view'),
        url(r'^timeline/', 'timeline_view', name='library_timeline_view'),
)

## Login Views

## External App Views
urlpatterns += patterns(
    '',
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^taggit_autocomplete_modified/', include('taggit_autocomplete_modified.urls')),
#    url(r'^grappelli/', include('grappelli.urls')),

)

## App Views
urlpatterns += patterns(
    '',
    url(r'^lists/', include('lists.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/(?P<username>(?!signout|signin)[\.\w-]+)/$',
       'library.views.my_profile_detail',
       name='userena_profile_detail'),
    url(r'^accounts/', include('userena.urls')),
#    url(r'^settings/', include('livesettings.urls')),
    url(r'^bookshelf/', include('bookshelf.urls')),
    url(r'^reservations/', include('reservations.urls')),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    #url(r'^transactions/', include('transaction.urls')),
)

urlpatterns += patterns(
    'library.views',
    url(r'^help/search/$', 'help_search', name='library_help_search_view'),
    url(r'^help/browse/$', 'help_browse', name='library_help_browse_view'),
    url(r'^help/lists/$', 'help_lists', name='library_help_lists_view'),
    url(r'^help/reservations/$', 'help_reservations', name='library_help_reservations_view'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
