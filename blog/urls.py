from django.urls import path
from .views import (
     HomeView, PostDetailView, react_to_post
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),

    path('post/<int:post_id>/react/', react_to_post, name='react_to_post'),

]