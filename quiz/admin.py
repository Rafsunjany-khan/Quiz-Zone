from django.contrib import admin
from .models import User, Category, Quiz, Question, Option, QuizAttempt, Rating

# ------------------------
# User Admin
# ------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone', 'is_active')
    search_fields = ('email', 'full_name', 'phone')


# ------------------------
# Option Inline for Question
# ------------------------
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # show 4 option fields
    max_num = 4
    min_num = 4


# ------------------------
# Question Admin
# ------------------------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'points')
    inlines = [OptionInline]


# ------------------------
# Quiz Admin
# ------------------------
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'has_time_limit', 'time_limit')


# ------------------------
# Category Admin
# ------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# ------------------------
# Quiz Attempt Admin
# ------------------------
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'started_at', 'completed_at')


# ------------------------
# Rating Admin
# ------------------------
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score')
