from django.contrib import admin
from .models import Category, Post, Tag, Emoji, Reaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'id', 'views')
    search_fields = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'post', 'id', 'ip_address')
    search_fields = ('emoji',)