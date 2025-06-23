from django.contrib import admin
from django.utils.html import format_html_join, mark_safe

from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display  = ('surname', 'name', 'patronymic', 'book_count')
    search_fields = ('surname', 'name')
    list_filter   = ('surname',)

    readonly_fields = ('display_books',)

    fieldsets = (
        (None, {
            'fields': ('name', 'surname', 'patronymic'),
        }),
        ('Books by this author', {
            'fields': ('display_books',),
        }),
    )


    def book_count(self, obj):
        """Кол-во книг (для списка)."""
        return obj.books.count()
    book_count.short_description = 'Books'

    def display_books(self, obj):
        """HTML-список связанных книг (только для чтения)."""
        books = obj.books.all()
        if not books:
            return "—"
        html = format_html_join(
            mark_safe('<br>'),
            '<a href="/admin/book/book/{}/change/">{}</a>',
            ((b.id, b.name) for b in books)
        )
        return html

    display_books.short_description = 'Books'
