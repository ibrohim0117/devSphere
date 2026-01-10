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


from .models import Post, Category, Tag, Reaction, Comment
from .filter_manager import FilterManager
from .forms import PostCreateForm, CommentForm
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
        # Faqat bitta marta views sonini oshirish
        # F() expression bilan race condition'ni oldini olish
        Post.objects.filter(id=post.id).update(views=F('views') + 1)
        post.refresh_from_db()
        return post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # get_object() allaqachon chaqirilgan, shuning uchun self.object dan foydalanish
        post = self.object
        # O'z post'ini olib tashlash
        data['related_posts'] = Post.objects.filter(
            category=post.category,
            is_active=True
        ).exclude(id=post.id).select_related('author', 'category').prefetch_related('tags')[:5]
        
        # Commentlar va form
        data['comment_form'] = CommentForm()
        # Faqat active commentlar va parent=None bo'lganlar (reply emas)
        # Replies ham faqat active bo'lganlarini olish
        top_level_comments = post.comments.filter(
            is_active=True, 
            parent=None
        ).select_related('author').prefetch_related(
            Prefetch(
                'replies',
                queryset=Comment.objects.filter(is_active=True).select_related('author'),
                to_attr='active_replies'
            )
        ).order_by('-created_at')
        data['comments'] = top_level_comments
        
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
        # Superuser barcha postlarni tahrirlay oladi
        if not self.request.user.is_superuser and post.author != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Siz bu postni tahrirlash huquqiga ega emassiz!")
        return post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category'] = Category.objects.all()
        data['tags'] = Tag.objects.all()
        return data

    def form_valid(self, form):
        # Faqat oddiy userlar tahrirlaganda is_active=False qilamiz
        # Superuser tahrirlaganda is_active holati o'zgarmaydi
        if not self.request.user.is_superuser:
            # User postni tahrirlaganda, post yana admin tomonidan ko'rib chiqilishi kerak
            # Shuning uchun is_active=False qilamiz
            form.instance.is_active = False
            messages.success(self.request, "✅ Post muvaffaqiyatli yangilandi va adminga yuborildi! Admin tasdiqlagandan keyin post saytda ko'rinadi.")
        else:
            # Superuser tahrirlaganda
            messages.success(self.request, "✅ Post muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

    def get_success_url(self):
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


def add_comment(request, post_slug):
    """Post ga comment qo'shish"""
    if not request.user.is_authenticated:
        messages.error(request, "Izoh yozish uchun tizimga kirishingiz kerak!")
        return redirect('login')
    
    if request.method != 'POST':
        return redirect('post', slug=post_slug)
    
    post = get_object_or_404(Post, slug=post_slug, is_active=True)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, "✅ Izohingiz muvaffaqiyatli qo'shildi!")
    else:
        messages.error(request, "Xatolik: iltimos, izohingizni to'g'ri to'ldiring.")
    
    return redirect('post', slug=post_slug)


def reply_comment(request, post_slug, comment_id):
    """Commentga reply qilish"""
    if not request.user.is_authenticated:
        messages.error(request, "Javob yozish uchun tizimga kirishingiz kerak!")
        return redirect('login')
    
    if request.method != 'POST':
        return redirect('post', slug=post_slug)
    
    post = get_object_or_404(Post, slug=post_slug, is_active=True)
    parent_comment = get_object_or_404(Comment, id=comment_id, post=post, is_active=True)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        reply = form.save(commit=False)
        reply.post = post
        reply.author = request.user
        reply.parent = parent_comment
        reply.save()
        messages.success(request, "✅ Javobingiz muvaffaqiyatli qo'shildi!")
    else:
        messages.error(request, "Xatolik: iltimos, javobingizni to'g'ri to'ldiring.")
    
    return redirect('post', slug=post_slug)



