from django.contrib import admin
from .models import CustomUser, UserProfile, Category, Quiz, Question, Option, UserQuizAttempt, UserAnswer, Rating
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserQuizAttempt)
admin.site.register(UserAnswer)
admin.site.register(Rating)
