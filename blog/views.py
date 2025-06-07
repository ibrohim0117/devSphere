from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)
from blog.models import Post, Category, Tag
from .filter_manager import FilterManager

# views.py
from django.http import JsonResponse
from .models import Post, Reaction
from .utils import get_client_ip


def react_to_post(request, post_id):
    if request.method == 'POST':
        # print("OKKK")
        emoji = request.POST.get('emoji')
        ip_address = get_client_ip(request)
        post = Post.objects.get(id=post_id)
        if Reaction.objects.filter(post=post, ip_address=ip_address).exists():
            return JsonResponse({'error': 'Siz allaqachon ovoz bergansiz!'}, status=400)

        Reaction.objects.create(post=post, emoji=emoji, ip_address=ip_address)
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Noto‘g‘ri so‘rov turi'}, status=405)


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