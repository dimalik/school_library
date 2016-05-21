# -*- coding: utf-8 -*-
from django.db import models

from bookshelf.models import Item


class InPresentation(models.Model):
    book = models.ForeignKey(Item, verbose_name=u'Βιβλίο')
    display_from = models.DateField(blank=True, verbose_name=u'Προβολή από')
    display_until = models.DateField(blank=True, verbose_name=u'Προβολή μέχρι')
    
    class Meta:
        verbose_name = u'Παρουσίαση'
        verbose_name_plural = u'Παρουσιάσεις'
    
    def __unicode__(self):
        return "%s" % (self.book.title)