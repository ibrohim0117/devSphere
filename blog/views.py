from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)

from blog.models import Post, Category


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'