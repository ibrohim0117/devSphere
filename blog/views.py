from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)

from blog.models import Post, Category


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category'] = Category.objects.all()
        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    slug_field = 'slug'