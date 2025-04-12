from django.contrib import admin
from .models import Category, Post, Tag, Emoji


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
