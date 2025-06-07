from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)
from django.db.models import Q


from blog.models import Post, Category, Tag


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
        return queryset

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