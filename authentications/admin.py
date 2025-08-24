from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'phone', 'is_admin', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    list_filter = ('is_admin', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'password1', 'password2', 'is_admin', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )

admin.site.register(User, UserAdmin)
