from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)
from django.db.models import Q, Count
from django.utils.timezone import now, timedelta

from blog.models import Post, Category, Tag
from .filter_manager import FilterManager


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        filter_option = self.request.GET.get('filter')
        category_option = self.request.GET.get('category')
        tag_option = self.request.GET.get('tag')

        data = FilterManager(
            queryset=queryset,
            search=search,
            filter_option=filter_option,
            category_option=category_option,
            tag_option=tag_option,
        )

        return data.all_filters()


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category'] = Category.objects.all()
        data['tags'] = Tag.objects.all()
        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views += 1
        post.save(update_fields=['views'])
        return post