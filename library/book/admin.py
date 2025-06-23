from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display   = ('name', 'display_authors', 'count')
    search_fields  = ('name',)
    list_filter    = ('authors__surname', 'name')

    # authors больше НЕ указываем здесь — только «простые» поля
    fieldsets = (
        ('Static data',  {'fields': ('name', 'description')}),
        ('Mutable data', {'fields': ('count',)}),
    )

    # вывод виджета выбора авторов сбоку
    filter_horizontal = ('authors',)      # можно filter_vertical = ('authors',)

    def display_authors(self, obj):
        return ', '.join(f'{a.name} {a.surname}' for a in obj.authors.all())
    display_authors.short_description = 'Authors'
