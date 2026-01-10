from django.urls import path
from .views import (
     HomeView, PostDetailView, react_to_post, PostCreateView,
     MyPostsView, PostUpdateView, PostDeleteView, AdminPostsView,
     toggle_post_status, add_comment, reply_comment
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('post-create/', PostCreateView.as_view(), name='post_create'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('admin/posts/', AdminPostsView.as_view(), name='admin_posts'),
    path('admin/post/<int:post_id>/toggle-status/', toggle_post_status, name='toggle_post_status'),

    path('post/<int:post_id>/react/', react_to_post, name='react_to_post'),
    
    # Comments
    path('post/<slug:post_slug>/comment/', add_comment, name='add_comment'),
    path('post/<slug:post_slug>/comment/<int:comment_id>/reply/', reply_comment, name='reply_comment'),

]