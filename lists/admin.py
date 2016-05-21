from lists.models import BookList
from django.contrib import admin

class BookListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'public', 'created_at', 'likes', 'get_book_count')
    fieldsets = (
                            (None, {
                            'fields': ('title', 'user', 'books', 'public', 'description', 'image', ),
                            },
                            ),
                            )
    list_filter = ('public',)
    filter_horizontal = ('books',)
    

admin.site.register(BookList, BookListAdmin)