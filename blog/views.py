from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import F, Prefetch
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect


from .models import Post, Category, Tag, Reaction
from .filter_manager import FilterManager
from .forms import PostCreateForm
from .utils import get_client_ip


def react_to_post(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Noto\'g\'ri so\'rov turi'}, status=405)
    
    try:
        emoji = request.POST.get('emoji')
        if not emoji:
            return JsonResponse({'error': 'Emoji tanlanmagan'}, status=400)
        
        # Emoji validation
        valid_emojis = [choice[0] for choice in Reaction.EMOJI_CHOICES]
        if emoji not in valid_emojis:
            return JsonResponse({'error': 'Noto\'g\'ri emoji'}, status=400)
        
        try:
            post = Post.objects.get(id=post_id, is_active=True)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post topilmadi'}, status=404)
        
        ip_address = get_client_ip(request)
        if Reaction.objects.filter(post=post, ip_address=ip_address).exists():
            return JsonResponse({'error': 'Siz allaqachon ovoz bergansiz!'}, status=400)

        Reaction.objects.create(post=post, emoji=emoji, ip_address=ip_address)
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'error': 'Xatolik yuz berdi'}, status=500)


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'
    paginate_by = 4
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags', 'reactions'
        )
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
        # Pagination uchun query parametrlar
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        data['query_string'] = query_params.urlencode()
        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    slug_field = 'slug'

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'author').prefetch_related('tags', 'reactions')

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # F() expression bilan race condition'ni oldini olish
        Post.objects.filter(id=post.id).update(views=F('views') + 1)
        post.refresh_from_db()
        return post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        post = self.get_object()
        # O'z post'ini olib tashlash
        data['related_posts'] = Post.objects.filter(
            category=post.category,
            is_active=True
        ).exclude(id=post.id).select_related('author', 'category').prefetch_related('tags')[:5]
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
        form.instance.author = self.request.user
        messages.success(self.request, "✅ Post adminga yuborildi!")
        return super().form_valid(form)


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'my_posts.html'
    context_object_name = 'post_list'
    paginate_by = 10
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).select_related('category', 'author').prefetch_related('tags', 'reactions').order_by('-created_at')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        data['query_string'] = query_params.urlencode()
        return data


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'edit_post.html'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        if post.author != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Siz bu postni tahrirlash huquqiga ega emassiz!")
        return post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category'] = Category.objects.all()
        data['tags'] = Tag.objects.all()
        return data

    def get_success_url(self):
        messages.success(self.request, "✅ Post muvaffaqiyatli yangilandi!")
        return reverse_lazy('my_posts')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('my_posts')

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        if post.author != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Siz bu postni o'chirish huquqiga ega emassiz!")
        return post

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "✅ Post muvaffaqiyatli o'chirildi!")
        return super().delete(request, *args, **kwargs)


class AdminPostsView(UserPassesTestMixin, ListView):
    model = Post
    template_name = 'admin_posts.html'
    context_object_name = 'post_list'
    paginate_by = 15

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_queryset(self):
        queryset = Post.objects.all().select_related('category', 'author').prefetch_related('tags', 'reactions').order_by('-created_at')
        
        # Filterlar
        status_filter = self.request.GET.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        data['query_string'] = query_params.urlencode()
        data['status_filter'] = self.request.GET.get('status', '')
        data['search_query'] = self.request.GET.get('q', '')
        # Statistika
        data['total_posts'] = Post.objects.count()
        data['active_posts'] = Post.objects.filter(is_active=True).count()
        data['inactive_posts'] = Post.objects.filter(is_active=False).count()
        return data


def toggle_post_status(request, post_id):
    """Superuser uchun post holatini o'zgartirish"""
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "Sizda bu funksiyani ishlatish huquqi yo'q!")
        return redirect('home')
    
    post = get_object_or_404(Post, id=post_id)
    post.is_active = not post.is_active
    post.save()
    
    status = "faollashtirildi" if post.is_active else "o'chirildi"
    messages.success(request, f"✅ Post muvaffaqiyatli {status}!")
    
    # Qaysi sahifadan kelgan bo'lsa, o'sha sahifaga qaytish
    referer = request.META.get('HTTP_REFERER', reverse_lazy('admin_posts'))
    return redirect(referer)



