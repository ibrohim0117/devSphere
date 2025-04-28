from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)

from blog.models import Post, Category


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        data = Post.objects.all().order_by('-views')
        data = {
            'posts': Post.objects.all(),
            'top_posts': data,
        }
        return data


from django.utils import timezone
from datetime import timedelta


class SingleView(DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        post = Post.objects.filter(slug=self.kwargs['slug']).first()

        if post:
            post.created_at_plus_5 = post.created_at + timedelta(hours=5)

        context.update({
            'post': post,
            'categories': categories,
        })
        return context


class ArchiveView(TemplateView):
    template_name = 'archive.html'


class CategoryView(TemplateView):
    template_name = 'category.html'


class ElementsView(TemplateView):
    template_name = 'elements.html'


class GenericsView(TemplateView):
    template_name = 'generic.html'


class SearchView(TemplateView):
    template_name = 'search.html'

