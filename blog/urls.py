from django.urls import path
from .views import (
     HomeView, PostDetailView, ReactToPostView, PostCreateView,
     MyPostsView, PostUpdateView, PostDeleteView, AdminPostsView,
     TogglePostStatusView, AddCommentView, ReplyCommentView,
     CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
     TagListView, TagCreateView, TagUpdateView, TagDeleteView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('post-create/', PostCreateView.as_view(), name='post_create'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('admin/posts/', AdminPostsView.as_view(), name='admin_posts'),
    path('admin/post/<int:post_id>/toggle-status/', TogglePostStatusView.as_view(), name='toggle_post_status'),
    
    # Category Management URLs
    path('admin/categories/', CategoryListView.as_view(), name='category_list'),
    path('admin/category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('admin/category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('admin/category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Tag Management URLs
    path('admin/tags/', TagListView.as_view(), name='tag_list'),
    path('admin/tag/create/', TagCreateView.as_view(), name='tag_create'),
    path('admin/tag/<int:pk>/edit/', TagUpdateView.as_view(), name='tag_edit'),
    path('admin/tag/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    
    path('post/<int:post_id>/react/', ReactToPostView.as_view(), name='react_to_post'),
    path('post/<slug:post_slug>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('post/<slug:post_slug>/comment/<int:comment_id>/reply/', ReplyCommentView.as_view(), name='reply_comment'),
]