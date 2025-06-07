from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)
from django.db.models import Q, Count
from django.utils.timezone import now, timedelta

from blog.models import Post, Category, Tag


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        filter_option = self.request.GET.get('filter')


        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()

        if filter_option == 'yangilar':
            queryset = queryset.order_by('-created_at')
        elif filter_option == 'top':
            queryset = queryset.order_by('-views')
        elif filter_option == 'yonmoqda':
            queryset = queryset.filter(views__gte=100).order_by('-views')
        elif filter_option == 'emoji':
            queryset = queryset.annotate(
                emoji_count=Count('emoji')
            ).filter(emoji_count__gt=0).order_by('-emoji_count')
        elif filter_option == 'hafta':
            one_week_ago = now() - timedelta(days=7)
            queryset = queryset.filter(created_at__gte=one_week_ago)
        elif filter_option == 'oy':
            one_month_ago = now() - timedelta(days=30)
            queryset = queryset.filter(created_at__gte=one_month_ago)
        elif filter_option == 'hammasi':
            pass

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