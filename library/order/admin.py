from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'get_books', 'created_at', 'plated_end_at', 'end_at')
    list_filter   = ('books', 'user__email', 'created_at')
    search_fields = ('books__name', 'user__email')

    def get_books(self, obj):
        return ", ".join(book.name for book in obj.books.all())
    get_books.short_description = 'Books'
