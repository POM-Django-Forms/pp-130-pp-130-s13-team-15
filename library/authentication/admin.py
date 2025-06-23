from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'email', 'first_name', 'last_name',
        'role', 'is_active', 'is_staff',
    )
    list_filter = (
        'role', 'is_active', 'is_staff',
    )
    search_fields = (
        'email', 'first_name', 'last_name',
    )
    ordering = ('email',)

    readonly_fields = (
        'last_login', 'created_at', 'updated_at',
    )

    fieldsets = (
        ('Credentials', {
            'fields': ('email', 'password'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'middle_name'),
        }),
        ('Permissions', {
            'fields': (
                'role', 'is_active', 'is_staff',
                'is_superuser', 'groups', 'user_permissions'
            ),
        }),
        ('Important dates', {
            'fields': (),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'first_name', 'last_name',
                'role', 'is_active',
            ),
        }),
    )
