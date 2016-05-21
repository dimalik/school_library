from assignments.models import Assignment
from django.contrib import admin
    
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'book',)
    fieldsets = (
                            (None, {
                            'fields': ('title', 'participants', 'book', 'file', 'description', ),
                            },
                            ),
                            )
    filter_horizontal = ('participants',)
    
    
admin.site.register(Assignment, AssignmentAdmin)
