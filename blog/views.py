from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView
)
from django.contrib import messages


from .models import Post, Category, Tag, Reaction
from .filter_manager import FilterManager
from .forms import PostCreateForm
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
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        post = Post.objects.filter(slug=slug).first()
        if post:
            data['related_posts'] = Post.objects.filter(category__slug=post.category.slug).all()
        return data


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'new_post.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category'] = Category.objects.all()
        data['tags'] = Tag.objects.all()
        return data
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Post adminga yuborildi!")
        return super().form_valid(form)



