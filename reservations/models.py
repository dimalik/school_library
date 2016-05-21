# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
import datetime

from bookshelf.models import Item


class Reservation(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Χρήστης')
    book = models.ForeignKey(Item, verbose_name=u'Βιβλίο')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Η κράτηση έγινε')
    reserved_until = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=2), editable=False,
                                          verbose_name=u'Η κράτηση ισχύει μέχρι')
    class Meta:
        verbose_name = u'Κράτηση'
        verbose_name_plural = u'Κρατήσεις'

    def __unicode__(self):
        return "%s: %s" % (self.user.username, self.book)   