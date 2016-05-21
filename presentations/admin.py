from presentations.models import InPresentation
from django.contrib import admin

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('book', 'display_from', 'display_until',)
    fieldsets = (
                            (None, {
                            'fields': ('book', 'display_from', 'display_until',),
                            },
                            ),
                            )

admin.site.register(InPresentation, PresentationAdmin)