from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'book', 'created_at', 'plated_end_at', 'end_at')
    list_filter   = ('book__name', 'user__email', 'created_at')
    search_fields = ('book__name', 'user__email')
