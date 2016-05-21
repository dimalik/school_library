# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect

from bookshelf.models import Item
from reservations.models import Reservation
from bookshelf.models import BookNotAvailableError


def make_reservation(request):
    if request.is_ajax() and request.method == "POST":
        user = request.user
        book = Item.objects.get(id=request.POST['book'])
        response_dict = {}

        if not book.status:
            msg = (u'Το βιβλίο αυτό δεν είναι διαθέσιμο', 404,)
        elif Reservation.objects.filter(user=user).count() > 4:
            msg = (u'Έχετε υπερβεί τον μέγιστο αριθμό κρατήσεων', 500,)
        elif Reservation.objects.filter(user__username=user).filter(book__title=book.title).count() >= 1:
            msg = (u'Έχετε κάνει ήδη κράτηση για το συγκεκριμένο βιβλίο', 500,)
        else:
            res = Reservation()
            res.user = user
            res.book = book
            try:
                book.num_available_copies -= 1
                book.save()
                res.save()
            except BookNotAvailableError:
                raise Http404
            msg = (u'Η κράτησή σας έγινε με επιτυχία', 201,)
            response_dict['content'], response_dict['code'] = msg[0], msg[1]
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        raise Http404


def delete_reservation(request):
    if request.is_ajax() and request.method == "POST":
        reservation = Reservation.objects.get(id=request.POST['reservation_id'])
        if request.user != reservation.user:
            raise Http404
        else:
            reservation.delete()
            response_dict = {}
            response_dict.update({'content': 'to vivlio diagrafike apo ti lista kratisewn sas'})
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    raise Http404