# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from bookshelf.models import Item
from django.core.exceptions import ValidationError

import datetime

from bookshelf.models import BookNotAvailableError


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Χρήστης")
    book = models.ForeignKey(Item, verbose_name="Βιβλίο", blank=True, null=True)
    isbn = models.CharField(max_length=255, verbose_name="ISBN", blank=True, null=True)
    date_issued = models.DateField(verbose_name="Ημερομηνία δανεισμού", auto_now_add=True,
                                   null=True)
    date_due = models.DateField(verbose_name="Ημερομηνία επιστροφής", default=datetime.date.today() +
                                                                              datetime.timedelta(days=20))
    date_returned = models.DateField(verbose_name="Ημερομηνία που επεστράφη", auto_now=False,
                                     auto_now_add=False, blank=True, null=True)
                                     
    class Meta:
        verbose_name = u'Δανεισμός'
        verbose_name_plural = u'Δανεισμοί'
    
    def status(self):
        if self.date_due < datetime.date.today():
            return -1
        elif self.date_due < (datetime.date.today() + datetime.timedelta(days=5)):
            return 0
        else:
            return 1
            
    def return_book(self):
        if not self.book.status:
            self.book.status = True
        self.book.num_available_copies += 1
        self.book.save()
        if self.book.parapanw_antitypo:
            for book in Item.objects.filter(title=self.book.title):
                if not book.parapanw_antitypo:
                    if not book.status:
                        book.status = True
                    book.num_available_copies += 1
                    book.save()

    def clean(self):
        if not self.book:
            if not self.isbn:
                raise ValidationError(u'Πρέπει να δώσετε είτε το τίτλο του βιβλίου είτε κωδικό ISBN')
            if self.isbn:
                self.book = Item.objects.get(isbn=self.isbn)
        if self.book:
            if self.isbn:
                raise ValidationError(u'Πρέπει να δώσετε είτε το τίτλο του βιβλίου είτε κωδικό ISBN')

    def save(self):
        if not self.book:
            self.book = Item.objects.get(isbn=self.isbn)
        try:
            self.book.num_available_copies -= 1
            self.book.save()
            if self.book.parapanw_antitypo:
                for book in Item.objects.filter(title=self.book.title):
                    if not book.parapanw_antitypo:
                        book.num_available_copies -= 1
                        book.save()
        except BookNotAvailableError: pass

        ## TODO: na kanw send_mail() ston daneizomeno otan daneistei vivlio

        super(Transaction, self).save()
        
    def __unicode__(self):
        return '{0}: {1}'.format(self.user, self.book)

