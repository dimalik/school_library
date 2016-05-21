from django.contrib import admin
from reservations.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at', 'reserved_until',)


admin.site.register(Reservation, ReservationAdmin)