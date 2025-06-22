from django.contrib import admin
from .models import UserProfile, Article, Category

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'description')
    search_fields = ('user__username', 'description')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'category')
    search_fields = ('title', 'author__user__username', 'category__title')
    list_filter = ('category', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'title': ('title',)}
    




