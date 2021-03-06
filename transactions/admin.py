# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib import admin
from transactions.models import Transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

import datetime


def return_books(modeladmin, request, queryset):
    queryset.update(date_returned=datetime.date.today())
    for obj in queryset:
        obj.return_book()


return_books.short_description = u"Επιστροφή συγκεκριμένου βιβλίου"


class IsOnLoanFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'Καθυστέρηση')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'late'

    def lookups(self, request, model_admin):
        """
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
        return (
            ('nai', _(u'Έχει καθυστερήσει')),
            ('oxi', _(u'Δεν έχει καθυστερήσει')),
        )

    def queryset(self, request, queryset):

        """
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'nai':
            return queryset.filter(due__lte=datetime.datetime.today())
        if self.value() == 'oxi':
            return queryset.filter(due__gte=datetime.datetime.today())


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'date_issued', 'date_due', 'date_returned',)
    list_filter = (IsOnLoanFilter,)
    actions = [return_books]
    
    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'success',
            0: 'warning',
            -1: 'error',
        }.get(obj.status())
        if css_class:
            return {'class': css_class, 'data': obj.book.title}


admin.site.register(Transaction, TransactionAdmin)

