from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = patterns(
    'reservations.views',
    url(r'^make_reservation/$', 'make_reservation', name='reservations_create_reservation'),
    url(r'^delete_reservation/$', 'delete_reservation', name='reservations_delete_reservation'),
)