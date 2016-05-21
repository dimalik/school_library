from suggestions.models import Suggestion
from django.contrib import admin

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('book', 'display_from', 'display_until',)
    fieldsets = (
                            (None, {
                            'fields': ('book', 'display_from', 'display_until',),
                            },
                            ),
                            )
    
admin.site.register(Suggestion, SuggestionAdmin)
